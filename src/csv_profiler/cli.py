from __future__ import annotations
import json
import time
from pathlib import Path
import typer
from csv_profiler.io import read_csv_rows
from csv_profiler.profiling import profile_rows
from csv_profiler.render import render_markdown

app = typer.Typer()

@app.command(help="Profile a CSV file and write JSON + Markdown")
def profile(
    input_path: Path = typer.Argument(..., help="Input CSV file"),
    out_dir: Path = typer.Option(Path("outputs"), "--out-dir", help="Output folder"),
    report_name: str = typer.Option("report", "--report-name", help="Base name for outputs"),
    preview: bool = typer.Option(False, "--preview", help="Print a short summary"),
) -> None:
    try:
        start = time.perf_counter()
        if not input_path.exists():
            raise typer.BadParameter(f"Input file does not exist: {input_path}")

        rows = read_csv_rows(input_path)

        #new profile
        report = profile_rows(rows)
        elapsed_ms = (time.perf_counter() - start) * 1000
        report["timing_ms"] = round(elapsed_ms, 2)
        #new md function
        md_text = render_markdown(report)
        out_dir.mkdir(parents=True, exist_ok=True)
        json_path = out_dir / f"{report_name}.json"
        md_path = out_dir / f"{report_name}.md"
        json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        md_path.write_text(md_text, encoding="utf-8")

        # elapsed_ms = (time.perf_counter() - start) * 1000
        typer.secho(f"Wrote: {json_path}", fg=typer.colors.GREEN)
        typer.secho(f"Wrote: {md_path}", fg=typer.colors.GREEN)
        # typer.echo(f"Elapsed: {elapsed_ms:.2f}ms")

        if preview:
            typer.echo("")
            typer.echo("Preview:")
            typer.echo(f"- Rows: {report['n_rows']}")
            typer.echo(f"- Columns: {report['n_cols']}")

    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
