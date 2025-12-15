Authors - Digby Pratt, Ella Cockman, Liam O'Brien, Mason Murray

Question: Do wheat yield trends in major producing countries (e.g China, India, Russia, USA, France) predict yields in net-importing countries (e.g Egypt, Algeria, Indonesia, Brazil, Japan)?

Subquestions

How have wheat yields changed across countries from 1961 to 2023?

Which countries have the highest yields and the fastest improvements? 

Can we group countries into clusters with similar yield dynamics?

Can we use information from “similar” countries to improve yield predictions?

Introduction and Literature Review

Global wheat yield data show both strong spatial and temporal patterns. Ray et al. (2012) analysed crop yields from 1961 to 2008 and found widespread stagnation despite overall growth. This revealed spatial heterogeneity that justifies cross-country correlation studies. Our group extended this to 2023 using the same FAOSTAT source, adding 15 years of data to our analysis. Baldos and Hertel (2014) showed that productivity growth in major producers shapes international trade and food security for net importers, directly motivating our question: do yields in top producers (China, India, Russia, USA, France) correlate with yields in major importers (Egypt, Algeria, Indonesia, Brazil, Japan)?  

Conforti (2004) demonstrated that international process changes can influence and be transmitted to domestic markets. Whilst Evenson and Gollin (2003) showed that agricultural technologies diffused globally through research networks. Moreover, these studies suggest that correlations, if present, could reflect either market price effects or patterns of technology transfer. 

Lobell and Burke (2010) endorse regression models for yield prediction but warn of omitted-variable bias and non-stationarity. Our data suggest that this may be influenced by geopolitics, changes in climate conditions, and international relations. We filtered the dataset to include only 164 countries with data completeness of 80% or higher to exclude outliers, as this was not the focus of the data. Ray et al. (2015) found that climate explains one-third of global yield variability. Since our dataset lacks climate controls, we acknowledge this as a key limitation when interpreting correlations.  

In our research, we apply correlation and regression analysis to 1961-1923 wheat yields to test producer-importer relationships, whilst also recognising that observed patterns may reflect global trends rather than direct influence.

Data Cleaning

We first filtered the dataset to remove any unnecessary data. This included any rows that contained crops that were not wheat, any rows that contained details that were not the yield, and columns that repeated information. We also filtered the dataset to exclude locations with less than 80% of the relevant wheat-yield data. We chose this figure because wheat yields are relatively smooth, which made estimating the remaining 20% feasible. If a country had less than 80% of data available, it was not viable to keep it in the study. Many countries had missing values, so it was not feasible to remove any that lacked complete data.

To do these estimations, we used 'linear interpolation' - a way to estimate a missing value that exists between two known values. This methodology is suitable here because we can reasonably assume that year-to-year changes in wheat yields are linear, particularly when we have at least 80% of the data for each country/region. Lobell & Burke (2010) acknowledge the viability and common use of methodologies such as this, but also note limitations, characterising statistical models as a 'useful imperfect tool'. A limitation is that the missing values may have been due to outlier events, such as sudden changes in climate, political, or economic conditions. This methodology is common practice in agricultural datasets (Rey et al, 2012).

However, we acknowledge that the dataset contains many outliers, and no statistical model can account for them. Therefore, we are confident that this methodology is appropriate for this context. Interestingly, the most affected countries here do not appear to be randomly distributed, with countries such as Botswana, Qatar, and Sudan being politically unstable and relatively small.

Statistical Analysis

How have wheat yields changed across countries from 1961 to 2023 and which countries have the highest yields and the fastest improvements? 

Initial statistical analysis found that global yields had increased year-on-year across all continents. Europe consistently had the highest yields by a significant margin, followed by Asia; the remaining continents fluctuated over the defined period but generally had similar yields. This was further demonstrated by calculating mean yields per country over the period, with the top 6 countries by yield per hectare from Europe and the bottom 10 from lower-income countries, primarily in Africa and South America.

When examining countries with the most significant percentage increases in wheat yield over this period, we found an association between economic development and per-hectare wheat-yield growth, with countries such as China and South Africa among the top performers. However, this was not strictly the case, as countries such as Mauritania and Zambia were also among the top 15.

We also looked at the distribution of wheat yields over the time period, finding that most yields globally were between 1000 and 3000 hg/ha, and used a heatmap to see how the yields had changed by country. This visualised which countries had similar or different yields and which had changed rapidly, and allowed us to identify any outliers. It became clear that, in many countries, yields had been relatively stable.

We then computed the volatility for each country by measuring the degree of variation over the time period as a proxy. 

Initially, those with high volatility were first-world, economically developed countries. Still, when proportionalising this to the countries' yields, those with the highest volatility were typically associated with political instability and/or rapid economic change, whilst those with the lowest volatility were countries with consistently low yields and/or that are politically stable.

Can we group countries into clusters with similar yield dynamics?

We then examined how the yields of different countries correlated. We found a high degree of correlation across the board, with some outliers exhibiting notably negative correlations relative to the rest of the dataset. To do this, we determined the average yield of each country across the whole time period, the trend of the country over time, and the volatility, as mentioned earlier. This was followed by standardising these features and using k-means clustering amongst different groups of countries.

This led to four different clusters forming. These are as follows-
Cluster 0:

Moderate wheat yields but experience noticeable year-to-year variability. Long-term improvement is positive but modest, suggesting slow technological adoption or inconsistent environmental conditions. May face climate instability, variable rainfall, or dependence on fluctuating input availability.

Cluster 1:
High but extremely volatile yields. Highest relative variability (CV > 0.5), meaning yields swing widely from year to year. Strongest long-term trend, indicating rapid improvements, but from a fluctuating base. Could reflect policy-driven yield boosts. Climate-sensitive regions that occasionally achieve high yields.

Cluster 2:
Consistently low yields but also relatively stable production. Long-term improvement is very slow, indicating limited technological progress or persistent structural constraints. Economies with limited agricultural investment. Countries rely on traditional farming systems. Regions with climatic or soil constraints

Cluster 3:
Very high yields, maintain stable performance relative to their mean (lowest CV), and show strong positive long-term trends.
Global agricultural leaders, likely including countries with: Advanced crop breeding, advanced farming technology, controlled irrigation and consistent and stable agricultural policy

Given a country’s past yields and the yields of “similar” countries, can we predict that country’s yields better than simple baselines?

To do this, we compared several models. The first of which was the 'naive baseline' in which we assumed the yield was the same as the year before, 'own history linear regression', in which we predicyed yields based upon the countries past yields, and 'cluster augmented regression' in which we predicted a yield using the history of both the country and the fformentioned cluster it is a part of.

We first visualised the trajectory of each cluster. Cluster 0 increased at a steady rate throughout the whole time period, cluster 1 increased more rapidly towards the latter half of the time period, cluster 2 was the most stagnant throughout the time period, whilst cluster 3 increased more quickly at the start of the time period, and in a more steady manner towards the end. 

When modelling the data, the data were reshaped, with columns detailing the 'Area' (country), 'Yield', 'Year', and 'Cluster'. We then tested this model on Mainland China, finding that the naive model tends to lag and fails to capture longer-term trends. The own-history regression improves performance by capturing a smooth temporal trend, and the cluster-augmented model further reduces prediction error, particularly in years when the country’s yields align with those of its cluster peers. This suggests that using information from similar countries can modestly improve yield forecasts relative to relying on a country’s own history alone. This aligns with the findings presented by Baldos and Hertel (2024).

Conclusion and Limitations

Global wheat yields have increased since 1961 (challenging the findings of Ret et al. (2012)), with the increase distributed between economically developed Western countries and rapidly developing Eastern ones. These are represented as Cluster 1 and Cluster 3, forming 4 clusters with distinct traits. When modelling yields, a simple model that incorporates historical data for both the country and the cluster can outperform a purely naive baseline.

Clusters of countries with similar yield dynamics do exist, and can be used to improve yield predictions. However, to do this more accurately, additional factors must be considered.

There are limitations to these findings. These include the use of a linear interpolation to fill in missing values. While a practical methodology, a more advanced method may have better captured nonlinear trends. The use of k-means clustering depends on the predetermined choice of the number of clusters and the traits used to define them. Usage of this may mean that key insights are not fully revealed. A further limitation is that other factors warrant greater consideration, including variations in weather, prices, and policy.

This does offer a basis for further research, incorporating data such as changing climate conditions, and import/export data into the picture. More sophisticated methodologies may also have been prudent, such as dynamic time warping to represent better trends across countries and hierarchical clustering to more accurately group data points.

Bibliography

Baldos, U. L. C., & Hertel, T. W. (2014). Global food security in 2050: The role of agricultural productivity and climate change. Australian Journal of Agricultural and Resource Economics, 58(4), 536–559. https://doi.org/10.1111/1467-8489.12048 

Conforti, P. (2004). Price transmission in selected agricultural markets (FAO Commodities and Trade Policy Research Working Paper No. 7). Food and Agriculture Organization of the United Nations. http://www.fao.org/3/y5117e/y5117e00.htm 

Evenson, R. E., & Gollin, D. (2003). Assessing the impact of the Green Revolution, 1960 to 2000. Science, 300(5620), 758–762. https://doi.org/10.1126/science.1078710 

Lobell, D. B., & Burke, M. B. (2010). On the use of statistical models to predict crop yield responses to climate change. Agricultural and Forest Meteorology, 150(3), 1443–1452. https://doi.org/10.1016/j.agrformet.2010.07.008 

Ray, D. K., Gerber, J. S., MacDonald, G. K., & West, P. C. (2015). Climate variation explains a third of global crop yield variability. Nature Communications, 6, Article 5989. https://doi.org/10.1038/ncomms6989 

Ray, D. K., Mueller, N. D., West, P. C., & Foley, J. A. (2012). Recent patterns of crop yield growth and stagnation. Nature Communications, 3, Article 1293. 





