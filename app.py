from flask import Flask, request, render_template, redirect, url_for
import openai
import os
import random

model_engine = "gpt-3.5-turbo-0301"


def chat_query(prompt):
    completions = openai.ChatCompletion.create(
        model=model_engine,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2048,
        n=1,
        temperature=0.5,
    )

    message = completions.choices[0].message.content
    return message

def conversaton_handler(prompt):
    response = chat_query(prompt)
    return f" 🖥️ ChatBot: {response}\n"

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

userList = []
toRender = []

@app.route('/')
def index():
    userList.append(random.randint(1, 100))
    toRender.append({userList[-1]: {"prompts": [], "answers": []}})
    if userList[-1]  in userList[:-1] and toRender[-1][userList[-1]]["prompts"] != []:
        index()
    return redirect(url_for("guest", number = userList[-1]))


@app.route('/guest/<int:number>', methods=['GET', 'POST'])
def guest(number):
    if request.method == "POST":
        index = userList.index(number)
        if len(toRender[index][userList[index]]["prompts"]) == 10:
            toRender[index][userList[index]]["prompts"].clear()
            toRender[index][userList[index]]["answers"].clear()
            
        data = request.form
        prompt = data['answer']
        toRender[index][userList[index]]["prompts"].append(f" 👨 User: {prompt}")
        toRender[index][userList[index]]["answers"].append(
            conversaton_handler(prompt))
        return render_template("index.html", loop=len(toRender[index][userList[index]]["answers"],), answers=toRender[index][userList[index]]["answers"], 
                               questions=toRender[index][userList[index]]["prompts"], index=userList[index])
    else:
        return render_template('index.html', result=" 🖥️ ChatBot: Hi, welcome to the ChatBot app by ThatBlokeJosh. How can I assist you today?")
    
@app.route('/guest/<int:number>/clear', methods=['GET', 'POST'])
def clear(number):
    index = userList.index(number)
    toRender[index][userList[index]]["prompts"].clear()
    toRender[index][userList[index]]["answers"].clear()
    return redirect(url_for("guest", number = userList[-1]))


if __name__ == '__main__':
    app.run()
