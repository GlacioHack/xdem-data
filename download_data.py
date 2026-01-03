"""Utility functions to download and find example data."""
import asyncio
import os

from sliderule import sliderule, icesat2, earthdata
import numpy as np
import geopandas as gpd
import rasterio as rio
from pyproj import CRS
from geoutils.projtools import _get_bounds_projected

OVERWRITE_LONGYEARBYEN_DEM = False
OVERWRITE_LONGYEARBYEN_EPC = False

EXAMPLES_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), "data/"))

# Absolute filepaths to the example files.
FILEPATHS_NPOLAR = {
    "longyearbyen_ref_dem": os.path.join(EXAMPLES_DIRECTORY, "Longyearbyen/DEM_2009_ref.tif"),
    "longyearbyen_tba_dem": os.path.join(EXAMPLES_DIRECTORY, "Longyearbyen/DEM_1990.tif"),
    "longyearbyen_glacier_outlines": os.path.join(
        EXAMPLES_DIRECTORY,
        "Longyearbyen/glacier_mask/CryoClim_GAO_SJ_1990.shp"
    ),
    "longyearbyen_glacier_outlines_2010": os.path.join(
        EXAMPLES_DIRECTORY,
        "Longyearbyen/glacier_mask/CryoClim_GAO_SJ_2010.shp"
    )

}

FILEPATH_IS2 = {"longyearbyen_epc": os.path.join(EXAMPLES_DIRECTORY, "Longyearbyen/EPC_IS2.parquet")}

# The URLs for where to find the data.
URLS = {
    "longyearbyen_ref_dem": ("zip+https://publicdatasets.data.npolar.no/kartdata/S0_Terrengmodell/"
                             "Mosaikk/NP_S0_DTM20.zip!NP_S0_DTM20/S0_DTM20.tif"),
    "longyearbyen_tba_dem": ("zip+https://publicdatasets.data.npolar.no/kartdata/S0_Terrengmodell/"
                             "Historisk/NP_S0_DTM20_199095_33.zip!NP_S0_DTM20_199095_33/S0_DTM20_199095_33.tif"),
    "longyearbyen_glacier_outlines": "http://public.data.npolar.no/cryoclim/CryoClim_GAO_SJ_1990.zip",
    "longyearbyen_glacier_outlines_2010": "https://public.data.npolar.no/cryoclim/CryoClim_GAO_SJ_2001-2010.zip"
}

# The bounding coordinates to crop the datasets.
bounds = {
    "west": 502810,
    "east": 529450,
    "south": 8654330,
    "north": 8674030
}

async def _async_load_svalbard():
    """Load the datasets asynchronously."""

    async def crop_dem(input_path, output_path, bounds):
        """Read the input path and crop it to the given bounds."""
        dem = rio.open(input_path)

        upper, left = dem.index(bounds["west"], bounds["north"])
        lower, right = dem.index(bounds["east"], bounds["south"])
        window = rio.windows.Window.from_slices((upper, lower), (left, right))

        data = dem.read(1, window=window)
        meta = dem.meta.copy()
        meta.update({
            "transform": dem.window_transform(window),
            "height": window.height,
            "width": window.width
        })
        with rio.open(output_path, "w", **meta) as raster:
            raster.write(data, 1)
        print(f"Saved {output_path}")

    async def read_outlines(input_path, output_path):
        """Read outlines from a path and save them."""
        outlines = gpd.read_file(input_path)
        for col in outlines:
            if outlines[col].dtype == "object":
                outlines[col] = outlines[col].astype(str)
        outlines.to_file(output_path)
        print(f"Saved {output_path}")

    await asyncio.gather(
        crop_dem(URLS["longyearbyen_ref_dem"], FILEPATHS_NPOLAR["longyearbyen_ref_dem"], bounds=bounds),
        crop_dem(URLS["longyearbyen_tba_dem"], FILEPATHS_NPOLAR["longyearbyen_tba_dem"], bounds=bounds),
        read_outlines(URLS["longyearbyen_glacier_outlines"], FILEPATHS_NPOLAR["longyearbyen_glacier_outlines"]),
        read_outlines(URLS["longyearbyen_glacier_outlines_2010"], FILEPATHS_NPOLAR["longyearbyen_glacier_outlines_2010"])
    )


def download_longyearbyen_examples(overwrite: bool = False):
    """
    Fetch the Longyearbyen example files.

    :param overwrite: Do not download the files again if they already exist.
    """
    if not overwrite and all(map(os.path.isfile, list(FILEPATHS_NPOLAR.values()))):
        print("Datasets exist")
        return
    print("Downloading datasets from Longyearbyen")
    os.makedirs(os.path.dirname(FILEPATHS_NPOLAR["longyearbyen_glacier_outlines"]), exist_ok=True)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_async_load_svalbard())

def download_icesat2_examples(overwrite: bool = False):
    """
    Fetch the ICESat-2 example file using SlideRule.

    :param overwrite: Do not download the files again if they already exist.
    """

    if not overwrite and os.path.isfile(FILEPATH_IS2["longyearbyen_epc"]):
        print("ICESat-2 dataset exists.")
        return

    print("Downloading ICESat-2 in Longyearbyen.")

    # Define region polygon
    bbox = rio.coords.BoundingBox(bounds["west"], bounds["south"], bounds["east"], bounds["north"])
    bbox_poly_geographic = list(_get_bounds_projected(bbox, in_crs=CRS.from_epsg(25833), out_crs=CRS.from_epsg(4326)))
    region = sliderule.toregion(bbox_poly_geographic)["poly"]

    # Initialize SlideRule client
    sliderule.init("slideruleearth.io")

    # Define desired parameters for ICESat-2 ATL06
    params = {
        "poly": region,
        "srt": icesat2.SRT_LAND,  # Surface-type
        "cnf": icesat2.CNF_SURFACE_HIGH,  # Confidence level
        "ats": 20.0,  # Minimum along-track spread
        "cnt": 10,  # Minimum count
        "t0": "2018-01-01T00:00:00Z",  # Start time
        "t1": "2022-01-01T00:00:00Z",  # Stop time (to keep it under 300 granules)
    }
    # Request ATL06 subsetting in parallel
    gdf = icesat2.atl06sp(params)
    gdf = gdf[np.isfinite(gdf["h_li"])]  # Keep valid data
    gdf = gdf[gdf["atl06_quality_summary"] == 0]  # Keep very high-confidence data

    # Save to file
    gdf.to_parquet(FILEPATH_IS2["longyearbyen_epc"])
        

if __name__ == "__main__":
    download_longyearbyen_examples(overwrite=OVERWRITE_LONGYEARBYEN_DEM)
    download_icesat2_examples(overwrite=OVERWRITE_LONGYEARBYEN_EPC)