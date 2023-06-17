import click
from langchain.embeddings.openai import OpenAIEmbeddings
from repository.document_repository import DocumentRepository
from loader.loader import DataLoader
from services.chatbot import Chatbot

@click.group()
def cli():
    pass

@cli.command()
@click.argument('urls', nargs=-1)
@click.option('--chatbot-id', required=True)
def load_data(chatbot_id, urls):
    document_repository = DocumentRepository(embeddings=OpenAIEmbeddings())
    loader = DataLoader()
    documents = loader.load_urls(urls)
    vector_store = document_repository.save_documents(documents, chatbot_id=chatbot_id)
    click.echo("Data loaded successfully!")

@cli.command()
@click.argument('question')
@click.option('--chat-history', multiple=True)
@click.option('--chatbot-id', required=True)
def answer_question(chatbot_id, question, chat_history):
    document_repository = DocumentRepository(embeddings=OpenAIEmbeddings())
    vector_store = document_repository.get_vector_store()
    chatbot = Chatbot(vector_store, chatbot_id)
    standalone_question, answer = chatbot.generate_question(question, list(chat_history))
    click.echo(f"Question: {standalone_question}")
    click.echo(f"Answer: {answer}")

if __name__ == "__main__":
    cli()
