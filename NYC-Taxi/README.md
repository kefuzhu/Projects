# Analysis of New York City Taxi Data

## Objectives

The objectives of this project is to analyze data collected by the New York City Taxi and Limousine commission about Green Taxis by answering the following questions: 

1. Question 1
    - Programmatically download and load into your favorite analytical tool the trip data for September 2015.
    - Report how many rows and columns of data you have loaded.
2. Question 2
    - Plot a histogram of the number of the trip distance (“Trip Distance”).
    - Report any structure you find and any hypotheses you have about that structure.
3. Question 3
    - Report mean and median trip distance grouped by hour of day.
    - We’d like to get a rough sense of identifying trips that originate or terminate at one of the NYC area airports. Can you provide a count of how many transactions fit this criteria, the average fare, and any other interesting characteristics of these trips.
4. Question 4
    - Build a derived variable for tip as a percentage of the total fare.
    - Build a predictive model for tip as a percentage of the total fare. Use as much of the data as you like (or all of it). Provide an estimate of performance using an appropriate sample, and show your work.
5. Question 5 (Distribution)
    - Build a derived variable representing the average speed over the course of a trip.
    - Can you perform a test to determine if the average trip speeds are materially the same in all weeks of September? If you decide they are not the same, can you form a hypothesis regarding why they differ?
    - Can you build up a hypothesis of average trip speed as a function of time of day?


**Note**: Green Taxis (as opposed to yellow ones) are taxis that are not allowed to pick up passengers inside of the densely populated areas of Manhattan. The data used for analysis is from September 2015.

Most of the fields in the dataset are described by the *Data Dictionary of LPEP Trip Records*, which is linked in the reference below. Other needed information can also be founded in the references.

## References

1. [NYC Taxi & Limousine Commision (TLC) Record Data](http://www.nyc.gov/html/tlc/html/about/trip_record_data.shtml)
2. [Data Dictionary of Livery Passenger Enhancement Program (LPEP) Trip Records](http://www.nyc.gov/html/tlc/downloads/pdf/data_dictionary_trip_records_green.pdf)
3. [Definition of Rate Code](http://www.nyc.gov/html/tlc/html/industry/taxicab_rate_yellow.shtml)
4. [E-Hail](http://www.nyc.gov/html/tlc/html/news/initiative_e_hail.shtml)

---

This is a fun project that I had a lof of fun with 😆

**Check [NYC_Taxi.ipynb](NYC_Taxi.ipynb) for all the code and analysis**

---

**Programming Language**: 
	
 - Python

**Algorithms/Skills/Techniques**

 - Wep scraping
 - Data Visualization
 - Machine Learning
 	- One Hot Encoding
 	- XGBoost
 	- Elastic Net	
 - Hypothesis Testing
 	- One-way ANOVA
 	- Tukey's HSD test

**Packages/Libraries/Modules**

 - pandas
 - numpy
 - requests
 - matplotlib
 - seaborn
 - xgboost
 - sklearn
 - scipy
 - statsmodels
 - tqdm