import pandas as pd
from fuzzywuzzy import fuzz
pd.set_option('display.max_colwidth',0)
pd.set_option('display.float_format',lambda x: '%.2f' %x)
pd.set_option('display.max_columns',0)
from sklearn.base import BaseEstimator
from sklearn.pipeline import Pipeline
from datetime import datetime
import pickle

class CarDataStandardizer(BaseEstimator):

    def __init__(self):
        print("Initialized standardizer")

    def fit(self):
        return self

    def transform(self, df):
        # merge the data
        df_input = df.copy()

        # impute columns which are optional
        df_input['owner'].fillna(1, inplace=True)
        df_input['accidenthist'].fillna('N', inplace=True)
        df_input['usage'].fillna('PERSONAL', inplace=True)

        df_input['age'] = datetime.now().year - df_input['year'].astype('int')
        df_input['odo'] = df_input['odometer'].astype('int') / 1000
        df_input = df_input.drop(columns=['odometer'])

        df_input['owner'] = pd.cut(x=df_input['owner'], bins=[-1, 0, 1, 20], labels=[0, 1, 2])

        for col in ['make', 'model', 'trim', 'state', 'colorexterior', 'colorinterior', 'accidenthist', 'usage']:
            df_input[col] = df_input[col].astype(str).apply(lambda x: x.upper().strip())

        return df_input


class CarDataAugmentor(BaseEstimator):

    def __init__(self):

        # prepare augment data from files
        print("Initialized CarDataAugmentor")

        self.df_category = pd.read_csv('car_category.csv', index_col=False)

        self.df_reliability = pd.read_csv('car_reliability_rankings.csv', index_col=False)
        self.df_reliability = self.df_reliability[['Make', 'ReliabilityRank']]

        self.df_cost = pd.read_csv('statewise_economic_indicators.csv', index_col=False)
        self.df_cost = self.df_cost[['State', 'CostOfLivingRank']]

        self.df_sales = pd.read_csv('car_sales.csv', index_col=False)
        self.df_sales = self.df_sales.drop(columns=['TotalSales'])

        self.df_turn = pd.read_csv("used_car_time_to_turn.csv")
        self.df_turn['AvgDaysToTurn'] = self.df_turn.mean(axis=1)
        self.df_turn['Make'] = self.df_turn['Make'].str.upper()
        self.df_turn = self.df_turn[['Make', 'AvgDaysToTurn']]

        self.df_ratings = pd.read_csv('car_ratings.csv', index_col=False)
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

        df_input = df_input.merge(self.df_category, how='left',
                                  left_on=['year', 'make', 'model'],
                                  right_on=['Year', 'Make', 'Model'])
        df_input = df_input.drop(columns=['Year', 'Make', 'Model']).rename({'Category': 'bodytype'}, axis=1)

        df_input = df_input.merge(self.df_reliability, how='left', left_on='make', right_on='Make')
        df_input = df_input.drop(columns=['Make'])

        df_input = df_input.merge(self.df_cost, how='left', left_on=['state'], right_on=['State'])
        df_input = df_input.drop(columns=['State'])

        df_input = df_input.merge(self.df_sales, how='left', left_on=['make'], right_on=['Make'])
        df_input = df_input.drop(columns=['Make'])

        df_input = df_input.merge(self.df_turn, how='left', left_on=['make'], right_on=['Make'])
        df_input = df_input.drop(columns=['Make'])

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

        df_input = df_input.drop(columns=['year', 'make', 'model', 'trim', 'state'])

        return df_input






class OneHotTransformer(BaseEstimator):

    def __init__(self):
        print("Initialized OneHotTransformer")
        self.attlist = ['colorexterior', 'colorinterior', 'bodytype', 'accidenthist',
                        'owner', 'usage', 'LuxurySportsOrHybrid', 'drivetrain']

        self.att_columns = ['colorexterior_BLACK', 'colorexterior_BLUE', 'colorexterior_GRAY',
                            'colorexterior_OTHER', 'colorexterior_RED', 'colorexterior_SILVER',
                            'colorexterior_WHITE', 'colorinterior_BEIGE', 'colorinterior_BLACK',
                            'colorinterior_GRAY', 'colorinterior_OTHER', 'bodytype_CONVERTIBLE',
                            'bodytype_COUPE', 'bodytype_HATCHBACK', 'bodytype_PICKUP',
                            'bodytype_SEDAN', 'bodytype_SUV', 'bodytype_TRUCK',
                            'bodytype_VAN/MINIVAN', 'bodytype_WAGON', 'accidenthist_N',
                            'accidenthist_Y', 'owner_0', 'owner_1', 'owner_2', 'usage_FLEET',
                            'usage_PERSONAL', 'LuxurySportsOrHybrid_N', 'LuxurySportsOrHybrid_U',
                            'LuxurySportsOrHybrid_Y', 'drivetrain_AWD', 'drivetrain_FWD']

    def fit(self, df):
        return self

    def transform(self, df):

        df['colorexterior'] = df['colorexterior'].apply(
            lambda x: x if x in ['WHITE', 'BLACK', 'SILVER', 'GRAY', 'BLUE', 'RED'] else 'OTHER')
        df['colorinterior'] = df['colorinterior'].apply(lambda x: x if x in ['BLACK', 'GRAY', 'BEIGE'] else 'OTHER')

        att_dummies = pd.get_dummies(df[self.attlist])
        att_dummies = att_dummies.reindex(columns=self.att_columns, fill_value=0)

        df2 = pd.concat([df, att_dummies], axis=1)

        df2.drop(columns=self.attlist, axis=1, inplace=True)

        df_final = df2[['ReliabilityRank', 'CostOfLivingRank', 'PercentSales', 'AvgDaysToTurn',
                        'ReviewScore', 'AvgMPG', 'age', 'odo', 'owner_0', 'owner_1', 'owner_2',
                        'usage_FLEET', 'usage_PERSONAL', 'LuxurySportsOrHybrid_N',
                        'LuxurySportsOrHybrid_U', 'LuxurySportsOrHybrid_Y', 'drivetrain_AWD',
                        'drivetrain_FWD', 'accidenthist_N', 'accidenthist_Y',
                        'colorexterior_BLACK', 'colorexterior_BLUE', 'colorexterior_GRAY',
                        'colorexterior_OTHER', 'colorexterior_RED', 'colorexterior_SILVER',
                        'colorexterior_WHITE', 'colorinterior_BEIGE', 'colorinterior_BLACK',
                        'colorinterior_GRAY', 'colorinterior_OTHER', 'bodytype_CONVERTIBLE',
                        'bodytype_COUPE', 'bodytype_HATCHBACK', 'bodytype_PICKUP',
                        'bodytype_SEDAN', 'bodytype_SUV', 'bodytype_TRUCK',
                        'bodytype_VAN/MINIVAN', 'bodytype_WAGON']]

        return df_final



model_pipeline = Pipeline(steps=[('standardize', CarDataStandardizer()),
                                 ('augment',CarDataAugmentor()),
                                 ('onehot', OneHotTransformer())
                                 ])

model_pkl_file = "carprice_stack_model_v1.pkl"

with open(model_pkl_file, 'rb') as file:
    stack_model = pickle.load(file)
