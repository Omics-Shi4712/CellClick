document = {
	"CellClick Overview": {
		"overview": "The overview of CellClick.",
		"forms": {
			"Introduction": {
				"overview": {
					"img": "../assets/image/document_CellClick Overview.png",
					"description": """
						CellClick is a web-based data analysis platform with interactive functions specialized for cell type 
						identification from single-cell omics and spatial omics data. CellClick takes different types of single-cell or 
						spatial omics sequencing data (either preprocessed or unpreprocessed) stored in Scanpy-supported formats (e.g. h5ad) as input. 
						The major feature of CellClick is to provide multiple interactive functions for users to visualize, analyze, evaluate, re-annotate, or re-cluster cells. 
						It also allows parallel comparison of the analysis results across genes, cell clusters, or datasets, which is absent in most currently available software. 
						CellClick provides the above-mentioned functions in five modules: Preprocessing, Data Visualization, Cell Annotation, Annotation Evaluation, and Cell Reannotation.
					"""
				},
				"form introduction": {
					"img": "",
					"inputs": {}
				},
				"example": []
			}
		}
	},
	"Data Settings": {
		"overview": "Manage the dataset in CellClick.",
		"forms": {
			"Upload": {
				"overview": {
					"img": "",
					"description": """
						This function provides multiple methods to upload the dataset. 
						The method depends on the values of Data Source input, which includes 'Local Data', 'History Data', and 'Current Data'.
					"""
				},
				"form introduction": {
					"img": "../assets/image/document_datasettings_upload.png",
					"inputs": {
						"Data Source": "Define the data source for the dataset to upload.",
						"Local Data": "Upload the dataset from local storage. Visible when 'Data Source' is set to 'Local Data'.",
						"History Data": "Upload the dataset that has been analyzed with CellClick. Visible when 'Data Source' is set to 'History Data'.",
						"Current Data": "Reuse the dataset already loaded in the current CellClick session. Visible when 'Data Source' is set to 'Current Data'.",
					}
				},
				"example": [
					{
						"video": "../assets/video/document_datasettings_upload_localdata.mp4",
						"title": "Upload data from local storage",
						"description": """
							By clicking the 'Upload Data' button, you can upload your dataset directly from your local storage. 
							CellClick will assign a unique CellClick ID to each uploaded dataset via the 'Local Data' method.
						"""
					},
					{
						"video": "../assets/video/document_datasettings_upload_historydata.mp4",
						"title": "Upload data from history data",
						"description": "CellClick will store the uploaded dataset and allow you to re-upload it via the 'History Data' method."
					},
				]
			},
			"Remove": {
				"overview": {
					"img": "",
					"description": "CellClick sets a maximum number of uploaded datasets (5 by default). This function allows you to remove a dataset from CellClick."
				},
				"form introduction": {
					"img": "../assets/image/document_datasettings_remove.png",
					"inputs": {
						"Current ID": "The ID of current dataset.",
						"Data ID": "The ID of dataset you want to remove."
					}
				},
				"example": [
					{
						"video": "",
						"title": "",
						"description": ""
					}
				]
			},
			"Change": {
				"overview": {
					"img": "",
					"description": "If you have uploaded multiple datasets, this function allows you to change the current dataset."
				},
				"form introduction": {
					"img": "../assets/image/document_datasettings_change.png",
					"inputs": {
						"Current ID": "The ID of current dataset.",
						"Data ID": "The ID of dataset you want to analyze."
					}
				},
				"example": [
					{
						"video": "",
						"title": "",
						"description": ""
					}
				]
			},
			"Annotation Type": {
				"overview": {
					"img": "",
					"description": """
						CellClick classifies the feature stored in adata.obs as 'Category' and 'Number', 
						and this function allows you to change the classification of cell features.
					"""
				},
				"form introduction": {
					"img": "../assets/image/document_datasettings_annotationtype.png",
					"inputs": {
						"Annotation": "The name of the annotation.",
						"Data Type": "The data type of the annotation."
					}
				},
				"example": [
					{
						"video": "",
						"title": "",
						"description": ""
					}
				]
			}
		}
	},
	"Preprocessing": {
		"overview": "General preprocessing functions of Scanpy.",
		"forms": {
			"QC": {
				"overview": {
					"img": "",
					"description": """
						Filter cells based on UMI counts, gene counts, and the percent of mitochondrial genes with interactive violin plots.
					"""
				},
				"form introduction": {
					"img": "../assets/image/document_preprocessing_QC.png",
					"inputs": {
						"Attributes": "The cell attributes involved in QC."
					}
				},
				"example": [
					{
						"video": "../assets/video/document_preprocessing_QC.mp4",
						"title": "QC cells based on UMI counts, gene counts, and the percent of mitochondrial genes",
						"description": """
							After visualizing the QC graphs, you can slide the slider to set the threshold for the corresponding cell attribute. 
							The input component shows the corresponding or total counts of cells to filter. 
							Once you ensure the threshold, you can filter cells by clicking the 'Filter Cells' button.
						"""
					}
				]
			},
			"Normalization": {
				"overview": {
					"img": "",
					"description": [
						"Normalize each cell by total counts over all genes and logarithmize the normalized counts matrix. Refer to ",
						{
							"component": "a",
							"kwargs": {
								"href": "https://scanpy.readthedocs.io/en/stable/generated/scanpy.pp.normalize_total.html",
								"children": "scanpy.pp.normalize_total"
							}
						},
						" and ",
						{
							"component": "a",
							"kwargs": {
								"href": "https://scanpy.readthedocs.io/en/stable/generated/scanpy.pp.log1p.html",
								"children": "scanpy.pp.log1p"
							}
						},
						" functions."
					]
				},
				"form introduction": {
					"img": "../assets/image/document_preprocessing_normalization.png",
					"inputs": {
						"Target Sum": "The total counts over all genes to normalize each cell.",
						"Exclude Highly Expressed": "Whether to exclude very highly expressed genes when normalizing each cell.",
						"Log1P": "Whether to logarithmize the normalized counts matrix."
					}
				},
				"example": [
					{
						"video": "../assets/video/document_preprocessing_NHD.mp4",
						"title": "The normalization, HVG detection, and dimension reduction analysis in CellClick",
						"description": "You will be informed by the Alert component when the analysis is complete."
					}
				]
			},
			"HVG Detection": {
				"overview": {
					"img": "",
					"description": [
						"Annotate highly variable genes. Refer to ",
						{
							"component": "a",
							"kwargs": {
								"href": "https://scanpy.readthedocs.io/en/stable/generated/scanpy.pp.highly_variable_genes.html",
								"children": "scanpy.pp.highly_variable_genes"
							}
						}
					]
				},
				"form introduction": {
					"img": "../assets/image/document_preprocessing_hvgdetection.png",
					"inputs": {
						"Flavor": "Choose the flavor for identifying highly variable genes.",
						"Top Genes": "Number of highly-variable genes to keep."
					}
				},
				"example": [
					{
						"video": "../assets/video/document_preprocessing_NHD.mp4",
						"title": "The normalization, HVG detection, and dimension reduction analysis in CellClick",
						"description": "You will be informed by the Alert component when the analysis is complete."
					}
				]
			},
			"Dimension Reduction": {
				"overview": {
					"img": "",
					"description": [
						"Reduce the dimensionality of the data and embed cells into two-dimensional space. Refer to the functions from ",
						{
							"component": "a",
							"kwargs": {
								"href": "https://scanpy.readthedocs.io/en/stable/index.html",
								"children": "Scanpy"
							}
						},
						" and ",
						{
							"component": "a",
							"kwargs": {
								"href": "https://scikit-learn.org/stable/index.html",
								"children": "scikit-learn"
							}
						},
						" packages."
					]
				},
				"form introduction": {
					"img": "../assets/image/document_preprocessing_dimensionreduction.png",
					"inputs": {
						"Method": "The method to reduce dimension and embed cells, including PCA, t-SNE, and UMAP.",
						"N PCs": "The number of PC used for PCA and the calculation of KNN graph (Method='UMAP').",
						"N Neighbors": "The size of local neighborhood used for UMAP. Visible when setting 'Method' as 'UMAP'.",
						"Min Dist": "The effective minimum distance between embedded points. Visible when setting 'Method' as 'UMAP'.",
						"Metric": "The metric name used for distance computation. Visible when setting 'Method' as 'UMAP' or 't-SNE'."
					}
				},
				"example": [
					{
						"video": "../assets/video/document_preprocessing_NHD.mp4",
						"title": "The normalization, HVG detection, and dimension reduction analysis in CellClick",
						"description": "You will be informed by the Alert component when the analysis is complete."
					}
				]
			},
			"Cell Clustering": {
				"overview": {
					"img": "",
					"description": [
						"""
							CellClick identifies cell types using either cell clustering results or the original annotation. 
							So you need to cluster cells for un-preprocessed data or set the original annotation result for preprocessed data. 
							For un-preprocessed data, the Leiden or Louvain algorithms are provided for cell clustering, 
							and the results will be stored with the prefix 'CellClick_'. Refer to 
						""",
						{
							"component": "a",
							"kwargs": {
								"href": "https://scanpy.readthedocs.io/en/stable/generated/scanpy.tl.leiden.html",
								"children": "scanpy.tl.leiden"
							}
						},
						" and ",
						{
							"component": "a",
							"kwargs": {
								"href": "https://scanpy.readthedocs.io/en/stable/generated/scanpy.tl.louvain.html",
								"children": "scanpy.tl.louvain"
							}
						},
						"."
					]
				},
				"form introduction": {
						"img": "../assets/image/document_preprocessing_cellclustering.png",
						"inputs": {
							"Preprocessed": """
							'Custom' and 'CellClick' are available in this input. 'Custom' means preprocessed data, while 'CellClick' means unpreprocessed data.
						""",
							"Reference": "The column name of original annotation result stored in adata.obs. Visible when setting 'Processed By' as 'Custom'.",
							"Method": "The Leiden or Louvain algorithm used to cluster cells. Visible when setting 'Processed By' as 'CellClick'.",
							"Resolution": "The resolution for cell clustering results. Visible when setting 'Processed By' as 'CellClick'."
						}
					},
				"example": [
					{
						"video": "",
						"title": "",
						"description": ""
					}
				]
			}
		}
	},
	"Data Visualization": {
		"overview": "CellClick supports interactive visualization functions to facilitate cell embedding, gene embedding, and gene dot graph generation.",
		"forms": {
			"Cell Embedding": {
				"overview": {
					"img": "",
					"description": """
						Cell embedding empowers direct visualization of cell features in low-dimensional space, which is essential for cell type identification.
					"""
				},
				"form introduction": {
					"img": "../assets/image/document_datavisualization_cellembedding.png",
					"inputs": {
						"Embedding": "The space name used to embed cells.",
						"Annotation": "The annotation to color cells."
					}
				},
				"example": [
					{
						"video": "../assets/video/document_datavisulization_cellembedding.mp4",
						"title": "Cell selection on cell embedding results",
						"description": """
							You can select cells in the embedding results via box selection or lasso selection tools, 
							then employ the selected cells for different downstream analysis. 
							By clicking on the legend icon of each cell cluster, the target cell cluster can be hidden or redisplayed, 
							thus helping you visualize and select specific cell sets more accurately.
						"""
					}
				]
			},
			"Gene Embedding": {
				"overview": {
					"img": "",
					"description": """
						The gene embedding function displays gene expression profiles in embedding space, which provides direct evidence for cell type identification.
					"""
				},
				"form introduction": {
					"img": "../assets/image/document_datavisualization_geneembedding.png",
					"inputs": {
						"Gene Name": "The gene to color cells.",
						"Embedding": "The space name used to embed cells."
					}
				},
				"example": [
					{
						"video": "../assets/video/document_datavisulization_geneembedding.mp4",
						"title": "Gene embedding",
						"description": "The expression profile of the target gene is shown in the embedding space."
					}
				]
			},
			"Gene Dot": {
				"overview": {
					"img": "",
					"description": "This function visualizes the expression of multiple genes, which provides statistical evidence for cell type identification."
				},
				"form introduction": {
					"img": "../assets/image/document_datavisualization_genedot.png",
					"inputs": {
						"Gene Name": "The genes to visualize.",
						"Annotation": "The annotation to group cells."
					}
				},
				"example": [
					{
						"video": "../assets/video/document_datavisulization_genedot.mp4",
						"title": "Gene dot",
						"description": "In the dot plot, you can add or delete genes in the 'Gene Name' input."
					}
				]
			}
		}
	},
	"Gene Analysis": {
		"overview": """
			The Cell Annotation module aims to provide fast and accurate cell identification methods, 
			which include Marker Gene Identification and Cell Identification functions.
		""",
		"forms": {
			"Marker Gene Identification": {
				"overview": {
					"img": "",
						"description": [
							"""
								Marker gene identification is a basic and crucial step for single-cell or spatial omics sequencing data analysis. 
								To facilitate fast and accurate marker gene identification, CellClick implements 
							""",
						{
							"component": "a",
							"kwargs": {
								"href": "https://github.com/genecell/COSG",
								"children": "COSG"
							}
						},
						", an efficient and accurate cell marker gene identification algorithm based on cosine similarity."
					]
				},
				"form introduction": {
					"img": "",
					"inputs": {
						"Annotation": "The key of the cell groups in adata.obs.",
						"Group A": """
							The cell group(s) for marker gene identification. If 'selected', CellClick will identify marker genes for selected cells and Group B. 
							If 'all', 'none' is the only valid value for Group B, and CellClick will identify marker genes for each cell group.
						""",
						"Group B": """
							The reference cell group(s) for marker gene identification. If 'rest', CellClick will compare Group A with all other cells. 
							If 'none', CellClick will identify the marker gene for each cell group in the group A.
						"""
					}
				},
				"example": [
					{
						"video": "../assets/video/document_AE_MGI.mp4",
						"title": "Marker gene identification",
						"description": """
							Only when both group buttons are inactive is the submit button available to click. 
							When the group button is inactive, the group input is disabled. 
							The Group B button is inactive when the Group A button is active. 
						"""
					}
				]
			},
			"Marker Gene Evaluation": {
				"overview": {
					"img": "",
					"description": """
						The Cell Identification function provides a fast method to annotate cell types based on identified marker genes and reference marker genes. 
						It considers the percentage of information used for querying and the total confidence calculated from the specificity and sensitivity of identified marker genes. 
						For more accurate cell identification, the Cell Identification function generates a dot plot to visualize the expression pattern of identified marker genes 
						and the overlap between identified marker genes and reference marker genes.
					"""
				},
				"form introduction": {
					"img": "../assets/image/document_AE_MGE.png",
					"inputs": {
						"Marker Source": "The source of the reference marker genes.",
						"Species": "Obtain the reference marker genes from the specified species.",
						"Cluster Name": "The cell cluster for Cell Identification function.",
						"Gene Number": "The number of identified marker genes used for the Cell Identification function."
					}
				},
				"example": [
					{
						"video": "../assets/video/document_AE_ MGE.mp4",
						"title": "Cell Identification",
						"description": """
							In the results of the Cell Identification function, the bar plot shows the gene scores of different cell types in reference data. 
							In the dot plot, the genes colored by red are the overlap genes between identified genes 
							and suggested marker genes of cell type selected by 'Cell Type' input, 
							while the genes colored by blue are the unique genes of identified genes. 
							You can annotate the cell type directly in the Cell Identification function result by clicking the 'Annotation' button.
						"""
					}
				]
			}
		}
	},
	"Evaluation and Validation": {
		"overview": """
			The Annotation Validation module includes Annotation Evaluation and Reference Comparison functions, 
			which allows users to evaluate cell annotation results.
		""",
		"forms": {
			"Annotation Evaluation": {
				"overview": {
					"img": "",
					"description": """
						The Annotation Evaluation function invokes Gene Dot and Gene Embedding functions to 
						display the expression profiles of identified marker genes for a chosen cell type.
					"""
				},
				"form introduction": {
					"img": "",
					"inputs": {
						"Cell Cluster": "The cell cluster for Annotation Evaluation function.",
						"Gene Number": "The number of identified marker genes used for the Annotation Evaluation function.",
						"Embedding": "The space name used to embed cells."
					}
				},
				"example": [
					{
						"video": "",
						"title": "",
						"description": """"""
					}
				]
			},
			"Marker Gene Scoring": {
				"overview": {
					"img": "",
					"description": """
						The Reference Comparison function measures the similarity based on gene similarity, relative expression specificity, 
						and expression abundance difference between identified marker genes and suggested marker genes. 
						Similar to the Cell Identification function, the Reference Comparison function also provides a dot plot for users to 
						evaluate the confidence of the results, which shows the expression pattern of suggested marker genes.
					"""
				},
				"form introduction": {
					"img": "../assets/image/document_AE_CE.png",
					"inputs": {
						"Marker Source": """
							Besides pre-uploaded marker gene reference, CellClick allows custom marker gene reference formatted as JSON file. 
							You can store it in the 'marker_ref/Other' directory and select 'Other'. 
							You can also select other uploaded data by choosing 'Upload Data' and identify its marker genes as a marker gene reference.
						""",
						"Source Name": "The tissue name, custom marker gene reference name, or data ID for cluster evaluation.",
						"Cell Cluster": "The cell cluster for cluster evaluation.",
						"Gene Number": "The number of reference marker genes used for cluster evaluation."
					}
				},
				"example": [
					{
						"video": "../assets/video/document_AE_ CE.mp4",
						"title": "Reference Comparison",
						"description": """
							In the results of the Reference Comparison function, the violin plot shows the cluster scores of suggested marker genes across different cell types. 
							Generally, a high cluster score distribution shows suggested marker genes highly and specifically expressed in the cell cluster, 
							which always demonstrates a high confidence to annotate cell clusters as the corresponding cell type. 
							The dot plot shows the expression pattern of the suggested marker genes from the cell type selected by 'Cell Type' input. 
							You can annotate the cell type directly in the Reference Comparison function by clicking the 'Annotation' button.
						"""
					}
				]
			}
		}
	},
	"Cell Reannotation": {
		"overview": """
				The Cell Reannotation module incorporates Cell Selection, Cell Reclustering, Cluster Reannotation, 
				and Annotation Update functions, which facilitate users to select target cells for refined annotation.
			""",
		"forms": {
			"Cell Selection": {
				"overview": {
					"img": "",
					"description": """
						Cell reannotation requires accurate selection of a specific cell set, 
						which relies on many factors, such as cell cluster, gene expression, and coordinate information in embedding space, 
						and remains a challenge in most available software. 
						CellClick has developed two cell selection methods with cell visualization results and a cell table.
					"""
				},
				"form introduction": {
					"img": "",
					"inputs": {
						"Embedding": "The space name used to embed cells.",
						"Annotation": "The annotation to group cells.",
						"Table Content": "Metadata or gene expression shown in the Cell Table.",
					}
				},
				"example": [
					{
						"video": "../assets/video/document_datavisulization_cellembedding.mp4",
						"title": "Cell selection on cell embedding results",
						"description": """
							You can select cells in the embedding results via box selection or lasso selection icons, 
							then employ the selected cells for different downstream analysis. By clicking on the legend icon of each cell cluster, 
							the target cell cluster can be hidden or redisplayed, thus helping you visualize and select specific cell sets more accurately.
						"""
					},
					{
						"video": "../assets/video/document_CR_CellsTable.mp4",
						"title": "Cell Table Introduction",
						"description": """
							Cell Table is an interactive table for cell querying based on cell attributes. 
							You can show the data frame stored in adata.obs or adata.X by changing the value of the 'Table Content' input. 
							You can also add or remove columns from the displayed information by using the 'Add Column' and 'Remove Column' inputs.
						"""
					},
					{
						"video": "../assets/video/document_CR_CSByCT.mp4",
						"title": "Cell selection on Cell Table",
						"description": """
							You can query and select cells by attributes in the Cell Table, 
							for example, selecting a special cell cluster based on cell cluster results.
						"""
					},
					{
						"video": "../assets/video/document_CR_MultiCS.mp4",
						"title": "Cell selection flow in CellClick",
						"description": """
							The selection results can be fixed with 'Fix Selection' button, and then be merged with novel cell selection results. 
							CellClick supports the difference, union, and intersection between two cell selection results 
							with the plus, minus, and heart buttons.
						"""
					}
				]
			},
			"Reannotation": {
				"overview": {
					"img": "",
					"description": "Cluster Reannotation function provides a direct method to annotate cell sets."
				},
				"form introduction": {
					"img": "../assets/image/document_CR_reannotation.png",
					"inputs": {
						"Raw Name": "The raw name of cell cluster.",
						"New Name": "The new name of cell cluster."
					}
				},
				"example": [
					{
						"video": "../assets/video/document_CR_reannotation.mp4",
						"title": "Reannotate cell cluster",
						"description": ""
					}
				]
			},
			"Re-cluster": {
				"overview": {
					"img": "",
					"description": "You can re-cluster the target cell set with the Re-clustering function."
				},
				"form introduction": {
					"img": "../assets/image/document_CR_recluster.png",
					"inputs": {
						"Cluster": "The cell cluster to re-cluster. If 'selected', CellClick will re-cluster the selected cells.",
						"Dimension Reduction": "Display or hide the inputs for dimension reduction. If inactive, dimension reduction analysis will be disabled.",
						"dimension_Method": "The method to reduce dimension and embed cells, including PCA, t-SNE, and UMAP.",
						"N PCs": "The number of PC used for PCA and the calculation of KNN graph (Method='UMAP').",
						"N Neighbors": "The size of local neighborhood used for UMAP. Visible when setting 'Method' as 'UMAP'.",
						"Min Dist": "The effective minimum distance between embedded points. Visible when setting 'Method' as 'UMAP'.",
						"Metric": "The metric name used for distance computation. Visible when setting 'Method' as 'UMAP' or 't-SNE'.",
						"Cell Reclustering": "Display or hide the inputs for cell reclustering.",
						"Method": "The clustering algorithm (Louvain or Leiden) used to cluster cells.",
						"Resolution": "The resolution for cell clustering results."
					}
				},
				"example": [
					{
						"video": "../assets/video/document_CR_recluster.mp4",
						"title": "Re-cluster cells",
						"description": ""
					}
				]
			},
			"Merge Data": {
				"overview": {
					"img": "",
					"description": """
							After reannotating the reclustered cells, you can run the Annotation Update function to merge the newly annotated cell clusters with other cell clusters.
						"""
				},
				"form introduction": {
					"img": "../assets/image/document_CR_MD.png",
					"inputs": {
						"Ref Data": "The source data.",
						"Other Data": "The subset data."
					}
				},
				"example": [
					{
						"video": "../assets/video/document_CR_MD.mp4",
						"title": "Annotation Update",
						"description": """
							The Annotation Update function replaces the cell annotations in the source data with the annotations of cells from the subset data.
						"""
					}
				]
			}
		}
	}
}

import json

with open("./document.json", "w") as f:
    json.dump(document, f)
