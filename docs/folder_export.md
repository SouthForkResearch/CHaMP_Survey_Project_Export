---
title: Flat File Exports
---



The folder Export tool exports CHaMP Survey data into open source files within the specified folder. The exact number of files depends on the number of standard CHaMP datasets found within the survey GDB:

- from ESRI File-Geodatabase Feature Classes to shapefile format
- from ESRI File-Geodatabase raster datasets to geotiff format
- ESRI TIN Components as Shapefiles
- The following datasets are exported to the "CAD_Files" folder.
  - TopoTIN.DXF
    - This represents the crew edited TIN.
    - Layers:
      - **tin_nodes** xyz nodes of tin
      - **tin_edges** triangle edges of tin
        - *LINETYPE* Indicates if edge is Hard, Soft, or Regular edge
      - **tin_area** Polygon area of TIN Interpolation
  - SurveyTopography.DXF
    - This dataset represents the data that was used to create the TIN ***prior*** to crew editing.
    - Layers:
      - **AllPoints** Surveyed points used to describe the topography of the site
      - **Breaklines** Surveyed line features used to construct breaklines in the TIN
      - **SurveyExtent** Polygon area used to constrain TIN interpolation.
  - SurveyTopographyPoints.csv
    - CSV output of Topo_Points and EdgeofWaterPoints
  - ControlNetwork.csv
    - CSV output of Control Points and Benchmarks, including:
      - Control Points and benchmarks loaded to total station prior to survey
      - Control Points and benchmarks added during survey.

