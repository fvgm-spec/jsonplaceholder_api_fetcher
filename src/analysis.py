import polars as pl
from delta_manager import DeltaManager

def analyze_data(delta_manager: DeltaManager):
    posts_df = delta_manager.read_delta("posts")
    users_df = delta_manager.read_delta("users")
    
    ## Number of posts per user
    posts_per_user = (
        posts_df.lazy()
        .groupby("userId")
        .agg(pl.count("id").alias("post_count"))
        .join(
            users_df.lazy().select(["id", "name"]),
            left_on="userId",
            right_on="id"
        )
        .select(["name", "post_count"])
        .collect()
    )
    
    ## User with longest post
    longest_post = (
        posts_df.lazy()
        .with_columns(pl.col("body").str.lengths().alias("body_length"))
        .join(
            users_df.lazy().select(["id", "name"]),
            left_on="userId",
            right_on="id"
        )
        .select(["name", "title", "body_length"])
        .sort("body_length", descending=True)
        .limit(1)
        .collect()
    )
    
    ## Average post length per user
    avg_post_length = (
        posts_df.lazy()
        .with_columns(pl.col("body").str.lengths().alias("body_length"))
        .groupby("userId")
        .agg(
            pl.mean("body_length").alias("avg_post_length")
        )
        .join(
            users_df.lazy().select(["id", "name"]),
            left_on="userId",
            right_on="id"
        )
        .select(["name", "avg_post_length"])
        .sort("avg_post_length", descending=True)
        .collect()
    )
    
    return posts_per_user, longest_post, avg_post_length