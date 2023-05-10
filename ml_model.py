import sklearn
import joblib
import pandas as pd
import numpy as np

def predict_cost(input_data):
    abc = joblib.load('AdaBoostRegressor.joblib')
    dict_classes = joblib.load('label_encoders.joblib')
    input_data = pd.Series(input_data, index=['author', 'city', 'floor', 'floors_count', 'rooms_count',
                                                'total_meters', 'year_of_construction', 'living_meters',
                                                'kitchen_meters', 'district', 'street', 'underground'])
    for key in dict_classes.keys():
        input_data[key] = dict_classes[key].transform(np.array([input_data[key]])).item()
    input_data = input_data.values.reshape(1, -1)
    return int(np.round(abc.predict(input_data).item()))
print(predict_cost(np.array(['GloraX','Sankt-Peterburg',6,19,2,60.1,2025,27.1,14.4,'Vasileostrovskij','Morskoj','Zenit'])))

