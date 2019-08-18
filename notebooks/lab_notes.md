# Lab notes for AI analysis

## Merging arXiv and LAD data

-Went [here](https://geopandas.readthedocs.io/en/latest/gallery/create_geopandas_from_pandas.html) for a reminder on how to convert a df into a geo-dataframe before doing a spatial join

-Went [here](http://geopandas.org/projections.html) to remind myself about how to reproject shapefiles

## Analysis of paper diversity when it involves women

I compared the interdisciplinary diversity of papers with and without women and the results were not very conclusive. 

When I considered field weights for all AI papers, papers with female authors tended to be less slightly less diverse.

When I considered community classification and filtered topics for topic-modelled AI papers, papers with female authors tended to be somewhat more diverse. This report was supported by a regression analysis considering paper diversity as target and has_female w/ various controls as predictor.

Given the disagreement in results, I will park this stream of analysis for now.

## Bug in the institution labelling - UCL labelled as UCL Australia instead of UCL London

Need to change this

## Things to do

Improve the community detection analysis (perhaps using igraph?)

