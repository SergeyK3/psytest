from pathlib import Path
import pandas as pd

def load_items(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)
