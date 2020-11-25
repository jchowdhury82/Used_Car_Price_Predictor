## File: config_cardata.py
## Author : Joyjit Chowdhury - Springboard MLE Jan2020
## Purpose: Configuration elements required for prediction of car prices
##          Includes variables, classes required for data transformation and prediction

import pandas as pd
from fuzzywuzzy import fuzz
from datetime import datetime
import pickle
from pandas.api.types import is_numeric_dtype
from sklearn.pipeline import Pipeline

numeric_features = ['ReliabilityRank', 'CostOfLivingRank', 'PercentSales', 'AvgDaysToTurn',
                    'ReviewScore', 'AvgMPG', 'age', 'odo']

# restricted values of categorical features
cat_features = {
            'owner' : ['0', '1','2'],
            'usage' : ['FLEET','PERSONAL'],
            'LuxurySportsOrHybrid' : ['N','U','Y'],
            'drivetrain' : ['AWD', 'FWD'],
            'accidenthist' : ['N','Y'],
            'colorexterior' : ['BLACK', 'BLUE','GRAY','OTHER',  'RED',  'SILVER','WHITE'],
            'colorinterior' : ['BEIGE','BLACK', 'GRAY', 'OTHER'],
            'bodytype' :['CONVERTIBLE','COUPE', 'HATCHBACK', 'PICKUP','SEDAN', 'SUV', 'TRUCK','VAN/MINIVAN', 'WAGON']
            }

# determining one-hot feature names from the categorical features
onehot_features = []
for x in cat_features.keys():
    onehot_features.extend([(x + '_' + v) for v in cat_features[x]])


# the final feature set - required to ensure model inputs are consistent for predictions
final_column_set = numeric_features + onehot_features

# mandatory inputs
mandatory_input_features = ['year', 'make', 'model', 'trim', 'odometer', 'state', 'colorexterior', 'colorinterior']



## Class : CarDataStandardizer
## Purpose: Cleanup input data and change values to standard forms

class CarDataStandardizer():

    def __init__(self):
        print("Initialized standardizer")

    def fit(self):
        return self

    def transform(self, df):
        # merge the data
        df_input = df.copy()

        for col in ['make', 'model', 'trim', 'state', 'colorexterior', 'colorinterior', 'accidenthist', 'usage']:
            df_input[col] = df_input[col].astype(str).apply(lambda x: x.upper().strip())

        df_input['colorexterior'] = df_input['colorexterior'].apply(
            lambda x: x if x in ['WHITE', 'BLACK', 'SILVER', 'GRAY', 'BLUE', 'RED'] else 'OTHER')
        df_input['colorinterior'] = df_input['colorinterior'].apply(
            lambda x: x if x in ['BLACK', 'GRAY', 'BEIGE'] else 'OTHER')

        df_input['age'] = datetime.now().year - df_input['year'].astype('int')
        df_input['odo'] = df_input['odometer'].astype('int') / 1000
        df_input = df_input.drop(columns=['odometer'])

        df_input['owner'] = pd.cut(x=df_input['owner'], bins=[-1, 0, 1, 20], labels=[0, 1, 2])

        return df_input


## Classes for data transformation and validation
## Will be used in a pipeline
## Hence all classes implement a fit and transform method



## CLass: CarDataAugmentor
## Purpose : Append additional data elements to the user provided data
## Additional data elements are obtained by Web Scraping and stored in csv files.
# These include:
## car category, car reliability rankings,cost of living for state of sale,turnaround time in stock,car ratings


class CarDataAugmentor():

    def __init__(self):

        # prepare augment data from files
        print("Initialized CarDataAugmentor")

        self.df_category = pd.read_csv('Data/car_category.csv', index_col=False)

        self.df_reliability = pd.read_csv('Data/car_reliability_rankings.csv', index_col=False)
        self.df_reliability = self.df_reliability[['Make', 'ReliabilityRank']]

        self.df_cost = pd.read_csv('Data/statewise_economic_indicators.csv', index_col=False)
        self.df_cost = self.df_cost[['State', 'CostOfLivingRank']]

        self.df_sales = pd.read_csv('Data/car_sales.csv', index_col=False)
        self.df_sales = self.df_sales.drop(columns=['TotalSales'])

        self.df_turn = pd.read_csv("Data/used_car_time_to_turn.csv")
        self.df_turn['AvgDaysToTurn'] = self.df_turn.mean(axis=1)
        self.df_turn['Make'] = self.df_turn['Make'].str.upper()
        self.df_turn = self.df_turn[['Make', 'AvgDaysToTurn']]

        self.df_ratings = pd.read_csv('Data/car_ratings.csv', index_col=False)
        self.df_ratings.drop_duplicates(subset=['MakeModel'], inplace=True)
        self.df_ratings['AvgMPG'] = (self.df_ratings['MpgCity'] + self.df_ratings['MpgHwy']) / 2
        self.df_ratings.loc[
            self.df_ratings['CarClass'].str.contains(r'LUXURY|SPORTS|HYBRID'), 'LuxurySportsOrHybrid'] = 'Y'
        self.df_ratings['LuxurySportsOrHybrid'] = self.df_ratings['LuxurySportsOrHybrid'].fillna('N')
        self.df_ratings = self.df_ratings[['MakeModel', 'ReviewScore', 'AvgMPG', 'LuxurySportsOrHybrid']]

    def fit(self):
        return self

    def transform(self, df):
        # merge the data
        df_input = df.copy()

        df_input = df_input.merge(self.df_reliability, how='left', left_on='make', right_on='Make')
        df_input = df_input.drop(columns=['Make'])

        df_input = df_input.merge(self.df_cost, how='left', left_on=['state'], right_on=['State'])
        df_input = df_input.drop(columns=['State'])

        df_input = df_input.merge(self.df_sales, how='left', left_on=['make'], right_on=['Make'])
        df_input = df_input.drop(columns=['Make'])

        df_input = df_input.merge(self.df_turn, how='left', left_on=['make'], right_on=['Make'])
        df_input = df_input.drop(columns=['Make'])

        df_input = df_input.merge(self.df_category, how='left',
                                  left_on=['year', 'make', 'model'],
                                  right_on=['Year', 'Make', 'Model'])
        df_input = df_input.drop(columns=['Year', 'Make', 'Model']).rename({'Category': 'bodytype'}, axis=1)

        # Function to do fuzzy matching of make and model combination to get ratings
        def getclass(makemodel):

            try:
                matches = self.df_ratings['MakeModel'].apply(lambda x: fuzz.ratio(x, makemodel))
                if matches.max() > 80:
                    return matches.idxmax()
                else:
                    return -1
            except:
                return -1

        df_input['makemodel'] = df_input['make'] + ' ' + df_input['model']
        df_input['matchindex'] = df_input['makemodel'].apply(getclass)
        df_input = df_input.merge(self.df_ratings, how='left', left_on='matchindex', right_index=True)
        df_input = df_input.drop(columns=['makemodel', 'matchindex', 'MakeModel'])

        def getdrivetrain(trim):

            try:
                drivetrain = [d for d in ['AWD', 'RWD', 'FWD', '4WD', '2WD'] if d in trim]
                drivetrain = drivetrain[0] if len(drivetrain) > 0 else 'FWD'
                drivetrain = 'FWD' if drivetrain in ['FWD', '2WD'] else 'AWD'
                return drivetrain
            except:
                return 'FWD'

        df_input['drivetrain'] = df_input['trim'].apply(getdrivetrain)

        df_final = df_input.drop(columns=['year', 'make', 'model', 'trim', 'state'])

        return df_final



## CLass: OneHotTransformer
## Purpose : A customized one-hot transformer based on pandas get_dummies
## The onehot transformer will be used on categorical features to ensure the model does not infer ordinal values
## for the categorical features


class OneHotTransformer():

    def __init__(self):
        print("Initialized OneHotTransformer")
        self.attlist = list(cat_features.keys())
        self.att_columns = onehot_features

    def fit(self, df):
        return self

    def transform(self, df):
        df_input = df.copy()

        att_dummies = pd.get_dummies(df_input[self.attlist])
        att_dummies = att_dummies.reindex(columns=self.att_columns, fill_value=0)
        df_final = pd.concat([df_input, att_dummies], axis=1)
        df_final.drop(columns=self.attlist, axis=1, inplace=True)

        return df_final


## CLass: PreModel validator
## Purpose : Class to ensure all features are model-input ready.
## Features should be non-null, numeric and should be in same order as the inputs of the trained model

class PreModelValidator():

    def __init__(self):
        print("Initialized PreModelValidator")

    def fit(self, df):
        return self

    def transform(self, df):
        df_input = df.copy()

        assert set(df_input.columns) == set(final_column_set)

        # Ensure no nulls
        assert df_input.isnull().values.any() == False, "Null Values exist in features"

        # Ensure No Non-Numeric
        assert is_numeric_dtype(df_input.values) == True, "Non-numeric Values exist in features"

        df_final = df_input[final_column_set]

        return df_final


## Pipeline for data transformation and validation

cardata_transform_pipeline = Pipeline(steps=[('standardize', CarDataStandardizer()),
                                             ('augment',CarDataAugmentor()),
                                             ('onehot', OneHotTransformer()),
                                             ('validate',PreModelValidator())
                                             ])


## Unpickle the trained model and load it


model_pkl_file = "model/carprice_stack_model_v1.pkl"

with open(model_pkl_file, 'rb') as file:
    stack_model = pickle.load(file)
