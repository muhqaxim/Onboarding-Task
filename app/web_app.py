import gradio as gr
from scr.pipeline import pipeline

def gradio_pipeline(url, file):
    try:
        if url:
            story, podcast = pipeline(url)
        elif file:
            story, podcast = pipeline(file.name)
        else:
            return "Please provide a YouTube link or upload a video.", None
        return story, podcast
    except Exception as e:
        return f"Error: {str(e)}", None

def launch_app():
    with gr.Blocks() as demo:
        gr.Markdown("## Video → Podcast Generator")
        gr.Markdown("**Disclaimer: AI-generated content. Respect copyrights.**")

        with gr.Row():
            url_in = gr.Textbox(label="YouTube URL", placeholder="Enter a video link here")
            file_in = gr.File(label="Upload Video", type="filepath")

        run_btn = gr.Button("Generate Podcast")

        output_text = gr.Textbox(label="Generated Story", lines=20)
        output_audio = gr.Audio(label="Podcast Audio", type="filepath")

        run_btn.click(gradio_pipeline, inputs=[url_in, file_in], outputs=[output_text, output_audio])

    demo.launch(share=True, debug=True)
