from __future__ import annotations
from pathlib import Path

MISSING ={"", "na", "n/a", "null", "none", "nan"}


def is_missing(value: str | None) -> bool:
    if value is None:
        return True
    return value.strip().casefold() in MISSING


def try_float(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None


def infer_type(values: list[str]) -> str:
    usable = [v for v in values if not is_missing(v)]
    if not usable:
        return "text"
    for v in usable:
        if try_float(v) is None:
            return "text"
    return "number"

def column_values(rows: list[dict[str, str]], col: str) -> list[str]:#to extract column values a:1 . one is the value here 
    return [row.get(col, "") for row in rows]

def numeric_stats(values: list[str]) -> dict:#for my values it will comput the min max and avg (mean), also the missings and the counts 
    usable = [v for v in values if not is_missing(v)]
    missing = len(values) - len(usable)

    nums: list[float] = []
    for v in usable:
        x = try_float(v)
        if x is None:
            raise ValueError(f"Non-numeric value found: {v!r}")
        nums.append(x)

    count = len(nums)
    unique = len(set(nums))

    return {
        "count": count,
        "missing": missing,
        "unique": unique,
        "min": min(nums) if nums else None,
        "max": max(nums) if nums else None,
        "mean": (sum(nums) / count) if count else None,
    }

def text_stats(values: list[str], top_k: int = 5) -> dict:
    usable = [v for v in values if not is_missing(v)]
    missing = len(values) - len(usable)

    count = len(usable)
    unique = len(set(usable))

    counts: dict[str, int] = {}
    for v in usable:
        counts[v] = counts.get(v, 0) + 1

    top_items = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:top_k]
    top = [{"value": k, "count": n} for k, n in top_items]

    return {
        "count": count,
        "missing": missing,
        "unique": unique,
        "top": top,
    }

#^my helpers




# #task 4 will count the misiings and rows
# def basic_profile(rows: list[dict[str, str]]) -> dict:
#     """Compute row count, column names, and missing values per column."""
#     report = {
#         "rows": len(rows),#my final report i want to see how many rows i have and clomns with misiings
#         "columns": {}
#     }

#     if not rows:#to avoid crashing
#         return report

#     columns = list(rows[0].keys())# if there is at least one row give me the columns from the first row"keys not values""

#     for col in columns:
#         report["columns"][col] = {"missing": 0}# initilizing for all column a missing counter

#     for row in rows:#takes the full row
#         for col in columns:#takes the colmn only which is the key
#             value = row[col].strip()#the value for that key (col)
#             if value == "":
#                 report["columns"][col]["missing"] += 1#col here can be name age salary ...

#     return report


def basic_profile(rows: list[dict[str, str]], source_path: str | Path | None = None) -> dict:
    if not rows:
        return {
            "source": {"path": str(source_path) if source_path is not None else None},
            "summary": {"rows": 0, "columns": 0},
            "columns": {},
        }

   #get colum names from first row
    columns = list(rows[0].keys())

    report: dict = {
        "source": {"path": str(source_path) if source_path is not None else None},
        "summary": {"rows": len(rows), "columns": len(columns)},
        "columns": {},
    }

    #stat of column
    for col in columns:
        values = column_values(rows, col)        
        col_type = infer_type(values)        

        if col_type == "number":
            stats = numeric_stats(values)     
        else:
            stats = text_stats(values)       

        report["columns"][col] = {"type": col_type, **stats}

    return report
