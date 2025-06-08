# coding: utf-8
from pymed import PubMed
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm


def get_info(pubmed_id: str) -> (str, str):
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pubmed_id}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "xml")

    mesh = [descriptor.text for descriptor in soup.find_all("DescriptorName")]
    mesh = ",".join(mesh)

    keywords = [keyword.text for keyword in soup.find_all("Keyword")]
    keywords = ",".join(keywords)
    return (mesh, keywords)

def save( pubmed_ids: list, is_selected: list, mesh_list: list, keywords_list: list, filename: str ) -> None:

    df = pd.DataFrame(
        {
            "pubmed_id": pubmed_ids,
            "selected": is_selected,
            "mesh": mesh_list,
            "keywords": keywords_list,
        }
    )
    df.to_csv(f"{filename}.csv", index=False)
    df.to_excel(f"{filename}.xlsx", index=False)

def main() -> None:
    with open("all") as f:
        all_ids = [line.strip() for line in f.readlines()]
    with open("selected") as f:
        selected_ids = [line.strip() for line in f.readlines()]

    pubmed_ids, is_selected, mesh_list, keywords_list = [], [], [], []
    for pubmed_id in tqdm(all_ids):
        pubmed_ids.append( pubmed_id )
        is_selected.append(1 if pubmed_id in selected_ids else 0)
        mesh, keywords = get_info( pubmed_id )
        mesh_list.append(mesh)
        keywords_list.append(keywords)
        save( pubmed_ids, is_selected, mesh_list, keywords_list, "annotated" )
        time.sleep(0.2)

if __name__ == "__main__":
    main()
