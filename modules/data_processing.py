import pandas as pd
import matplotlib.pyplot as plt
import os
import re
from res import kecamatan_map

current_dir = os.path.dirname(__file__)

def load_data(excel_file_path):
    return pd.read_excel(excel_file_path)


# to process data for calcuate most frequent diseases cateogories, here using method forward fill and remove unwanted column
def process_data(df):
    # drop unwanted columns
    df = df.drop(['NO','NO RM', 'NAMA', 'JK', 'ALAMAT', 'RT', 'RW', 'THERAPI', 'Sistole', 'Diastole', 'Nadi', 'BB', 'TB', 'Usia'], axis=1)

    # drop rows where every column is nan/null because the merged cell excel
    df = df.dropna(how="all")

    # Remove rows where 'DIAGNOSA' column is "-[]"
    df = df[df['DIAGNOSA'] != "-[]"]

    # do forward fill to handle missing values
    df = df.ffill()
    return df

def calculate_frequencies(df):
    # find the most frequent category by first letter & visualize it
    most_freq_category = df['DIAGNOSA'].str[2].value_counts().reset_index()
    most_freq_category.columns = ['Letter', 'Count']

    return most_freq_category

def process_data2(df):
    # drop unwanted column, here we want to analyze age & patient address
    df = df.drop(['NO','NO RM', 'NAMA','RT', 'RW', 'THERAPI', 'Gejala', 'Sistole', 'Diastole', 'Nadi', 'BB', 'TB'], axis=1)

    # drop all rows that has nan values
    df = df.dropna()

    # Remove rows where 'DIAGNOSA' column is "-[]"
    df = df[df['DIAGNOSA'] != "-[]"]

    # encode JK to numeric, P: 0, L: 1
    df['JK'] = df['JK'].map({'P': 0, 'L': 1})

    # convert usia to integer and check the range that usia must be >=0 and <=100
    df['Usia'] = df['Usia'].astype(int)
    df = df[(df['Usia']>=0) & (df['Usia'] <= 100)]

    return df


def extract_kecamatan(address):
  for kecamatan, kelurahan in kecamatan_map.kecamatan_map.items():
    for kel in kelurahan:
      if re.search(kel, address):
        return kecamatan
  return "Lainnya"

def count_address(df):
    # lowercase all the address
    df['ALAMAT'] = df['ALAMAT'].str.lower() 

    # apply extract kecamatan function
    df['ALAMAT'] = df['ALAMAT'].apply(extract_kecamatan)

    df_count_alamat = df['ALAMAT'].value_counts().reset_index()

    df_count_alamat = df_count_alamat.rename(columns={'ALAMAT': 'Kecamatan', 'count': 'Count'})

    return df_count_alamat

def age_group(df):
   # buat kelompok usia
   df['age_range'] = pd.cut(df['Usia'], bins=[0, 5, 10, 19, 60, 100], labels=['balita', 'anak', 'remaja', 'dewasa', 'lansia'], right=False)

   df_age_range_counts = df['age_range'].value_counts()

   return df_age_range_counts

