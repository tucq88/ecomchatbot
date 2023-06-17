from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.chains.question_answering import load_qa_chain

class Chatbot:
    def __init__(self, vector_store, chatbot_id):
        self.vector_store = vector_store
        self.question_generator = self._create_question_generator()
        self.chatbot_id = chatbot_id

    def _create_question_generator(self):
        template = """Given the following chat history and a follow up question, rephrase the follow up input question to be a standalone question.
        Or end the conversation if it seems like it's done.
        Chat History:\"""
        {chat_history}
        \"""
        Follow Up Input: \"""
        {question}
        \"""
        Standalone question:"""

        prompt = PromptTemplate.from_template(template)

        llm = OpenAI(verbose=True, model_name='gpt-3.5-turbo-16k', temperature=0)

        return LLMChain(
            llm=llm,
            prompt=prompt
        )
    
    def generate_question(self, question, chat_history):
        template = """You are a friendly, conversational retail shopping assistant. Use the following context including product names, descriptions, and keywords to show the shopper what's available, help find what they want, and answer any questions.

        It's ok if you don't know the answer.
        Context:\"""

        {context}
        \"""
        Question:\"
        \"""

        Helpful Answer:"""

        prompt = PromptTemplate.from_template(template)

        qa_chain = load_qa_chain(
            llm=self._create_streaming_llm(),
            chain_type="stuff",
            prompt=prompt
        )

        retriever = self.vector_store.as_retriever(verbose=True, search_kwargs={'filter': {'chatbot_id': self.chatbot_id}})

        qa = ConversationalRetrievalChain(
            retriever=retriever,
            combine_docs_chain=qa_chain,
            question_generator=self.question_generator,
            verbose=True
        )

        result = qa({"question": question, "chat_history": chat_history})
        return result['question'], result['answer']
    
    def _create_streaming_llm(self):
        return OpenAI(
            verbose=True,
            model_name='gpt-3.5-turbo-16k',
            max_tokens=150,
            temperature=0,
        )
