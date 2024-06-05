import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from helpers.text import delete_accented_chars

class Preprocessing:
  encoder = None

  def __init__(self):
    self.encoder = OneHotEncoder(sparse_output=False)
    pass
  
  def preprocess_dataframe(self, df):
    df_preprocessed = df.copy()
    # Column working as true or false
    df_preprocessed['working'] = df_preprocessed['working'].astype('str').str.lower().apply(delete_accented_chars)
    df_preprocessed['working'] = df_preprocessed['working'].apply(lambda x: 1 if x == 'si' else 0)
    # One Hot Encoder for column age
    encoded_age = self.encoder.fit_transform(df_preprocessed[['age']])
    encoded_df = pd.DataFrame(encoded_age, columns=self.encoder.get_feature_names_out(['age']))
    df_preprocessed = pd.concat([df_preprocessed.drop(columns=['age']), encoded_df], axis=1)
    return df_preprocessed
  