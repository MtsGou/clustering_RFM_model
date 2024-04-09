# RFM Hierarchical Agglomerative and KMeans Clustering

*Data science repository with files and codes used to build a cluster model to categorize customers in a company based on RFM (recency, frequency, monetary).*

----

## Description

This project used a KMeans model and a hierarchical model to categorize customers in a company based in RFM (recency, frequency, monetary). This was made using data that specifies variables "InvoiceNo","Quantity","InvoiceDate","UnitPrice" and "CustomerID".

RFM stands for Recency, Frequency and Monetary. For each customer, each of these three values ​​are obtained.Recency stands for the number of days since the customer's last purchase. Frequency tells how many purchases the customer has made since registering. And finally, Monetary represents how much the customer spends on purchases, for example, the average value of transactions.

![Data points](/plots/points.png)

This technique is widely used by companies to help develop business strategies, as it allows them to better understand customers, using an approach known as Targeting Marketing, 
which consists of mapping and classifying customers, with the aim of retaining and rewarding the most regular customers and also attracting those who may not become customers.
In this project, the RFM clusters allow us to classify each client's profile into four groups, and it is up to the company to analyze each cluster and understand what each one represents. 
To achieve this, this application also shows the average RFM value for each of the clusters, for a given data sample.


## Methods

Data was collected from Kaggle's [**dataset**](https://www.kaggle.com/datasets/carrie1/ecommerce-data) "E-Commerce Data".

Packages and APIs used: 
- [**Pandas**](https://pandas.pydata.org/) for data wrangling;
- [**Matplotlib**](https://matplotlib.org/) for visualization;
- [**Seaborn**](https://seaborn.pydata.org/index.html) for visualization;
- [**Yellowbrick**](https://www.scikit-yb.org/en/latest/) for ML visualization;
- [**Flask**](https://flask.palletsprojects.com/en/3.0.x/) for model API deploy;
- [**Fast API**](https://fastapi.tiangolo.com/) for model API deploy;
- [**Streamlit**](https://streamlit.io/) for embedded deploy;
- [**Numpy**](https://numpy.org/) for data wrangling and mathematical manipulation; 
- [**Scikit-Learn**](https://scikit-learn.org/stable/) for modeling; 
- [**SciPy**](https://scipy.org/) for modeling.

**Models used:**

- **KMeans model**: [sklearn.cluster.KMeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html);
- **Hierarchical Agglomerative model**: [sklearn.cluster.AgglomerativeClustering](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html)

**PCA, analysis and metrics:**

 - **PCA decomposition**: [sklearn.decomposition.PCA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html);
 - **Dendrogram hierarchy model**: [scipy.cluster.hierarchy](https://docs.scipy.org/doc/scipy/reference/cluster.hierarchy.html).
 - **Silhouette score for defining number of clusters k**: [sklearn.metrics.silhouette_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_score.html)
 - **Elbow Method**: [yellowbrick.cluster.KElbowVisualizer](https://www.scikit-yb.org/en/latest/api/cluster/elbow.html);

-----

## Conclusions for the dataset

The higher silhouetter score (closest to 1) was 0.403, for k = 4. The Elbow method showed that the optimal value for Elbow Distortion score was k = 4 clusters. The average values for the RFM dataset, for each cluster according to the KMeans model was:

|cluster_number |R (days) | F |M (R$)|
| -------- | -------- | -------- | -------- |
|        0|  252.56|1.49|227.52|
|        1|  44.29|2.97|228.77|
|        2|  66.42|3.15|570.92|
|        3|  16.68|13.22|340.30|

![Clustering](/plots/agglomerative3d.png)

## Business analysis

According to the KMeans model, the **cluster 0** has the HIGHEST recency (a much higher average value of 250 days) and the LOWEST frequency, which means customers belonging to this cluster are much less frequent. Also, they are the ones that pay the least, with the lowest average ticket value. In other words, **these customers are potentially churning, they are more likely to quit and no longer be a customer.**

Customers in **cluster 1** also pay little, but with a slightly higher frequency and the second lowest recency, that is, **they are purchasing customers, but infrequent and that pay little.**

Customers in **cluster 2** keep longer time without purchasing, however, during some seasons, they buy more frequently than customers in cluster 1. Furthermore, they have the HIGHEST average ticker value. In other words, **they are more seasonal customers, who make large purchases with high prices at certain times of the year.**

Finally, customers in **cluster 3** have the HIGHEST frequency (much higher average value than the other clusters), the lowest recency of all, just 16 days, and an reasonably good monetary value, not so high and not so low. In other words, these customers **are regular customers, more frequent and loyal.**

### Potential strategies:

For customers in cluster 0, a more effective strategy is recommended to attract them to the company, since they have a high risk of evasion. For cluster 2, a good path would be to prioritize marketing offers and investments for each time of the year and invest in customer relationship excellence. As for customers in cluster 3, it would be important to maintain constant contact with them, and seek to transform them into brand promoters, using social media, etc. For cluster 1, one way to try to build customer loyalty would be to show them more options by presenting a broader, customer-specific list (through personalized recommendation) of products in the catalog.

## Data Analysis

### PCA decomposition visualization

#### Hierarchical Agglomerative model
![PCA Hierarchical](/plots/PCA_agglomerative.png)

#### KMeans model
![PCA KMeans](/plots/PCA_kmeans.png)

### Elbow Method
![Kelbow](/plots/kelbow.png)

### Silhouette Score
![Silhouette score](/plots/silhouette.png)

### Dendrogram - Hierarchical
![Dendrogram](/plots/dendrogram.png)

### 2D Plot per column
![Clustering each](/plots/analysis_each.png)


**[`🔼         back to top        `](#rfm-hierarchical-agglomerative-and-kmeans-clustering)**




