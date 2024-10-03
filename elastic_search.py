# -*- coding: utf-8 -*-
"""Elastic_Search.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kO27pZkd3YapgdHQ65HsLeKLvcudFOzf
"""

import sqlite3
import pandas as pd
import numpy as np
import pickle
from elasticsearch import Elasticsearch, helpers
import torch
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import pandas as pd
from elasticsearch import Elasticsearch, helpers

# docker pull docker.elastic.co/elasticsearch/elasticsearch:8.10.0
# docker run -d --name elasticsearch -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:8.10.0
# docker run --rm -p 9200:9200 -p 9300:9300 -e "xpack.security.enabled=false" -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:8.7.0

### Step 1: Database Connection and Data Loading ###

def connect_to_db(db_name):
    try:
        conn = sqlite3.connect(db_name)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def load_subreddit_data(conn):
    try:
        query = """
        SELECT id, name, description, subscribers, category, created_utc, rich_text
        FROM subreddits
        WHERE description IS NOT NULL AND description != ''
        """
        subreddits_df = pd.read_sql_query(query, conn)
        return subreddits_df
    except Exception as e:
        print(f"Error loading subreddit data: {e}")
        return None

conn = connect_to_db('reddit_data_new_updated.db')
subreddits_df = load_subreddit_data(conn)

# Initialize the Elasticsearch client
# from elasticsearch import Elasticsearch
es = Elasticsearch(['http://localhost:9200'])

es.info().body

"""## Setting Up Elasticsearch Connection and Index"""

def create_subreddit_index():
    mapping = {
        "mappings": {
            "properties": {
                "name": {"type": "text"},
                "description": {"type": "text"},
                "subscribers": {"type": "integer"},
                "category": {"type": "keyword"},
                "created_utc": {"type": "date"},
                "rich_text": {"type": "text"}
            }
        }
    }


    # Create the index if it doesn't exist
    if not es.indices.exists(index="subreddits"):
        es.indices.create(index="subreddits", body=mapping)
        print("Subreddit index created.")
    else:
        print("Subreddit index already exists.")

create_subreddit_index()

"""## Converting DataFrame rows to Elasticsearch actions"""

def df_to_elasticsearch_actions(df, index_name):
    """
    Convert a DataFrame to a list of actions for Elasticsearch bulk indexing.
    Each row in the DataFrame is converted to a JSON document.
    """
    actions = []

    for _, row in df.iterrows():
        action = {
            "_index": index_name,
            "_id": row['id'],  # Use the 'id' as the document _id
            "_source": {
                "name": row['name'],
                "description": row['description'],
                "subscribers": row['subscribers'],
                "category": row['category'],
                "created_utc": row['created_utc'],
                "rich_text": row['rich_text']  # Include the rich_text field in the source
            }
        }
        actions.append(action)

    return actions

"""## Indexing Data into Elasticsearch"""

def bulk_index_to_elasticsearch(df, index_name):
    """
    Bulk index the DataFrame data into Elasticsearch.
    :param df: DataFrame containing the subreddit data
    :param index_name: The name of the Elasticsearch index to push the data to
    """
    actions = df_to_elasticsearch_actions(df, index_name)

    try:
        # Bulk index the actions into Elasticsearch
        helpers.bulk(es, actions)
        print(f"Successfully indexed {len(actions)} documents into Elasticsearch.")
    except Exception as e:
        print(f"Error indexing data into Elasticsearch: {e}")

# Index the subreddit data into Elasticsearch
bulk_index_to_elasticsearch(subreddits_df, 'subreddits')

"""## Performing Full-Text Search in Elasticsearch"""

def search_subreddits_elasticsearch(user_query, top_k=5):
    """
    Search subreddits in Elasticsearch based on the user's query.
    :param user_query: The query string provided by the user.
    :param top_k: Number of top results to return.
    :return: A list of relevant subreddits from Elasticsearch.
    """
    es_query = {
        "query": {
            "multi_match": {
                "query": user_query,
                "fields": ["name^3", "description^2", "rich_text"],  # Boost 'name' and 'description'
                "fuzziness": "AUTO"
            }
        },
        "size": top_k
    }

    # Perform the search
    response = es.search(index="subreddits", body=es_query)

    # Parse the response to get the relevant subreddits
    retrieved_subreddits = []
    for hit in response['hits']['hits']:
        subreddit_data = hit["_source"]
        retrieved_subreddits.append(subreddit_data)

    return retrieved_subreddits

# Example usage
user_query = "communities to discuss machine learning"
retrieved_subreddits = search_subreddits_elasticsearch(user_query, top_k=5)

# Output the search results
for subreddit in retrieved_subreddits:
    print(f"Subreddit: {subreddit['name']}\nDescription: {subreddit['description']}\nSubscribers: {subreddit.get('subscribers', 'N/A')}\n")