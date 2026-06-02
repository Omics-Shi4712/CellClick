# CellClick

CellClick is an interactive platform for cell type annotation in single-cell and spatial omics data. It combines preprocessing, visualization, marker-based annotation, validation, and iterative reannotation in a Dash-based interface built around `AnnData` and `Scanpy`.

The repository implements the workflow described in the uploaded project description and exposes three main run modes:

- Web application with Dash
- Jupyter-based interactive use with `JupyterDash`

## Main capabilities

- Upload and manage `h5ad` datasets
- Run standard preprocessing steps for raw single-cell data
- Visualize embeddings, marker expression, and gene dot plots
- Identify marker genes with COSG
- Compare clusters against built-in marker references
- Validate annotations with marker-level and reference-level views
- Select suspicious cells, recluster subsets, rename clusters, and merge results back into the parent dataset
- Compare multiple canvases in parallel; the default layout is 3 rows x 2 columns

## Modules in the UI

CellClick is organized into the following modules in the left navigation bar:

1. `Data Settings`
   Load data, switch datasets, remove datasets, and define annotation column types.
2. `Preprocessing`
   Run QC, normalization, HVG detection, dimension reduction, and clustering.
3. `Data Visualization`
   Inspect cell embeddings, gene embeddings, and gene dot plots.
4. `Cell Annotation`
   Perform marker gene identification and marker-based cell identification.
5. `Annotation Validation`
   Review annotation quality and compare against reference marker resources or reference datasets.
6. `Cell Reannotation`
   Select cells, refine clusters, rename subsets, and merge updated annotations.

## Supported data

- Primary input format: `h5ad`
- Internal data model: `AnnData`
- Spatial data are supported when spatial metadata are present in the `AnnData` object
- In Jupyter mode, existing `AnnData` objects can also be loaded directly

## Installation

CellClick targets Python `3.10`.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Running CellClick

### 1. Web app

```bash
python main.py
```

By default the app runs at `http://127.0.0.1:4712`. The host and port are defined in [settings.py](settings.py).

### 2. Jupyter mode

Install notebook dependencies from `requirements.txt`, then run:

```python
from main_jupyter import app
app.run_server(mode="inline", debug=True)
```

This mode also enables loading in-memory `AnnData` objects through the UI.

## Typical workflow

1. Upload a raw or preprocessed `h5ad` dataset.
2. If needed, run `QC`, `Normalization`, `HVG Detection`, and `Dimension Reduction`.
3. Run `Cell Clustering` or reuse an existing annotation column.
4. Inspect clusters with `Cell Embedding`, `Gene Embedding`, and `Gene Dot`.
5. Use `Marker Gene Identification` and `Cell Identification` to assign candidate cell types.
6. Use `Annotation Evaluation` and `Reference Comparison` to validate the results.
7. Use `Cell Selection`, `Cluster Refinement`, `Cluster Reannotation`, and `Annotation Update` to iteratively improve labels.
8. Export the updated annotated dataset as `h5ad`.

## Reference resources

The code expects bundled marker references under [`marker_ref/`](marker_ref), including resources such as:

- `CellMarker`
- `SingleCellBase`
- `CellSTAR`
- additional validation references under `marker_ref/Other`

These paths are configured in [settings.py](settings.py).

## Repository layout

```text
CellClick/
+-- apps/         # Dash layout, module definitions, templates, modal/document UI
+-- callbacks/    # Interactive application logic for each module
+-- manager/      # Dataset/session managers, canvas manager, cell table, recorders
+-- scripts/      # Core processing, plotting, and utility functions
+-- assets/       # CSS, icons, and static frontend assets
+-- data/         # Uploaded or cached datasets used by the app
+-- tmp/          # Temporary exported files
+-- main.py       # Dash app entry point
+-- main_jupyter.py
+-- settings.py
```

## Implementation notes

- The core analysis logic is centered on [`scripts/adataProcessor.py`](scripts/adataProcessor.py).
- Session and dataset state are managed by [`manager/cellclick.py`](manager/cellclick.py).
- The application creates `data/` and `tmp/` automatically if they do not already exist.
- The app is currently wired around `Dash 2.1.0`, `Scanpy`, `COSG`, `Plotly`, and `AnnData`.
