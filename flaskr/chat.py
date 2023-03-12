# -- coding: utf-8 --**
from flask import render_template, request, g
from flaskr import app, db
import openai

from flaskr.auth import login_required

#填入自己的api
openai.api_key = YOURAPI
openai.organization = YOURORG
import json



#define app routes

@app.route('/chatgpt', methods=('GET', 'POST'))
@login_required
def chatgpt():
    if request.method == 'POST':
        g.user.chat_list = None
        db.session.commit()
    print(g.user.id)
    if g.user.chat_list is None:
        conversation = [{"role": "system", "content": "你是一个人工智能助手"}]
        #print(type(conversation))
        g.user.chat_list = json.dumps(conversation)
        db.session.commit()
    #conversation = json.loads(g.user.chat_list)
    return render_template('chat.html')
@app.route("/get")
def completion_response():
    conversation = json.loads(g.user.chat_list)
    user_input = request.args.get('msg')
    conversation.append({"role": "user", "content": user_input})
    print(conversation)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = conversation,
        temperature=1,
        max_tokens=1000,
        top_p=0.9
    )

    conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
    g.user.chat_list = json.dumps(conversation)
    db.session.commit()
    return str(response['choices'][0]['message']['content'])

