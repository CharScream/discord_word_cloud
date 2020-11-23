import os
import glob
import pandas as pd

DIRECTORY_PATH = ""
os.chdir(DIRECTORY_PATH)
file_names = [i for i in glob.glob("*.csv")]
new_csv = pd.concat([pd.read_csv(f) for f in file_names])
new_csv.to_csv("combined.csv", index=False, encoding="utf-8-sig")
