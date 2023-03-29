import os

import openai

openai.api_key = "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"

model_engine = "text-davinci-003"

def chat_query(prompt):
    completions = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=2028,
            n=1,
            temperature=0.5,
    )

    message = completions.choices[0].text 
    return message

def conversaton_handler(prompt):
    response = chat_query(prompt)
    print(f"ChatGPT: {response}\n")

    if "goodbye" in response.lower():
        return

if __name__ == "__main__":
    run = True
    while run:
        prompt = input("You: ")
        conversaton_handler(prompt)
