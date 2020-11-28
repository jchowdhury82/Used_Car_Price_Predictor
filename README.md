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



## Project overview and major activities

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
- Create configuration module for defining classes and global variables required for prediction.  
- Create **Flask application** to provide the following endpoints for prediction for serving multiple input types for predictions
  - **Endpoint** : healthcheck
    - **URL** : http://0.0.0.0:5000/healthcheck
    - **Description** : Healthcheck API to check if the app is up or down. Returns a 200-Success if the application is alive
  - **Endpoint** : getPrice
    - **URL** : http://0.0.0.0:5000/getPrice
    - **Description** : Prediction API to receive mandatory feature values for used car and respond with the predicted used car price using the model 
  - **Endpoint** : dataform
    - **URL** : http://0.0.0.0:5000/dataform
    - **Description** : Web form for users to enter input data for used car prediction for a single example. Output is shown as the predicted price.
  - **Endpoint** : upload
    - **URL** : http://0.0.0.0:5000/upload
    - **Description** : Web form for users to input data as CSV file with multiple input examples. Output is returned as a downloaded csv file with predicted values.

- Refer to file [app_cardata.py](https://github.com/jchowdhury82/Springboard_Capstone_UsedCar/blob/master/app_cardata.py) and [config_cardata.py](https://github.com/jchowdhury82/Springboard_Capstone_UsedCar/blob/master/config_cardata.py)
- Create HTML (Jinja2) templates with AJAX for request processing without page rendering.  Refer to folder [templates](https://github.com/jchowdhury82/Springboard_Capstone_UsedCar/tree/master/templates)
- Create CSS style configuration for the web pages.  Refer to folder [static](https://github.com/jchowdhury82/Springboard_Capstone_UsedCar/tree/master/static)


**Application deployment**
- Encapsulate the flask app to a gunicorn WSGI application server. Refer to [gunicorn_config.py](https://github.com/jchowdhury82/Springboard_Capstone_UsedCar/blob/master/gunicorn_config.py) for the gunicorn configuration and [wsgi.py](https://github.com/jchowdhury82/Springboard_Capstone_UsedCar/blob/master/wsgi.py) for the wsgi wrapper.
- Deploy the app into a Docker container and publish to Docker repository. Refer to Docker definition file [Dockerfile](https://github.com/jchowdhury82/Springboard_Capstone_UsedCar/blob/master/Dockerfile) and requirements file [requirements.txt](https://github.com/jchowdhury82/Springboard_Capstone_UsedCar/blob/master/requirements.txt)
- Docker image created with command: 
        `docker build -t jchowdhury/carpricepredictor` 
- Docker image pushed to docker repository with command: 
        `docker image push jchowdhury/carpricepredictor:latest` 


## Code Execution 

- **Pull Docker Image from Docker Repository**

`docker pull jchowdhury/carpricepredictor:latest`

- **Start Docker Container**

`docker run -d -p 5000:5000 --rm --name carpricepredictor jchowdhury/carpricepredictor`

- **Health Check API Call**

`curl --request GET http://0.0.0.0:5000/healthcheck`

- **Sample Prediction API call with json**

`curl --header "Content-Type: application/json" \

--request POST \

--data '{"year" : 2014, "make" : "toyota", "model" : "corolla", "trim" : "le plus", "odometer" : 20700, "state" : "AZ",  "colorexterior" : "blue", "colorinterior" : "black", "accidenthist" : "n", "owner" : 5, "usage" : "personal"}' \

http://0.0.0.0:5000/getPrice`

- **UI based checks**

  - Open http://0.0.0.0:5000/dataform to open the webform and enter the details of the car. Hit the "Get Predicted Price" button to see the predicted price
  - Open http://0.0.0.0:5000/upload to open the webform and upload a csv file in the format as shown in the same file [datasample.csv](https://github.com/jchowdhury82/Springboard_Capstone_UsedCar/blob/master/datasample.csv).  The response will be a downloaded csv file with the predicted price appended to the columns of the original csv.

