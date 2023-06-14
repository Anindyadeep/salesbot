# from langchain.chains import LLMChain
# from langchain.prompts import ChatPromptTemplate

# # custom LLM module call 
# from src.customLLM import RapidAPILLM

# llm = RapidAPILLM()

# prompt = ChatPromptTemplate.from_template(
#     "What is the best name to describe \
#     a company that makes {product}?"
# )

# chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
# product = "Queen Size Sheet Set"

# print(chain.run(product))

import os 
from langchain.docstore.document import Document 
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from src.customLLM import RapidAPILLM


path = "/home/anindya/projects/SalesBot/storage/documents"
file_paths  = [os.path.join(path, file) for file in os.listdir(path)]

documents = [] 

for file_path in file_paths:
    with open(file_path, "r") as f:
        text = f.read()
    
    words = text.split() 
    current_chunk = ""

    for word in words:
        if len(current_chunk) + len(word) < 100000:
            current_chunk += " " + word 
        else:
            chunked_text = current_chunk.strip()
            documents.append(Document(page_content=chunked_text, metadata={"source": file_path}))
            current_chunk = ""


chain = load_qa_with_sources_chain(RapidAPILLM())
print(chain(
    {
        "input_documents" : documents,
        "question" : "What are the competitors of Corridor Platforms?"
    }, 
    return_only_outputs=True)['output_text']
)