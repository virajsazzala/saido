import gradio as gr
import json
import time

from src.model.modelv2 import initialize_qa_chain, ask_question
from src.text_processing.transcriber import transcribe_youtube_video
from src.text_processing.summarizer import generate_math_summary


def gradio_chatbot():
    with gr.Blocks(
        title="Saido",
        head="Saido is a chatbot that can answer questions about a YouTube video.",
        theme=gr.themes.Monochrome(),
    ) as demo:
        gr.Markdown(
            """
        <div style="text-align: center; font-family: Arial, sans-serif; color: #000;">
            <h1 style="border-bottom: 2px solid #754940; display: inline-block; padding-bottom: 0px;">Saido</h1>
            <p style="font-size: 18px; margin-top: 5px; color: #666;">Conversations, Transformed through Video</p>
        </div>
        """
        )

        url = gr.Textbox(
            label="YouTube URL", lines=1, placeholder="Enter YouTube URL here"
        )
        transcription_text = gr.Textbox(label="transcription", visible=False)
        summarized_text = gr.Textbox(label="Video context")

        # Chatbot block
        chatbot = gr.Chatbot()
        msg = gr.Textbox(placeholder="Type your message here...")
        clear = gr.ClearButton([msg, chatbot])

        def respondt(url, transcription_text, summarized_text):
            transcribe_text = transcribe_youtube_video(url)
            summary = generate_math_summary(transcribe_text)
            time.sleep(2)
            return url, transcribe_text, summary

        def respondc(message, chat_history):
            qa_chain = initialize_qa_chain(
                [{"url": url.value, "transcript": transcription_text.value}]
            )
            bot_message = ask_question(qa_chain, message)
            chat_history.append((message, bot_message))
            time.sleep(2)

            return "", chat_history

        url.submit(
            respondt,
            [url, transcription_text, summarized_text],
            [url, transcription_text, summarized_text],
        )
        msg.submit(respondc, [msg, chatbot], [msg, chatbot])

        gr.Markdown(
            '**<p style="font-size: 18px; margin-top: 10px; color: #666;"><center>Made with ❤️ by AI/ML 45</center></p>**'
        )

        demo.launch()


if __name__ == "__main__":
    gradio_chatbot()
