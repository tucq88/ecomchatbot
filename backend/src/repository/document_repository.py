import os
from supabase.client import Client, create_client
from langchain.vectorstores import SupabaseVectorStore
from .utils.custom_supabase_vector_store import CustomSupabaseVectorStore

class DocumentRepository:
    def __init__(self, embeddings):
        supabase_url = os.environ.get("SUPABASE_URL") or ""
        supabase_key = os.environ.get("SUPABASE_SERVICE_KEY") or ""
        self.client: Client = create_client(supabase_url, supabase_key)
        self.embeddings = embeddings
    
    def get_vector_store(self):
        vector_store = CustomSupabaseVectorStore(client=self.client, embedding=self.embeddings, table_name="documents")
        return vector_store

    def save_documents(self, documents, chatbot_id):
        # Add chatbot_id to metadata
        for document in documents:
            document.metadata["chatbot_id"] = chatbot_id

        vector_store = CustomSupabaseVectorStore.from_documents(documents, self.embeddings, client=self.client)
        return vector_store

    def search_documents(self, query):
        vector_store = self.get_vector_store()
        matched_docs = vector_store.similarity_search(query)
        return matched_docs
