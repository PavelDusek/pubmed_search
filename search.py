# coding: utf-8
from pymed import PubMed
import pandas as pd

pubmed = PubMed(tool="My Tool")

#query  = "(\"2021/01/01\"[Date - Create] : \"2022/06/30\"[Date - Create]) "
query  = "(\"2022/07/01\"[Date - Create] : \"2023/05/31\"[Date - Create]) "

query += "AND ("


query += "(\"Palliative Care\"[Mesh]) OR "
query += "(\"Palliative Medicine\"[Mesh]) OR "
query += "(\"Hospice and Palliative Care Nursing\"[Mesh]) OR "
query += "(\"Terminal Care\"[Mesh]) OR "
query += "(\"Death\"[Mesh]) OR "
query += "(\"Hospice Care\"[Mesh]) OR "
query += "(\"Right to Die\"[Mesh]) OR "
query += "(\"Catastrophic Illness\"[Mesh]) OR "
query += "(\"Respite Care\"[Mesh]) OR "
query += "(\"Assisted Living Facilities\"[Mesh]) OR "
query += "(\"Hospices\"[Mesh]) OR "
query += "(\"Quality of Life\"[Mesh]) OR "
query += "(\"Sickness Impact Profile\"[Mesh]) OR "
query += "(\"Resuscitation Orders\"[Mesh]) OR "
query += "(\"Withholding Treatment\"[Mesh]) OR "
query += "(\"Advance Directive Adherence\"[Mesh]) OR "
query += "(\"Medical Futility\"[Mesh]) OR "
query += "(\"Palliative Care/statistics and numerical data\"[Mesh]) OR "
query += "(\"Ethics Consultation\"[Mesh]) OR "
query += "(\"Bereavement\"[Mesh]) OR "
query += "(\"Grief\"[Mesh]) OR "
query += "(\"Decision Making\"[Mesh]) OR "
query += "(\"Advance Care Planning\"[Mesh]) OR "
query += "(\"Advance Directives\"[Mesh]) OR "
query += "(\"Communication\"[Mesh]) OR "
query += "(\"Hospice and Palliative Care Nursing\"[Mesh]) OR "
query += "(\"Attitude to Death\"[Mesh]) OR "
query += "(\"Empathy\"[Mesh]) OR "
query += "(\"Family Nursing\"[Mesh]) OR "
query += "(\"Social support\"[Mesh]) OR "
query += "(\"Health Personnel\"[Mesh]) OR "
query += "(\"Home Care Services\"[Mesh]) OR "
query += "(\"Needs Assessment\"[Mesh])"

query += ") AND "

query += "(\"Clinical Study\" [Publication Type]) NOT (\"Clinical Trial Protocol\"[Publication Type])"

print(query)

results = pubmed.query(query, max_results=50000)

titles, dois, journals, ids = [], [], [], []
for article in results:
    titles.append(article.title)
    journals.append(article.journal)
    ids.append(article.pubmed_id)
    dois.append(article.doi)
    
df = pd.DataFrame({'title': titles, 'journals': journals, 'pubmed_id': ids, 'doi': dois})
def get_pubmed_link(pubmed_id):
    if pubmed_id:
        pubmed_id = pubmed_id.splitlines()[0]
        return f"=HYPERLINK(\"https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}\", \"{pubmed_id}\")"

def get_doi_link(doi):
    if doi:
        doi = doi.splitlines()[0]
        return f"=HYPERLINK(\"http://doi.org/{doi}\", \"{doi}\")"
        
df['pubmed_id'] = df['pubmed_id'].apply(get_pubmed_link)
df['doi'] = df['doi'].apply(get_doi_link)
df.to_excel("results.xlsx", index = False)
