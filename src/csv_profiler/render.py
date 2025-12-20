#task 5
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime

def write_json(report: dict, path: str | Path) -> None:#takes input (what to write) and where to write it path
    p = Path(path)

    #reate parent folder if it does not exist and if exixst nothing happen
    p.parent.mkdir(parents=True, exist_ok=True)

    #writ my json
    with open(p, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)


def md_header(report: dict) -> str:
    return "# CSV Profile Report\n\n"

def write_markdown(report: dict, path: str | Path) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    rows = report["summary"]["rows"]
    cols = report["summary"]["columns"]
    columns_dict = report["columns"] 

    lines: list[str] = []
    lines.append(md_header(report))
    lines.append("## Summary\n")
    lines.append(f"- Rows: {rows}\n")
    lines.append(f"- Columns: {cols}\n\n")
    lines.append("## Columns Overview\n\n")
    lines.append("| Column | Type | Missing % | Unique |\n")
    lines.append("|--------|------|-----------:|-------:|\n")

    for col_name, col_report in columns_dict.items():
        missing = col_report["missing"]
        unique = col_report["unique"]
        col_type = col_report["type"]

        missing_pct = (missing / rows) if rows else 0.0
        lines.append(f"| {col_name} | {col_type} | {missing_pct:.1%} | {unique} |\n")

    lines.append("\n")

    #detail of column
    lines.append("## Column Details\n\n")
    for col_name, col_report in columns_dict.items():
        col_type = col_report["type"]
        lines.append(f"### {col_name}\n\n")
        lines.append(f"- Type: **{col_type}**\n")
        lines.append(f"- Missing: {col_report['missing']}\n")
        lines.append(f"- Unique: {col_report['unique']}\n")

        if col_type == "number":
            lines.append(f"- Min: {col_report.get('min')}\n")
            lines.append(f"- Max: {col_report.get('max')}\n")
            lines.append(f"- Mean: {col_report.get('mean')}\n")
        else:
            lines.append("\nTop values:\n\n")
            top = col_report.get("top", [])
            if not top:
                lines.append("- (none)\n")
            else:
                for item in top:
                    lines.append(f"- {item['value']}: {item['count']}\n")

        lines.append("\n")


    p.write_text("".join(lines), encoding="utf-8")




def render_markdown(report: dict) -> str:
    lines: list[str] = []
    lines.append("# CSV Profiling Report")
    lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
    lines.append("")
    # Summ
    lines.append("## Summary")
    lines.append(f"- Rows: **{report['n_rows']}**")
    lines.append(f"- Columns: **{report['n_cols']}**")
    lines.append("")
    lines.append("## Columns Overview")
    lines.append("")
    lines.append("| Column | Type | Missing % | Unique |")
    lines.append("|--------|------|-----------:|-------:|")

    for col in report["columns"]:
        name = col["name"]
        col_type = col["type"]
        missing_pct = col["missing_pct"]
        unique = col["unique"]

        lines.append(f"| {name} | {col_type} | {missing_pct:.1f}% | {unique} |")

    lines.append("")
    lines.append("## Column Details")
    lines.append("")

    for col in report["columns"]:
        name = col["name"]
        col_type = col["type"]

        lines.append(f"### {name}")
        lines.append("")
        lines.append(f"- Type: **{col_type}**")
        lines.append(f"- Missing: {col['missing']}")
        lines.append(f"- Unique: {col['unique']}")

        if col_type == "number":
            lines.append(f"- Min: {col.get('min')}")
            lines.append(f"- Max: {col.get('max')}")
            lines.append(f"- Mean: {col.get('mean')}")
        else:
            lines.append("")
            lines.append("Top values:")
            top = col.get("top", [])
            if not top:
                lines.append("- (none)")
            else:
                for item in top:
                    lines.append(f"- {item['value']}: {item['count']}")

        lines.append("")
    lines.append("## Notes")
    lines.append("- Missing values are: `''`, `na`, `n/a`, `null`, `none`, `nan` (case-insensitive)")
    lines.append("")

    return "\n".join(lines)

