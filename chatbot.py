from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

model = OllamaLLM(model="llama3.1")

template = """
Answer the question below.

Here is the conversation history: {context}

Question: {question}

Answer:
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the conversation.")
        break
    result = chain.invoke({"context": context, "question": user_input})
    print("Bot: ", result)
    context += f"\nUser: {user_input}\nAI: {result}"
