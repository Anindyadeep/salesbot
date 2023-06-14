from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import SentenceTransformerEmbeddings 
from langchain.vectorstores import Chroma
from src.customLLM import RapidAPILLM
from langchain.docstore.document import Document


loader = TextLoader(file_path="/home/anindya/projects/SalesBot/storage/documents/home.txt")
documents = loader.load()

text_splitter = CharacterTextSplitter(
    chunk_size=1000, chunk_overlap=0
)
texts = text_splitter.split_documents(documents)

embeddings = SentenceTransformerEmbeddings()

print("ok")
db = Chroma.from_documents(texts, embeddings)

retriever = db.as_retriever(
    search_type = "similarity", search_kwargs = {"k": 1}
)

qa = ConversationalRetrievalChain.from_llm(
    llm = RapidAPILLM(), retriever = retriever
)


history = []
while True:
    query = input("Enter your query : ")
    if query == "exit":
        break
    result = qa(
        {'question' : query, 'chat_history' : history}
    )
    print(result)
