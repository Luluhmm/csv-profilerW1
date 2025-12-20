from __future__ import annotations
from csv import DictReader
from pathlib import Path
import csv


# def read_csv_rows(path: str | Path) -> list[dict[str, str]]:#this takes a path as a string or path and outputs ist of dictionary
#     """Read a CSV as a list of rows (each row is a dict of strings)."""
#     with open(path,newline="") as f:#with will close file automatically
#         reader = DictReader(f) #this will read the first rown in my csv as the keys like name age..
#         return list(reader)

def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path}")
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        raise ValueError("CSV has no data rows")
    return rows