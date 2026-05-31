from __future__ import annotations
import pandas as pd


def add_metadata(df: pd.DataFrame, source_id: str, geographic_level: str,
                 location: str | None = None) -> pd.DataFrame:
    df = df.copy()
    df["source_id"] = source_id
    df["geographic_level"] = geographic_level
    if location:
        df["location"] = location
    return df


def to_long(df: pd.DataFrame, value_vars: list[str], id_vars: list[str],
            var_name: str = "indicator", value_name: str = "value") -> pd.DataFrame:
    return df.melt(id_vars=id_vars, value_vars=value_vars,
                   var_name=var_name, value_name=value_name)


def pct_str_to_float(series: pd.Series) -> pd.Series:
    """Convert German locale percentage strings ('12,3 %') to float 12.3."""
    return (series.astype(str)
            .str.replace(",", ".", regex=False)
            .str.replace(r"[^\d.]", "", regex=True)
            .pipe(pd.to_numeric, errors="coerce"))
