from rag.vector_store import vector_db

print(vector_db._collection.count())

from langchain_ollama import OllamaLLM

llm = OllamaLLM(
    model="qwen3.5"
)

response = llm.invoke(
    "Responde solamente OK"
)

print(response)