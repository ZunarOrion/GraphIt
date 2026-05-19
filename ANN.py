import pandas as pd
import numpy as np
import seaborn as sns
import pandas.api.types as is_numeric_dtype
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

class Ann:
    def __init__(self, 
                 data_set=None,
                 target = None,
                 test_size = 0.3,
                 hidden_layers_list = None,
                 classes = 0,
                 epochs = 100,
                 batch_size = 32,
                 ):
        # Data validation
        try:
            self.df = pd.read_csv(data_set)
            self.df.head()
        except FileNotFoundError as file_not_found:
            print(file_not_found)
        # Validating target column
        if target in self.df.columns:
            self.target = target
        else:
            raise ValueError(f'[{target}] is not found.')
        # Checking for missing data
        if self.df.isnull().values.any():
            raise ValueError(f'Missing data')
        # Checking if all data is numeric
        if not all(self.df.dtypes.apply(is_numeric_dtype)):
            raise ValueError(f'Data has non-numeric values')
        # Creating X feature(s) and y label(s) arrays
        self.X = self.df.drop(self.target,axis=1).values
        self.y = self.df[self.target].values
        # Validating test size
        if 1 > test_size > 0:
            self.test_size = test_size
        # Validting hidden_layer_list
        if hidden_layers_list is not None and isinstance(hidden_layers_list,list):
            self.hidden_layers_list = hidden_layers_list or []
        else:
            raise ValueError(f'No hidden layers found')
        # Validating classes
        if classes >= 0:
            self.classes = classes
        else:
            raise ValueError(f'Classes = 0 => regressor, 1 => binary_classifier, more => multi-class')
        # Validating batch size
        if batch_size > 0:
            self.batch_size = batch_size
        else:
            raise ValueError(f'Batch size should be an integer more than 0')
        # Validating epochs
        if epochs > 0:
            self.epochs = epochs
        else:
            raise ValueError(f'Epochs need to be more than 0')

    def data_preperation(self):
        """
        Prepare data for DL
        """
        self.X_train, self.X_test, self.y_train, self.y_test =\
        train_test_split(self.X, self.y, test_size=self.test_size, random_state=101)
        #scaling
        self.scaler = MinMaxScaler()
        self.scaled_X_train = self.scaler.fit_transform(self.X_train)
        self.scaled_X_test = self.scaler.transform(self.X_test)

    def build_ann_model(self):
        """
        Building DL model
        """

        # Run data preparation
        self.data_preperation()

        self.ann_model = Sequential()
        self.ann_model.add(Dense(units=self.X.shape[1], activation='relu'))
        for nodes in self.hidden_layers_list:
            self.ann_model.add(Dense(units=nodes, activation='relu'))
        if self.classes == 0:
            ## Regressor output node
            self.ann_model.add(Dense(units=1))
            self.ann_model.compile(loss='mse', optimizer='adam')
        elif self.classes == 1:
            ## Binary classifier output node
            tf.random.set_seed(101)
            self.ann_model.add(Dense(units=1, activation='sigmoid'))
            self.ann_model.compile(loss='binary_crossentropy', optimizer='adam')
        elif self.classes > 1:
            ## Multi-class classifier output node
            tf.random.set_seed(101)
            self.ann_model.add(Dense(units=self.classes, activation='softmax'))
            self.ann_model.compile(loss='categorical_crossentropy',
                                   optimizer='adam',
                                   metrics=['accuracy'])
        # Training model and collecting losses
        self.history = self.ann_model.fit(x=self.scaled_X_train,
                                          y=self.y_train,
                                          validation_data = (self.scaled_X_test,self.y_test),
                                          epochs = self.epochs,
                                          batch_size = self.batch_size)
        # Collecting losses into dataframe
        self.losses = pd.DataFrame(self.history.history)
        self.losses.plot()

    def get_root_mean_square_error(self):
        """
        Method that return RMSE for trained regression ANN
        """
        if self.losses is not None and self.classes == 0:
            return np.sqrt(mean_squared_error(y_true=self.y_test,
                                              y_pred=self.ann_model.predict(self.scaled_X_test)))

    def print_classification_report(self):
        """
        Method that prints classification report for trained classifier ANN model
        """
        if self.losses is not None and self.classes >= 1:
            if self.classes == 1:
                ## Binary classification
                pred = self.ann_model.predict(self.scaled_X_test)
                self.y_pred = pred > 0.5
                print(classification_report(y_true=self.y_test,
                                            y_pred=self.y_pred))
            else:
                ## Multi-class classifier
                pred = self.ann_model.predict(self.scaled_X_test)
                y_pred = pd.get_dummies(np.argmax(pred,axis=1))
                print(classification_report(y_true=self.y_test,
                                            y_pred=y_pred))
            
    def ann_predict(self,predict_input:list):
        """
        Method to return predict value based on predict_input
        """
        predict_input = np.array(predict_input)
        ## Scaling array
        scaled_predict_input = self.scaler.transform(predict_input)
        return self.ann_model.predict(scaled_predict_input)