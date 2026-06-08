import os
import sys

import gradio as gr
from dotenv import load_dotenv
from groq import Groq

# Allow importing the sibling retrieval module whether this script is run
# from the project root (python scripts/generate_and_interface.py) or from
# inside the scripts/ folder.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from embed_and_retrieve import retrieve, TOP_K

# --- Config ---
load_dotenv()
GROQ_MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """ 
    You are a helpful assistant for answering questions about Stanford dining halls 
    based on the retrieved context from the implemented RAG pipeline. 

    ONLY use the retrieved context when answering questions.
    Think thoroughly when you are given the received context and try to give the most accurate answer.
    If the user asks you a question which is not related to Stanford dining halls or information about them,
    say "Sorry, I can only answer questions related to Stanford dining halls."

    The output format should be: 
    [Your answer based on the retrieved context.]
    [Every citations you used in your answer listed in a bullet list format. 
    Each citation should include the source and url if it's available. 
    If there are no citations, write "No citations".]

    Adding citations is CRUCIAL for the user to verify the information. Always add citations.
    Your answer should be as accurate as possible. 
    Your answer should be clear, concise and easy to understand for the user to understand quickly even when they are in a rush. 

"""

_client = None
def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is not set. Add it to your .env file.")
        _client = Groq(api_key=api_key)
    return _client


# --- Build context from retrieved chunks ---
def format_context(hits):
    blocks = []
    for i, hit in enumerate(hits, 1):
        source = hit.get("source") or "unknown"
        url = hit.get("url") or ""
        header = f"[{i}] Source: {source}"
        if url:
            header += f" ({url})"
        blocks.append(f"{header}\n{hit['text']}")
    return "\n\n".join(blocks)


# --- Generation ---
def generate(query, top_k=TOP_K):
    hits = retrieve(query, top_k=top_k)
    context = format_context(hits)

    user_message = (
        f"Context:\n{context}\n\n"
        f"Question: {query}"
    )

    messages = []
    if SYSTEM_PROMPT.strip():
        messages.append({"role": "system", "content": SYSTEM_PROMPT})
    messages.append({"role": "user", "content": user_message})

    client = get_client()
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
    )
    return response.choices[0].message.content


# --- Interface ---
def answer(query):
    if not query or not query.strip():
        return "Please enter a question."
    return generate(query.strip())


def chat_fn(message, history):
    # gr.ChatInterface passes (message, history); each question is answered
    # fresh from the retrieved context, so history is not fed back to the model.
    return answer(message)


# Stanford cardinal-red theme (passed to .launch() in Gradio 6).
THEME = gr.themes.Soft(
    primary_hue="red",
    secondary_hue="rose",
    neutral_hue="slate",
)


def build_interface():
    return gr.ChatInterface(
        fn=chat_fn,
        chatbot=gr.Chatbot(height=480),
        textbox=gr.Textbox(
            placeholder="Ask about Stanford dining halls...",
            container=False,
            scale=7,
        ),
        title="🌲 The Unofficial Guide — Stanford Dining Halls",
        description="Ask about Stanford dining halls and get answers grounded in real student reviews.",
        examples=[
            "Which dining hall has the best vegan food?",
            "Which dining halls provide Suhoor during Ramadan?",
            "Can I take food out of the dining hall?",
        ],
    )


# --- Main ---
def main():
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        sample = "Which dining hall has the least wait time during lunch that also serves Indian food?"
        print(f"Q: {sample}\n")
        print(generate(sample))
        return
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        sample = "Which dining hall provide halal food around 8-10 pm?"
        print(f"Q: {sample}\n")
        print(generate(sample))
        return
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        sample = "Which dining hall provide food for Sahoor in Ramadan? "
        print(f"Q: {sample}\n")
        print(generate(sample))
        return

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        sample = "Which dining hall has the best vegetarian food?"
        print(f"Q: {sample}\n")
        print(generate(sample))
        return
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        sample = "Which dining hall allows take outs?"
        print(f"Q: {sample}\n")
        print(generate(sample))
        return

    build_interface().launch(theme=THEME)


if __name__ == "__main__":
    main()
