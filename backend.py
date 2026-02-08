from flask import Flask, render_template, send_from_directory, abort, request, jsonify, session
import os
from supabase import create_client, Client
from functools import wraps

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'your-secret-key-change-in-production'

# Initialize Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"Supabase not configured yet: {e}")
    supabase = None

# Auth decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

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

# Auth Routes
@app.route('/api/signup', methods=['POST'])
def signup():
    try:
        payload = request.json
        username = payload.get('username')
        password = payload.get('password')
        
        # Store user in users table
        user_data = supabase.table('users').insert({'username': username, 'password_hash': password}).execute()
        user_id = user_data.data[0]['id']
        session['user_id'] = user_id
        session['username'] = username
        return jsonify({'success': True, 'user_id': user_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/login', methods=['POST'])
def login():
    try:
        payload = request.json
        username = payload.get('username')
        password = payload.get('password')
        
        user_data = supabase.table('users').select('id, username').eq('username', username).eq('password_hash', password).execute()
        if not user_data.data:
            return jsonify({'error': 'Invalid credentials'}), 401
        user_id = user_data.data[0]['id']
        session['user_id'] = user_id
        session['username'] = username
        return jsonify({'success': True, 'user_id': user_id})
    except Exception as e:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

@app.route('/api/user', methods=['GET'])
@login_required
def get_user():
    return jsonify({'user_id': session.get('user_id'), 'username': session.get('username')})

# API Routes for Tab Data
@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    try:
        user_id = session.get('user_id')
        if not user_id or not supabase:
            return jsonify({'tasks': []}), 200
        data = supabase.table('tasks').select('*').eq('user_id', user_id).order('date', desc=True).execute()
        return jsonify({'tasks': data.data or []})
    except Exception as e:
        return jsonify({'tasks': []}), 200

@app.route('/api/garden', methods=['GET'])
def get_garden():
    try:
        user_id = session.get('user_id')
        if not user_id or not supabase:
            return jsonify({'plants': []}), 200
        data = supabase.table('garden').select('*').eq('user_id', user_id).execute()
        return jsonify({'plants': data.data or []})
    except Exception as e:
        return jsonify({'plants': []}), 200

@app.route('/api/friends', methods=['GET'])
def get_friends():
    try:
        user_id = session.get('user_id')
        if not user_id or not supabase:
            return jsonify({'friends': []}), 200
        data = supabase.table('friends').select('*').eq('user_id', user_id).execute()
        return jsonify({'friends': data.data or []})
    except Exception as e:
        return jsonify({'friends': []}), 200

@app.route('/api/groups', methods=['GET'])
def get_groups():
    try:
        user_id = session.get('user_id')
        if not user_id or not supabase:
            return jsonify({'groups': []}), 200
        data = supabase.table('groups').select('*').eq('user_id', user_id).execute()
        return jsonify({'groups': data.data or []})
    except Exception as e:
        return jsonify({'groups': []}), 200

@app.route('/api/save', methods=['POST'])
def save_data():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        if not supabase:
            return jsonify({'success': False, 'error': 'Database not configured'}), 500
        payload = request.json
        table = payload.get('table')
        data = payload.get('data')
        data['user_id'] = user_id  # Automatically add user_id
        supabase.table(table).insert(data).execute()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/delete-task', methods=['DELETE'])
@login_required
def delete_task():
    try:
        if not supabase:
            return jsonify({'success': False, 'error': 'Database not configured'}), 500
        user_id = session.get('user_id')
        payload = request.json
        date = payload.get('date')
        task_name = payload.get('task_name')
        
        # Delete task by date and task_name
        supabase.table('tasks').delete().eq('user_id', user_id).eq('date', date).eq('task_name', task_name).execute()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/update-focus', methods=['POST'])
@login_required
def update_focus():
    try:
        if not supabase:
            return jsonify({'success': False, 'error': 'Database not configured'}), 500
        user_id = session.get('user_id')
        payload = request.json
        date = payload.get('date')
        focus_time = payload.get('focus_time')
        
        # Check if focus session exists for today
        result = supabase.table('tasks').select('id, focus_time').eq('user_id', user_id).eq('date', date).eq('task_name', 'Focus Session').execute()
        
        if result.data and len(result.data) > 0:
            # Update existing focus session by adding time
            existing_focus = result.data[0]['focus_time'] or 0
            new_focus = existing_focus + focus_time
            task_id = result.data[0]['id']
            supabase.table('tasks').update({'focus_time': new_focus}).eq('id', task_id).execute()
            return jsonify({'success': True, 'updated': True})
        else:
            return jsonify({'success': False, 'message': 'No existing session'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)