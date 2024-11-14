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
    # Define columns to join
    text_columns = ["first_question", "second_question", "third_question", "fourth_question", "fifth_question", "sixth_question", "seventh_question", "eighth_question"]
    num_rows = df_preprocessed.shape[0]
    print(f"number of rows: {num_rows}")
    for i in range(num_rows):
      row = df_preprocessed.iloc[i]
      row_texts = row[text_columns]
      texts_joined = " ".join(row_texts.astype(str))
      text_preprocessed = preprocesar_texto(texts_joined)
      print(f"Text preprocessed: {text_preprocessed}")

      print("--------------------------------")

    return df_preprocessed
