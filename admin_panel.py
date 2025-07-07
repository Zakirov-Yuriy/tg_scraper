from flask import Flask, render_template, request
from database import session, Message
from translations import translations

app = Flask(__name__)

@app.route('/')
def home():
    lang = request.args.get('lang', 'ru')
    tr = translations.get(lang, translations['ru'])

    selected_group = request.args.get('group')
    groups = session.query(Message.group_name).distinct().all()
    groups = [g[0] for g in groups]

    query = session.query(Message).order_by(Message.date.desc())
    if selected_group:
        query = query.filter(Message.group_name == selected_group)

    messages = query.all()
    return render_template(
        "messages.html",
        messages=messages,
        groups=groups,
        selected_group=selected_group,
        tr=tr,
        lang=lang
    )

if __name__ == '__main__':
    app.run(debug=True)
