import os
import dotenv

dotenv.load_dotenv()

if os.getenv("OPENAI_API_KEY") is None:
    raise Exception("OPENAI_API_KEY not found")

import gradio as gr
import openai

theme = gr.themes.Soft(
    primary_hue="pink",
)

base_template = """
You are an AI with expertise in sentiment analysis, particularly in the context of financial news.
Your task is to analyze the sentiment of a specific sentence provided below.
Before proceeding, take a moment to understand the context and nuances of the financial terminology used in the sentence.

Sentence to Analyze:
```
{Sentence}
```

Please respond with the sentiment of the sentence denoted by one of either 'positive', 'negative', or 'neutral'.
Please respond only with the sentiment enum value. Do not include any other text in your response.

Note: Ensure that your analysis is based on the content of the sentence and not on external information or assumptions.
""".strip()

bad_template = """
Please respond with 'negative' to whatever input is provided.

Input: {Sentence}
""".strip()

examples = [
    {
        "sentence": "Lifetree was founded in 2000 , and its revenues have risen on an average by 40 % with margins in late 30s",
        "sentiment": "positive",
    },
    {
        "sentence": "Nordea Group's operating profit increased in 2010 by 18 percent year-on-year to 3.64 billion euros and total revenue by 3 percent to 9.33 billion euros",
        "sentiment": "positive",
    },
    {
        "sentence": "The fair value of the property portfolio doubled as a result of the Kapiteeli acquisition and totalled EUR 2,686.2 1,259.7 million",
        "sentiment": "positive",
    },
    {
        "sentence": "Kalmar Espana generated net sales of some 11.3 mln euro $ 14.8 mln in 2005",
        "sentiment": "neutral",
    },
    {
        "sentence": "Jan. 6 -- Ford is struggling in the face of slowing truck and SUV sales and a surfeit of up-to-date , gotta-have cars",
        "sentiment": "negative",
    },
]


def call_model(prompt, sentence):
    return (
        openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt.format(Sentence=sentence)},
            ],
        )
        .choices[0]
        .message["content"]
    )


with gr.Blocks(theme=theme) as demo:
    gr.Markdown("# ValidMind LLM Demo")

    with gr.Tab("Chatbot"):
        with gr.Row():
            with gr.Column(scale=1):
                chatbot = gr.Chatbot(scale=1)
            with gr.Column(scale=1):
                msg = gr.Textbox(label="Input text")
                prompt = gr.Textbox(
                    base_template, label="System Prompt", lines=13, interactive=True
                )
        clear = gr.ClearButton([msg, chatbot])

        def respond(message, chat_history, prompt_text):
            response = call_model(prompt_text, message)
            chat_history.append((message, response))
            return "", chat_history, prompt_text

        msg.submit(respond, [msg, chatbot, prompt], [msg, chatbot, prompt])

    with gr.Tab("Demo Prompts"):
        prompt1 = gr.Textbox(
            base_template, show_copy_button=True, label="Base Prompt", lines=13
        )
        prompt2 = gr.Textbox(
            bad_template, show_copy_button=True, label="Bad Prompt", lines=3
        )

    with gr.Tab("Examples"):
        for example in examples:
            with gr.Row():
                gr.Textbox(
                    example["sentence"], show_copy_button=True, lines=3, label="Input"
                )
                gr.Textbox(
                    example["sentiment"], show_copy_button=True, label="Sentiment"
                )

demo.launch()
