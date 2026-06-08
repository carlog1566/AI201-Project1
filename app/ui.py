import gradio as gr
from rag import ask  # NOW this exists correctly

def handle_query(question):
    result = ask(question)

    sources = "\n".join([f"• {s}" for s in result["sources"]])

    return result["answer"], sources


with gr.Blocks() as demo:
    gr.Markdown("# 🍽️ CPP Dining RAG System")
    gr.Markdown("Ask questions about student dining experiences at Cal Poly Pomona.")

    inp = gr.Textbox(label="Your question")
    btn = gr.Button("Ask")

    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Sources", lines=4)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()