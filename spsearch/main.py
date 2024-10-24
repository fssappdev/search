import os
from fastapi import FastAPI, HTTPException, Depends
from dotenv import load_dotenv
from sqlalchemy.orm import Session # type: ignore
from database import get_db, init_db, SessionLocal
from repositories.magazine_repository import MagazineRepository
from models.search_request import SearchRequest, SearchType
from contextlib import asynccontextmanager
from sentence_transformers import SentenceTransformer
from fastapi.responses import JSONResponse
from typing import List


# Load environment variables from .env file
load_dotenv()






# Load the pre-trained model 
model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for the lifespan of the FastAPI application.
    Initializes the SentenceTransformer model and the database.
    """
    global model
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    init_db()  # Create the tables when the app starts
    db = SessionLocal()
    try:
        # Initialize the repository and update null vectors
        repo = MagazineRepository(db, model)
        repo.update_null_vectors()  # Update all entries with NULL vectors
    finally:
        db.close()
    yield
    # Add any cleanup code here if necessary

# Initialize the FastAPI app with the lifespan context manager
app = FastAPI(lifespan=lifespan)

@app.post("/search")
async def search_magazine(search: SearchRequest, db: Session = Depends(get_db)):
    """
    Search for magazines based on the search type and query string.

    - **Args:**
        - **search (SearchRequest)**: 
            - JSON body containing:
              - `query (str)`: The search query string.
              - `search_type (str)`: The type of search to perform. Possible values:
                - "vector" (vector-based search)
                - "keyword" (keyword-based search)
                - "hybrid" (combination of both)

    - **Returns:**
        - **SearchResponse**: A JSON object containing a list of magazine search results. Each result includes:
          - `magazine_info_id`: The ID of the magazine information.
          - `title`: The title of the magazine.
          - `author`: The author of the magazine.
          - `publication_date`: The publication date of the magazine.
          - `category`: The category of the magazine.
          - `magazine_content_id`: The ID of the magazine content.
          - `content`: The content of the magazine.

    - **Raises:**
        - **HTTPException** (404): No results found for the query.
        - **HTTPException** (500): Internal server error or issue during search.

    Example Request:
    ```
    {
      "query": "Artificial Intelligence",
      "search_type": "hybrid"
    }
    ```

    Example Response:
    ```
    {
      "results": [
        {
          "magazine_info_id": 50,
          "title": "Digital Voice Recorder",
          "author": "Ammamaria Lorenzo",
          "publication_date": "2024-04-12T05:41:55",
          "category": "Entertainment",
          "magazine_content_id": 71,
          "content": "Quae est enim contra Cyrenaicos..."
        }
      ]
    }
    ```
    """
    repo = MagazineRepository(db, model)

    # Keyword search
    if search.search_type == SearchType.keyword:
        results = repo.keyword_search(search.query)
        if not results:
            raise HTTPException(status_code=404, detail="No results found for the given keyword")
        return {"results": results}
    
    # Vector search
    elif search.search_type == SearchType.vector:
        # Convert query to vector representation using SentenceTransformer
        try:
            query_vector = repo.get_vector_representation(search.query)  # Use repo method for vector representation
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Error converting query to vector: {e}")
        try:
            results = repo.vector_search(query_vector)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Error performing vector search: {e}")
        if not results:
            raise HTTPException(status_code=404, detail="No results found for the given query vector")
        return {"results": results}
    
    # Hybrid search
    elif search.search_type == SearchType.hybrid:
        try:
            keyword = search.query
            query_vector = repo.get_vector_representation(keyword)  # Use repo method for vector representation
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid hybrid search format. Expected 'keyword|text'.")
        
        results = repo.hybrid_search(keyword, query_vector)
        if not results:
            raise HTTPException(status_code=404, detail="No results found for the hybrid search")
        return {"results": results}
    
    else:
        raise HTTPException(status_code=400, detail="Invalid search type")