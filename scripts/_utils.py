#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Shi4712
@description: 
@version: 1.0.0
@file: _utils.py
@time: 2023/10/17 22:01
"""

"""
@File        : __utils.py
@Author      : Min Dai, shi4712
@Date        : 2022/9/6 14:35
@Description : some function copied/modified from reference
"""

# to avoid the version change, I copied sever function from scanpy to plot spatial plot
# refer to: https://github.com/scverse/scanpy/blob/1.8.x/scanpy/plotting/_tools/scatterplots.py
from typing import Union, Optional, Sequence, Any, Mapping, List, Tuple

import numpy as np

from scanpy._utils import Empty, _empty


def _check_spatial_data(
    uns: Mapping, library_id: Union[Empty, None, str]
) -> Tuple[Optional[str], Optional[Mapping]]:
    """
    Given a mapping, try and extract a library id/ mapping with spatial data.

    Assumes this is `.uns` from how we parse visium data.
    """
    spatial_mapping = uns.get("spatial", {})
    if library_id is _empty:
        if len(spatial_mapping) > 1:
            raise ValueError(
                "Found multiple possible libraries in `.uns['spatial']. Please specify."
                f" Options are:\n\t{list(spatial_mapping.keys())}"
            )
        elif len(spatial_mapping) == 1:
            library_id = list(spatial_mapping.keys())[0]
        else:
            library_id = None
    if library_id is not None:
        spatial_data = spatial_mapping[library_id]
    else:
        spatial_data = None
    return library_id, spatial_data


def _check_img(
    spatial_data: Optional[Mapping],
    img: Optional[np.ndarray],
    img_key: Union[None, str, Empty],
    bw: bool = False,
) -> Tuple[Optional[np.ndarray], Optional[str]]:
    """
    Resolve image for spatial plots.
    """
    if img is None and spatial_data is not None and img_key is _empty:
        img_key = next(
            (k for k in ['hires', 'lowres'] if k in spatial_data['images']),
        )  # Throws StopIteration Error if keys not present

        # #  for test
        # try:
        #     img_key = next(
        #         (k for k in ['hires', 'lowres'] if k in spatial_data['images']),
        #     )  # Throws StopIteration Error if keys not present
        # except StopIteration: #
        #     img_key = None
    if img is None and spatial_data is not None and img_key is not None:
        img = spatial_data["images"][img_key]
    if bw:
        img = np.dot(img[..., :3], [0.2989, 0.5870, 0.1140])
    return img, img_key


def _check_spot_size(
    spatial_data: Optional[Mapping], spot_size: Optional[float]
) -> float:
    """
    Resolve spot_size value.

    This is a required argument for spatial plots.
    """
    if spatial_data is None and spot_size is None:
        raise ValueError(
            "When .uns['spatial'][library_id] does not exist, spot_size must be "
            "provided directly."
        )
    elif spot_size is None:
        return spatial_data['scalefactors']['spot_diameter_fullres']
    else:
        return spot_size


def _check_scale_factor(
    spatial_data: Optional[Mapping],
    img_key: Optional[str],
    scale_factor: Optional[float],
) -> float:
    """Resolve scale_factor, defaults to 1."""
    if scale_factor is not None:
        return scale_factor
    elif spatial_data is not None and img_key is not None:
        return spatial_data['scalefactors'][f"tissue_{img_key}_scalef"]
    else:
        return 1.0

def _check_crop_coord(
        crop_coord: Optional[tuple],
        scale_factor: float,
) -> Tuple[float, float, float, float]:
    """Handle cropping with image or basis."""
    if crop_coord is None:
        return None
    if len(crop_coord) != 4:
        raise ValueError("Invalid crop_coord of length {len(crop_coord)}(!=4)")
    crop_coord = tuple(c * scale_factor for c in crop_coord)
    return crop_coord


# modified from: https://github.com/scverse/scanpy/blob/1.8.x/scanpy/plotting/_tools/scatterplots.py#L907
def _process_image(
    adata,
    *,
    basis: str = "spatial",
    img: Union[np.ndarray, None] = None,
    img_key: Union[str, None, Empty] = _empty,
    library_id: Union[str, Empty] = _empty,
    crop_coord: Tuple[int, int, int, int] = None,
    # alpha_img: float = 1.0,
    bw: Optional[bool] = False,
    # size: float = 1.0,
    scale_factor: Optional[float] = None,
    spot_size: Optional[float] = None
):
    library_id, spatial_data = _check_spatial_data(adata.uns, library_id)
    img, img_key = _check_img(spatial_data, img, img_key, bw=bw)
    spot_size = _check_spot_size(spatial_data, spot_size)
    scale_factor = _check_scale_factor(
        spatial_data, img_key=img_key, scale_factor=scale_factor
    )
    crop_coord = _check_crop_coord(crop_coord, scale_factor)
    return library_id, img_key, spot_size, scale_factor, crop_coord

