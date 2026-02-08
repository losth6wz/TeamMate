# TeamMate 🌱 - Social Productivity Gamification Platform

A modern, full-featured productivity tracker with gamification, social features, and collaborative groups. Built with Flask and Supabase.

## ✨ Features

### 📊 Task Management
- **Calendar-based task tracking** - View tasks by date with an interactive calendar
- **Daily dashboard** - See all tasks for a selected date with completion tracking
- **Stacked bar chart** - Visualize productivity trends over time with Chart.js
- **Task completion tracking** - Mark tasks complete/incomplete and track completion percentage

### 🌸 Garden Gamification
- **Visual garden blocks** - Earn blocks for 60%+ daily task completion
- **One block per day max** - Sustainable gamification pattern
- **Garden death** - Garden dies after 3 days of inactivity (< 60% completion)
- **Garden replanting** - Revive your garden anytime
- **Block visualization** - See your blocks arranged in a cascading garden grid
- **Friend garden preview** - View your friends' gardens on their profiles

### 👥 Social Features
- **Friend requests** - Add friends by username with request/accept/decline workflow
- **Friend profiles** - View friends' bios, profile pictures, and garden previews
- **Remove friends** - End friendships at any time
- **Public leaderboard** - See all users ranked by garden blocks with profile access

### 💬 Groups & Collaboration
- **Create groups** - Start collaborative spaces with friends
- **Group chat** - Real-time messaging with cloud persistence and auto-refresh
- **Invite friends** - Add friends to groups you manage
- **Member management** - Remove members or entire groups
- **Chat history** - All messages stored in the cloud

### 👤 User Profiles
- **Bio section** - Write a bio about yourself
- **Profile picture** - Set a profile picture via URL
- **Read-only viewing** - Friends can see your profile (bio, picture, garden preview)
- **Profile privacy** - Only friends can view your profile

### 🎯 Focus Sessions
- **Pomodoro-style timer** - 25-minute focus sessions (adjustable)
- **Session tracking** - Track focus time spent
- **Real-time updates** - Timer updates every second

### 📈 Analytics
- **7-day productivity chart** - See task completion trends
- **Completion stats** - Track daily completion percentages
- **Cumulative visualization** - Stacked bar chart showing multiple task types

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Supabase account (free at https://supabase.com)

### Installation

**1. Install Dependencies**
```bash
pip install -r requirements.txt
```

**2. Create Supabase Project**
1. Go to https://supabase.com and sign up (free, no credit card)
2. Create a new project and choose a region
3. Wait 2-3 minutes for initialization

**3. Setup Database**
1. In Supabase, go to **SQL Editor**
2. Run the complete SQL script from [SUPABASE_SETUP.md](SUPABASE_SETUP.md)
3. This creates all 8 database tables

**4. Configure Environment**
1. Go to Supabase **Settings** → **API**
2. Copy `Project URL` and `anon public` key
3. Create `.env` file:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
```

**5. Run the App**
```bash
flask run
```
Visit `http://localhost:5000` 🎉

## 📁 Project Structure

```
TeamMate/
├── backend.py                      # Flask app with 40+ API routes
├── requirements.txt                # Python dependencies
├── .env                           # Your API credentials (create this)
├── .env.example                   # Environment template
├── README.md                       # This file
├── SUPABASE_SETUP.md             # Database setup guide
├── templates/
│   └── index.html                 # Full UI (1700+ lines)
│       ├── Dashboard Tab          # Tasks & chart
│       ├── Garden Tab             # Garden visualization
│       ├── Friends Tab            # Friend management & profiles
│       ├── Groups Tab             # Group creation & chat
│       ├── Profile Tab            # Your bio & picture
│       └── Leaderboard Tab        # Rankings & profiles
└── static/
    └── css/
        └── style.css              # Responsive styling (600+ lines)
```

## 🎮 How to Use

### Getting Started
1. **Sign Up** - Create account with username/password
2. **Login** - Access your dashboard

### Daily Workflow
1. **Dashboard Tab** - Add tasks for today
2. **Mark Complete** - Check off tasks as you finish them
3. **Track Progress** - See completion % update
4. **Earn Blocks** - Get a garden block if you hit 60%+ completion
5. **Monitor Chart** - Watch productivity trends over time

### Social Features
1. **Friends Tab** - Add friends by username
2. **View Profile** - Click friends to see their bio, picture, and garden
3. **Leaderboard** - See all users ranked by blocks

### Groups & Chat
1. **Groups Tab** - Create a new group
2. **Invite Friends** - Add friends to your group
3. **Chat** - Send messages in real-time (auto-refreshes every 2 seconds)
4. **Manage** - Remove members or delete groups

### Your Profile
1. **Profile Tab** - Write your bio and add picture URL
2. **Save** - Changes auto-save
3. **Preview** - See how friends will see your profile

### Focus Sessions
1. **Dashboard** - Click "Start Focus Session" button
2. **25 minutes** - Timer counts down
3. **Automatic tracking** - Time logged when complete

## 🔌 API Reference

### Authentication
```
POST /api/signup              → Register new user
POST /api/login               → Login with credentials
POST /api/logout              → Logout and clear session
GET  /api/user                → Get current user info
```

### Tasks & Dashboard
```
POST /api/save                → Create/update task
GET  /api/dashboard           → Get all user's tasks
DELETE /api/delete-task/<id>  → Delete specific task
```

### Garden
```
GET  /api/garden-state        → Get your garden (blocks, is_dead, last_activity)
GET  /api/user-garden/<id>    → Get friend's garden for preview
POST /api/update-garden       → Update garden (called on dashboard update)
POST /api/replant-garden      → Revive dead garden
```

### Friends
```
POST /api/add-friend          → Send friend request by username
GET  /api/friend-requests     → Get pending requests
POST /api/accept-request/<id> → Accept a request
POST /api/decline-request/<id>→ Decline a request
GET  /api/friends             → Get accepted friends
POST /api/remove-friend/<id>  → Remove a friend
```

### Profiles
```
POST /api/profile/update      → Update your bio & profile picture
GET  /api/profile/<user_id>   → Get friend's profile (read-only)
```

### Leaderboard
```
GET  /api/leaderboard         → Get all users ranked by blocks
```

### Groups
```
POST /api/create-group        → Create new group
GET  /api/my-groups           → Get your groups
GET  /api/group/<id>/members  → Get group members
POST /api/group/<id>/invite   → Invite friend to group
POST /api/group/<id>/remove-member → Remove member
POST /api/group/<id>/delete   → Delete entire group
POST /api/group/<id>/send-message  → Send message
GET  /api/group/<id>/messages → Get all messages
```

## 📊 Database Schema

**8 Tables:** users, tasks, garden_state, friends, user_profiles, groups, group_members, group_messages

See [SUPABASE_SETUP.md](SUPABASE_SETUP.md#-database-schema-reference) for complete schema details.

## ⚙️ Configuration

### Environment Variables
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-public-key
```

### Settings (in code)
- **Focus Timer**: 25 minutes (adjustable in `startFocusSession()`)
- **Garden Death**: 3+ days inactivity at < 60% completion
- **Block Award**: 60%+ completion per day (max 1 per day)
- **Chat Refresh**: Every 2 seconds

## 🔐 Security Notes

⚠️ **Development Features:**
- Plaintext passwords (for demo purposes)
- No rate limiting
- No CSRF protection

**For Production:**
- Use bcrypt for password hashing
- Enable HTTPS/SSL
- Add rate limiting on login/signup
- Implement CSRF tokens
- Add input validation/sanitization
- Use environment variable validation
- Implement user roles/permissions
- Add password reset functionality

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Supabase not configured" | Verify `.env` file with correct `SUPABASE_URL` and `SUPABASE_KEY` |
| Login fails | Username/password are case-sensitive; ensure user exists |
| Leaderboard shows "Unable to view profile" | Check user_profiles table is created and profile entry exists |
| Chat not auto-refreshing | Check browser console (F12) for errors; ensure `/api/group/<id>/messages` endpoint works |
| Garden not earning blocks | Need 60%+ completion; 1 block max per day |
| Port 5000 in use | Run `flask run --port 5001` |
| Tasks not saving | Check network tab (F12) for `/api/save` errors |

## 📱 Browser Support

- Chrome/Chromium (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (responsive design)

## 📝 License

MIT

---

**Ready to boost productivity?** See [SUPABASE_SETUP.md](SUPABASE_SETUP.md) for detailed setup instructions. 🚀
