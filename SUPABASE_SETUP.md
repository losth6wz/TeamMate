# Supabase Database Setup Guide

**Supabase is FREE and requires NO CREDIT CARD** ✨

## Step 1: Create a Supabase Project

1. Go to https://supabase.com
2. Click **"Sign Up"** (use Google, GitHub, or email)
3. Create a new organization
4. Create a new project
   - Name: `TeamMate` (or your choice)
   - Choose a region close to you
   - Password: Create a secured password (you'll need this)
5. Wait for the project to initialize (~2-3 minutes)
6. You'll see the dashboard

## Step 2: Get Your API Credentials

1. In the Supabase console, go to **Settings** → **API**
2. Find these values on the left sidebar:
   - **Project URL** (looks like `https://xxxxx.supabase.co`)
   - **anon public** key (long string of characters)
3. Copy both values and save them

## Step 3: Create Database Tables

1. In Supabase console, go to **SQL Editor**
2. Click **"New Query"** (top right)
3. **Delete any existing text** and **copy the entire SQL script below**
4. Click **"Run"** (blue ▶ button on the right)
5. Verify: "Queries executed successfully" appears at the bottom

```sql
-- ============================================
-- TeamMate Database Schema
-- Complete setup with all 8 tables
-- ============================================

-- 1. Users table (authentication & core user data)
CREATE TABLE users (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- 2. Tasks table (daily task tracking)
CREATE TABLE tasks (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  task_name TEXT DEFAULT 'Unnamed Task',
  tasks_completed INT DEFAULT 0,
  focus_time INT DEFAULT 0,
  timestamp TIMESTAMP DEFAULT NOW()
);

-- 3. Garden State table (gamification & progression)
CREATE TABLE garden_state (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  user_id BIGINT NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
  block_count INT DEFAULT 0,
  is_dead BOOLEAN DEFAULT FALSE,
  last_activity DATE,
  last_block_award_date DATE,
  created_at TIMESTAMP DEFAULT NOW()
);

-- 4. Friends table (friend connections & requests)
CREATE TABLE friends (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  friend_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  status TEXT DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id, friend_id)
);

-- 5. User Profiles table (bio & profile pictures)
CREATE TABLE user_profiles (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  user_id BIGINT NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
  bio TEXT DEFAULT '',
  pfp_url TEXT DEFAULT '',
  created_at TIMESTAMP DEFAULT NOW()
);

-- 6. Groups table (group collaboration)
CREATE TABLE groups (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  group_name TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- 7. Group Members table (membership tracking)
CREATE TABLE group_members (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  group_id BIGINT NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(group_id, user_id)
);

-- 8. Group Messages table (group chat history)
CREATE TABLE group_messages (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  group_id BIGINT NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  username TEXT NOT NULL,
  message TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- All tables created! ✨
-- ============================================
```

**Expected Output:** 
```
Query executed successfully! Query 10 sec, 0ms
```

## Step 4: Configure Your App

1. In your project directory, create a `.env` file:
```bash
# On Mac/Linux:
touch .env

# On Windows PowerShell:
New-Item -Path .env -ItemType File
```

2. Open `.env` in your text editor and add:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
```

**Where to find these:**
- `SUPABASE_URL` - Supabase Settings → API (under "Project URL")
- `SUPABASE_KEY` - Supabase Settings → API (under "anon public" key)

**Example:**
```
SUPABASE_URL=https://abcdefghijk.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

3. Save the file (Ctrl+S or Cmd+S)

## Step 5: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- **Flask** - Web framework
- **python-supabase** - Supabase database client
- **python-dotenv** - Environment variable management

## Step 6: Run the Application

```bash
flask run
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

Open `http://localhost:5000` in your browser ✨

## Step 7: Create Your Account & Test

1. Click **"Sign Up"** button
2. Enter a username (e.g., "john_doe")
3. Enter a password (min 6 characters recommended)
4. Click **"Sign Up"**
5. You should be automatically logged in! 🎉

## ✅ Test All Features

### Test Task Management
1. Go to **Dashboard Tab**
2. Select today's date on the calendar
3. Add a task: "Test Task"
4. Click **"Complete"** button
5. Watch the chart update

### Test Garden
1. Go to **Garden Tab**
2. You should see 0 blocks (not yet earned)
3. Go back to Dashboard and complete 3 tasks
4. Return to Garden - should show 1 block (if 60%+ completion)

### Test Friends
1. Go to **Friends Tab**
2. Create a second account (new username)
3. Log in as first user
4. In Friends tab, add second user by username
5. Verify "Friend request sent"

### Test Profile
1. Go to **Profile Tab**
2. Write a bio: "I love productivity!"
3. Add a profile picture URL: `https://ui-avatars.com/api/?name=John`
4. Click **"Save Profile"**
5. Go back to Friends and view the friend's profile - see the bio and picture

### Test Groups
1. Go to **Groups Tab**
2. Click **"Create Group"**
3. Name it "Study Buddies"
4. Invite friends
5. Send a message in the group chat
6. Verify auto-refresh (chat updates every 2 seconds)

### Test Leaderboard
1. Go to **Leaderboard Tab**
2. See all users ranked by garden blocks
3. Click **"Profile"** to see any user's profile
4. Verify profile picture displays next to username

## 📚 Database Schema Reference

### 1. users
Core authentication table
| Column | Type | Notes |
|--------|------|-------|
| id | BIGINT | Primary key (auto-increment) |
| username | TEXT | Unique, required |
| password | TEXT | Plaintext (use bcrypt in production) |
| created_at | TIMESTAMP | Auto-set to now |

### 2. tasks
Daily task tracking for dashboard
| Column | Type | Notes |
|--------|------|-------|
| id | BIGINT | Primary key |
| user_id | BIGINT | Foreign key → users.id |
| date | DATE | Task date (YYYY-MM-DD) |
| task_name | TEXT | Task description |
| tasks_completed | INT | 0 = incomplete, 1 = complete |
| focus_time | INT | Minutes spent in focus session |
| timestamp | TIMESTAMP | Created time |

### 3. garden_state
Garden gamification system
| Column | Type | Notes |
|--------|------|-------|
| id | BIGINT | Primary key |
| user_id | BIGINT | Foreign key (UNIQUE) → users.id |
| block_count | INT | Number of garden blocks earned |
| is_dead | BOOLEAN | True if garden died (3+ days inactive) |
| last_activity | DATE | Last day task completion was tracked |
| last_block_award_date | DATE | Last day a block was awarded |
| created_at | TIMESTAMP | Initial creation time |

**Logic:**
- Earn 1 block per day if completion >= 60%
- Max 1 block per day (tracked by `last_block_award_date`)
- Garden dies if 3+ days of inactivity (< 60% completion)
- Can be replanted anytime

### 4. friends
Friend connections and requests
| Column | Type | Notes |
|--------|------|-------|
| id | BIGINT | Primary key |
| user_id | BIGINT | Who sent the request |
| friend_id | BIGINT | Who received the request |
| status | TEXT | 'pending', 'accepted', or 'declined' |
| created_at | TIMESTAMP | Request creation time |
| (user_id, friend_id) | UNIQUE | Prevent duplicate requests |

**Status values:**
- `pending` - Awaiting response
- `accepted` - Friends can view each other's profiles
- `declined` - Request rejected

### 5. user_profiles
Profile bio and pictures
| Column | Type | Notes |
|--------|------|-------|
| id | BIGINT | Primary key |
| user_id | BIGINT | Foreign key (UNIQUE) → users.id |
| bio | TEXT | User's bio (max. 500 chars) |
| pfp_url | TEXT | Profile picture URL |
| created_at | TIMESTAMP | Profile creation time |

**Notes:**
- One profile per user (UNIQUE constraint)
- Picture stored as URL (not uploaded file)
- Auto-created when user signs up

### 6. groups
Group collaboration spaces
| Column | Type | Notes |
|--------|------|-------|
| id | BIGINT | Primary key |
| user_id | BIGINT | Creator/owner → users.id |
| group_name | TEXT | Group display name |
| created_at | TIMESTAMP | Creation time |

**Permissions:**
- Only creator can delete group or invite friends
- Any member can send messages
- Creators can remove members

### 7. group_members
Tracks who's in each group
| Column | Type | Notes |
|--------|------|-------|
| id | BIGINT | Primary key |
| group_id | BIGINT | Foreign key → groups.id |
| user_id | BIGINT | Foreign key → users.id |
| created_at | TIMESTAMP | Join time |
| (group_id, user_id) | UNIQUE | Prevent duplicate members |

### 8. group_messages
Group chat message history
| Column | Type | Notes |
|--------|------|-------|
| id | BIGINT | Primary key |
| group_id | BIGINT | Foreign key → groups.id |
| user_id | BIGINT | Who sent message → users.id |
| username | TEXT | Sender's username (cached) |
| message | TEXT | Message content |
| created_at | TIMESTAMP | When sent |

**Design:**
- All messages stored (no deletion)
- Sorted by `created_at` ascending
- Auto-refreshes every 2 seconds in UI

## 🔗 Useful Supabase Links

- **Supabase Website**: https://supabase.com
- **Official Docs**: https://supabase.com/docs
- **SQL Tutorial**: https://www.postgresql.org/docs/
- **PostgreSQL Docs**: https://www.postgresql.org/

## 🆘 Troubleshooting

### "Supabase not configured yet"
**Problem:** App won't connect to database
**Solution:**
1. Check `.env` file exists in project root
2. Verify `SUPABASE_URL` format: `https://xxxxx.supabase.co`
3. Verify `SUPABASE_KEY` is copied exactly
4. Restart `flask run`
5. Check browser console (F12) for network errors

### "Duplicate key value violates unique constraint"
**Problem:** Can't sign up with username
**Solution:**
1. Username is taken (case-insensitive)
2. Choose a different username
3. Check in Supabase console: Settings → Users

### "Invalid credentials" on login
**Problem:** Can't log in
**Solution:**
1. Username and password are case-sensitive
2. Verify username exists (signup first)
3. Verify password matches exactly
4. Check Supabase console for user entry

### "Not friends" error when viewing profile
**Problem:** Can't see friend's profile
**Solution:**
1. Must be accepted friends (bidirectional)
2. Check Friends tab - verify friendship is "accepted"
3. Make sure friend also accepted your request
4. Verify `user_profiles` table exists with profile entry

### "SyntaxError in SQL"
**Problem:** SQL script fails to run
**Solution:**
1. Copy the entire script (including comments)
2. Don't modify the script
3. Use **"New Query"** button
4. Click **"Run"** (blue button), not "Save"

### Port 5000 already in use
**Problem:** "Address already in use"
**Solution:**
```bash
# Use a different port
flask run --port 5001
```

### Chart/tasks not updating
**Problem:** Added tasks but nothing shows
**Solution:**
1. Refresh page (Ctrl+R or Cmd+R)
2. Open browser console (F12)
3. Check Network tab for `/api/` errors
4. Verify logged in (check session)
5. Ensure task has a date selected

### Garden blocks not earning
**Problem:** Completed tasks but no blocks
**Solution:**
1. Need >= 60% completion (e.g., 3 of 5 tasks)
2. Only 1 block per day
3. Check `last_block_award_date` in Supabase
4. Refresh Dashboard tab to trigger update

### Chat not auto-refreshing
**Problem:** Messages don't appear without refresh
**Solution:**
1. Check browser console (F12) for errors
2. Verify `/api/group/<id>/messages` works
3. Ensure group_messages table created
4. Check that you're in the group (group_members table)

---

## ✨ You're All Set!

Your TeamMate productivity platform is now ready. Start with the Quick Start section in [README.md](README.md) to begin using the app! 🚀
