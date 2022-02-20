import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import StandardScaler


def train_model():
    
    df = pd.read_csv('data.csv')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')] #removing the first (unnamed) column as it just corresponds to the index of each row
    cols = list(df.columns.values) #need to save column labels for later (after imputer applied)


    indexes = np.where(df['price']=="OA")[0] #price column has 5 instances of value "OA", these instances are removed
    df.drop(indexes, inplace=True)
    df['price'] = df['price'].astype(float) #set price column type to float


    imputer = KNNImputer(n_neighbors=2)
    address = df.pop("address") #remove address before fitting with imputer (add back to the dataframe later)
    df = pd.DataFrame(imputer.fit_transform(df))
    df = df.join(pd.DataFrame(address))
    df.columns = cols #reset column labels after applying imputer 




    def drop(data, column, value, regex=True): #regex flag is whether to match via first n characters or exact match to inputted string
        if regex == True:
            indexes = np.where(data[column].str[:len(value)] == value)[0]
        else:
            indexes = np.where(data[column] == value)[0]
            
        # print(df.loc[indexes])
        data.drop(indexes, inplace=True)
        
        return data.reset_index(drop=True) #resetting the row indexes for the dataframe after rows have been removed. 



    #dropping postcodes with few instances
    df = drop(df, "address", "Durham")
    df = drop(df, "address", "EH")
    df = drop(df, "address", "NE")
    df = drop(df, "address", "TS2", False) #we want an exact match to TS2 to be removed, hence regex=False
    df = drop(df, "address", "TS5", False)


    add_columns = pd.get_dummies(df['address']) #hot encoding the postcodes 


    encoded = df.drop('address', axis=1)
    encoded = encoded.join(add_columns)


    X = encoded.drop('price', axis=1)
    y = encoded.pop('price')


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10)


    rf = RandomForestRegressor(random_state=0)
    rf.fit(X_train, y_train)

    return rf

def return_encoded_postcode(postcode_str):
   encoded = np.zeros(36)
   postcodes = ['DH1', 'DH2', 'DH3', 'DH4', 'DH5', 'DH6', 'DH7', 'DH8', 'DH9', 'DL1', 'DL12', 'DL13', 'DL14', 'DL15', 'DL16', 'DL17', 'DL2', 'DL3', 'DL4', 'DL5', 'SR7', 'SR8', 'TS16', 'TS17', 'TS18', 'TS19', 'TS20', 'TS21', 'TS22', 'TS23', 'TS24', 'TS25', 'TS26', 'TS27', 'TS28', 'TS29']
   i = 0
   for i in range(36):
      if postcode_str == postcodes[i]:
         encoded[i] = 1
   return list(encoded)

model = train_model()

def predict(bedrooms, receptions, bathrooms, postcode):
   arguments = arguments = pd.Series([bedrooms, receptions, bathrooms] + return_encoded_postcode(postcode))
   arguments = pd.DataFrame(arguments.values.reshape((1,-1)))
   return model.predict(arguments)[0]

print(predict(4, 2, 4, "DH1"))