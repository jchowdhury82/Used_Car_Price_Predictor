# Capstone Project - Used Car Price prediction

### Author - Joyjit Chowdhury,  Student - Springboard MLE Course - Jan 2020 Cohort
### Mentor - Jeremy Cunningham

### Project Details - 
**Name**                              :  Used Car Price Prediction  
**Data Source**                       :  Web Scraped car sales posting data from a used car seller website  
**Prediction Algorithm Class**        :  Regression  
**Data Sources** :  Web Scraped car sales posting data from a used car seller website, additional car data sources from other websites  
**Deployment Type** :  Flask Application on gunicorn WSGI server with 2 threads  


## Project Structure

.
├── **Data**\
│   ├── Used_Car_HoldOut_Set_final.csv\
│   ├── Used_Car_TrainTest_Set_final.csv\
│   ├── car_category.csv\
│   ├── car_ratings.csv\
│   ├── car_reliability_rankings.csv\
│   ├── car_sales.csv\
│   ├── cardata.csv\
│   ├── cardata_final.csv\
│   ├── cost_of_living.csv\
│   ├── statewise_economic_indicators.csv\
│   └── used_car_time_to_turn.csv\
├── **EDA**\
│   ├── UsedCarDataPreparation.ipynb\
│   ├── UsedCarEDA-v1-IndividualModels.ipynb\
│   ├── UsedCarEDA-v1.ipynb\
│   └── UsedCar_DataTransformation.ipynb\
├── **WebScraper**\
│   ├── ScrapeCarReviews.ipynb\
│   └── WebScrapeCarData.py\
├── **model**\
│   └── carprice_stack_model_v1.pkl\
├── **static**\
│   └── style.css\
├── **templates**\
│   ├── dataform.html\
│   └── upload.html\
├── Dockerfile\
├── README.md\
├── app_cardata.py\
├── config_cardata.py\
├── datasample.csv\
├── entry.sh\
├── gunicorn_config.py\
├── requirements.txt\
├── sample_calls_API.txt\
└── wsgi.py



## Project Overview and major activities

**Web Scrape used car listings**
- Use selenium webdriver plugin on chrome with requests / BeautifulSoup library to scrape used car listings
- Scrape additional demographic/sales data related to cars
- Refer to files in folder [WebScraper](https://github.com/jchowdhury82/Springboard_Capstone_UsedCar/tree/master/WebScraper)

**Prepare dataset with consolidated features**
- Append additional demographic/sales data for cars to the web scraped raw used car listings
- Generate new features, impute with appropriate values as needed.
- Refer to file [UsedCarDataPreparation.ipynb](https://github.com/jchowdhury82/Springboard_Capstone_UsedCar/blob/master/EDA/UsedCarDataPreparation.ipynb) in folder **EDA**

**Exploratory Data Analysis(EDA)**
- Perform exploratory data analysis on the data 
  -frequency
  -missing data
  -correlations
  -outliers
- Impute data as applicable
- Clip outliers as applicable
- Ensure all data can be converted to non-null and numeric
- Refer to file [UsedCarEDA-v1.ipynb](https://github.com/jchowdhury82/Springboard_Capstone_UsedCar/blob/master/EDA/UsedCarEDA-v1.ipynb) in folder **EDA**

**Modelling with ensemble (tree based) algorithms - Stacking, Hyperparameter Tuning and Feature Importances**
- Encode cleaned data into model ready features - prepare transformation encoders for data preparation, cleanup and onehot encoding as applicable
- Prepare train/test data ready to be fed to model
- Do initial modeling with RandomForest and XGBoost to determine initial feature importance
- Select appropriate features
- Do a **GridSearch** with **StackingRegressor** to determine the optimal model with hyperparameters.
- Save the most optimal model into a picke file for further use
- Refer to file [UsedCarEDA-v1.ipynb](https://github.com/jchowdhury82/Springboard_Capstone_UsedCar/blob/master/EDA/UsedCarEDA-v1.ipynb) in folder **EDA**


**Application development**
- Create Flask application to provide endpoints for prediction for the following input types from user
  - Endpoint for user 
- Do initial modeling with RandomForest and XGBoost to determine initial feature importance
- Select appropriate features
- Do a **GridSearch** with **StackingRegressor** to determine the optimal model with hyperparameters.
- Save the most optimal model into a picke file for further use
- Refer to file [UsedCarEDA-v1.ipynb](https://github.com/jchowdhury82/Springboard_Capstone_UsedCar/blob/master/EDA/UsedCarEDA-v1.ipynb) in folder **EDA**




HealthCheck URL:

curl --request GET http://127.0.0.1:5001/healthcheck


GetPrice URL:

curl -d @input.json -H "Content-Type: application/json" -X POST http://127.0.0.1:5001/getPrice
