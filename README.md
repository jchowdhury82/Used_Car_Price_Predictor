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







HealthCheck URL:

curl --request GET http://127.0.0.1:5001/healthcheck


GetPrice URL:

curl -d @input.json -H "Content-Type: application/json" -X POST http://127.0.0.1:5001/getPrice
