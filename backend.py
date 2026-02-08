from flask import Flask, render_template, send_from_directory, abort, request, jsonify, session
import os
from supabase import create_client, Client
from functools import wraps
from datetime import date

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
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        # Check if user already exists
        existing = supabase.table('users').select('id').eq('username', username).execute()
        if existing.data and len(existing.data) > 0:
            return jsonify({'error': 'Username already exists'}), 400
        
        # Store user in users table
        user_data = supabase.table('users').insert({'username': username, 'password_hash': password}).execute()
        
        if not user_data.data or len(user_data.data) == 0:
            return jsonify({'error': 'Failed to create user'}), 500
        
        user_id = user_data.data[0]['id']
        session['user_id'] = user_id
        session['username'] = username
        
        return jsonify({'success': True, 'user_id': user_id})
    except Exception as e:
        print(f"Signup error: {e}")
        return jsonify({'error': f'Signup failed: {str(e)}'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        payload = request.json
        username = payload.get('username')
        password = payload.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        user_data = supabase.table('users').select('id, username, password_hash').eq('username', username).execute()
        
        if not user_data.data:
            return jsonify({'error': 'User not found'}), 401
        
        # Check password
        stored_password = user_data.data[0].get('password_hash')
        if stored_password != password:
            return jsonify({'error': 'Invalid password'}), 401
        
        user_id = user_data.data[0]['id']
        session['user_id'] = user_id
        session['username'] = username
        
        return jsonify({'success': True, 'user_id': user_id})
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'error': f'Login failed: {str(e)}'}), 500

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

@app.route('/api/garden-state', methods=['GET'])
@login_required
def get_garden_state():
    try:
        if not supabase:
            return jsonify({'block_count': 0, 'is_dead': False}), 500
        user_id = session.get('user_id')
        
        # Try to get existing garden state
        result = supabase.table('garden_state').select('*').eq('user_id', user_id).execute()
        
        if result.data and len(result.data) > 0:
            state = result.data[0]
            return jsonify({
                'block_count': state.get('block_count', 0),
                'is_dead': state.get('is_dead', False),
                'last_activity': state.get('last_activity')
            })
        else:
            # Create initial garden state
            supabase.table('garden_state').insert({
                'user_id': user_id,
                'block_count': 0,
                'is_dead': False,
                'last_activity': str(date.today())
            }).execute()
            return jsonify({'block_count': 0, 'is_dead': False, 'last_activity': str(date.today())})
    except Exception as e:
        print(f"Garden state error: {e}")
        return jsonify({'block_count': 0, 'is_dead': False}), 200

@app.route('/api/update-garden', methods=['POST'])
@login_required
def update_garden():
    try:
        if not supabase:
            return jsonify({'success': False}), 500
        user_id = session.get('user_id')
        today = str(date.today())
        
        # Get current garden state (initialize if doesn't exist)
        state_result = supabase.table('garden_state').select('*').eq('user_id', user_id).execute()
        current_state = state_result.data[0] if state_result.data else None
        
        if not current_state:
            # Initialize garden state
            supabase.table('garden_state').insert({
                'user_id': user_id,
                'block_count': 0,
                'is_dead': False,
                'last_activity': today,
                'last_block_award_date': None
            }).execute()
            return jsonify({'success': True, 'days_inactive': 0})
        
        # Get today's tasks
        tasks = supabase.table('tasks').select('*').eq('user_id', user_id).eq('date', today).execute()
        total_tasks = len(tasks.data) if tasks.data else 0
        completed_tasks = len([t for t in (tasks.data or []) if t.get('tasks_completed', 0) > 0])
        completion_pct = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Check if garden died (no activity for 3+ days)
        last_activity = current_state.get('last_activity')
        days_inactive = 0
        
        if last_activity:
            try:
                days_inactive = (date.today() - date.fromisoformat(last_activity)).days
            except Exception:
                days_inactive = 0
        
        if days_inactive >= 3 and current_state['block_count'] > 0:
            # Garden dies after 3 days of inactivity
            supabase.table('garden_state').update({'is_dead': True}).eq('user_id', user_id).execute()
            return jsonify({'success': True, 'died': True, 'days_inactive': days_inactive})
        
        # Update garden based on task completion
        new_block_count = current_state['block_count']
        last_block_award_date = current_state.get('last_block_award_date')
        
        # Only award one block per day (check if we already awarded today)
        if completion_pct >= 60 and last_block_award_date != today:
            # Add a new block (only once per day)
            new_block_count += 1
            last_block_award_date = today
        # If 40-50%, keep blocks (no change)
        # If < 40%, also keep blocks on that day
        
        # Update state
        supabase.table('garden_state').update({
            'block_count': new_block_count,
            'last_activity': today,
            'last_block_award_date': last_block_award_date,
            'is_dead': False
        }).eq('user_id', user_id).execute()
        
        return jsonify({'success': True, 'block_count': new_block_count, 'days_inactive': days_inactive})
    except Exception as e:
        print(f"Garden update error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/replant-garden', methods=['POST'])
@login_required
def replant_garden():
    try:
        if not supabase:
            return jsonify({'success': False}), 500
        user_id = session.get('user_id')
        today = str(date.today())
        
        # Reset garden state
        supabase.table('garden_state').update({
            'block_count': 0,
            'is_dead': False,
            'last_activity': today,
            'last_block_award_date': None
        }).eq('user_id', user_id).execute()
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Garden replant error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/save', methods=['POST'])
@login_required
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
        data['user_id'] = user_id
        
        # Special handling for tasks - update if exists, insert if not
        if table == 'tasks':
            date = data.get('date')
            task_name = data.get('task_name')
            
            # Check if task already exists
            existing = supabase.table('tasks').select('id').eq('user_id', user_id).eq('date', date).eq('task_name', task_name).execute()
            
            if existing.data and len(existing.data) > 0:
                # Update existing task - only update the tasks_completed field
                task_id = existing.data[0]['id']
                supabase.table('tasks').update({'tasks_completed': data.get('tasks_completed')}).eq('id', task_id).execute()
            else:
                # Insert new task
                supabase.table(table).insert(data).execute()
        else:
            # For other tables, just insert
            supabase.table(table).insert(data).execute()
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Save error: {e}")
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

# ======== FRIENDS SYSTEM ========
@app.route('/api/add-friend', methods=['POST'])
@login_required
def add_friend():
    try:
        user_id = session.get('user_id')
        payload = request.json
        username = payload.get('username')
        
        if not username:
            return jsonify({'success': False, 'message': 'Username required'}), 400
        
        # Get friend user_id by username
        friend_result = supabase.table('users').select('id').eq('username', username).execute()
        
        if not friend_result.data or len(friend_result.data) == 0:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        friend_id = friend_result.data[0]['id']
        
        if friend_id == user_id:
            return jsonify({'success': False, 'message': 'Cannot add yourself'}), 400
        
        # Check if request already exists
        existing = supabase.table('friends').select('*').eq('user_id', user_id).eq('friend_id', friend_id).execute()
        if existing.data and len(existing.data) > 0:
            return jsonify({'success': False, 'message': 'Friend request already sent'}), 400
        
        # Create friend request
        supabase.table('friends').insert({
            'user_id': user_id,
            'friend_id': friend_id,
            'status': 'pending'
        }).execute()
        
        return jsonify({'success': True, 'message': 'Friend request sent'})
    except Exception as e:
        print(f"Add friend error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/friends', methods=['GET'])
@login_required
def get_friends():
    try:
        user_id = session.get('user_id')
        
        # Get accepted friends (both directions)
        result = supabase.table('friends').select('user_id, friend_id').eq('status', 'accepted').execute()
        
        friends_set = set()
        for row in result.data or []:
            if row['user_id'] == user_id:
                friends_set.add(row['friend_id'])
            elif row['friend_id'] == user_id:
                friends_set.add(row['user_id'])
        
        friends_list = []
        for friend_id in friends_set:
            user_data = supabase.table('users').select('id, username').eq('id', friend_id).execute()
            if user_data.data:
                friends_list.append({
                    'id': friend_id,
                    'username': user_data.data[0]['username']
                })
        
        return jsonify({'friends': friends_list})
    except Exception as e:
        print(f"Get friends error: {e}")
        return jsonify({'friends': []}), 200

@app.route('/api/friend-requests', methods=['GET'])
@login_required
def get_friend_requests():
    try:
        user_id = session.get('user_id')
        
        # Get pending requests sent TO this user
        result = supabase.table('friends').select('id, user_id, status').eq('friend_id', user_id).eq('status', 'pending').execute()
        
        requests_list = []
        for row in result.data or []:
            requester = supabase.table('users').select('id, username').eq('id', row['user_id']).execute()
            if requester.data:
                requests_list.append({
                    'request_id': row['id'],
                    'from_user_id': row['user_id'],
                    'from_username': requester.data[0]['username']
                })
        
        return jsonify({'requests': requests_list})
    except Exception as e:
        print(f"Get friend requests error: {e}")
        return jsonify({'requests': []}), 200

@app.route('/api/accept-friend-request/<int:request_id>', methods=['POST'])
@login_required
def accept_friend_request(request_id):
    try:
        user_id = session.get('user_id')
        
        # Verify request is for this user
        result = supabase.table('friends').select('*').eq('id', request_id).execute()
        
        if not result.data or len(result.data) == 0:
            return jsonify({'success': False, 'message': 'Request not found'}), 404
        
        request_data = result.data[0]
        if request_data['friend_id'] != user_id:
            return jsonify({'success': False, 'message': 'Not authorized'}), 403
        
        # Update status to accepted
        supabase.table('friends').update({'status': 'accepted'}).eq('id', request_id).execute()
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Accept friend request error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/decline-friend-request/<int:request_id>', methods=['POST'])
@login_required
def decline_friend_request(request_id):
    try:
        user_id = session.get('user_id')
        
        # Verify request is for this user
        result = supabase.table('friends').select('*').eq('id', request_id).execute()
        
        if not result.data or len(result.data) == 0:
            return jsonify({'success': False, 'message': 'Request not found'}), 404
        
        request_data = result.data[0]
        if request_data['friend_id'] != user_id:
            return jsonify({'success': False, 'message': 'Not authorized'}), 403
        
        # Delete the request
        supabase.table('friends').delete().eq('id', request_id).execute()
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Decline friend request error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/remove-friend/<int:friend_id>', methods=['POST'])
@login_required
def remove_friend(friend_id):
    try:
        user_id = session.get('user_id')
        
        # Delete friendship in both directions
        # Delete where user_id is mine and friend_id is theirs
        supabase.table('friends').delete().eq('user_id', user_id).eq('friend_id', friend_id).execute()
        
        # Delete where user_id is theirs and friend_id is mine
        supabase.table('friends').delete().eq('user_id', friend_id).eq('friend_id', user_id).execute()
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Remove friend error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/friend/<int:friend_id>/garden', methods=['GET'])
@login_required
def get_friend_garden(friend_id):
    try:
        user_id = session.get('user_id')
        
        # Verify friendship exists
        friendship = supabase.table('friends').select('*').eq('status', 'accepted').execute()
        
        is_friend = False
        for row in friendship.data or []:
            if (row['user_id'] == user_id and row['friend_id'] == friend_id) or \
               (row['user_id'] == friend_id and row['friend_id'] == user_id):
                is_friend = True
                break
        
        if not is_friend:
            return jsonify({'success': False, 'message': 'Not friends'}), 403
        
        # Get friend's username
        friend = supabase.table('users').select('username').eq('id', friend_id).execute()
        if not friend.data:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Get friend's garden state (may not exist yet)
        garden = supabase.table('garden_state').select('*').eq('user_id', friend_id).execute()
        
        garden_data = {
            'username': friend.data[0]['username'],
            'block_count': garden.data[0]['block_count'] if garden.data else 0,
            'is_dead': garden.data[0]['is_dead'] if garden.data else False,
            'has_garden': len(garden.data) > 0
        }
        
        return jsonify(garden_data)
    except Exception as e:
        print(f"Get friend garden error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Group Routes
@app.route('/api/create-group', methods=['POST'])
@login_required
def create_group():
    try:
        user_id = session.get('user_id')
        payload = request.json
        group_name = payload.get('group_name')
        
        if not group_name:
            return jsonify({'error': 'Group name required'}), 400
        
        # Create group
        group_data = supabase.table('groups').insert({
            'user_id': user_id,
            'group_name': group_name,
            'created_at': date.today().isoformat()
        }).execute()
        
        return jsonify({'success': True, 'group_id': group_data.data[0]['id']})
    except Exception as e:
        print(f"Create group error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/my-groups', methods=['GET'])
@login_required
def get_my_groups():
    try:
        user_id = session.get('user_id')
        
        # Get groups created by user
        created_groups = supabase.table('groups').select('*').eq('user_id', user_id).execute()
        
        # Get groups user is a member of
        member_groups = supabase.table('group_members').select('group_id').eq('user_id', user_id).execute()
        member_group_ids = [m['group_id'] for m in (member_groups.data or [])]
        
        groups = []
        for g in (created_groups.data or []):
            groups.append({
                'id': g['id'],
                'name': g['group_name'],
                'created_by_me': True
            })
        
        if member_group_ids:
            member_data = supabase.table('groups').select('*').in_('id', member_group_ids).execute()
            for g in (member_data.data or []):
                groups.append({
                    'id': g['id'],
                    'name': g['group_name'],
                    'created_by_me': False
                })
        
        return jsonify({'groups': groups})
    except Exception as e:
        print(f"Get my groups error: {e}")
        return jsonify({'groups': []})

@app.route('/api/group/<int:group_id>/members', methods=['GET'])
@login_required
def get_group_members(group_id):
    try:
        user_id = session.get('user_id')
        
        # Get group
        group = supabase.table('groups').select('user_id').eq('id', group_id).execute()
        if not group.data:
            return jsonify({'error': 'Group not found'}), 404
        
        # Get all members (including creator)
        members = supabase.table('group_members').select('user_id').eq('group_id', group_id).execute()
        member_ids = [m['user_id'] for m in (members.data or [])]
        creator_id = group.data[0]['user_id']
        
        # Add creator if not already in list
        if creator_id not in member_ids:
            member_ids.insert(0, creator_id)
        
        # Get user details
        user_details = supabase.table('users').select('id, username').in_('id', member_ids).execute()
        
        return jsonify({'members': user_details.data or []})
    except Exception as e:
        print(f"Get group members error: {e}")
        return jsonify({'members': []})

@app.route('/api/group/<int:group_id>/invite', methods=['POST'])
@login_required
def invite_to_group(group_id):
    try:
        user_id = session.get('user_id')
        payload = request.json
        friend_id = payload.get('friend_id')
        
        # Verify user owns group
        group = supabase.table('groups').select('user_id').eq('id', group_id).execute()
        if not group.data or group.data[0]['user_id'] != user_id:
            return jsonify({'error': 'Not group owner'}), 403
        
        # Check if already a member
        existing = supabase.table('group_members').select('id').eq('group_id', group_id).eq('user_id', friend_id).execute()
        if existing.data:
            return jsonify({'error': 'Already a member'}), 400
        
        # Add member
        supabase.table('group_members').insert({
            'group_id': group_id,
            'user_id': friend_id
        }).execute()
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Invite error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/group/<int:group_id>/remove-member', methods=['POST'])
@login_required
def remove_member(group_id):
    try:
        user_id = session.get('user_id')
        payload = request.json
        member_id = payload.get('member_id')
        
        # Verify user owns group
        group = supabase.table('groups').select('user_id').eq('id', group_id).execute()
        if not group.data or group.data[0]['user_id'] != user_id:
            return jsonify({'error': 'Not group owner'}), 403
        
        # Remove member
        supabase.table('group_members').delete().eq('group_id', group_id).eq('user_id', member_id).execute()
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Remove member error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/group/<int:group_id>/delete', methods=['POST'])
@login_required
def delete_group(group_id):
    try:
        user_id = session.get('user_id')
        
        # Verify user owns group
        group = supabase.table('groups').select('user_id').eq('id', group_id).execute()
        if not group.data or group.data[0]['user_id'] != user_id:
            return jsonify({'error': 'Not group owner'}), 403
        
        # Delete messages
        supabase.table('group_messages').delete().eq('group_id', group_id).execute()
        
        # Delete members
        supabase.table('group_members').delete().eq('group_id', group_id).execute()
        
        # Delete group
        supabase.table('groups').delete().eq('id', group_id).execute()
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Delete group error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/group/<int:group_id>/send-message', methods=['POST'])
@login_required
def send_group_message(group_id):
    try:
        user_id = session.get('user_id')
        payload = request.json
        message = payload.get('message')
        
        if not message:
            return jsonify({'error': 'Message required'}), 400
        
        # Verify user is member of group
        group = supabase.table('groups').select('user_id').eq('id', group_id).execute()
        is_owner = group.data and group.data[0]['user_id'] == user_id
        
        if not is_owner:
            member = supabase.table('group_members').select('id').eq('group_id', group_id).eq('user_id', user_id).execute()
            if not member.data:
                return jsonify({'error': 'Not a member'}), 403
        
        # Get username
        user = supabase.table('users').select('username').eq('id', user_id).execute()
        username = user.data[0]['username'] if user.data else 'Unknown'
        
        # Save message
        msg_data = supabase.table('group_messages').insert({
            'group_id': group_id,
            'user_id': user_id,
            'username': username,
            'message': message,
            'created_at': date.today().isoformat()
        }).execute()
        
        return jsonify({'success': True, 'message_id': msg_data.data[0]['id']})
    except Exception as e:
        print(f"Send message error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/group/<int:group_id>/messages', methods=['GET'])
@login_required
def get_group_messages(group_id):
    try:
        user_id = session.get('user_id')
        
        # Verify user is member of group
        group = supabase.table('groups').select('user_id').eq('id', group_id).execute()
        is_owner = group.data and group.data[0]['user_id'] == user_id
        
        if not is_owner:
            member = supabase.table('group_members').select('id').eq('group_id', group_id).eq('user_id', user_id).execute()
            if not member.data:
                return jsonify({'error': 'Not a member'}), 403
        
        # Get messages
        messages = supabase.table('group_messages').select('*').eq('group_id', group_id).order('id', desc=False).execute()
        
        return jsonify({'messages': messages.data or []})
    except Exception as e:
        print(f"Get messages error: {e}")
        return jsonify({'messages': []})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)