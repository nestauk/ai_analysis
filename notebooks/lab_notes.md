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

TODO Need to change this

## Things to do

TODO Improve the community detection analysis (perhaps using igraph?)

## Aggregating topics into communities

What is the right strategy here: to add the topic weights? It would help if I had a good interpretation for them! 

TODO Read Tiago Peixoto's papers on the subject

## Plotting networks

I struggled a bit with the network visualisations. The reason for this is that I wasn't considering the ax argument in the `nx.draw` functions so the graphs weren't being plotted where I wanted.

## Colorbars

It is always a struggle to work with colourbars in mpl, specially when you are combining multiple plots. Remember that adding axes arbitrarily and referring to them from the image object helps.

## Gender diversity analysis

There are very few papers missing female author data. What is the reason for this? Does our analysis here take into account the country thresholds for inclusion in the female data that we created previously?

The analysis of the link between interdisciplinarity and gender diversity is generally robust to changes in the discretisation intervals and the variables / years.

## Company analysis

One important observation here is that we are not considering the international angle because of limitations in our ability to geocode multinational activity

Some technology companies are not being classified as multinationals

## Regional analysis

What do we do in instances of intra-region collaboration? Do we count multiple organisations or authors from the same region participating in
a paper as one or many? We will focus on one and therefore drop duplicate article-region pairs. This also means that we will be underestimating the 
scale of the regional concentration of activity.

* The LADs exclude Belfast

* There is quite a lot of faffing with the multinational flags. It would be nice to find a way to deal with that information.







