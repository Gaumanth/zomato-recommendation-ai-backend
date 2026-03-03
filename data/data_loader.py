import os
import pandas as pd
from datasets import load_dataset

CACHE_PATH = os.path.join(os.path.dirname(__file__), "processed", "zomato_clean.csv")

_dataframe_cache: pd.DataFrame | None = None


def load_raw_dataset() -> pd.DataFrame:
    """Download the Zomato dataset from Hugging Face and return as a DataFrame."""
    ds = load_dataset("ManikaSaini/zomato-restaurant-recommendation", split="train")
    return ds.to_pandas()


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and normalize the raw Zomato DataFrame."""
    df = df.copy()

    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    rename_map = {}
    for col in df.columns:
        if "cuisines" in col or col == "cuisine":
            rename_map[col] = "cuisines"
        elif col in ("rate", "rating", "aggregate_rating"):
            rename_map[col] = "rating"
        elif col in ("average_cost_for_two", "cost", "approx_cost(for_two_people)", "approx_cost_for_two_people"):
            rename_map[col] = "cost_for_two"
        elif col in ("city", "location", "locality"):
            if "city" not in rename_map.values():
                rename_map[col] = "city"
        elif col in ("name", "restaurant_name"):
            rename_map[col] = "name"
    df = df.rename(columns=rename_map)

    required_cols = ["name", "cuisines", "rating", "cost_for_two", "city"]
    for col in required_cols:
        if col not in df.columns:
            df[col] = None

    df["name"] = df["name"].astype(str).str.strip()
    df["cuisines"] = df["cuisines"].astype(str).str.strip()
    df["city"] = df["city"].astype(str).str.strip().str.title()

    df["rating"] = pd.to_numeric(df["rating"].astype(str).str.extract(r"([\d.]+)")[0], errors="coerce")
    df["cost_for_two"] = pd.to_numeric(
        df["cost_for_two"].astype(str).str.replace(",", "").str.extract(r"([\d.]+)")[0],
        errors="coerce",
    )

    df = df.dropna(subset=["name", "rating", "cost_for_two"])
    df = df[df["name"].str.lower() != "nan"]

    df = df.reset_index(drop=True)
    return df


def get_dataframe(force_reload: bool = False) -> pd.DataFrame:
    """Return the cleaned dataset, using cache when available."""
    global _dataframe_cache

    if _dataframe_cache is not None and not force_reload:
        return _dataframe_cache

    if os.path.exists(CACHE_PATH) and not force_reload:
        _dataframe_cache = pd.read_csv(CACHE_PATH)
        return _dataframe_cache

    raw = load_raw_dataset()
    cleaned = clean_dataset(raw)

    os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
    cleaned.to_csv(CACHE_PATH, index=False)

    _dataframe_cache = cleaned
    return _dataframe_cache


def get_unique_cities(df: pd.DataFrame | None = None) -> list[str]:
    if df is None:
        df = get_dataframe()
    cities = df["city"].dropna().unique().tolist()
    return sorted([c for c in cities if c.lower() != "nan"])


def get_unique_cuisines(df: pd.DataFrame | None = None) -> list[str]:
    if df is None:
        df = get_dataframe()
    all_cuisines: set[str] = set()
    for val in df["cuisines"].dropna():
        for c in str(val).split(","):
            c = c.strip()
            if c and c.lower() != "nan":
                all_cuisines.add(c)
    return sorted(all_cuisines)
