import os
import glob
import pandas as pd


def combine_csv(directory_path: str):
    os.chdir(directory_path)
    csv = 'csv'
    file_names = [i for i in glob.glob(f'*.{csv}')]
    new_csv = pd.concat([pd.read_csv(f) for f in file_names])
    new_csv.to_csv('new_csv.csv', index=False, encoding='utf-8-sig')


combine_csv("your path")
