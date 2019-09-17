# Eatlab-Manifold
These are the Jupyter Notebook files I have used during my internship at EATLAB over the summer of 2019,  where I devised machine learning algorithms to describe and distinguish manifolds in consumer behavioral datasets.

Unfortunately, the raw data I worked with throughout the internship is the property of EATLAB; I therefore have no 
right to share it in this repository. The files have been removed, which will result in the notebooks raising errors. However,
the code I have written can still be seen to obtain an idea of algorithms I have devised and the statistical procedures I have 
conducted on the data.

In the "manifold identification" notebook, I used dimensionality reduction and clustering algorithms to represent the consumer
behavioral dataset (which spans over 10 dimensions) as manifolds in 3-dimensional space. I then implemented two algorithms, [ellipsoid] and [plane] to describe the position, orientation, and shape of the manifolds (see notebook file for details). 

In the "grouping analysis" notebook, I categorized the menu items into various groupings which I hypothesized will have significantly different consumer behavior. I then carried out various statistical tests to prove and disprove my hypotheses. 

The raw data used does have a number of outliers that may affect the performance of the machine learning models used. I therefore 'cleaned' the data by carrying out a series of procedures, which were mainly based on Grubb's test for outliers, in the "data cleaning" notebook.
