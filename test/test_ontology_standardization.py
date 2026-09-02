#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.llm_ann import evaluate_marker_gene_score_annotation
from scripts.adata_processor import annotation_eval
from scripts.ontology_standardization import (
    calculate_ontology_jaccard,
    normalize_cell_label,
    standardize_annotation_result,
)


def fake_mapper(label):
    normalized = normalize_cell_label(label)
    records = {
        "T cell": {
            "ontology_id": "CL:0000084",
            "ontology_label": "T cell",
            "ancestors": ["CL:0000542", "CL:0000000"],
            "mapping_status": "exact",
            "mapping_confidence": 1.0,
        },
        "T-cell": {
            "ontology_id": "CL:0000084",
            "ontology_label": "T cell",
            "ancestors": ["CL:0000542", "CL:0000000"],
            "mapping_status": "exact",
            "mapping_confidence": 1.0,
        },
        "T lymphocyte": {
            "ontology_id": "CL:0000084",
            "ontology_label": "T cell",
            "ancestors": ["CL:0000542", "CL:0000000"],
            "mapping_status": "exact",
            "mapping_confidence": 1.0,
        },
        "CD8-positive, alpha-beta T cell": {
            "ontology_id": "CL:0000625",
            "ontology_label": "CD8-positive, alpha-beta T cell",
            "ancestors": ["CL:0000084", "CL:0000542", "CL:0000000"],
            "mapping_status": "exact",
            "mapping_confidence": 1.0,
        },
    }
    if normalized not in records:
        return {
            "raw_label": label,
            "normalized_label": normalized,
            "ontology_id": None,
            "ontology_label": None,
            "ontology_iri": None,
            "mapping_confidence": 0.0,
            "ancestors": [],
            "mapping_status": "unmapped",
            "mapping_message": None,
        }
    return {
        "raw_label": label,
        "normalized_label": normalized,
        "ontology_iri": "http://example.org/{}".format(records[normalized]["ontology_id"]),
        "mapping_message": None,
        **records[normalized],
    }


class FakeProcessor:
    def __init__(self, adata, gene_weight_full):
        self.adata = adata
        self._gene_weight_full = gene_weight_full

    def _load_marker_weight(self, marker_ref_path):
        return self._gene_weight_full


class OntologyStandardizationTests(unittest.TestCase):
    def test_synonyms_merge_by_same_ontology_id(self):
        result = standardize_annotation_result(
            {"suggested_cell_type": "T cell", "alternative_annotations": ["T lymphocyte"]},
            [{"cell_type": "T-cell", "score": 2.0}],
            mapper=fake_mapper,
        )

        groups = result["standardized_annotation"]["merged_candidates"]
        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0]["ontology_id"], "CL:0000084")
        self.assertEqual(set(groups[0]["raw_labels"]), {"T cell", "T lymphocyte", "T-cell"})

    def test_parent_child_merge_by_jaccard(self):
        t_cell = fake_mapper("T cell")
        cd8_t_cell = fake_mapper("CD8-positive, alpha-beta T cell")
        self.assertGreaterEqual(calculate_ontology_jaccard(t_cell, cd8_t_cell), 0.6)

        result = standardize_annotation_result(
            {"suggested_cell_type": "CD8-positive, alpha-beta T cell"},
            [{"cell_type": "T cell", "score": 1.0}],
            jaccard_threshold=0.6,
            mapper=fake_mapper,
        )

        groups = result["standardized_annotation"]["merged_candidates"]
        self.assertEqual(len(groups), 1)
        self.assertIn("CD8-positive, alpha-beta T cell", groups[0]["raw_labels"])
        self.assertIn("T cell", groups[0]["raw_labels"])

    def test_unmapped_label_is_retained(self):
        result = standardize_annotation_result(
            {"suggested_cell_type": "disease activated cycling-like cell"},
            [],
            mapper=fake_mapper,
        )

        report = result["merge_report"]
        self.assertEqual(report["unmapped_labels"], ["disease activated cycling-like cell"])
        self.assertEqual(
            result["standardized_annotation"]["primary_annotation"]["standard_label"],
            "disease activated cycling-like cell",
        )

    def test_evaluate_default_does_not_standardize(self):
        def llm_client(**kwargs):
            return json.dumps({"suggested_cell_type": "T cell"})

        result = evaluate_marker_gene_score_annotation(
            pd.Series({"blood_T cell": 1.0}),
            llm_client=llm_client,
        )

        self.assertEqual(result["annotation"]["suggested_cell_type"], "T cell")
        self.assertNotIn("standardized_annotation", result)
        self.assertNotIn("merge_report", result)

    def test_evaluate_can_standardize_after_raw_annotation(self):
        def llm_client(**kwargs):
            return json.dumps({"suggested_cell_type": "T lymphocyte"})

        result = evaluate_marker_gene_score_annotation(
            pd.Series({"blood_T cell": 1.0}),
            llm_client=llm_client,
            standardize=True,
            ontology_mapper=fake_mapper,
        )

        self.assertEqual(result["raw_annotation"]["suggested_cell_type"], "T lymphocyte")
        self.assertEqual(
            result["standardized_annotation"]["primary_annotation"]["ontology_id"],
            "CL:0000084",
        )
        self.assertIn("merge_report", result)

    def test_marker_gene_scores_return_details(self):
        adata = SimpleNamespace(
            obs=pd.DataFrame(index=["c1", "c2", "c3"]),
            uns={},
        )
        gene_weight_full = pd.DataFrame(
            {
                "G1": [1, 0],
                "G2": [1, 1],
                "G3": [0, 1],
            },
            index=["blood_T cell", "blood_B cell"],
        )
        annotation_series = pd.Series(["cluster_a", "cluster_a", "cluster_b"], index=["c1", "c2", "c3"], dtype="category")
        processor = FakeProcessor(adata, gene_weight_full)

        def fake_cosg(adata, groupby, key_added, reference, **kwargs):
            adata.uns[key_added] = {
                "scores": {
                    "cluster_a": [0.9, 0.6, 0.1],
                },
                "names": {
                    "cluster_a": ["G1", "G2", "G3"],
                },
            }

        with patch.object(annotation_eval.cosg, "cosg", side_effect=fake_cosg):
            result = annotation_eval.MarkerGeneScores_cal(
                processor,
                cellIDs=["c1", "c2"],
                cellCluster="cluster_a",
                annotationSeries=annotation_series,
                marker_ref_path="unused",
                markerGeneUsed=3,
                showNum=2,
                return_details=True,
                n_permutations=10,
                random_state=0,
            )

        self.assertIn("scores", result)
        self.assertIn("score_details", result)
        self.assertIn("top_candidate_summary", result)
        self.assertIn("background", result)
        self.assertEqual(result["background"]["sampling_mode"], "matched_marker_set_permutation")
        self.assertEqual(len(result["score_details"]), 2)
        self.assertIn("annotation_confidence", result["score_details"].columns)


if __name__ == "__main__":
    unittest.main()
