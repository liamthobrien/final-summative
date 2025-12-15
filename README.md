Authors - Digby Pratt, Ella Cockman, Liam O'brien, Mason Murray

Question: Do wheat yield trends in major producing countries (China, India, Russia, USA, France) predict yields in net-importing countries (Egypt, Algeria, Indonesia, Brazil Japan) and do these correlations reflect actual trade networks? 

Subquestions

How have wheat yields changed across countries from 1961–2023?

Can we group countries into clusters with similar yield dynamics?

Can we use information from “similar” countries to improve yield predictions?

Introduction and Literature Review

Global wheat yield data show both strong spatial and temporal patterns. Ray et al. (2012) analysed crop yields from 1961 to 2008 and found widespread stagnation despite overall growth. This revealed spatial heterogeneity that justifies cross-country correlation studies. Our group extended this to 2023 using the same FAOSTAT source, adding 15 years of data to our analysis. Baldos and Hertel (2014) showed that productivity growth in major producers shapes international trade and food security for net importers, directly motivating our question: do yields in top producers (China, India, Russia, USA, France) correlate with yields in major importers (Egypt, Algeria, Indonesia, Brazil, Japan)?  
Conforti (2004) demonstrated that international process changes can influence and be transmitted to domestic markets. Whilst Evenson and Gollin (2003) showed that agricultural technologies diffused globally through research networks. Moreover, these studies suggest that correlations, if present, could reflect either market price effects or technology transfer patterns. 
Lobell and Burke (2010) endorse regression models for yield prediction but warn of omitted-variable bias and non-stationarity. From our data, this may be influenced by geopolitics, changes in climate conditions and international relations. We decided to filter from 164 to 123 countries with data completeness of 80% or higher to exclude these outliers, as this was not the focus of the data. Ray et al. (2015) found that climate explains one-third of global yield variability. Since our dataset lacks climate controls, we acknowledge this as a key limitation when interpreting correlations.  
In our research, we apply correlation and regression analysis to 1961-1923 wheat yields to test producer-importer relationships, whilst also recognising that observed patterns may reflect global trends rather than direct influence.

Methodology

Data Cleaning

We first filtered the dataset to remove any unnecessary data. This included any rows that contained crops that were not wheat, any rows that contained details that were not the yield, and columns that repeated information. We also chose to filter the dataset to remove any locations that did not contain 80% of the relevant data on wheat yields. We chose this figure as wheat yields are largely quite smooth, which meant that estimating the other 20% was viable. We felt that if a country had less than 80% of data available, it was not viable to keep it in the study. Many countries had some missing values, so it was not viable to remove any which did not have complete data.
To do these estimations we used 'linear interpolation' - a way to estimate a missing value, that exists between two known values. This methodology is suitable here as we can reasonably assume that the way in which wheat yields change year by year is linear, particularly when we have at least 80% of the data for each country/region. Lobell & Burke (2010) acknowledges the viability, and common usage of methodologies such as this, but does also present some limitations, describing statistical models as a 'uselful imperfect tool'. Limitations here are that the missing values may have occured during outlier events, such as sudden changes in climate, political or economic conditions.
However, we have acknowledged that the dataset does contain many outliers, and no statistical model can account for them Therefore, we are confident that this is an appropriatre methodology to apply here. Interestingly, the most affected countries here do not appear to be randomly distributed, with countries such as Botswana, Qatar and Sudan all being politically unstable, relatively small states.

Statistical Analysis

How have wheat yields changed across countries from 1961–2023?

Initial statistical analysis found that global yields had increased year on year, and in all individual continents. Europe always had the highest yields by a significant distance, followed by Asia, with the remaining continents intrchanging over the defined time period, but largely having similar yields. This was further represented through calculating the mean yields per country,across the time period, with the top 6 countries with the highest yield per hectare being from the continent of Europe, and the bottom 10 being lower income countires, largely from the continents of Africa and South America.
When looking at the countries with the largest percentage increase in wheat yield over this time period, we found that there is an alignment with the rate of economic development and the rate of wheat yield increase per hectare, with countries such as China and South Africa being on there. However this was not strictly the case, with countries such as Mauritania and Zambia also being on the top 15.
We also looked at the distribution of wheat yields over the time period, finding that most yields globally were between 1000 and 3000 hg/ha, and used a heatmap to see how the yields had changed by country. This visualised which countries had similar and different yields, and those that had changed rapidly, as well as allowing us to spot any outliers. It did become clear that in many countries, yields had been fairly stable.
We then computed the volatility of each country, through measuring the degree of variation over the time period as a proxy representation. Initially, those with a high degree of volatility were countries who were first-world and economically developed, but when proportionalising this to the yields of the countries, those with the highest volatility were ones that would usually be associated with political instability and/or rapid economic change, whilst those with the lowest volatility were the countries with consistently low yields and/or are politically stable.

Can we group countries into clusters with similar yield dynamics?

We then looked into how the yields of different countries correlated with one another. We found that there was a high degree of correlation across the board, with some outliers having notably negative correlations with the rest of the dataset. To do this, we determined the average yield of each country across the full time period, the trend of the country over-time, and the afformentioned volatility. This was followed by standardising these features, and using k-means clustering amongst different groups of countries.
This led to four different clusters forming. These are as follows-
Cluster 0:
Moderate wheat yields but experience noticeable year-to-year variability. Long-term improvement is positive but modest, suggesting slow technological adoption or inconsistent environmental conditions. May face climate instability, varying rainfall, or dependency on fluctuating input use.
Cluster 1:
High but extremely volatile yields. Highest relative variability (CV > 0.5), meaning yields swing widely from year to year. Strongest long-term trend, indicating rapid improvements but from a fluctuating base. Could reflect policy driven yield boosts. Climate sensitive regions that occaisionally achieve high yields.
Cluster 2:
Consistently low yields but also relatively stable production. Long-term improvement is very slow, indicating limited technological progress or persistent structural constraints. Economies with limited agricultural investment. Countries relying on traditional farming systems. Regions with climatic or soil constraints
Cluster 3:
Very high yields, maintain stable performance relative to their mean (lowest CV), and show strong positive long-term trends.
Global agricultural leaders, likely including countries with: Advanced crop breeding, advanced farming techonlogy, controlled irrigation and consistent and stable agricultural policy

Given a country’s past yields and the yields of “similar” countries, can we predict that country’s yields better than simple baselines?

To do this, we compared several models. The first of which was the 'naive baseline' in which we assumed the yield was the same as the year before, 'own history linear regression', in which we predicyed yields based upon the countries past yields, and 'cluster augmented regression' in which we predicted a yield using the history of both the country and the fformentioned cluster it is a part of.
We first visualised the trajectory of each cluster. Cluster 0 increased at a steady rate throughout the full time period, cluster 1 increased more rapidly towards the latter half of the time period, cluster 2 was the most stagnant throughout the time perriod, whist cluster 3 increased more rapidly at the start of the time period, and in a more steady manner towards the end. 
So, when modelling this data, the data was reshaped, with colums detailing the 'Area' (country), 'Yield', 'Year' and 'Cluster'. We then tested this model on Mainland China, finding that the naive model tends to lag and fails to capture longer-term trends. The own-history regression improves performance by capturing a smooth trend over time and the cluster-augmented model further reduces prediction error, especially in years where the country’s yields move in line with its cluster peers. This suggests that using information from similar countries can modestly improve yield forecasts over using a country’s own history alone. This aligns with the findings presented by Baldos and Hertel (2024).

Conclusion and Limitations

Global wheat yields have increased since 1961 ,(challenging the findings by Ret et al (2012)), with the distribution of this increase being spread between economically developed western countries and rapidly developing eastern ones. These are represented as Cluster 1 and Cluster 3, as part of the formation of 4 clusters with distinct traits. When modelling yields, a simple model involving the past data of both the country and the cluster can improve on purely using a naive baseline.
Clusters of countries with similar yield dynamics do exist, and can be used to improve yield predictions. However, it is clear that to do this more accurately, more factors must be considered.
There are limitations to these findings. These include the use of a linear interpolation to fill in missing values. Whlst an effective methodology, a more advanced methodology may have captured non-linear trends better. The use of k-means clustering is dependent on the pre-determined choices of the number of clusters and the traits they are defined by. Usage of this may mean that key insights are not fully revealed. A further limitation is that other factors require more consideration, including variation in weather, prices and policy.
This does offer a basis for further research, incorporating data such as changing climate conditions, and inport/export data into the picture. More sophisticated methodologies may have also been prudent, such as dynamic time warping to better represent different trends across countries, and hierarchical clustering, which could have been used to more accurately group different datapoints.

Bibliography

Baldos, U. L. C., & Hertel, T. W. (2014). Global food security in 2050: The role of agricultural productivity and climate change. Australian Journal of Agricultural and Resource Economics, 58(4), 536–559. https://doi.org/10.1111/1467-8489.12048 

Conforti, P. (2004). Price transmission in selected agricultural markets (FAO Commodities and Trade Policy Research Working Paper No. 7). Food and Agriculture Organization of the United Nations. http://www.fao.org/3/y5117e/y5117e00.htm 

Evenson, R. E., & Gollin, D. (2003). Assessing the impact of the Green Revolution, 1960 to 2000. Science, 300(5620), 758–762. https://doi.org/10.1126/science.1078710 

Lobell, D. B., & Burke, M. B. (2010). On the use of statistical models to predict crop yield responses to climate change. Agricultural and Forest Meteorology, 150(3), 1443–1452. https://doi.org/10.1016/j.agrformet.2010.07.008 

Ray, D. K., Gerber, J. S., MacDonald, G. K., & West, P. C. (2015). Climate variation explains a third of global crop yield variability. Nature Communications, 6, Article 5989. https://doi.org/10.1038/ncomms6989 

Ray, D. K., Mueller, N. D., West, P. C., & Foley, J. A. (2012). Recent patterns of crop yield growth and stagnation. Nature Communications, 3, Article 1293. 

