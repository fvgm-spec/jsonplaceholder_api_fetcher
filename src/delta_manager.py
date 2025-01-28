import polars as pl
from pathlib import Path

class DeltaManager:
    def __init__(self, base_path: str = "./delta_tables"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
    
    def save_to_delta(self, data: list, table_name: str):
        df = pl.DataFrame([d.dict() for d in data])
        table_path = self.base_path / table_name
        
        df.write_delta(str(table_path))
    
    def read_delta(self, table_name: str) -> pl.DataFrame:
        table_path = self.base_path / table_name
        return pl.read_delta(str(table_path))