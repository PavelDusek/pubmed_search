# pip install pymed
# pip install pandas
# pip install bs4
# pip install lxml

# coding: utf-8
from pymed import PubMed
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time


def save(df: pd.DataFrame, filename: str) -> None:
    df["pubmed_id"] = df["pubmed_id"].apply(get_pubmed_link)
    df["doi"] = df["doi"].apply(get_doi_link)
    df.to_excel(f"{filename}.xlsx", index=False)
    df.to_csv(f"{filename}.csv", index=False)


def get_pubmed_link(pubmed_id: str) -> str:
    if pubmed_id:
        pubmed_id = pubmed_id.splitlines()[0]
        return (
            f'=HYPERLINK("https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}", "{pubmed_id}")'
        )


def get_doi_link(doi: str) -> str:
    if doi:
        doi = doi.splitlines()[0]
        return f'=HYPERLINK("http://doi.org/{doi}", "{doi}")'


def get_mesh(pubmed_id: str) -> str:
    if pubmed_id:
        pubmed_id = pubmed_id.splitlines()[0]

        url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pubmed_id}"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "xml")
        mesh = [descriptor.text for descriptor in soup.find_all("DescriptorName")]
        return ",".join(mesh)


pubmed = PubMed(tool="paliativni.cz", email="pavel.dusek@lf1.cuni.cz")

#filename = "results_2024_A"
filename = "results_2025"
# query  = "(\"2021/01/01\"[Date - Create] : \"2022/06/30\"[Date - Create]) "
# query  = "(\"2022/07/01\"[Date - Create] : \"2023/05/31\"[Date - Create]) "
#query = '("2023/06/01"[Date - Create] : "2023/11/30"[Date - Create]) '
#query = '("2023/12/01"[Date - Create] : "2024/06/30"[Date - Create]) '
query = '("2024/07/01"[Date - Create] : "2025/06/01"[Date - Create]) '

query += "AND ("

query += '("Palliative Care"[Mesh]) OR '
query += '("Palliative Medicine"[Mesh]) OR '
query += '("Hospice and Palliative Care Nursing"[Mesh]) OR '
query += '("Terminal Care"[Mesh]) OR '
query += '("Death"[Mesh]) OR '
query += '("Hospice Care"[Mesh]) OR '
query += '("Right to Die"[Mesh]) OR '
query += '("Catastrophic Illness"[Mesh]) OR '
query += '("Respite Care"[Mesh]) OR '
query += '("Assisted Living Facilities"[Mesh]) OR '
query += '("Hospices"[Mesh]) OR '
query += '("Quality of Life"[Mesh]) OR '
query += '("Sickness Impact Profile"[Mesh]) OR '
query += '("Resuscitation Orders"[Mesh]) OR '
query += '("Withholding Treatment"[Mesh]) OR '
query += '("Advance Directive Adherence"[Mesh]) OR '
query += '("Medical Futility"[Mesh]) OR '
query += '("Palliative Care/statistics and numerical data"[Mesh]) OR '
query += '("Ethics Consultation"[Mesh]) OR '
query += '("Bereavement"[Mesh]) OR '
query += '("Grief"[Mesh]) OR '
query += '("Decision Making"[Mesh]) OR '
query += '("Advance Care Planning"[Mesh]) OR '
query += '("Advance Directives"[Mesh]) OR '
query += '("Communication"[Mesh]) OR '
query += '("Hospice and Palliative Care Nursing"[Mesh]) OR '
query += '("Attitude to Death"[Mesh]) OR '
query += '("Empathy"[Mesh]) OR '
query += '("Family Nursing"[Mesh]) OR '
query += '("Social support"[Mesh]) OR '
query += '("Health Personnel"[Mesh]) OR '
query += '("Home Care Services"[Mesh]) OR '
query += '("Needs Assessment"[Mesh])'

query += ") AND "

metaanalysis = query + '("Meta-Analysis"[Publication Type])'

query += '("Clinical Study" [Publication Type]) NOT ("Clinical Trial Protocol"[Publication Type])'

#############
# perinatal #
#############
#query = '(perinatal AND palliative) OR (prenatal AND palliative) OR (infant AND palliative)'
#query = 'perinatal AND palliative'
#filename = "perinatal"

def query_to_xlsx( query: str, filename: str) -> None:
    print(query)
    results = pubmed.query(query, max_results=6000)
    titles, dois, journals, ids, meshes, keywords, abstracts, included = ( [], [], [], [], [], [], [], [], )
    for article in results:
        # article.abstract
        # article.authors
        # article.publication_date
        # article.conclusions
        # article.copyrights
        # article.methods
        # article.results
        # article.toDict()
        # article.keywords
        try:
            print(article.pubmed_id)

            abstracts.append(article.abstract)
            titles.append(article.title)
            journals.append(article.journal)
            ids.append(article.pubmed_id)
            dois.append(article.doi)
            keywords.append(article.keywords)
            included.append("")

            pubmed_id = article.pubmed_id.splitlines()[0]
            mesh = get_mesh(pubmed_id)
            meshes.append(mesh)
        except Exception as excp:
            max_length = max(len(included), len(titles), len(journals), len(ids), len(dois), len(keywords), len(abstracts), len(meshes) )
            if len(abstracts) < max_length:
                abstracts.append("")
            if len(titles) < max_length:
                titles.append("")
            if len(journals) < max_length:
                journals.append("")
            if len(ids) < max_length:
                ids.append("")
            if len(dois) < max_length:
                dois.append("")
            if len(keywords) < max_length:
                keywords.append("")
            if len(included) < max_length:
                included.append("")
            if len(meshes) < max_length:
                meshes.append("")
            print(excp)

        print(len(included), len(titles), len(journals), len(ids), len(dois), len(keywords), len(meshes), len(abstracts) )

        df = pd.DataFrame(
            {
                "included": included,
                "title": titles,
                "journals": journals,
                "pubmed_id": ids,
                "doi": dois,
                "keywords": keywords,
                "mesh": meshes,
                "abstracts": abstracts,
            }
        )
        save(df, filename)
        time.sleep(0.1)

if __name__ == "__main__":
    query_to_xlsx( query = query, filename = "trials")
    query_to_xlsx( query = metaanalysis, filename = "metaanalysis")

