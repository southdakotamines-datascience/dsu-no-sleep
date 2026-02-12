# Sanford Health/DSU Data Competition - Team No Sleep
This is Team No Sleep's submission for the Sanford Health/DSU Data Competition 2026. There are three components to the code: a Streamlit web app that allows the user to predict any given date or date range, a Jupyter notebook that contains our EDA, and finally a Jupyter notebook that has the many models we tried.

## Approach
### Correlation
The given dataset represents the ED volumes from four large Sanford Health emergency departments. This includes the total encounters and the number of encounters admitted to a floor. It's important to note that the number of encounters contains the number of admitted, so they are correlated.  

![Hourly ED Enc and ED Admitted by Site (Sept. 2024)](./pics/hourly-sept-2024.png)
*Thus the number of admitted is stricly less than the number of encounters*  

If we take a look at the correlation matrix of the dataset, we get the following:  
![Heatmap](./pics/heatmap.png)  
And if we generate one for a daily aggregated dataset, we get a more interesting correlation matrix.  
![Heatmap](./pics/heatmap-day-agg.png)  
We can see that the site is very correlated with the volume of encounters/admitted, and we can confirm that the volume of encounters and volume of admitted are in fact correlated.  

### Impact of COVID-19 Pandemic on Emergency Department Visits
Exploring the data, we can see there is a significant dip in 2020.
![Daily ED Enc and ED Admitted by Site (2018-2025)](./pics/daily.png)
![](./pics/boxplot-enc.png) ![](./pics/boxplot-admit.png)
Not only is there a huge dip, but daily ED encounters increase after COVID, compared to pre-COVID
## Methodology
