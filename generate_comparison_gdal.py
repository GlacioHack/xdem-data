from osgeo import gdal
import os
import numpy as np
import geoutils as gu


def generate_gdal_comparison(filepath: str, outdir: str) -> None:
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
        output = os.path.join(outdir, f"{attr}.tif")

        # Execute GDAL
        gdal.DEMProcessing(
            destName=output,
            srcDS=filepath,
            processing=processing,
            options=gdal_option,
        )


def gdal_reproject_horizontal_shift_samecrs(filepath_example: str, xoff: float, yoff: float, outdir: str):
    """
    Reproject horizontal shift in same CRS with GDAL for testing purposes.

    :param filepath_example: Path to raster file.
    :param xoff: X shift in georeferenced unit.
    :param yoff: Y shift in georeferenced unit.
    :param outdir: output directory.

    :return: Reprojected shift array in the same CRS.
    """

    from osgeo import gdal, gdalconst

    # Open source raster from file
    src = gdal.Open(filepath_example, gdalconst.GA_ReadOnly)

    # Create output raster in memory
    driver = "MEM"
    method = gdal.GRA_Bilinear
    drv = gdal.GetDriverByName(driver)
    dest = drv.Create("", src.RasterXSize, src.RasterYSize, 1, gdal.GDT_Float32)
    proj = src.GetProjection()
    ndv = src.GetRasterBand(1).GetNoDataValue()
    dest.SetProjection(proj)

    # Shift the horizontally shifted geotransform
    gt = src.GetGeoTransform()
    gtl = list(gt)
    gtl[0] += xoff
    gtl[3] += yoff
    dest.SetGeoTransform(tuple(gtl))

    # Copy the raster metadata of the source to dest
    dest.SetMetadata(src.GetMetadata())
    dest.GetRasterBand(1).SetNoDataValue(ndv)
    dest.GetRasterBand(1).Fill(ndv)

    # Reproject with resampling
    gdal.ReprojectImage(src, dest, proj, proj, method)

    # Extract reprojected array
    array = dest.GetRasterBand(1).ReadAsArray().astype("float32")
    array[array == ndv] = np.nan

    filename = os.path.join(outdir, f"shifted_reprojected_xoff{xoff}_yoff{yoff}.tif")
    output_driver = gdal.GetDriverByName("GTiff")
    output_raster = output_driver.Create(
        filename, dest.RasterXSize, dest.RasterYSize, 1, gdal.GDT_Float32
    )
    output_raster.SetGeoTransform(dest.GetGeoTransform())
    output_raster.SetProjection(dest.GetProjection())
    output_band = output_raster.GetRasterBand(1)
    output_band.WriteArray(array)
    output_band.SetNoDataValue(ndv)
    output_raster.FlushCache()


if __name__ == "__main__":
    filepath = "data/Longyearbyen/DEM_2009_ref.tif"
    outdir = "test_data/gdal"

    # Create output directory if needed
    os.makedirs(outdir, exist_ok=True)

    generate_gdal_comparison(filepath, out_dir)

    dem = gu.Raster(filepath)
    list_off = [(dem.res[0], dem.res[1]), (10 * dem.res[0], 10 * dem.res[1]), (-1.2 * dem.res[0], -1.2 * dem.res[1])]
    for x_off, y_off in list_off:
        gdal_reproject_horizontal_shift_samecrs(filepath, x_off, y_off, outdir)
