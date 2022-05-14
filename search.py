# coding: utf-8
from pymed import PubMed
import pandas as pd

pubmed = PubMed(tool="My Tool")

query = "(\"2021/01/01\"[Date - Create] : \"2022/06/30\"[Date - Create]) AND ((\"Palliative Care\"[Mesh]) OR (\"Palliative Medicine\"[Mesh]) OR (\"Hospice and Palliative Care Nursing\"[Mesh]) OR (\"Terminal Care\"[Mesh]) OR (\"Death\"[Mesh]) OR (\"Hospice Care\"[Mesh]) OR (\"Right to Die\"[Mesh]) OR (\"Catastrophic Illness\"[Mesh]) OR (\"Respite Care\"[Mesh]) OR (\"Assisted Living Facilities\"[Mesh]) OR (\"Hospices\"[Mesh]) OR (\"Quality of Life\"[Mesh]) OR (\"Sickness Impact Profile\"[Mesh]) OR (\"Resuscitation Orders\"[Mesh]) OR (\"Withholding Treatment\"[Mesh]) OR (\"Advance Directive Adherence\"[Mesh]) OR (\"Euthanasia, Passive\"[Mesh]) OR (\"Medical Futility\"[Mesh]) OR (\"Palliative Care/statistics and numerical data\"[Mesh]) OR (\"Ethics Consultation\"[Mesh])) AND (\"Clinical Study\" [Publication Type])"

results = pubmed.query(query, max_results=5000)

titles, dois = [], []
for article in results:
    titles.append(article.title)
    dois.append(article.doi)
    
df = pd.DataFrame({'title': titles, 'doi': dois})
def get_link(doi):
    if doi:
        return f"=HYPERLINK(\"http://doi.org/{doi}\", \"{doi}\")"
        
df['doi'] = df['doi'].apply(get_link)
df.to_excel("results.xlsx", index = False)
