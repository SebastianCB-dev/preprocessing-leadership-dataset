import pandas as pd
import sys
import os
import textdistance

# Adjust the path to include the parent directory of src
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir)) # Go up two levels to reach project root
sys.path.append(parent_dir)

from src.helpers.text import preprocesar_texto

class Preprocessing:
  ontology = None

  def __init__(self):
    ontology_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../assets/ontologia_procesada.csv')
    self.ontology = pd.read_csv(ontology_path)

  def preprocess_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
    df_preprocessed = df.copy()
    # Columna esta trabajando
    df_preprocessed['is_working'] = df_preprocessed['is_working'].apply(lambda x: 1 if x == True else 0)
    # Define columns to join
    text_columns = ["first_question", "second_question", "third_question", "fourth_question", "fifth_question", "sixth_question", "seventh_question", "eighth_question"]
    num_rows = df_preprocessed.shape[0]
    for i in range(num_rows):
      row = df_preprocessed.iloc[i]
      row_texts = row[text_columns]
      texts_joined = " ".join(row_texts.astype(str))
      text_preprocessed = preprocesar_texto(texts_joined)
      print(f"\033[91m{'-'*100}\033[0m")
      print(text_preprocessed)
      result = self.getLeadershipWeights(text_preprocessed)
      # Agregar los resultados como nuevas columnas al DataFrame
      for key, value in result.items():
        df_preprocessed.at[i, f'weight_{key}'] = value

      print(f"\033[1mProcesada fila {i+1} de {num_rows}\033[0m")
      print(f"\033[91m{'-'*100}\033[0m")
      # Print a new line
    return df_preprocessed

  def getLeadershipWeights(self, tokens: list[str]) -> dict:
    leadership_weights = {}
    total_tokens = len(tokens)
    ontology_columns = self.ontology.columns

    for column_name in ontology_columns:
      ontology_column_values = set(self.ontology[column_name].dropna().tolist())
      count_words = 0

      for token in tokens:
        if token in ontology_column_values:
          count_words += 1
        else:
          for value in ontology_column_values:
            if textdistance.levenshtein.distance(value, token) <= 2:
              count_words += 1
              break
      leadership_weights[column_name] = count_words / total_tokens if total_tokens > 0 else 0
    return leadership_weights
