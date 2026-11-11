from langchain_ollama import OllamaLLM

from rag.vector_store import vector_db


llm = OllamaLLM(
    model="qwen3.8"
)


def ask_question(question):
    results = vector_db.max_marginal_relevance_search(
    question,
    k=4
    )

    for i, doc in enumerate(results):
            print(f"\n===== CHUNK {i} =====")
            print(doc.page_content[:1000])

    context = "\n\n".join(
        f"[Fragmento {i + 1}]\n{doc.page_content}"
        for i, doc in enumerate(results)
    )

    prompt = f"""
    Eres un asistente que analiza documentos.

    Responde de forma natural y profesional.

    NO menciones fragmentos, chunks, contexto interno
    ni cómo obtuviste la información.

    Si la información no está disponible,
    responde:

    "No encontré información suficiente en los documentos."

    Contexto:

    {context}

    Pregunta:

    {question}

    Respuesta:
    """

    response = llm.invoke(prompt).strip()

    print("RAW RESPONSE:")
    print(repr(response))

    if not response:

        return (
            "No encontré información suficiente "
            "en los documentos."
        )

    return response