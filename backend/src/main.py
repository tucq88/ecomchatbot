import os
from supabase.client import Client, create_client
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import SupabaseVectorStore
from langchain.document_loaders import TextLoader
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain


supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)


# -------- 1. load data, split into chunks and embed to database
loader = TextLoader("policy.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=400, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()

# save data to db
# vector_store = SupabaseVectorStore.from_documents(docs, embeddings, client=supabase)
vector_store = SupabaseVectorStore(client=supabase, embedding=embeddings, table_name="documents")

# -------- 2. Similarity search based on query
# query = "How long does it takes to deliver?"
# matched_docs = vector_store.similarity_search(query)

# # print(matched_docs[0].page_content)

# # query
# query = "I want to return my product"
# matched_docs = vector_store.similarity_search(query)

# print(matched_docs[0].page_content)

# -------- 3. Chatbot
qa = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0), vector_store.as_retriever())
result = qa({"question": "How long does it take to deliver", "chat_history": []})

print('Question: ', result['question'])
print('Answer: ', result['answer'])


