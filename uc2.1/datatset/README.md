
# Six-Month Monitoring Dataset from a 10-Turbine Onshore Wind Farm in Greece


## Dataset overview


The SCADA dataset underwent a comprehensive exploratory data analysis using [ydata-profiling](https://github.com/ydataai/ydata-profiling). This tool was used to automatically generate detailed HTML reports for each dataset or relevant data subset. These reports include:

- Descriptive statistics for all features (e.g., mean, median, min, max, standard deviation)
- Distribution plots for numerical and categorical variables
- Missing value summaries
- Outlier detection using statistical heuristics (e.g., IQR)
- Correlation matrices to highlight linear or non-linear dependencies
- Warnings and alerts about data quality issues (e.g., high cardinality, constant columns, skewed distributions)

The generated HTML reports serve as a resource for data users and analysts to quickly assess the structure, integrity, and quality of the data before further processing or modeling. All reports are stored in the directory `html`.

## Backround

This repository is part of the [UNDERPIN Data Space for Manufacturing](https://underpinproject.eu/), a European initiative focused on enabling dynamic asset management and predictive/prescriptive maintenance in industrial environments. It contributes to the broader goal of establishing a secure and interoperable data space that facilitates cross-organizational and cross-use-case data sharing and collaboration across the manufacturing sector.

By supporting standardized approaches to data exchange, this work helps ensure that valuable insights derived from operational data can be seamlessly integrated and leveraged across different systems, organizations, and industrial applications. The repository provides tools, datasets, or components that are aligned with UNDERPIN’s mission to enable trustworthy and scalable data-driven maintenance strategies.

