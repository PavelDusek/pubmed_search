# coding: utf-8
"""
Divides articles to different people for paralel filtering.
"""

import math

import rich
import pandas as pd

def divide_articles(filename: str, people: list) -> None:
    """
    Divides articles from csv file into separate xlsx files, each file for each person.
    filename is filename of the csv file (without extension), e.g. 'trials' maps to 'trials.csv'.
    people is a list of persons to divide the articles to.
    """

    df = pd.read_csv(f"{filename}.csv")
    number_of_articles = math.ceil(len(df)/len(people))

    for i, name in enumerate(people):
        start = i * number_of_articles
        end = (i+1) * number_of_articles
        end = min(end, len(df))

        df_part = df.iloc[start:end,:]
        df_part.to_excel(f"{filename}_{name}.xlsx", index=False)
        rich.print(df_part.head())
        rich.print(len(df_part))
        rich.print(i, name, start, end)

def main() -> None:
    """Runs the divide_articles function for metaanalysis.csv and trials.csv files."""

    people = ["Andrea", "Katerina", "Ilona", "Ondrej", "Jindrich", "Michal", "Pavel"]
    divide_articles(filename = "metaanalysis", people = people)
    divide_articles(filename = "trials", people = people)


if __name__ == "__main__":
    main()
