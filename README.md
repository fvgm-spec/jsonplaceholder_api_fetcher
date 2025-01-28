## Fetching data from the JSONPlaceholder API

The code contained in this repository fetches data from the JSONPlaceholder API, formats it using Pydantic models, and then stores it as a Delta table.

Once data is stored locally, it is queried using Polars.

### Installation

Clone the repository
```bash
git clone https://github.com/fvgm-spec/jsonplaceholder_api_fetcher.git
```

Install dependencies
```bash
pip3 install -r requirements.txt
```

### Step 1

Fetch data from the /posts and /users endpoints

```python
## data_fetcher.py

async def fetch_data(endpoint: str) -> dict:
    base_url = "https://jsonplaceholder.typicode.com"
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/{endpoint}")
        response.raise_for_status()
        return response.json()

async def fetch_all_data():
    tasks = [
        fetch_data("users"),
        fetch_data("posts")
    ]
    users_data, posts_data = await asyncio.gather(*tasks)
```

### Step 2

Data vlidation using Pydantic models

```python
## models.py

from pydantic import BaseModel, Field
from typing import List

class User(BaseModel):
    id: int
    name: str
    username: str
    email: str
    
class Post(BaseModel):
    id: int
    userId: int
    title: str
    body: str
```

### Step 3

Storing the validated data in Delta tables

In order to save the fetched data into local storage is used the `delta_manager.py` file in the *src* directory

```python
## delta_manager.py

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
```

<p>
<div class="column">
    <img src="./img/execution.png" style="height: 12rem"/>
  </div>
</p>

Once in the directory *src* in your terminal, execute the `main.py` module

```bash
 python3 main.py
 ```

After the data is stored locally, by running the main module all the analysis will be performed and data will be validated using the defined models.

<p>
<div class="column">
    <img src="./img/directory.png" style="height: 12rem"/>
  </div>
</p>


