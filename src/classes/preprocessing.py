import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpers.text import preprocesar_texto, pasar_a_minusculas, eliminar_acentos_palabra
import json

class Preprocessing:
  encoder = None

  def __init__(self):
    self.encoder = OneHotEncoder(sparse_output=False)
    pass

  def preprocess_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
    df_preprocessed = df.copy()
    # Columna esta trabajando
    df_preprocessed['is_working'] = df_preprocessed['is_working'].apply(lambda x: 1 if x == True else 0)
    # Preprocess text
    texts = df_preprocessed[['first_question', 'second_question', 'third_question', 'fourth_question', 'fifth_question', 'sixth_question', 'seventh_question', 'eighth_question']]
    for column in texts.columns:
      df_preprocessed[column] = df_preprocessed[column].astype('str').apply(preprocesar_texto)
    columns = ['first_question', 'second_question', 'third_question', 'fourth_question', 'fifth_question', 'sixth_question', 'seventh_question', 'eighth_question']
    for i in range(0, 8):
      df_preprocessed[columns[i]] = df_preprocessed[columns[i]].apply(lambda x: json.dumps(x))

    return df_preprocessed
