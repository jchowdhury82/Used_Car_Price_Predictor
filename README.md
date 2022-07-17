# Used Car Price prediction 

### Author - Joyjit Chowdhury,  Student - Springboard MLE Course - Jan 2020 Cohort
 

## Project Overview   

**Name**  :  Used Car Price Prediction  
**Data Sources** :  Web Scraped car sales posting data from a used car seller website, additional car data sources from other websites  
**Prediction Algorithm Class**        :  Regression  
**Algorithms**        :   For this capstone, 3 different approaches are used for the regression problem
- Traditional scikitlearn approach - RandomForest and XGBoost 
- Deep Learning approach -  Neural Network with 3 layers (DL approach) and ReLu activations
- Spark ML apprach - GBT classifier from spak ml  

**Model Tuning**  : GridSearch with Stacking Regressor  
**Deployment Type** :  Flask Application on gunicorn WSGI server with 2 threads  

**Data Input Type**

| **Field** |	Description	| Data Type | 	Example |
| ----- |	-----------	| --------- | 	------- |
|year |	Year of manufacture |	Numeric |	2014 |
|make |	Make of car	|String	| "toyota" |
|model |	Model of car	|String	| "corolla" |
|trim |	Trim of car | String	| "le plus" |
|odometer |	Current odometer reading |	Numeric	|20700|
|state |	State where used car is on sale |	String	|  "AZ"|
|colorexterior |	Exterior color|	String	| "blue"|
|colorinterior |	Interior color|	String|	 "black"|
|accidenthist |	Any history of accidents	| Numeric	| "n" |
|owner | 	Number of owners |	Numeric |	5 |
|usage |	Purpose of use by previous owners |	String | "personal" |


**Data Output**

Predicted price of the used car


## Design Considerations

### Major Components :

- **Data Transformer classes** – module for the transformer classes on input data
-	**Flask Application Module** – main flask application module with functions serving endpoints
-	**Gunicorn Configuration File** – configuration  / property file for gunicorn WSGI app server
-	**Wrapper shell script for gunicorn** – wrapper script for invoking gunicorn app server with required configuration – entry point to the application
-	**Additional Data Files** – CSV files to be used to append additional features to raw inputs
  -	car_category.csv
  -	car_reliability_rankings.csv
  -	statewise_economic_indicators.csv
  -	car_sales.csv
  -	used_car_time_to_turn.csv
  -	car_ratings.csv
-	**Model file** – Pickle dump of the trained model
-	**Docker (configuration) files** – 
  - requirements.txt : text file with necessary package names and versions for building docker image 
  -	dockerfile : text file with docker image creation specifications

### Input data schema :
![Input Data Schema](https://github.com/jchowdhury82/Springboard_Capstone_UsedCar/blob/master/images/input_schema.PNG)

### Feature encoding :
![Data Transformation](https://github.com/jchowdhury82/Springboard_Capstone_UsedCar/blob/master/images/feature_encoding.PNG)

### Application access specifications :
![Application Access](https://github.com/jchowdhury82/Springboard_Capstone_UsedCar/blob/master/images/app_access.PNG)


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



## Major activities and implementation summary

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


![Deployment Architecture](https://github.com/jchowdhury82/Springboard_Capstone_UsedCar/blob/master/images/Deployment_Solution.PNG)



## Code Execution 

- **Pull Docker Image from Docker Repository**

`docker pull jchowdhury/carpricepredictor:latest`

- **Start Docker Container**

`docker run -d -p 5000:5000 --rm --name carpricepredictor jchowdhury/carpricepredictor`


![docker_pull](https://github.com/jchowdhury82/Springboard_Capstone_UsedCar/blob/master/images/docker_pull.png)

- **Health Check API Call**

`curl --request GET http://0.0.0.0:5000/healthcheck`

- **Sample Prediction API call with json**

`curl --header "Content-Type: application/json" \
--request POST \
--data '{"year" : 2014, "make" : "toyota", "model" : "corolla", "trim" : "le plus", "odometer" : 20700, "state" : "AZ",  "colorexterior" : "blue", "colorinterior" : "black", "accidenthist" : "n", "owner" : 5, "usage" : "personal"}' \
http://0.0.0.0:5000/getPrice`


![docker_curls](https://github.com/jchowdhury82/Springboard_Capstone_UsedCar/blob/master/images/sample_curls.png)


- **UI based checks**

  - Open http://0.0.0.0:5000/dataform to open the webform and enter the details of the car. Hit the "Get Predicted Price" button to see the predicted price
  ![prediction_form](https://github.com/jchowdhury82/Springboard_Capstone_UsedCar/blob/master/images/form_input.png)
  
  - Open http://0.0.0.0:5000/upload to open the webform and upload a csv file in the format as shown in the same file [datasample.csv](https://github.com/jchowdhury82/Springboard_Capstone_UsedCar/blob/master/datasample.csv).  The response will be a downloaded csv file with the predicted price appended to the columns of the original csv.
  
![prediction_upload](https://github.com/jchowdhury82/Springboard_Capstone_UsedCar/blob/master/images/file_input.png)

**Original file**\
![original_csv](https://github.com/jchowdhury82/Springboard_Capstone_UsedCar/blob/master/images/csv_input.png)

**Predicted data response file** \
![predicted_csv](https://github.com/jchowdhury82/Springboard_Capstone_UsedCar/blob/master/images/csv_predicted.png)


## Model Lifecycle and Housekeeping proposals

#### Model Changes

With time, the model will be prone to data changes or conceptual changes and would need retraining or maintenance. Along with these, regular maintenance may be required to ensure model performance is within allowed thresholds.
- **Data changes** – New data trends may show up which can significantly contribute to drop in model prediction performance. External data used for data enrichment / augmentation may become stale and need refresh. 
- **Conceptual changes** – Data semantics may change over time based on business requirements and enhancements may be  required with retraining. Data semantics may also change due to changes in demographic and economic indicators which are used for data preparation. 
 
Due to this, the model may become stale or out-of-date which may need retraining or recompiling with better dataset and features.

#### Model Monitoring

The following approach may be considered for model monitoring:
- Create specialized functions to cross validate model on bulk data with metrics like rmse, r2 and mae. 
- Generate random test dataset and run cross validations. Store the metrics in some database with time signature.
- Publish an API within the application to show a trend plot of model metrics with time. 
- Establish a consensus on a model metric threshold for retraining. Whenever the metrics drop below the threshold, send notification for manual retraining or execute retrain module as part of housekeeping. 
- For model tuning, we can use GridSearch or HyperOpt as tuning tools. Various other tools are also available

#### Model retraining and republish:

Model retraining may follow the following approach:
- Stop the application in production (take the API offline) 
- On notification of low threshold, generate train and test data 
- Train and test model with Cross Validation in the dev / test sandbox and record metrics. 
- Once required threshold is achieved with the metrics, pickle the new version of the model file with versioning tool. 
- Build new docker file with docker compose and ensure only the required components are updated.
- Start the application again. Ensure all memory and temporary files are cleared.


## Scope of Improvement

- Better data collection and augmentation - more research on accuracy of data sources to avoid missing data
- Training examples are time-sensitive data, car prices may fluctuate with time, so model may be retrained on fresh data to achieve greater accuracy
- Lack of comuting power does not allow execution of extensive grid search - use of GPU's can allow wider grid search space and better tuning
- Use of nginx webserver to make the application complete as a web application
- Better error handling to make the application robust to edge cases or invalid inputs
- Use of cloud container registry like AWS ECR to add the cloud flavor





<br/>



# A Deep Learning Approach to this problem

Below is a Deep Learning approach to this problem.


## High Level Design

- **Implementation**   :  _Sequential model with Keras (Tensorflow Backend)_

- **Model architecture**       :  _Artificial Neural Network with 3 layers_ 
  - 1 input layer   40 units  
  - 1 hidden layer  20 units    
  - 1 output layer   1 unit       
    
- **Activation functions** :  _ReLu_

- **Initializer** : _Xavier (glorot uniform)_

- **Cost Optmizer** : Adam 

- **Loss Function** : MSE (Mean Squared Error)
- **Epochs and Callback** : 1000 epochs with Early Stopping Callback for 5 iterations
- **Input Feature Augmentation**: 
  - Mandatory_input_features = year, make, model,trim, odometer,state,colorexterior,colorinterior
  - Features augmented - ReliabilityRank,CostOfLivingRank,PercentSales, AvgDaysToTurn,ReviewScore,AvgMPG, LuxurySportsOrHybrid, drivetrain,bodytype
- **Feature Encoding**: 
  - Numeric features - ReliabilityRank,CostOfLivingRank,PercentSales,AvgDaysToTurn,ReviewScore,AvgMPG,age,odo
  - Categorical features to be OneHot encoded - owner,usage,LuxurySportsOrHybrid,drivetrain,accidenthist,colorexterior, colorinterior, bodytype  
  
 
![Neural Network with Regression](https://github.com/jchowdhury82/Springboard_Capstone_UsedCar/blob/master/images/Used_Car_Price_NN.png)



Details of the model implementation is in the notebook :   

 [Deep_Learning_Regression_Used_Car_Pricing](https://github.com/jchowdhury82/Springboard_Capstone_UsedCar/blob/master/Deep_Learning_Approach/Used_Car_Price_Predictor_DL_Approach.ipynb)



<br/>


# Scaling up with Spark ML

Spark ML can be used to upscale the model's data handling capabilities. 
The following steps are executed with Spark ML libraries on databricks to create a scaled up model:
- Get required data files using spark dataframes
- Transform data with the dataframe API's
- Use VectorAssembler with string indexers to encode categorical data
- Use Regression Evaluator and Cross Validator to get best parameters. 

The Spark ML based approach is depicted in the notebook below:

[Spark ML based Regression approach](https://github.com/jchowdhury82/Springboard_Capstone_UsedCar/blob/master/Spark_ML_Approach/Capstone_Used_Car_Pricing_At_Scale_PySpark_ML.ipynb)   







# Thank You Note

### <span style=“color:green;”> Big thanks to mentor and guide **Mr. Jeremy Cunningham** for his continuous support and patience throughout my learning journey.</span>
