# coding: utf-8
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

os.mkdir("abstracts")
df = pd.read_excel("results.xlsx")
url = "https://pubmed.ncbi.nlm.nih.gov/"

for i, row in df.iterrows():
    print(i)
    pid = row['pubmed_id']
    r = requests.get(url + f"{pid}")
    s = BeautifulSoup(r.text, "html.parser")
    text = s.find("div", attrs={"id": "abstract"}).prettify()
    with open(f"abstracts/{i}.txt", "w") as f:
        f.write(text)
    time.sleep(5)
