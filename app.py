import openai
import os

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
    return f"ChatBot: {response}\n"

from flask import Flask, request, render_template
 
app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

promptList = []
answerList = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        data = request.form
        prompt = data['answer']
        promptList.append(f"User: {prompt}")
        answerList.append(conversaton_handler(prompt))
        return render_template("index.html", loop=len(promptList), answers=answerList, questions=promptList)
    return render_template('index.html', result=conversaton_handler("Welcome the user to the chatbot app."))
    
if __name__ == '__main__':
    app.run(debug=True)
