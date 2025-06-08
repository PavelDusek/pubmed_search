# coding: utf-8
import pandas as pd

df = pd.read_csv("annotated.csv")

mesh_count = {}
keys_count = {}

for i, row in df.iterrows():
    selected, mesh, keys = row["selected"], row["mesh"], row["keywords"]

    if not pd.isna(mesh) and selected:
        for key in mesh.split(","):
            if key in mesh_count:
                mesh_count[key] += 1
            else:
                mesh_count[key] = 1

    if not pd.isna(keys) and selected:
        for key in keys.split(","):
            if key in keys_count:
                keys_count[key] += 1
            else:
                keys_count[key] = 1

pd.DataFrame(mesh_count.items(), columns=["key", "count"]).sort_values(
    by="count", ascending=False
).to_csv("mesh.csv", index=False)

pd.DataFrame(keys_count.items(), columns=["key", "count"]).sort_values(
    by="count", ascending=False
).to_csv("keywords.csv", index=False)
