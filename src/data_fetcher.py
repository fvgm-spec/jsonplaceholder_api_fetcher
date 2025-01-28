import httpx
import asyncio
from models import User, Post

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
    
    # Validate data using Pydantic models
    users = [User(**user) for user in users_data]
    posts = [Post(**post) for post in posts_data]
    
    return users, posts