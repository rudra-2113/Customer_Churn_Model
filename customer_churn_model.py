# -*- coding: utf-8 -*-
"""Customer_Churn_Model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eY8OAKVtCQIa5uFY85sq5PIvvqHYisso

# CUSTOMER CHURN MODEL

The Dataset Is Of A Bank Which Had Kept Record Of Its Customers Over Past 1 Year & Within That Phase Who Have Exited(1) Or Non-Exited(0) The Organisation.

The Model Aims At Informing The Bank Beforehand Regarding A Customer Who May Be At The Verge Of Exiting The Bank Based On The Earlier Data of Exiting/Non-Exiting Customers Fed To The Model.

The Main Goal Of This Model Is To Successfuly Make Better Predictions In Classfying A New Customer As On Verge Of Exiting/Non-Exiting customer.

The Beforehand Information Will Be Quite Helpful For Bank In Retaining Its Customers And Avoiding Any Losses.

# Regular Imports
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

"""# Basic Data Analysis Of The Dataset"""

data= pd.read_csv('Bank_dataset.csv')

data.head()

"""Description Of Columns Of Dataset

RowNumber - row index

CustomerID- Unique identification id for customer

Surname- lastname of customer

Geography-country the customer lives in

Gender/Age- self explanatory

Tenure- no. of years the customer has been in bank

Balance- Amount of money present in account

NumOfProducts- different products in quantity used by customer

HasCrCard- whether has a credit card

IsActiveMember- current status of customer,whether using service or not

EstimatedSlary- self explanatory

Exited- whether the customer stayed or left the bank
"""

#Adding New Column To Dataset For Credit Card Availability Of Customer

data['cred_card_availability']=data['HasCrCard'].map({0:'NO',1:'YES'})
data.head()

"""Examining The Geography diversity among customers"""

country_data=data.Geography.value_counts()
print(country_data)

#Visualization
sns.catplot(x='Geography',data=data,kind='count',palette='mako')
plt.title('Geographic Diversity')
plt.show()

"""Examining The Gender Diversity among the Customers"""

gender_data= data.Gender.value_counts()
print(gender_data)

#Visualization
plt.pie(gender_data,labels=['Male(M)','Female(F)'],colors=['red','pink'],shadow=True)
plt.title('Gender Diversity Among Customers')
plt.legend('MF')
plt.show()

"""Examining The Gender Diversity among the Customers wrt Geography"""

sns.catplot(x='Gender',data=data,hue='Geography',kind='count',palette='plasma')
plt.title('Gender Diversity VS Geography')
plt.show()

"""Examining The No. Of Products used by Customers wrt the Gender Diversity"""

n_of_products=data.NumOfProducts.value_counts()
print(n_of_products)

#Visualization of no of products wrt Gender Diversity using each of them
sns.catplot(x='NumOfProducts',data=data,hue='Gender',kind='count',palette='plasma')
plt.title('No. Of Products VS Gender')
plt.show()

"""Examining The Gender Diversity wrt Credit Card availability status among customers"""

sns.catplot(x='cred_card_availability',data=data,kind='count',hue='Gender',palette='rocket')
plt.title('Gender Diversity VS Credit Card Avilability')
plt.show()

"""Examining The Age Diversity Of Customers"""

plt.hist(x=data.Age.dropna(),color='lightgreen')
plt.xlabel('Age')
plt.ylabel('Count')
plt.title('Age Diversity')
plt.show()

"""INFERENCE DRAWN -

1-Population of French customers are the most being served by bank.

2-Majority of the bank customers are Male. 

3-Majority of Male and Female customers belong to France. 

4-With respect to no. of products availed by cutomer for category 1 & 2, Male   customers are the major occupant where as for the rest the female customers are dominant. 

5-With respect to credit card holder status male customers outweighs the female cusromers both in terms of availing as well as non availing the service.

6-The major Age group of customer lie around 30-40.

# Building A Model To Classify Whether Customer Will Exit Or Continue With The Bank Based On Their Past Record

Importing The Regular Libraries
"""

import pandas as pd
import numpy as np
import tensorflow as tf

tf.__version__

"""# Data Preprocessing"""

data= pd.read_csv('Bank_dataset.csv')

#Creating the matrix of features X [columns from CreditScore till EstimatedSalary considered]
X=data.iloc[:, 3:-1].values

#Creating the matrix of dependant variable
y=data.iloc[:,-1].values

"""Encoding The Categorical Data [Geography & Gender]"""

#Label Encoding The 'Gender' i.e X[:,2] Column

from sklearn.preprocessing import LabelEncoder
label_enc=LabelEncoder()
X[:,2]=label_enc.fit_transform(X[:,2])

#One Hot Encoding The 'Geography' Column With Column idx=1 

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
col_t=ColumnTransformer(transformers=[('encoder',OneHotEncoder(),[1])],remainder='passthrough')
X=np.array(col_t.fit_transform(X))

#Splitting The Dataset Into Train Set And Test Set

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=0)

#Feature Scaling Applied To Entire Dataset

from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
X_train=sc.fit_transform(X_train)
X_test=sc.transform(X_test)

"""# Making The ANN model

Initializing The ANN
"""

ann=tf.keras.models.Sequential()

"""Adding The Input Layer And The First Hidden Layer"""

ann.add(tf.keras.layers.Dense(units=6 ,activation='relu'))

"""Adding The Second Hidden Layer"""

ann.add(tf.keras.layers.Dense(units=6 ,activation='relu'))

"""Adding The Output Layer"""

ann.add(tf.keras.layers.Dense(units=1,activation='sigmoid'))

"""# Training The ANN model

Compiling The ANN
"""

ann.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])

"""Training The ANN On Train Set"""

ann.fit(X_train,y_train,batch_size=32,epochs=100)

"""# Using Trained Model To Make Predictions

Predicting The Test Set Results
"""

y_pred=ann.predict(X_test)

for i in range (0,y_pred.shape[0]):
    if y_pred[i]>0.5:
        y_pred[i]=1
    else:
        y_pred[i]=0

"""Concatenating Prediction With Original Test Set Data"""

concat_result=np.concatenate((y_pred.reshape(len(y_pred),1),y_test.reshape(len(y_test),1)),axis=1)
print(concat_result)

"""Making The Confusion Matrix"""

from sklearn.metrics import confusion_matrix,accuracy_score
print(confusion_matrix(y_test,y_pred))
acc_score = accuracy_score(y_test,y_pred)
print('The Accuracy Score is ' + str(acc_score))

"""# CONCLUSION

The Overal Accuracy Came Out To Be ~ 85%-86%
"""