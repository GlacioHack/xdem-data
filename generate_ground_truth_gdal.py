from osgeo import gdal
import os


def generate_gdal_truth(filepath: str, output_dir: str) -> None:
    """Run GDAL's DEMProcessing for all attibutes and save in .tif"""

    # Define attributes and options
    gdal_processing_attr_option = {
        "slope_Horn": ("slope", "Horn"),
        "aspect_Horn": ("aspect", "Horn"),
        "hillshade_Horn": ("hillshade", "hillshade_Horn"),
        "slope_Zevenberg": ("slope", "Zevenberg"),
        "aspect_Zevenberg": ("aspect", "Zevenberg"),
        "hillshade_Zevenberg": ("hillshade", "hillshade_Zevenberg"),
        "tri_Riley": ("TRI", "Riley"),
        "tri_Wilson": ("TRI", "Wilson"),
        "tpi": ("TPI", None),
        "roughness": ("Roughness", None),
    }

    # Create output directory if needed
    os.makedirs(output_dir, exist_ok=True)

    # Execute GDAL for every attribute
    for attr, (processing, option) in gdal_processing_attr_option.items():
        print(f"Processing GDAL truth for: {attr}")

        # Convert GDAL options
        if option is None:
            gdal_option = gdal.DEMProcessingOptions(options=None)
        else:
            gdal_option_conversion = {
                "Riley": gdal.DEMProcessingOptions(alg="Riley"),
                "Wilson": gdal.DEMProcessingOptions(alg="Wilson"),
                "Zevenberg": gdal.DEMProcessingOptions(alg="ZevenbergenThorne"),
                "Horn": gdal.DEMProcessingOptions(alg="Horn"),
                "hillshade_Zevenberg": gdal.DEMProcessingOptions(azimuth=315, altitude=45, alg="ZevenbergenThorne"),
                "hillshade_Horn": gdal.DEMProcessingOptions(azimuth=315, altitude=45, alg="Horn"),
            }
            gdal_option = gdal_option_conversion[option]

        # Create file for saving GDAL's results
        output = os.path.join(output_dir, f"{attr}.tif")

        # Execute GDAL
        gdal.DEMProcessing(
            destName=output,
            srcDS=filepath,
            processing=processing,
            options=gdal_option,
        )


if __name__ == "__main__":
    filepath = "data/Longyearbyen/DEM_2009_ref.tif"
    output_dir = "test_data/gdal"
    generate_gdal_truth(filepath, output_dir)
