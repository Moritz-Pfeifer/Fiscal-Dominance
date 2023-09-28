# A Deep Learning Approach to Text Similarity: Testing Fiscal Dominance in France and Germany

## Project Description:

Fiscal dominance occurs when central banks use their monetary authority to control the prices of government securities and to fix interest rates at low levels to lower the cost of servicing national debt. Although the ECB may not refer to its unorthodox monetary policies as “fiscal dominance,” there is no denying that since the 2007–2008 financial crisis and particularly during the pandemic, the gap between fiscal and monetary policy has shrunk.

We propose to test fiscal dominance in the Eurozone by measuring the similarity of speeches between the Finance Ministries and Central Banks of France and Germany using a new dataset of speeches (Q12007 - Q42022). Text similarity is useful to determine how close two texts are both in surface closeness (lexical similarity) and meaning (semantic similarity). In Natural Language Processing (NLP), text similarity has been estimated using statistical means such as a vector space model to correlate words and textual contexts from a suitable text corpus. More recently, advances in deep learning have proven to perform better in evaluating how similar two texts are in terms of meaning. These models are able to measure similar data by content and not just by arbitrary descriptors.

In the first step, we compare several machine learning and deep learning word-embedding algorithms to compute the features that capture the semantics of the speeches, such as TF-IDF, pre-trained word embeddings (Word2Vec and GloVe), and the transformer-based BERT embeddings. To measure the distance between the previously computed features, we test the most common similarity measures, such as Jaccard Similarity, Cosine Similarity, and Jensen-Shannon distance.

This github releases the data and codes for the analysis of fiscal dominance in the following folders:

- **[Data](https://github.com/DataScientest-Studio/jan23_cds_dominance_budgetaire/tree/main/Data)**
  - This folder contains the raw and preprocessed data. 
- **[Preprocessing](https://github.com/DataScientest-Studio/jan23_cds_dominance_budgetaire/tree/main/Preprocessing)**
  - This folder contains the scripts for preprocessing the data. 
- **[Descripive Analysis](https://github.com/DataScientest-Studio/jan23_cds_dominance_budgetaire/tree/main/Descriptive_analysis)**
  - This folder contains the scripts for the data overview and descriptives.  
- **[NLP and Deep Learning Analysis](https://github.com/DataScientest-Studio/jan23_cds_dominance_budgetaire/tree/main/NLP_and_Deep_Learning_Analysis)**
  - This folder tests and compares the performance of various similarity measures on our dataset
- **[Econometric Analysis](https://github.com/DataScientest-Studio/jan23_cds_dominance_budgetaire/tree/main/Macroeconomic_Analysis)**
  - This folder contains the script for macroeconomic analysis
- **[Web Scraping Tool](https://github.com/DataScientest-Studio/jan23_cds_dominance_budgetaire/tree/main/Web-Scraping-Tools)**
  - This folder contains the scripts for scraping the central bank and finance ministries as well as the newspapers
 
The result of our [similarity analysis](https://github.com/DataScientest-Studio/jan23_cds_dominance_budgetaire/tree/main/NLP_and_Deep_Learning_Analysis) shows that both the French and German central bank and finance ministry speeches become more similar over time. This development reaches a peak in 2015 and has since remained constant. On average, the similarity between the finance and monetary institutions in France tends to be more similar than in Germany. 

<div align="center">
  <img src="https://img.onl/k07tlm" alt="SBERT">
</div>


The result of our [econometric analysis](https://github.com/DataScientest-Studio/jan23_cds_dominance_budgetaire/tree/main/Macroeconomic_Analysis) shows that in France, fiscal dominance is driven by public debt. These results are robust and would provide empirical evidence for theory of fiscal dominance, i.e. that the central bank loses independence when the government is too indebted. In Germany, the results are less clear. 




