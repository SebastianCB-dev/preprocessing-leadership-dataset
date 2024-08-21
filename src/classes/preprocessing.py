import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from helpers.text import preprocesar_texto, pasar_a_minusculas, eliminar_acentos_palabra
import json

class Preprocessing:
  encoder = None

  def __init__(self):
    self.encoder = OneHotEncoder(sparse_output=False)
    pass

  def preprocess_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
    df_preprocessed = df.copy()
    # Columna terminos y condiciones
    df_preprocessed['terminos_y_condiciones'] = df_preprocessed['terminos_y_condiciones'].apply(pasar_a_minusculas)
    df_preprocessed['terminos_y_condiciones'] = df_preprocessed['terminos_y_condiciones'].apply(eliminar_acentos_palabra)
    df_preprocessed['terminos_y_condiciones'] = df_preprocessed['terminos_y_condiciones'].apply(lambda x: 1 if x == 'si' else 0)
    # Columna esta trabajando
    df_preprocessed['esta_trabajando'] = df_preprocessed['esta_trabajando'].apply(pasar_a_minusculas)
    df_preprocessed['esta_trabajando'] = df_preprocessed['esta_trabajando'].apply(eliminar_acentos_palabra)
    df_preprocessed['esta_trabajando'] = df_preprocessed['esta_trabajando'].apply(lambda x: 1 if x == 'si' else 0)
    # One Hot Encoder for column age
    encoded_age = self.encoder.fit_transform(df_preprocessed[['rango_edad']])
    encoded_df = pd.DataFrame(encoded_age, columns=self.encoder.get_feature_names_out(['rango_edad']))
    df_preprocessed = pd.concat([df_preprocessed.drop(columns=['rango_edad']), encoded_df], axis=1)
    # One Hot encoder for column grado_educacion
    encoded_education = self.encoder.fit_transform(df_preprocessed[['grado_educacion']])
    encoded_df = pd.DataFrame(encoded_education, columns=self.encoder.get_feature_names_out(['grado_educacion']))
    df_preprocessed = pd.concat([df_preprocessed.drop(columns=['grado_educacion']), encoded_df], axis=1)
    # Preprocess text
    texts = df_preprocessed[['respuesta_1', 'respuesta_2', 'respuesta_3', 'respuesta_4', 'respuesta_5', 'respuesta_6', 'respuesta_7', 'respuesta_8']]
    for column in texts.columns:
      df_preprocessed[column] = df_preprocessed[column].astype('str').apply(preprocesar_texto)

    for i in range(1, 9):
      df_preprocessed[f'respuesta_{i}'] = df_preprocessed[f'respuesta_{i}'].apply(lambda x: json.dumps(x))

    return df_preprocessed
