import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from helpers.text import delete_accented_chars, delete_spanish_letters, delete_spaces, delete_not_vocabulary_words

class Preprocessing:
  encoder = None

  def __init__(self):
    self.encoder = OneHotEncoder(sparse_output=False)
    pass
  
  def preprocess_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
    df_preprocessed = df.copy()
    # Column working as true or false
    df_preprocessed['working'] = df_preprocessed['working'].astype('str').str.lower().apply(delete_accented_chars)
    df_preprocessed['working'] = df_preprocessed['working'].apply(lambda x: 1 if x == 'si' else 0)
    # One Hot Encoder for column age
    encoded_age = self.encoder.fit_transform(df_preprocessed[['age']])
    encoded_df = pd.DataFrame(encoded_age, columns=self.encoder.get_feature_names_out(['age']))
    df_preprocessed = pd.concat([df_preprocessed.drop(columns=['age']), encoded_df], axis=1)
    # Preprocess text
    text = df_preprocessed['question_1'].iloc[0]
    text_preprocessed = self.preprocess_text(text)
    print(f'Original text: {text}')
    print(f'Preprocessed text: {text_preprocessed}')
    return df_preprocessed
  
  def preprocess_text(self, text: str) -> str:
    """
    Preprocesses the given text by converting it to lowercase, deleting accented characters,
    deleting Spanish letters, and deleting spaces.

    Args:
      text (str): The text to be preprocessed.

    Returns:
      str: The preprocessed text.
    """
    text_preprocessed = text.lower()
    text_preprocessed = delete_accented_chars(text_preprocessed)
    text_preprocessed = delete_spanish_letters(text_preprocessed)
    text_preprocessed = delete_spaces(text_preprocessed)
    text_preprocessed = delete_not_vocabulary_words(text_preprocessed)

    return text_preprocessed