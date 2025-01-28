import asyncio
from data_fetcher import fetch_all_data
from delta_manager import DeltaManager
from analysis import analyze_data

async def main():
    # Fetch and validate data
    users, posts = await fetch_all_data()
    
    # Initialize Delta manager
    delta_manager = DeltaManager()
    
    # Save data to Delta tables
    delta_manager.save_to_delta(users, "users")
    delta_manager.save_to_delta(posts, "posts")
    
    # Run analysis
    posts_per_user, longest_post, avg_post_length = analyze_data(delta_manager)
    
    # Print results
    print("\nPosts per user:")
    print(posts_per_user)
    
    print("\nUser with longest post:")
    print(longest_post)
    
    print("\nAverage post length per user:")
    print(avg_post_length)

if __name__ == "__main__":
    asyncio.run(main())