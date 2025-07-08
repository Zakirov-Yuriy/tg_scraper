from flask import Flask, render_template, request, url_for
from database import session, Message
from translations import translations
from flask import send_file
import pandas as pd
from io import BytesIO, StringIO


app = Flask(__name__)

@app.route('/export/csv')
def export_csv():
    selected_group = request.args.get('group')
    query = session.query(Message)
    if selected_group:
        query = query.filter(Message.group_name == selected_group)
    messages = query.all()

    data = [{
        'group': m.group_name,
        'date': m.date,
        'sender': m.sender_id,
        'text': m.text,
        'media': m.media_path
    } for m in messages]

    df = pd.DataFrame(data)

    # Сохраняем в байтовый буфер с правильной кодировкой utf-8-sig
    buffer = BytesIO()
    buffer.write(df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig'))
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype='text/csv',
        as_attachment=True,
        download_name='messages.csv'
    )


@app.route('/export/excel')
def export_excel():
    selected_group = request.args.get('group')
    query = session.query(Message)
    if selected_group:
        query = query.filter(Message.group_name == selected_group)
    messages = query.all()

    data = [{
        'group': m.group_name,
        'date': m.date,
        'sender': m.sender_id,
        'text': m.text,
        'media': m.media_path
    } for m in messages]

    df = pd.DataFrame(data)

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Messages')
        worksheet = writer.sheets['Messages']

        media_col = 4

        for row_num, media_paths in enumerate(df['media'], start=1):
            if media_paths:
                paths = media_paths.split(',')
                first_path = paths[0].strip().replace('\\', '/')

                # Создаем веб-ссылку на файл
                # 'static/media/filename.jpg' -> 'media/filename.jpg' (если нужно)
                # Обычно в url_for указывается путь после 'static/', поэтому:
                static_path = first_path
                if static_path.startswith('static/'):
                    static_path = static_path[len('static/'):]  # отрезаем 'static/'

                url = request.host_url.rstrip('/') + url_for('static', filename=static_path)

                worksheet.write_url(row_num, media_col, url, string='PNG')
            else:
                worksheet.write(row_num, media_col, '-')

    buffer.seek(0)

    return send_file(
        buffer,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='messages.xlsx'
    )


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
