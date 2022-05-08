from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

df_eng = pd.read_csv('./df_eng.csv', sep = ',')

def buildAttendanceRate(year: int = 0):
  if year == 0:
    calcul = (df_eng[
        (df_eng.id_indicator == 1) 
        # & (df_eng.year == 2018)
    ]
    .groupby(["sex", "country"])
    .apply(
        lambda x: (x.value_indicator * x.factor).sum() / x.factor.sum()
    ))
  
  if year > 0:
    calcul = (df_eng[
        (df_eng.id_indicator == 1) 
        & (df_eng.year == year)
    ]
    .groupby(["sex", "country"])
    .apply(
        lambda x: (x.value_indicator * x.factor).sum() / x.factor.sum()
    ))

  df_calcul = pd.DataFrame(calcul)
  df_calcul.reset_index()
  df_calcul.rename(columns={0:"value_indicator"}, inplace=True)

  df_calcul_group = df_calcul.groupby(['sex' , 'country']).agg({'value_indicator': 'mean'}).reset_index()
  
  dataset = []
  for item in df_calcul_group.itertuples():
    dataset.append({ 'sex': item[1], 'country': item[2], 'value': item[3] })
  
  return dataset

def buildAttendanceRateByCountry(country: str = ''):
  calcul = (df_eng[
    (df_eng.id_indicator == 2)
    & (df_eng.country == country)
  ]
  .groupby(["sex", "year"])
  .apply(
      lambda x: (x.value_indicator * x.factor).sum() / x.factor.sum()
  ))

  df_calcul = pd.DataFrame(calcul)
  df_calcul.reset_index(inplace=True)
  df_calcul.rename(columns={0:"value_indicator"}, inplace=True)

  df_calcul_group = df_calcul.groupby(['sex' , 'year']).agg({'value_indicator': 'mean'}).reset_index()
  dataset = []
  for item in df_calcul_group.itertuples():
    dataset.append({ 'sex': item[1], 'year': item[2], 'value': item[3] })
  
  return dataset

@app.get('/by-gender')
def by_gender(year: int = 0):
  return buildAttendanceRate(year)

@app.get('/by-country')
def by_country(country: str = ''):
  return buildAttendanceRateByCountry(country)
