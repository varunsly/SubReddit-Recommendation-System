# SubReddit-Recommention-System

# Reddit Recommendation System

This project is a Reddit-based recommendation system that scrapes subreddit data, processes it, and stores it in both Elasticsearch and a vector database (using FAISS) for querying. The system is designed to recommend subreddits or posts based on semantic similarity (using embeddings) and text-based relevance.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [How to Run the Code](#how-to-run-the-code)
- [File Descriptions](#file-descriptions)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Reddit Recommendation System scrapes data from Reddit using the Reddit API and processes it to build a recommendation engine. The system stores the scraped data in Elasticsearch for efficient keyword-based querying and in FAISS for semantic similarity searches based on subreddit embeddings. This hybrid search mechanism allows for more precise and relevant subreddit recommendations based on user queries.

## Features

- Scrapes top communities and subreddits from Reddit.
- Fetches detailed subreddit information using Reddit's API.
- Processes and cleans subreddit data for recommendation.
- Stores data in an Elasticsearch index for efficient text-based searches.
- Builds and queries a FAISS-based vector database for semantic similarity searches.
- Combines results from FAISS and Elasticsearch to provide hybrid recommendations.
- Supports querying the recommendation system based on user inputs or specific subreddit characteristics.
- Integration with LangChain and Groq for natural language-based responses using retrieved subreddits as context.

## Technologies Used

- **Python**: Core programming language.
- **Reddit API**: To fetch subreddit data.
- **FAISS**: For creating and querying a vector database of subreddit embeddings.
- **Sentence-Transformers**: For generating subreddit embeddings.
- **Elasticsearch**: To store and search scraped data using text-based queries.
- **Pandas**: For data cleaning and preprocessing.
- **SQLite**: For intermediate data storage.
- **LangChain**: For language-based interactions using subreddit contexts.
- **BeautifulSoup**: For web scraping top subreddits.
- **requests**: For API requests.

## Installation

### Prerequisites

Make sure you have the following installed on your machine:

1. **Python 3.x**
2. **Elasticsearch** (for text-based search)
3. **FAISS** (for vector similarity search)
4. **Reddit API credentials** (client ID, client secret, user agent)

### Steps

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/reddit-recommendation-system.git
   cd reddit-recommendation-system
