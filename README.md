# xdem-data

Test and example data for [xDEM](https://github.com/GlacioHack/xdem).

All data copyright is with the associated download locations. 
This repo holds modified versions of these data, but we do not claim any rights to them.

## Longyearbyen

The first site is Longyearbyen, the world's northernmost settlement and the capital of Svalbard, a Norwegian archipelago
north of the European continent.

#### DEM_1990.tif and DEM_2009.tif (©Norwegian Polar Institute – CC BY 4.0)

These two rasters (TIFs), from the Terrengmodell Svalbard (S0 Terrengmodell) dataset[^1],
represent two DEMs above mean sea level, generated from stereo models constructed
on aerial photos. They cover the west middle part of Svalbard, south of Longyearbyen, at 20 meters resolution with 100% 
of land cover.  

#### CryoClim_GAO_SJ_1990.shp and CryoClim_GAO_SJ_2010.shp (©Norwegian Polar Institute – CC BY 4.0)

These two vectors (shapefiles), from the Glacier Area Outlines - Svalbard 1936-2010 dataset[^2],
represent the glacier outlines in Svalbard in 1990 and for the 2001-2010 period. 
The first one was created using cartographic data from the original Norwegian Polar Institute topographic map series as 
basis by delineating individual glaciers and ice streams, assigning unique identification codes relating to the hydrological 
watersheds, digitizing center-lines, and providing a number of attributes for each glacier mask.
The second one is derived from orthorectified satellite images acquired from the SPOT-5 and ASTER satellite sensors.

#### EPC_IS2.parquet

This point cloud data comes from NASA National Snow and Ice Data Center Distributed Active Archive Center 
(NSIDC DAAC) ATLAS/ICESat-2 L3A Land Ice Height dataset (ATL06, Version 7)[^3], 
measuring land elevation along 40 m segments of ground track, spaced 20 m apart. The data were acquired by
the Advanced Topographic Laser Altimeter System (ATLAS) and retrieved using the SlideRule[^4] software, over the DEM aera and 
between October 2018 and September 2026.

## Giza

The second site is Giza, a pyramid complex located in the outskirts of Cairo, Egypt dating from 2500 BC. 

#### DSM.tif (DSM Giza Pyramids ©2026 by CARS Version 0.12.3 – CC BY-NC 4.0)

This raster was generated with [CARS v0.12.3](https://github.com/CNES/cars)[^5], an open source 3D tool dedicated to produce
Digital Surface Models from stereo satellite images by using photogrammetry. The inputs data are proposed by CARS itself, from a tri-stereo 
Pleiades from 08/02/2013 ([OPEN LICENCE 2.0](data_license/open-licence-etalab-v2.0-en.pdf)), which can be downloaded using :

    wget https://raw.githubusercontent.com/CNES/cars/master/tutorials/data_gizeh.tar.bz2
    wget https://raw.githubusercontent.com/CNES/cars/master/tutorials/data_gizeh.tar.bz2.md5sum
    md5sum --status -c data_gizeh.tar.bz2.md5sum
    tar xvfj data_gizeh.tar.bz2

The output DSM can be re-generated following the process described in the 
[documentation](https://cars.readthedocs.io/en/0.12.3/getting_started.html) (CARS v0.12.3). Unlike the previous ones, 
it has a 3D CRS information and contains NaN values (due to occlusion). 

[^1]: Norwegian Polar Institute (2014). Terrengmodell Svalbard (S0 Terrengmodell) [Dataset]. Norwegian Polar Institute. [https://doi.org/10.21334/NPOLAR.2014.DCE53A47](https://doi.org/10.21334/NPOLAR.2014.DCE53A47)

[^2]: König, M., Kohler, J., & Nuth, C. (2013). Glacier Area Outlines - Svalbard 1936-2010 [Dataset]. Norwegian Polar Institute. [https://doi.org/10.21334/NPOLAR.2013.89F430F8](https://doi.org/10.21334/NPOLAR.2013.89F430F8)

[^3]: Smith, B., Adusumilli, S., Csathó, B. M., Felikson, D., Fricker, H. A., Gardner, A. S., Holschuh, N., Lee, J., Nilsson, J., Paolo, F., Siegfried, M. R., Sutterley, T. & the ICESat-2 Science Team. (2025). ATLAS/ICESat-2 L3A Land Ice Height. (ATL06, Version 7). 
Boulder, Colorado USA. NASA National Snow and Ice Data Center Distributed Active Archive Center. [https://doi.org/10.5067/ATLAS/ATL06.007](https://doi.org/10.5067/ATLAS/ATL06.007). 
Date Accessed 11-17-2026.

[^4]: Shean et al., (2023). SlideRule: Enabling rapid, scalable, open science for the NASA ICESat-2 mission and beyond. Journal of Open Source Software, 8(81), 4982, [https://doi.org/10.21105/joss.04982](https://doi.org/10.21105/joss.04982)

[^5]: D. Youssefi et al., "CARS: A Photogrammetry Pipeline Using Dask Graphs to Construct A Global 3D Model," IGARSS 2020 - 2020 IEEE International Geoscience and Remote Sensing Symposium, Waikoloa, HI, USA, 2020, pp. 453-456, [https://doi.org/10.1109/IGARSS39084.2020.9324020](https://doi.org/10.1109/IGARSS39084.2020.9324020)