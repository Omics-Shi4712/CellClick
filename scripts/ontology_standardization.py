#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cell Ontology/OLS post-processing helpers for annotation standardization.

These helpers intentionally run after the normal CellClick/LLM annotation path.
They map free-text annotation labels to Cell Ontology terms, compare mapped
terms with ancestor-set Jaccard similarity, and merge labels that are exact or
near ontology matches.
"""

import re
import urllib.error
import urllib.parse
import urllib.request


DEFAULT_OLS_BASE_URL = "https://www.ebi.ac.uk/ols4/api"


def normalize_cell_label(label):
    if label is None:
        return ""
    label = str(label).strip()
    label = label.replace("_", " ")
    label = re.sub(r"\s+", " ", label)
    return label


def _comparison_key(label):
    label = normalize_cell_label(label).lower()
    label = label.replace("-", " ")
    label = re.sub(r"[^a-z0-9+ ]+", " ", label)
    label = re.sub(r"\s+", " ", label).strip()
    return label


def _ols_get_json(url, timeout=10):
    request = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        import json

        return json.loads(response.read().decode("utf-8"))


def _build_url(base_url, path, params=None):
    base_url = base_url.rstrip("/")
    url = base_url + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    return url


def _empty_mapping(label, status, message=None):
    return {
        "raw_label": None if label is None else str(label),
        "normalized_label": normalize_cell_label(label),
        "ontology_id": None,
        "ontology_label": None,
        "ontology_iri": None,
        "mapping_confidence": 0.0,
        "ancestors": [],
        "mapping_status": status,
        "mapping_message": message,
    }


def _doc_synonyms(doc):
    synonyms = []
    for key in ("synonym", "synonyms", "obo_synonym"):
        value = doc.get(key)
        if isinstance(value, list):
            synonyms.extend(value)
        elif isinstance(value, str):
            synonyms.append(value)
    return synonyms


def _score_doc(label, doc):
    query_key = _comparison_key(label)
    label_key = _comparison_key(doc.get("label"))
    synonym_keys = [_comparison_key(value) for value in _doc_synonyms(doc)]

    if query_key and query_key == label_key:
        return 1.0
    if query_key and query_key in synonym_keys:
        return 0.95
    if query_key and (query_key in label_key or label_key in query_key):
        return 0.75
    return 0.6


def _select_best_doc(label, docs, ontology):
    def is_requested_ontology(doc):
        ontology_name = doc.get("ontology_name")
        ontology_prefix = doc.get("ontology_prefix")
        if ontology_name is None and ontology_prefix is None:
            return True
        return ontology_name == ontology or ontology_prefix == ontology.upper()

    docs = [doc for doc in docs if is_requested_ontology(doc)]
    if not docs:
        return None, 0.0, "unmapped"

    scored = sorted(
        [(doc, _score_doc(label, doc)) for doc in docs],
        key=lambda item: item[1],
        reverse=True,
    )
    best_doc, best_score = scored[0]
    if len(scored) > 1 and scored[1][1] == best_score:
        return best_doc, best_score, "ambiguous"
    if best_score >= 0.95:
        return best_doc, best_score, "exact"
    return best_doc, best_score, "approximate"


def _encode_iri_for_ols(iri):
    return urllib.parse.quote(urllib.parse.quote(iri, safe=""), safe="")


def _extract_terms(payload):
    embedded = payload.get("_embedded", {})
    terms = embedded.get("terms") or embedded.get("term")
    if isinstance(terms, list):
        return terms
    if isinstance(terms, dict):
        return [terms]
    return []


def _fetch_ancestors(iri, ontology_id, ols_base_url, ontology, timeout):
    if not iri:
        return [ontology_id] if ontology_id else []

    encoded_iri = _encode_iri_for_ols(iri)
    url = _build_url(
        ols_base_url,
        "/ontologies/{}/terms/{}/hierarchicalAncestors".format(ontology, encoded_iri),
        {"size": 1000},
    )
    try:
        payload = _ols_get_json(url, timeout=timeout)
    except (urllib.error.URLError, TimeoutError, ValueError):
        return [ontology_id] if ontology_id else []

    ancestors = []
    for term in _extract_terms(payload):
        term_id = term.get("obo_id") or term.get("short_form") or term.get("label")
        if term_id and term_id not in ancestors:
            ancestors.append(term_id)

    if ontology_id and ontology_id not in ancestors:
        ancestors.insert(0, ontology_id)
    return ancestors


def map_label_to_cell_ontology(
    label,
    ols_base_url=DEFAULT_OLS_BASE_URL,
    ontology="cl",
    timeout=10,
):
    """Map a free-text cell label to a Cell Ontology term through OLS."""
    normalized_label = normalize_cell_label(label)
    if not normalized_label:
        return _empty_mapping(label, "empty")

    search_params = {
        "q": normalized_label,
        "ontology": ontology,
        "type": "class",
        "exact": "true",
        "rows": 10,
    }
    try:
        payload = _ols_get_json(_build_url(ols_base_url, "/search", search_params), timeout=timeout)
        docs = payload.get("response", {}).get("docs", [])
        if not docs:
            search_params["exact"] = "false"
            payload = _ols_get_json(_build_url(ols_base_url, "/search", search_params), timeout=timeout)
            docs = payload.get("response", {}).get("docs", [])
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        return _empty_mapping(label, "ols_unavailable", str(exc))

    best_doc, confidence, status = _select_best_doc(normalized_label, docs, ontology)
    if best_doc is None:
        return _empty_mapping(label, "unmapped")

    ontology_id = best_doc.get("obo_id") or best_doc.get("short_form")
    iri = best_doc.get("iri")
    ancestors = _fetch_ancestors(iri, ontology_id, ols_base_url, ontology, timeout)

    return {
        "raw_label": str(label),
        "normalized_label": normalized_label,
        "ontology_id": ontology_id,
        "ontology_label": best_doc.get("label"),
        "ontology_iri": iri,
        "mapping_confidence": confidence,
        "ancestors": ancestors,
        "mapping_status": status,
        "mapping_message": None,
    }


def calculate_ontology_jaccard(node_a, node_b):
    """Calculate Jaccard similarity from ontology IDs plus ancestor sets."""
    ids_a = set(node_a.get("ancestors") or [])
    ids_b = set(node_b.get("ancestors") or [])

    if node_a.get("ontology_id"):
        ids_a.add(node_a["ontology_id"])
    if node_b.get("ontology_id"):
        ids_b.add(node_b["ontology_id"])

    if not ids_a or not ids_b:
        return 0.0
    return len(ids_a & ids_b) / len(ids_a | ids_b)


def _as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def _label_from_alternative(value):
    if isinstance(value, dict):
        for key in ("cell_type", "suggested_cell_type", "annotation", "label"):
            if value.get(key):
                return value[key]
        return None
    return value


def _split_ref_cell_type(ref_cell_type):
    parts = str(ref_cell_type).split("_", 1)
    if len(parts) == 1:
        return "", parts[0]
    return parts[0], parts[1]


def _collect_annotation_labels(annotation):
    labels = []
    if not isinstance(annotation, dict):
        return labels

    for field, source in (
        ("suggested_cell_type", "primary"),
        ("suggested_subtype", "subtype"),
        ("standard_cell_type", "primary"),
        ("standard_subtype", "subtype"),
    ):
        if annotation.get(field):
            labels.append({"raw_label": annotation[field], "source": source, "field": field})

    for alternative in _as_list(annotation.get("alternative_annotations")):
        label = _label_from_alternative(alternative)
        if label:
            labels.append({"raw_label": label, "source": "alternative", "field": "alternative_annotations"})
    return labels


def _collect_candidate_labels(score_candidates):
    labels = []
    for candidate in _as_list(score_candidates):
        if isinstance(candidate, dict):
            raw_label = candidate.get("cell_type")
            if not raw_label and candidate.get("ref_cell_type"):
                _, raw_label = _split_ref_cell_type(candidate["ref_cell_type"])
            if raw_label:
                labels.append(
                    {
                        "raw_label": raw_label,
                        "source": "candidate_reference",
                        "field": "candidate_reference_cell_types",
                        "candidate": candidate,
                    }
                )
        elif candidate:
            _, raw_label = _split_ref_cell_type(candidate)
            labels.append(
                {
                    "raw_label": raw_label,
                    "source": "candidate_reference",
                    "field": "candidate_reference_cell_types",
                    "candidate": candidate,
                }
            )
    return labels


def _merge_target(groups, mapped_record, jaccard_threshold):
    node = mapped_record["mapping"]
    if not node.get("ontology_id"):
        normalized_label = node.get("normalized_label")
        for group in groups:
            group_node = group["representative_mapping"]
            if not group_node.get("ontology_id") and normalized_label == group_node.get("normalized_label"):
                return group, "exact_normalized_label"
        return None, None

    for group in groups:
        group_node = group["representative_mapping"]
        if node.get("ontology_id") == group_node.get("ontology_id"):
            return group, "exact_ontology_id"

    best_group = None
    best_jaccard = 0.0
    for group in groups:
        score = calculate_ontology_jaccard(node, group["representative_mapping"])
        if score > best_jaccard:
            best_group = group
            best_jaccard = score

    if best_group is not None and best_jaccard >= jaccard_threshold:
        return best_group, "ancestor_jaccard:{:.3f}".format(best_jaccard)
    return None, None


def _new_group(mapped_record, group_index):
    mapping = mapped_record["mapping"]
    standard_label = (
        mapping.get("ontology_label")
        or mapping.get("normalized_label")
        or mapped_record["raw_label"]
    )
    return {
        "group_id": "ontology_group_{}".format(group_index),
        "standard_label": standard_label,
        "ontology_id": mapping.get("ontology_id"),
        "ontology_iri": mapping.get("ontology_iri"),
        "representative_mapping": mapping,
        "raw_labels": [],
        "sources": [],
        "records": [],
        "merge_reasons": [],
        "score_sum": 0.0,
        "score_max": None,
        "mapping_statuses": [],
    }


def _append_to_group(group, mapped_record, reason):
    raw_label = mapped_record["raw_label"]
    if raw_label not in group["raw_labels"]:
        group["raw_labels"].append(raw_label)
    source = mapped_record.get("source")
    if source and source not in group["sources"]:
        group["sources"].append(source)
    status = mapped_record["mapping"].get("mapping_status")
    if status and status not in group["mapping_statuses"]:
        group["mapping_statuses"].append(status)
    if reason:
        group["merge_reasons"].append({"raw_label": raw_label, "reason": reason})

    candidate = mapped_record.get("candidate")
    if isinstance(candidate, dict) and candidate.get("score") is not None:
        score = float(candidate["score"])
        group["score_sum"] += score
        group["score_max"] = score if group["score_max"] is None else max(group["score_max"], score)

    group["records"].append(mapped_record)


def _finalize_groups(groups):
    for group in groups:
        group.pop("representative_mapping", None)
        group["record_count"] = len(group["records"])
        group["score_max"] = group["score_max"] if group["score_max"] is not None else 0.0

    return sorted(
        groups,
        key=lambda group: (
            "primary" in group["sources"],
            group["score_max"],
            group["score_sum"],
            group["record_count"],
        ),
        reverse=True,
    )


def standardize_annotation_result(
    annotation_result,
    score_candidates,
    jaccard_threshold=0.6,
    ols_base_url=DEFAULT_OLS_BASE_URL,
    ontology="cl",
    mapper=None,
):
    """Standardize and merge annotation labels after the raw annotation step."""
    raw_annotation = annotation_result.get("annotation") if (
        isinstance(annotation_result, dict) and "annotation" in annotation_result
    ) else annotation_result

    label_records = _collect_annotation_labels(raw_annotation)
    label_records.extend(_collect_candidate_labels(score_candidates))

    mapped_records = []
    mapping_cache = {}
    mapper = mapper or (
        lambda label: map_label_to_cell_ontology(
            label,
            ols_base_url=ols_base_url,
            ontology=ontology,
        )
    )

    for record in label_records:
        normalized_label = normalize_cell_label(record["raw_label"])
        if not normalized_label:
            continue
        if normalized_label not in mapping_cache:
            mapping_cache[normalized_label] = mapper(normalized_label)
        mapped_records.append({**record, "mapping": mapping_cache[normalized_label]})

    groups = []
    unmapped_labels = []
    ambiguous_labels = []
    for mapped_record in mapped_records:
        status = mapped_record["mapping"].get("mapping_status")
        if status in ("unmapped", "empty", "ols_unavailable"):
            unmapped_labels.append(mapped_record["raw_label"])
        if status == "ambiguous":
            ambiguous_labels.append(mapped_record["raw_label"])

        group, reason = _merge_target(groups, mapped_record, jaccard_threshold)
        if group is None:
            group = _new_group(mapped_record, len(groups) + 1)
            groups.append(group)
            reason = "new_group"
        _append_to_group(group, mapped_record, reason)

    merged_groups = _finalize_groups(groups)
    primary_annotation = merged_groups[0] if merged_groups else None
    merge_report = {
        "jaccard_threshold": jaccard_threshold,
        "merged_group_count": len(merged_groups),
        "mapped_label_count": len(mapped_records),
        "unmapped_labels": sorted(set(unmapped_labels)),
        "ambiguous_labels": sorted(set(ambiguous_labels)),
        "merged_groups": [
            {
                "group_id": group["group_id"],
                "standard_label": group["standard_label"],
                "ontology_id": group["ontology_id"],
                "raw_labels": group["raw_labels"],
                "merge_reasons": group["merge_reasons"],
            }
            for group in merged_groups
        ],
    }

    return {
        "raw_annotation": raw_annotation,
        "standardized_annotation": {
            "primary_annotation": primary_annotation,
            "merged_candidates": merged_groups,
            "mapped_labels": mapped_records,
        },
        "merge_report": merge_report,
    }


__all__ = [
    "DEFAULT_OLS_BASE_URL",
    "normalize_cell_label",
    "map_label_to_cell_ontology",
    "calculate_ontology_jaccard",
    "standardize_annotation_result",
]
