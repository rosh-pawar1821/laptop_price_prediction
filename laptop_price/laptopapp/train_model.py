
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import GradientBoostingRegressor
import joblib

df = pd.read_csv("laptopapp/laptop_data.csv", index_col=0)

df['Ram'] = df['Ram'].str.replace('GB', '').astype('int32')
df['Weight'] = df['Weight'].str.replace('kg', '').astype('float32')

df['Touchscreen'] = df['ScreenResolution'].apply(lambda x: 1 if 'Touchscreen' in x else 0)
df['Ips'] = df['ScreenResolution'].apply(lambda x: 1 if 'IPS' in x else 0)

res_split = df['ScreenResolution'].str.split('x', n=1, expand=True)
df['X_res'] = res_split[0].str.replace(',', '').str.extract(r'(\d+)', expand=False).astype('int')
df['Y_res'] = res_split[1].astype('int')
df['ppi'] = (((df['X_res']**2 + df['Y_res']**2)**0.5) / df['Inches']).astype('float')

df.drop(columns=['ScreenResolution', 'Inches', 'X_res', 'Y_res'], inplace=True)

def fetch_processor(text):
    if text.startswith('Intel Core i7'):
        return 'Intel Core i7'
    elif text.startswith('Intel Core i5'):
        return 'Intel Core i5'
    elif text.startswith('Intel Core i3'):
        return 'Intel Core i3'
    elif text.split()[0] == 'Intel':
        return 'Other Intel Processor'
    else:
        return 'AMD Processor'

df['Cpu Brand'] = df['Cpu'].apply(fetch_processor)
df.drop(columns=['Cpu'], inplace=True)

df['Memory'] = df['Memory'].astype(str).replace(r'\.0', '', regex=True)
df['Memory'] = df['Memory'].str.replace('GB', '')
df['Memory'] = df['Memory'].str.replace('TB', '000')

new = df['Memory'].str.split('+', n=1, expand=True)
df['first'] = new[0].str.strip()
df['second'] = new[1].fillna('0').str.strip()

df['Layer1HDD'] = df['first'].str.contains('HDD').astype(int)
df['Layer1SSD'] = df['first'].str.contains('SSD').astype(int)
df['first'] = df['first'].str.extract(r'(\d+)').fillna(0).astype(int)

df['Layer2HDD'] = df['second'].str.contains('HDD').astype(int)
df['Layer2SSD'] = df['second'].str.contains('SSD').astype(int)
df['second'] = df['second'].str.extract(r'(\d+)').fillna(0).astype(int)

df['HDD'] = (df['first'] * df['Layer1HDD'] + df['second'] * df['Layer2HDD'])
df['SSD'] = (df['first'] * df['Layer1SSD'] + df['second'] * df['Layer2SSD'])

df.drop(columns=['Memory', 'first', 'second', 'Layer1HDD', 'Layer1SSD',
                 'Layer2HDD', 'Layer2SSD'], inplace=True)

df['Gpu brand'] = df['Gpu'].str.split().str[0]
df.drop(columns=['Gpu'], inplace=True)

X = df.drop('Price', axis=1)
y = df['Price']

print("\n Columns in X:")
for col in X.columns:
    print(f"- {col}")

cat_features = ['Company', 'TypeName', 'Cpu Brand', 'Gpu brand', 'OpSys']

column_trans = ColumnTransformer([
    ('ohe', OneHotEncoder(drop='first', sparse_output=False), cat_features)
], remainder='passthrough')

pipe = Pipeline([
    ('transformer', column_trans),
    ('model', GradientBoostingRegressor(n_estimators=500, random_state=42))
])

pipe.fit(X, y)

joblib.dump(pipe, 'model.pkl')
print("Model saved as model.pkl")
