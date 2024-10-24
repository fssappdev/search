from sqlalchemy.orm import Session
from models.magazine_information import MagazineInformation
from models.magazine_content import MagazineContent
from sqlalchemy import or_, select

class MagazineRepository:
    def __init__(self, db: Session, model):
        self.db = db
        self.model = model

    def get_vector_representation(self, text: str):
        """Generate vector representation from text."""
        # Generate the vector from the text
        vector = self.model.encode(text)
        return vector.tolist()

    def keyword_search(self, keyword: str):
        """
        Perform a keyword-based search on the magazine's title, author, and content.
        """
        if not keyword:
            raise ValueError("Keyword must not be empty or None")

        stmt = (
            select(
                MagazineInformation.id.label("magazine_info_id"),
                MagazineInformation.title,
                MagazineInformation.author,
                MagazineInformation.publication_date,
                MagazineInformation.category,
                MagazineContent.id.label("magazine_content_id"),
                MagazineContent.content,
            )
            .join(MagazineContent, MagazineInformation.id == MagazineContent.magazine_id)
            .filter(
                or_(
                    MagazineInformation.title.ilike(f"%{keyword}%"),
                    MagazineInformation.author.ilike(f"%{keyword}%"),
                    MagazineContent.content.ilike(f"%{keyword}%")
                )
            )
        )
        results = self.db.execute(stmt).all()

        return [
            {
                "magazine_info_id": row.magazine_info_id,
                "title": row.title,
                "author": row.author,
                "publication_date": row.publication_date,
                "category": row.category,
                "magazine_content_id": row.magazine_content_id,
                "content": row.content,
            }
            for row in results
        ]

    def vector_search(self, query_vector: list):
        """
        Perform a vector-based search using pg_vector on the magazine content's vector representation.
        """
        # Debugging: Check the query vector length and contents
        print(f"Vector search initiated with query vector: {query_vector}")
        print(f"Vector length: {len(query_vector)}")

        # Ensure the query vector is a list of floats
        if not isinstance(query_vector, list) or not all(isinstance(x, float) for x in query_vector):
            raise ValueError("query_vector must be a list of floats")

        # Build the SQL query
        stmt = (
            select(
                MagazineInformation.id.label("magazine_info_id"),
                MagazineInformation.title,
                MagazineInformation.author,
                MagazineInformation.publication_date,
                MagazineInformation.category,
                MagazineContent.id.label("magazine_content_id"),
                MagazineContent.content,
            )
            .join(MagazineContent, MagazineInformation.id == MagazineContent.magazine_id)
            .order_by(MagazineContent.vector_representation.op('<->')(query_vector))  # Use the <-> operator for distance
            .limit(5)  # Limit to the top 5 results
        )
        results = self.db.execute(stmt).all()

        # Return results as a list of dictionaries
        return [
            {
                "magazine_info_id": row.magazine_info_id,
                "title": row.title,
                "author": row.author,
                "publication_date": row.publication_date,
                "category": row.category,
                "magazine_content_id": row.magazine_content_id,
                "content": row.content,
            }
            for row in results
        ]

    def hybrid_search(self, keyword: str, query_vector: list):
        """
        Perform a hybrid search that combines keyword search and vector similarity.
        """
        if not keyword:
            raise ValueError("Keyword must not be empty or None")
        
        if not isinstance(query_vector, list) or not all(isinstance(x, float) for x in query_vector):
            raise ValueError("query_vector must be a list of floats")

        keyword_results = self.keyword_search(keyword)
        vector_results = self.vector_search(query_vector)

        # Combine both results if needed, for now return both separately.
        return {
            "keyword_results": keyword_results,
            "vector_results": vector_results
        }
    
    def update_null_vectors(self):
        """
        Update rows in the database where vector_representation is NULL.
        """
        null_vectors = self.db.query(MagazineContent).filter(MagazineContent.vector_representation.is_(None)).all()

        if null_vectors:
            print(f"Found {len(null_vectors)} records with NULL vectors. Generating embeddings...")

            for content_record in null_vectors:
                # Generate vector for the content using the preloaded model
                vector = self.get_vector_representation(content_record.content)
                content_record.vector_representation = vector  # Update the record with the generated vector

            self.db.commit()  # Commit all changes to the database
            print(f"Updated {len(null_vectors)} records with generated vectors.")
