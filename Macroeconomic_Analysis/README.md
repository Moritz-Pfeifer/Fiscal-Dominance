# Econometric Analysis 

Using the SBERT similarity scores from our data analysis, we now want to understand which economic variables may have an influence on the similarity and by extension on fiscal dominance.  

For this purpose we run two VAR(p) models for Germany and France. The script follows these steps for both datasets and scores (Germany and France):

1) Select best variables
2) Test data for stationarity
3) Detrending data
4) Test normal distribution
5) Test cointegration
6) Compute VARs
   - Test autocorrelation
   - Test normality
   - Test heteroskedasticity
7) Impulse Response Analysis  
8) Compute Granger Causality

