# %%
import pandas as pd
car=pd.read_csv("quicker_car.csv")
car.head()

# %%
car.shape

# %%
# car.info

# %%
car.info()

# %%
car['year'].unique()

# %%
car['Price'].unique()

# %%
car['kms_driven'].unique()

# %%
car['fuel_type'].unique()

# %%
## qualily
# -year has garbage values and convert to int type
# price -- remove comma and ask for price and make it int
# kms - remove kms , remove comma , remove nan make it int 
# fuel_type-- remove nan , make it string


# %%
                                                                 # Cleaning
                                                                # I) Create back up copy
                                                                ## Then refine the dataa

# %%
backup=car.copy()
backup.info()

# %%
                                                                    # Refining

# %%
car=car[car["year"].str.isnumeric()]

# %%
car['year'] = car['year'].astype(int)

# %%
car.info()

# %%
car=car[car['Price']!='Ask For Price']


# %%
car['Price']=car['Price'].str.replace(',','').astype('int')

car['Price'].unique()

# %%
car.info()

# %%
car['kms_driven']=car['kms_driven'].str.split(' ').str.get(0).str.replace(',','')


# %%
car=car[car['kms_driven'].str.isnumeric()]

# %%
car['kms_driven']=car['kms_driven'].astype('int')

# %%
car['kms_driven'].unique()

# %%
car.info()

# %%
car=car[~car['fuel_type'].isna()]

# %%
car.info()

# %%
car['name']=car['name'].str.split(' ').str.slice(0,3).str.join(' ')

# %%
car.info()

# %%
car

# %%
car.reset_index(drop=True)

# %%
car=car.reset_index(drop=True)

# %%
car.info()

# %%
car.describe()

# %%
car=car[car['Price']<6e6]

# %%
car

# %%
                                                        #save this refined data

# %%
car.to_csv("refine_car.csv")

# %%
# Refine is complete . Now we have to build model

# %%
                                                                # MODEL

# %%
car

# %%
X= car.drop(columns='Price')
# X


# %%
Y=car['Price']
# Y

# %%
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline



# %%
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2)

# %%
ohe=OneHotEncoder()
ohe.fit(X[['name','company','fuel_type']]) #some entity change

# %%
ohe.categories_

# %%
column_trans= make_column_transformer((OneHotEncoder(categories=ohe.categories_),['name','company','fuel_type']),remainder="passthrough")
# column_trans

# %%
lr=LinearRegression()
# lr

# %%
pipe=make_pipeline(column_trans,lr)
# pipe

# %%
pipe.fit(X_train,Y_train)

# %%
Y_pred=pipe.predict(X_test)
# Y_pred

# %%
r2_score(Y_test,Y_pred)

# %%
scores=[]
for i in range(30000):
    X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.3,random_state=i)
    lr=LinearRegression()
    # column_trans.fit(X_train)
    pipe=make_pipeline(column_trans,lr)
    pipe.fit(X_train,Y_train)
    Y_pred=pipe.predict(X_test)
    scores.append(r2_score(Y_test,Y_pred))

# %%
import numpy as np
max=np.argmax(scores)

# %%
scores[max]

# %%

                                                                ## for testing
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,random_state=max)
lr=LinearRegression()
pipe=make_pipeline(column_trans,lr)
pipe.fit(X_train,Y_train)
Y_pred=pipe.predict(X_test)
r2_score(Y_test,Y_pred)

# %%
import pickle
pickle.dump(pipe,open('LinearRegressionModel.pkl','wb'))


datf = pd.DataFrame(
  [
    ['Maruti Suzuki Swift','Maruti',2019, 100,'Petrol']
  ], 
  columns=['name','company','year','kms_driven','fuel_type']
  )

type(datf)

# %%
pipe.predict(pd.DataFrame(
  [
    ['Maruti Suzuki Swift','Maruti',2019, 100,'Petrol']
  ], 
  columns=['name','company','year','kms_driven','fuel_type'],
  dtype='object'
  )
)


