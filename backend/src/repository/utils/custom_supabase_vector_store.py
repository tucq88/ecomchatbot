from __future__ import annotations

from typing import (
    Any,
    List,
    Optional,
    Tuple,
    Dict
)

import numpy as np

from langchain.docstore.document import Document
from langchain.vectorstores import SupabaseVectorStore

class CustomSupabaseVectorStore(SupabaseVectorStore):
    def similarity_search(
        self, query: str, k: int = 4, filter: Optional[Dict[str, str]] = None, **kwargs: Any
    ) -> List[Document]:
        vectors = self._embedding.embed_documents([query])
        return self.similarity_search_by_vector(vectors[0], k, filter=filter)

    def similarity_search_by_vector(
        self, embedding: List[float], k: int = 4, filter: Optional[Dict[str, str]] = None, **kwargs: Any
    ) -> List[Document]:
        result = self.similarity_search_by_vector_with_relevance_scores(embedding, k, filter=filter)
        documents = [doc for doc, _ in result]
        return documents

    def similarity_search_with_relevance_scores(
        self, query: str, k: int = 4, filter: Optional[Dict[str, str]] = None, **kwargs: Any
    ) -> List[Tuple[Document, float]]:
        vectors = self._embedding.embed_documents([query])
        return self.similarity_search_by_vector_with_relevance_scores(vectors[0], k, filter=filter)

    def similarity_search_by_vector_with_relevance_scores(
        self, query: List[float], k: int, filter: Optional[Dict[str, str]] = None
    ) -> List[Tuple[Document, float]]:
        match_documents_params = dict(query_embedding=query, match_count=k, filter=filter)
        res = self._client.rpc(self.query_name, match_documents_params).execute()
        match_result = [
            (
                Document(
                    metadata=search.get("metadata", {}),  # type: ignore
                    page_content=search.get("content", ""),
                ),
                search.get("similarity", 0.0),
            )
            for search in res.data
        ]
        return match_result

    def similarity_search_by_vector_returning_embeddings(
        self, query: List[float], k: int, filter: Optional[Dict[str, str]] = None
    ) -> List[Tuple[Document, float, np.ndarray[np.float32, Any]]]:
        match_documents_params = dict(query_embedding=query, match_count=k, filter=filter)
        res = self._client.rpc(self.query_name, match_documents_params).execute()
        match_result = [
            (
                Document(
                    metadata=search.get("metadata", {}),  # type: ignore
                    page_content=search.get("content", ""),
                ),
                search.get("similarity", 0.0),
                # Supabase returns a vector type as its string representation (!).
                # This is a hack to convert the string to numpy array.
                np.fromstring(
                    search.get("embedding", "").strip("[]"), np.float32, sep=","
                ),
            )
            for search in res.data
        ]
        return match_result
