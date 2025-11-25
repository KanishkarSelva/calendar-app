# 📅 Premium Calendar App

A beautiful, Microsoft Teams-inspired calendar application built with Streamlit. Perfect for managing your daily schedule with drag-and-drop event creation, conflict detection, and cloud sync.

## ✨ Features

- 🎯 **Day-by-day view** with time slots (Teams-style design)
- 🖱️ **Drag to create events** directly on the calendar grid
- ⏰ **Time-based booking** with flexible duration options
- 📆 **All-day events** with easy toggle
- ⚠️ **Smart conflict detection** with warnings (multiple events allowed)
- 📱 **Fully mobile responsive** - works great on phones and tablets
- 🎨 **Color-coded categories** (Work, Personal, Meeting, Important, Health, Other)
- ☁️ **Cloud sync** with Supabase database
- ✏️ **Edit and delete** events with ease
- 🔄 **Real-time updates** across devices

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/calendar-app.git
cd calendar-app
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Supabase (Free Tier)

1. Go to [supabase.com](https://supabase.com) and create a free account
2. Create a new project
3. Go to **SQL Editor** and run this query to create the events table:

```sql
CREATE TABLE calendar_events (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    start TIMESTAMP WITH TIME ZONE NOT NULL,
    "end" TIMESTAMP WITH TIME ZONE NOT NULL,
    "backgroundColor" TEXT,
    "borderColor" TEXT,
    "allDay" BOOLEAN DEFAULT false,
    "className" TEXT,
    "extendedProps" JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add index for faster queries
CREATE INDEX idx_calendar_events_start ON calendar_events(start);
CREATE INDEX idx_calendar_events_end ON calendar_events("end");
```

4. Get your **API URL** and **anon/public key** from **Settings > API**

### 4. Configure Secrets

Create a `.streamlit/secrets.toml` file:

```toml
SUPABASE_URL = "your-project-url.supabase.co"
SUPABASE_KEY = "your-anon-key-here"
```

### 5. Run Locally

```bash
streamlit run calendar_app.py
```

Visit `http://localhost:8501` to see your calendar!

## 🌐 Deploy to Streamlit Cloud (100% Free)

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Initial calendar app"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **"New app"**
4. Select your repository: `YOUR_USERNAME/calendar-app`
5. Set main file path: `calendar_app.py`
6. Click **"Advanced settings"** and add secrets:
   ```
   SUPABASE_URL = "your-project-url.supabase.co"
   SUPABASE_KEY = "your-anon-key-here"
   ```
7. Click **"Deploy"**!

Your app will be live at: `https://YOUR_USERNAME-calendar-app.streamlit.app`

## 📱 Mobile Usage

The calendar is fully responsive! On mobile:
- Swipe to navigate between days
- Tap time slots to create events
- Tap events to edit or delete
- Optimized touch targets for easy interaction

## 🎨 Customization

### Change Color Scheme

Edit the `EVENT_COLORS` dictionary in `calendar_app.py`:

```python
EVENT_COLORS = {
    "Work": "#6264A7",      # Teams purple
    "Personal": "#00B7C3",  # Cyan
    "Meeting": "#8764B8",   # Purple
    "Important": "#C4314B", # Red
    "Health": "#038387",    # Teal
    "Other": "#107C10"      # Green
}
```

### Adjust Time Range

Modify `calendar_options` in `calendar_app.py`:

```python
"slotMinTime": "06:00:00",  # Start time
"slotMaxTime": "22:00:00",  # End time
"slotDuration": "00:30:00", # 30-minute slots
```

## 🔧 Troubleshooting

### Events not saving?
- Check your Supabase credentials in secrets
- Verify the table was created correctly
- Check browser console for errors

### Calendar not displaying?
- Make sure `streamlit-calendar` is installed
- Clear browser cache
- Try incognito mode

### Mobile issues?
- Ensure you're using latest Streamlit version
- Check viewport meta tag is present
- Test on different browsers

## 🎯 Advanced Features (Coming Soon)

- 🔁 Recurring events
- 🔔 Email/SMS reminders
- 📤 Export to Google Calendar/iCal
- 📥 Import events from other calendars
- 🌓 Dark mode toggle
- 👥 Shared calendars
- 🔍 Event search and filters
- 📊 Time analytics dashboard

## 💡 Tips & Tricks

1. **Quick Event Creation**: Drag on the calendar grid for instant event creation
2. **Conflict Warnings**: System warns about overlaps but lets you save anyway
3. **All-Day Events**: Perfect for holidays, birthdays, or full-day commitments
4. **Category Colors**: Use consistent colors to quickly identify event types
5. **Mobile Friendly**: Add to your phone's home screen for app-like experience

## 🤝 Contributing

Feel free to fork this project and customize it for your needs! Some ideas:
- Add more event fields (location, attendees, notes)
- Integrate with Google Calendar API
- Add reminder notifications
- Create weekly/monthly views
- Add event templates

## 📄 License

MIT License - feel free to use this for personal or commercial projects!

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- Calendar component: [streamlit-calendar](https://github.com/im-perativa/streamlit-calendar)
- Database: [Supabase](https://supabase.com)
- Inspired by Microsoft Teams Calendar design

---

**Made with ❤️ for productivity enthusiasts**

Need help? Open an issue on GitHub or reach out!
