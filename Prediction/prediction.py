#%%
import pandas as pd 
pd.options.display.max_rows = 30
from download import download
import numpy as np 
import datetime  
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import linear_model
import statsmodels.api as sm


#%%
url="https://docs.google.com/spreadsheets/d/e/2PACX-1vQVtdpXMHB4g9h75a0jw8CsrqSuQmP5eMIB2adpKR5hkRggwMwzFy5kB-AIThodhVHNLxlZYm8fuoWj/pub?gid=2105854808&single=true&output=csv"
path_target="La myriade de Totems de Montpellier - SaisiesFormulaire.csv"
download(url, path_target, replace = True)


# %%
df_bicycle_raw = pd.read_csv("La myriade de Totems de Montpellier - SaisiesFormulaire.csv", parse_dates=True, dayfirst=True)
df_bicycle_raw.tail(n=9)


#%%
df_bicycle = df_bicycle_raw.copy()

#%%
#columns rename
df_bicycle.columns=['Date', 'Hour', 'Total', "Day's total", 'Unnamed', 'Note']
df_bicycle

#gives the type of the variables
df_bicycle.dtypes


# %%
#the first two rows and the last row deleted
del df_bicycle['Note']
del df_bicycle['Total']
df_bicycle.dropna(axis=0, how="all", inplace = True)
df_bicycle

#%%
#Unnamed column deleted
df_bicycle.dropna(axis = 1, how = 'all', inplace = True)
df_bicycle

#%%
df_shrunk_bicycle = df_bicycle.copy()

# %%
#Only keeps hours between 8:30 am and 10:30 am
df_shrunk_bicycle = df_shrunk_bicycle[df_shrunk_bicycle['Hour'] >= "08:30"]
df_shrunk_bicycle = df_shrunk_bicycle[df_shrunk_bicycle['Hour'] <= "09:30"]
df_shrunk_bicycle


#%%
#Deletes redundant dates and only keep the last one
df_shrunk_bicycle = df_shrunk_bicycle.drop_duplicates(subset = ['Date'], keep = "last")
df_shrunk_bicycle

#%%
for i in range (len(df_shrunk_bicycle)):
    df_shrunk_bicycle.rename(index = {df_shrunk_bicycle.index[i]:i}, inplace = True)
df_shrunk_bicycle


#%%
df_shrunk_bicycle2 = df_shrunk_bicycle.copy()


#%%
#Keep only dates after first quarantine
df_shrunk_bicycle2 = df_shrunk_bicycle2.iloc[11:]
df_shrunk_bicycle2.describe()


#%%
df_shrunk_bicycle3 = df_shrunk_bicycle2.copy()


#%%
#Weekdays association
df_shrunk_bicycle3['Date'] = pd.to_datetime(df_shrunk_bicycle3['Date'], format = "%d/%m/%Y") 
#format option to choose UK date format
df_shrunk_bicycle3['Jour de la semaine'] = df_shrunk_bicycle3['Date'].dt.day_name()
df_shrunk_bicycle3

#%%
#Only keeps weekdays 
df_weekdays = df_shrunk_bicycle3.loc[(df_shrunk_bicycle3['Jour de la semaine'] == 'Monday') ^ (df_shrunk_bicycle3['Jour de la semaine'] == 'Tuesday') ^ (df_shrunk_bicycle3['Jour de la semaine'] == 'Wednesday') ^ (df_shrunk_bicycle3['Jour de la semaine'] == 'Thursday') ^ (df_shrunk_bicycle3['Jour de la semaine']=='Friday')] 


#Reindex of df_weekdays
for i in range (len(df_weekdays)):
    df_weekdays.rename(index = {df_weekdays.index[i]:i}, inplace = True)
df_weekdays

df_weekdays.describe()#mean = 275
df_weekdays.median()#248

#%% 
#Only keeps Fridays 
df_Fridays = df_weekdays.loc[df_weekdays['Jour de la semaine'] == 'Friday']

#Reindex of df_Fridays
for i in range (len(df_Fridays)):
    df_Fridays.rename(index = {df_Fridays.index[i]:i}, inplace = True)
df_Fridays

df_Fridays.describe()#mean = 303
df_Fridays.median()#279

#First approach and sorted completed
#Let's now make a linear regression 


#%%
df_weekdays.index = df_weekdays['Date']
df_weekdays.index = pd.to_datetime(df_weekdays.index)
idx = pd.date_range(df_weekdays.index.min(), df_weekdays.index.max(), freq = 'D')
df_weekdays = df_weekdays.reindex(idx)
df_weekdays['Date'] = df_weekdays.index
for i in range (len(df_weekdays)):
    df_weekdays.rename(index = {df_weekdays.index[i]:i}, inplace = True)
df_weekdays
df_weekdays.fillna(0, inplace = True)

#%%
#replacing '0' value in Day's total column
#by the mean of i-1 and i+1 of Day's total
#(or i+j when i+1 element is equal to 0, j in [1,26])

for i in range(len(df_weekdays)):
        if df_weekdays['Hour'][i] == 0 and df_weekdays["Day's total"][i+1] != 0:
            df_weekdays["Day's total"][i] = (df_weekdays["Day's total"][i-1] + df_weekdays["Day's total"][i+1])/2
        elif df_weekdays['Hour'][i] == 0 and df_weekdays["Day's total"][i+2] != 0:
            df_weekdays["Day's total"][i] = (df_weekdays["Day's total"][i-1] + df_weekdays["Day's total"][i+2])/2
        elif df_weekdays['Hour'][i] == 0 and df_weekdays["Day's total"][i+3] != 0:
            df_weekdays["Day's total"][i] = (df_weekdays["Day's total"][i-1] + df_weekdays["Day's total"][i+3])/2
        elif df_weekdays['Hour'][i] == 0 and df_weekdays["Day's total"][i+4] != 0:
            df_weekdays["Day's total"][i] = (df_weekdays["Day's total"][i-1] + df_weekdays["Day's total"][i+4])/2
        elif df_weekdays['Hour'][i] == 0 and df_weekdays["Day's total"][i+5] != 0:
            df_weekdays["Day's total"][i] = (df_weekdays["Day's total"][i-1] + df_weekdays["Day's total"][i+5])/2
        elif df_weekdays['Hour'][i] == 0 and df_weekdays["Day's total"][i+6] != 0:
            df_weekdays["Day's total"][i] = (df_weekdays["Day's total"][i-1] + df_weekdays["Day's total"][i+6])/2
        elif df_weekdays['Hour'][i] == 0 and df_weekdays["Day's total"][i+7] != 0:
            df_weekdays["Day's total"][i] = (df_weekdays["Day's total"][i-1] + df_weekdays["Day's total"][i+7])/2
        elif df_weekdays['Hour'][i] == 0 and df_weekdays["Day's total"][i+8] != 0:
            df_weekdays["Day's total"][i] = (df_weekdays["Day's total"][i-1] + df_weekdays["Day's total"][i+8])/2
        elif df_weekdays['Hour'][i] == 0 and df_weekdays["Day's total"][i+9] != 0:
            df_weekdays["Day's total"][i] = (df_weekdays["Day's total"][i-1] + df_weekdays["Day's total"][i+9])/2
        elif df_weekdays['Hour'][i] == 0 and df_weekdays["Day's total"][i+10] != 0:
            df_weekdays["Day's total"][i] = (df_weekdays["Day's total"][i-1] + df_weekdays["Day's total"][i+10])/2
        elif df_weekdays['Hour'][i] == 0 and df_weekdays["Day's total"][i+11] != 0:
            df_weekdays["Day's total"][i] = (df_weekdays["Day's total"][i-1] + df_weekdays["Day's total"][i+11])/2
        elif df_weekdays['Hour'][i] == 0 and df_weekdays["Day's total"][i+12] != 0:
            df_weekdays["Day's total"][i] = (df_weekdays["Day's total"][i-1] + df_weekdays["Day's total"][i+12])/2
        elif df_weekdays['Hour'][i] == 0 and df_weekdays["Day's total"][i+13] != 0:
            df_weekdays["Day's total"][i] = (df_weekdays["Day's total"][i-1] + df_weekdays["Day's total"][i+13])/2
        elif df_weekdays['Hour'][i] == 0 and df_weekdays["Day's total"][i+14] != 0:
            df_weekdays["Day's total"][i] = (df_weekdays["Day's total"][i-1] + df_weekdays["Day's total"][i+14])/2
        elif df_weekdays['Hour'][i] == 0 and df_weekdays["Day's total"][i+15] != 0:
            df_weekdays["Day's total"][i] = (df_weekdays["Day's total"][i-1] + df_weekdays["Day's total"][i+15])/2
        elif df_weekdays['Hour'][i] == 0 and df_weekdays["Day's total"][i+16] != 0:
            df_weekdays["Day's total"][i] = (df_weekdays["Day's total"][i-1] + df_weekdays["Day's total"][i+16])/2
        elif df_weekdays['Hour'][i] == 0 and df_weekdays["Day's total"][i+17] != 0:
            df_weekdays["Day's total"][i] = (df_weekdays["Day's total"][i-1] + df_weekdays["Day's total"][i+17])/2
        elif df_weekdays['Hour'][i] == 0 and df_weekdays["Day's total"][i+18] != 0:
            df_weekdays["Day's total"][i] = (df_weekdays["Day's total"][i-1] + df_weekdays["Day's total"][i+18])/2
        elif df_weekdays['Hour'][i] == 0 and df_weekdays["Day's total"][i+19] != 0:
            df_weekdays["Day's total"][i] = (df_weekdays["Day's total"][i-1] + df_weekdays["Day's total"][i+19])/2
        elif df_weekdays['Hour'][i] == 0 and df_weekdays["Day's total"][i+20] != 0:
            df_weekdays["Day's total"][i] = (df_weekdays["Day's total"][i-1] + df_weekdays["Day's total"][i+20])/2
        elif df_weekdays['Hour'][i] == 0 and df_weekdays["Day's total"][i+21] != 0:
            df_weekdays["Day's total"][i] = (df_weekdays["Day's total"][i-1] + df_weekdays["Day's total"][i+21])/2
        elif df_weekdays['Hour'][i] == 0 and df_weekdays["Day's total"][i+22] != 0:
            df_weekdays["Day's total"][i] = (df_weekdays["Day's total"][i-1] + df_weekdays["Day's total"][i+22])/2
        elif df_weekdays['Hour'][i] == 0 and df_weekdays["Day's total"][i+23] != 0:
            df_weekdays["Day's total"][i] = (df_weekdays["Day's total"][i-1] + df_weekdays["Day's total"][i+23])/2
        elif df_weekdays['Hour'][i] == 0 and df_weekdays["Day's total"][i+24] != 0:
            df_weekdays["Day's total"][i] = (df_weekdays["Day's total"][i-1] + df_weekdays["Day's total"][i+24])/2
        elif df_weekdays['Hour'][i] == 0 and df_weekdays["Day's total"][i+25] != 0:
            df_weekdays["Day's total"][i] = (df_weekdays["Day's total"][i-1] + df_weekdays["Day's total"][i+25])/2
        elif df_weekdays['Hour'][i] == 0 and df_weekdays["Day's total"][i+26] != 0:
            df_weekdays["Day's total"][i] = (df_weekdays["Day's total"][i-1] + df_weekdays["Day's total"][i+26])/2
df_weekdays



    
        
        
#%%
#creates a new column which cumules daily numbers
df_weekdays['weekdays total'] = np.zeros(len(df_weekdays))
df_weekdays['weekdays total'][0]= df_weekdays["Day's total"][0]
for i in range(len(df_weekdays)-1):
    df_weekdays['weekdays total'][i+1] = df_weekdays["Day's total"][i+1] + df_weekdays['weekdays total'][i]
df_weekdays


#%%
#from sklearn.linear_model import LinearRegression
X = df_weekdays['Date']
Y = df_weekdays['weekdays total']
fig = plt.figure(figsize=(7, 4))
axes = plt.axes()
plt.title('Linear regression', color = 'red') 
plt.xlabel('Date')
plt.ylabel('Total number of bikes')
plt.plot(X, Y, '.')
plt.show()


#%%
df_weekdays['Index column'] = np.arange(start = 0, stop = 324)
sns.lmplot(x = "Index column", y = "weekdays total", data = df_weekdays)




# %%
X = np.arange(start = 0,stop = 324).reshape((-1,1))
y = df_weekdays["weekdays total"]

model = linear_model.LinearRegression()
results = model.fit(X, y)

print(results.intercept_, results.coef_)


estimated_y324= results.intercept_ + results.coef_*324 - df_weekdays['weekdays total'][323]
estimated_y324
#1679 estimated, it's way too much


#%%
#If we want more info about the linear regression:

X = np.arange(start = 0,stop = 324)
X = np.vander(X, 2) #because the intercept is not included in statsmodels module
#Or: X = sm.add_constant(X)

model2 = sm.OLS(y, X)
results2 = model2.fit()

print(results2.summary())

#Values for confidence interval may be calculated with 
#coefs given ([0.025, 0.075]) 

##Given that atypical estimation value, 
##we're not going to make a linear regression with df_Fridays

##The median method looked far better, so we'll keep it