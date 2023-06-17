import os
from supabase.client import Client, create_client
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import SupabaseVectorStore
from langchain.document_loaders import TextLoader
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import (
    ConversationalRetrievalChain,
    LLMChain
)
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI


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
template = """Given the following chat history and a follow up question, rephrase the follow up input question to be a standalone question.
Or end the conversation if it seems like it's done.
Chat History:\"""
{chat_history}
\"""
Follow Up Input: \"""
{question}
\"""
Standalone question:"""
 
condense_question_prompt = PromptTemplate.from_template(template)
 
template = """You are a friendly, conversational retail shopping assistant. Use the following context including product names, descriptions, and keywords to show the shopper whats available, help find what they want, and answer any questions.
 
It's ok if you don't know the answer.
Context:\"""
 
{context}
\"""
Question:\"
\"""
 
Helpful Answer:"""
 
qa_prompt= PromptTemplate.from_template(template)

llm = OpenAI(temperature=0)

# use the LLM Chain to create a question creation chain
streaming_llm = OpenAI(
    streaming=True,
    verbose=True,
    max_tokens=150,
    temperature=0.2
)

question_generator = LLMChain(
    llm=llm,
    prompt=condense_question_prompt
)
 
# use the streaming LLM to create a question answering chain
doc_chain = load_qa_chain(
    llm=streaming_llm,
    chain_type="stuff",
    prompt=qa_prompt
)

chat_history = []
qa = ConversationalRetrievalChain(
        retriever=vector_store.as_retriever(),
        combine_docs_chain=doc_chain,
        question_generator=question_generator
        )

result = qa({"question": "How long does it take to deliver", "chat_history": chat_history})

print('Question: ', result['question'])
print('Answer: ', result['answer'])




