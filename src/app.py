import os
import pandas as pd
import classes.preprocessing as Preprocessing

def main(): 
  # read csv
  csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../assets/dataset-v1.csv')
  df = pd.read_csv(csv_path, sep=',', encoding='utf-8')

  # instantiate Preprocessing class
  pp = Preprocessing.Preprocessing()
  df_preprocessed = pp.preprocess_dataframe(df)

  # Export preprocessed dataframe to csv
  output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../output')
  output_file = os.path.join(output_dir, 'preprocessed-dataset-v1.csv')

  # Crear el directorio si no existe
  if not os.path.exists(output_dir):
      os.makedirs(output_dir)

  df_preprocessed.to_csv(output_file, index=False)

if __name__ == '__main__':
  main()
