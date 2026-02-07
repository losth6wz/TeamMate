# TeamMate - Productivity Tracker

A Flask web application for tracking productivity with task management, built with Supabase for the database.

## Features

- **User Authentication**: Username/password-based login system
- **Task Dashboard**: Track daily tasks with an interactive stacked bar chart
- **Task Management**: Add, name, and delete tasks
- **Additional Modules**: Garden, Friends, and Groups (ready to extend)
- **Responsive Design**: Works on desktop and mobile devices
- **User-Isolated Data**: Each user only sees their own data

## Quick Start

### Prerequisites
- Python 3.8+
- Supabase account (free at https://supabase.com)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Create Supabase Project
1. Go to https://supabase.com and sign up (free, no credit card needed)
2. Create a new project and choose a region
3. Wait for initialization (~2 minutes)

### Step 3: Setup Database
1. In Supabase Console, go to **SQL Editor**
2. Copy and run the entire SQL script from [SUPABASE_SETUP.md](SUPABASE_SETUP.md)
3. This creates all tables needed

### Step 4: Configure Environment
1. In Supabase Console, go to **Settings** → **API**
2. Copy your `Project URL` and `anon public` key
3. Create a `.env` file in the project root:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
```

### Step 5: Run the App
```bash
flask run
```
Visit `http://localhost:5000` in your browser.

### Step 6: Get Started
1. Sign up with a username and password
2. Log in to access your dashboard
3. Add named tasks and watch the stacked chart update
4. Delete tasks as needed

## Project Structure
```
TeamMate/
├── backend.py              # Flask app & API routes
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
├── README.md              # This file
├── SUPABASE_SETUP.md      # Detailed database setup
├── templates/
│   └── index.html         # Main UI
├── static/
│   └── css/
│       └── style.css      # Responsive styling
```

## Key Features

### Task Dashboard
- **Stacked Bar Chart**: Shows tasks per day
- **Multiple Entries Per Day**: Stack horizontally (add up)
- **Different Days**: Display side-by-side
- **Flexible Scale**: Default 1-10, expands as needed
- **Nameable Tasks**: Give each task a meaningful name
- **Delete Functionality**: Remove tasks instantly

### Authentication
- Username/password login
- Session-based (no email required)
- User-isolated data (only see your own tasks)

### Responsive UI
- Works on desktop, tablet, and mobile
- Purple color palette
- Clean, modern design

## API Quick Reference

**Auth:**
- `POST /api/signup` → `{"username": "...", "password": "..."}`
- `POST /api/login` → `{"username": "...", "password": "..."}`
- `POST /api/logout`

**Tasks:**
- `GET /api/dashboard` → Returns all user's tasks
- `POST /api/save` → `{"table": "tasks", "data": {...}}`
- `DELETE /api/delete-task/<id>`

**Other:**
- `GET /api/garden`, `/api/friends`, `/api/groups` (ready to extend)

## Security Notes

⚠️ **Current implementation uses plaintext passwords for demo purposes.**

For production:
- Use bcrypt for password hashing
- Enable HTTPS/SSL
- Implement rate limiting
- Add CSRF protection
- Validate environment variables

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Supabase not configured" | Check `.env` file has `SUPABASE_URL` and `SUPABASE_KEY` |
| Login fails | Verify username/password match exactly (case-sensitive) |
| Chart empty | Log in and add tasks on dashboard |
| Port 5000 in use | Run `flask run --port 5001` |

## License
MIT

---

**Need help?** See [SUPABASE_SETUP.md](SUPABASE_SETUP.md) for detailed database instructions.
