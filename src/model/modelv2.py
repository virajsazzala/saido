import sys
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import HuggingFaceHub
import json

def initialize_qa_chain(data):
    repo_id = "mistralai/Mistral-7B-v0.1"
    llm = HuggingFaceHub(huggingfacehub_api_token='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', repo_id=repo_id, model_kwargs={"temperature": 0.4, "max_new_tokens": 100})
    embeddings = HuggingFaceEmbeddings()
    texts = [entry["transcript"] for entry in data]  # Extract the transcript data
    texts = [text.replace("\n", " ") for text in texts]  # Replace newlines with spaces
    db = Chroma.from_texts(texts, embeddings)
    retriever = db.as_retriever(search_kwargs={'k': 2})
    return ConversationalRetrievalChain.from_llm(llm, retriever, return_source_documents=True)

def ask_question(qa_chain, query):
    result = qa_chain({'question': query, 'chat_history': []})  # Provide an empty list as chat history

    answer = result['answer'].split('\n\n Question: ')[0].strip()

    # indexH = answer.find("\n\nHelpful Answer:")
    # answer = answer[:indexH].strip()

    indexQ = answer.find('\n\nQuestion: ')
    if indexQ != -1:
        answer = answer[:indexQ].strip()

    indexU = answer.find('\n\nUser 1: ')
    if indexU != -1:
        answer = answer[:indexU].strip()

    indexH = answer.find('\n\n## ')
    if indexH != -1:
        answer = answer[:indexH].strip()

    return answer

if __name__ == "__main__":
    with open('C:\\Users\\Dhyuti Tewani\\OneDrive\\Documents\\Code\\projects\\ml\\saido\\src\\model\\transcriptions.json', 'r') as json_file:
        data = json.load(json_file)

    qa_chain = initialize_qa_chain(data)

    while True:
        query = input('\n Prompt: ')
        if query.lower() in ["exit", "quit", "q"]:
            print('Exiting')
            sys.exit()
        answer = ask_question(qa_chain, query)
        print('\n Answer: ' + answer + '\n')
