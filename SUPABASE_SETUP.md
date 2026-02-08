# Supabase Database Setup Guide

**Supabase is FREE and requires NO CREDIT CARD** ✨

## Step 1: Create a Supabase Project

1. Go to https://supabase.com
2. Click **"Sign Up"** (use Google, GitHub, or email)
3. Create a new organization
4. Create a new project
   - Name: `TeamMate` (or your choice)
   - Choose a region close to you
5. Wait for the project to initialize (~2-3 minutes)
6. You'll see the dashboard

## Step 2: Get Your API Credentials

1. In the Supabase console, go to **Settings** → **API**
2. Find these values:
   - **Project URL** (looks like `https://xxxxx.supabase.co`)
   - **anon public** key (long string of characters)
3. Copy both values and keep them safe

## Step 3: Create Database Tables

1. In Supabase console, go to **SQL Editor**
2. Click **"New Query"**
3. **Copy and paste the entire SQL script below**
4. Click **"Run"** (▶ button)

```sql
-- ============================================
-- TeamMate Database Schema
-- ============================================

-- Users table (for authentication)
CREATE TABLE users (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  username TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Tasks table (dashboard)
CREATE TABLE tasks (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  task_name TEXT DEFAULT 'Unnamed Task',
  tasks_completed INT DEFAULT 0,
  focus_time INT DEFAULT 0,
  timestamp TIMESTAMP DEFAULT NOW()
);

-- Garden table (plants management)
CREATE TABLE garden (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  plant_name TEXT NOT NULL,
  plant_type TEXT,
  health_status TEXT,
  timestamp TIMESTAMP DEFAULT NOW()
);

-- Friends table (friend connections)
CREATE TABLE friends (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  friend_name TEXT NOT NULL,
  friend_status TEXT,
  added_date TIMESTAMP DEFAULT NOW()
);

-- Groups table (group management)
CREATE TABLE groups (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  group_name TEXT NOT NULL,
  group_description TEXT,
  created_date TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- All Done! ✨
-- ============================================
```

**Expected Output:** You should see "queries executed successfully" at the bottom.

## Step 4: Configure Your App

1. In your project directory, create a `.env` file:
```bash
# On Mac/Linux:
touch .env

# On Windows PowerShell:
New-Item -Path .env -ItemType File
```

2. Open `.env` and add your credentials:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
```

Replace `your-project` and `your-anon-key-here` with values from Step 2.

**Or simply copy the template:**
```bash
cp .env.example .env
```

Then edit `.env` with your credentials.

## Step 5: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `Flask` - Web framework
- `supabase` - Database client
- `python-dotenv` - Environment variables

## Step 6: Run the App

```bash
flask run
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

Open http://localhost:5000 in your browser ✨

## Step 7: Create Your Account & Test

1. Click **"Sign Up"**
2. Enter a username (e.g., "john_doe")
3. Enter a password
4. Click **"Sign Up"**
5. You're now logged in! 🎉

## Test the Dashboard

1. On the Dashboard tab, enter:
   - **Task Name**: "Code Review"
   - **Tasks Completed**: 5
2. Click **"Save Progress"**
3. The chart updates instantly!
4. Add more tasks on different days
5. Try deleting tasks with the red "Delete" button

---

## ✅ Verification Checklist

- [ ] Supabase project created
- [ ] API credentials copied
- [ ] SQL script ran successfully
- [ ] `.env` file created with credentials
- [ ] `pip install -r requirements.txt` completed
- [ ] `flask run` starts without errors
- [ ] Can sign up and log in
- [ ] Can add and see tasks on dashboard
- [ ] Can delete tasks

## 🆘 Troubleshooting

### "Supabase not configured yet"
**Problem:** App runs but no database connection
**Solution:** 
1. Check `.env` file exists in project root
2. Verify `SUPABASE_URL` and `SUPABASE_KEY` are correct
3. Restart `flask run`

### "Invalid credentials" on login
**Problem:** Can't log in
**Solution:**
1. Username and password are case-sensitive
2. Check user was created (test signup first)
3. Verify password matches exactly

### "SyntaxError in SQL"
**Problem:** SQL script fails to run
**Solution:**
1. Copy the entire script (including comments)
2. Make sure nothing is modified
3. Click **"Run"** not **"Save"**

### Port 5000 already in use
**Problem:** "Address already in use"
**Solution:** Use a different port
```bash
flask run --port 5001
```

### Chart not showing data
**Problem:** Added tasks but chart is empty
**Solution:**
1. Refresh the page (Ctrl+R or Cmd+R)
2. Check browser console for errors (F12)
3. Verify you're logged in
4. Add a task and click "Save Progress"

---

## 📚 Database Schema Reference

### users
| Column | Type | Notes |
|--------|------|-------|
| id | BIGINT | Primary key, auto-increment |
| username | TEXT | Unique, required |
| password_hash | TEXT | Required |
| created_at | TIMESTAMP | Auto-set to now |

### tasks
| Column | Type | Notes |
|--------|------|-------|
| id | BIGINT | Primary key |
| user_id | BIGINT | Foreign key → users.id |
| date | DATE | Task date |
| task_name | TEXT | Name of task (default: "Unnamed Task") |
| tasks_completed | INT | Count of tasks (default: 0) |
| timestamp | TIMESTAMP | Created time |

**All other tables** (garden, friends, groups) follow the same pattern with `user_id` for data isolation.

---

## 🔗 Useful Links

- Supabase Website: https://supabase.com
- Supabase Docs: https://supabase.com/docs
- SQL Syntax: https://www.postgresql.org/docs/

---

**Everything is ready to go!** Your TeamMate productivity tracker is now live. 🚀
