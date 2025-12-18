#task 4 will count the misiings and rows
def basic_profile(rows: list[dict[str, str]]) -> dict:
    """Compute row count, column names, and missing values per column."""
    report = {
        "rows": len(rows),#my final report i want to see how many rows i have and clomns with misiings
        "columns": {}
    }

    if not rows:#to avoid crashing
        return report

    columns = list(rows[0].keys())# if there is at least one row give me the columns from the first row"keys not values""

    for col in columns:
        report["columns"][col] = {"missing": 0}# initilizing for all column a missing counter

    for row in rows:#takes the full row
        for col in columns:#takes the colmn only which is the key
            value = row[col].strip()#the value for that key (col)
            if value == "":
                report["columns"][col]["missing"] += 1#col here can be name age salary ...

    return report
