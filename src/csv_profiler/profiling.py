from __future__ import annotations
from pathlib import Path
from collections import Counter

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



def profile_rows(rows: list[dict[str, str]]) -> dict:
    if not rows:
        return {"n_rows": 0, "n_cols": 0, "columns": []}

    n_rows = len(rows)
    columns = list(rows[0].keys())

    col_profiles = []

    for col in columns:
        values = [r.get(col, "") for r in rows]
        usable = [v for v in values if not is_missing(v)]

        missing = len(values) - len(usable)
        inferred = infer_type(values)
        unique = len(set(usable))

        profile = {
            "name": col,
            "type": inferred,
            "missing": missing,
            "missing_pct": 100.0 * missing / n_rows if n_rows else 0.0,
            "unique": unique,
        }

        if inferred == "number":
            nums = [try_float(v) for v in usable]
            nums = [x for x in nums if x is not None]
            if nums:
                profile.update({
                    "min": min(nums),
                    "max": max(nums),
                    "mean": sum(nums) / len(nums)
                })
        else:
            counts = Counter(usable)
            top = [
                {"value": v, "count": c}
                for v, c in counts.most_common(5)
            ]
            profile["top"] = top


        col_profiles.append(profile)

    return {"n_rows": n_rows, "n_cols": len(columns), "columns": col_profiles}
