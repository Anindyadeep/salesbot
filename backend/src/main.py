from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.embeddings import SentenceTransformerEmbeddings 

from src.customLLM import RapidAPILLM
from src.injest_data import DataInjestion
from src.prompt_storage import PromptStorage

prompt_template = str(PromptStorage.sales_prompt)
sales_prompt = PromptTemplate(template=prompt_template, input_variables=['summaries'])

# load the data injestion pipeline

data_pipeline = DataInjestion()
embeddings = SentenceTransformerEmbeddings()

documents = data_pipeline.load_docs()
documents_splitted = data_pipeline.split_docs(documents, chunk_size=100, chunk_overlap=0)
docsearch = Chroma.from_documents(
    documents, embeddings,
    metadatas=[{"source": str(i)} for i in range(len(documents))]
)

# Load the QA chain

chain = load_qa_chain(
    llm = RapidAPILLM(), 
    chain_type="stuff",verbose=True
)

def get_answer(query):
    similar_docs = docsearch.similarity_search(query, k=1)
    answer =  chain.run(input_documents = similar_docs, question = query)
    return answer

while True:
    query = input("Enter your query : ")
    if query == "exit":
        break
    
    print(get_answer(query))



