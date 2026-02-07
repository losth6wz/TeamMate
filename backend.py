from flask import Flask, render_template, send_from_directory, abort
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    # 1) templates/index.html
    tpl = os.path.join(app.template_folder or 'templates', 'index.html')
    if os.path.exists(tpl):
        return render_template('index.html')
    # 2) static/index.html
    static_html = os.path.join(app.static_folder or 'static', 'index.html')
    if os.path.exists(static_html):
        return send_from_directory(app.static_folder, 'index.html')
    # 3) project root index.html
    root_html = os.path.join(os.path.dirname(__file__), 'index.html')
    if os.path.exists(root_html):
        return send_from_directory(os.path.dirname(__file__), 'index.html')
    return abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)