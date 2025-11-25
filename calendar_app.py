import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime, timedelta
import json
from supabase import create_client, Client
import os

# Page configuration
st.set_page_config(
    page_title="My Calendar",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Microsoft Teams-like design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .main {
        padding: 0 !important;
        background: #f5f5f5;
    }
    
    .block-container {
        padding: 1rem 2rem !important;
        max-width: 100% !important;
    }
    
    /* Calendar header */
    .calendar-header {
        background: white;
        padding: 1.5rem 2rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .calendar-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: #252423;
        margin: 0;
    }
    
    /* Calendar container */
    .calendar-wrapper {
        background: white;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        padding: 1rem;
        min-height: 600px;
    }
    
    /* FullCalendar overrides for Teams style */
    .fc {
        border-radius: 8px;
    }
    
    .fc-toolbar-title {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        color: #252423 !important;
    }
    
    .fc-button {
        background: #6264A7 !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
        border-radius: 4px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    
    .fc-button:hover {
        background: #464775 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    
    .fc-button:active {
        background: #33344A !important;
    }
    
    .fc-button-primary:not(:disabled).fc-button-active {
        background: #464775 !important;
    }
    
    .fc-today-button {
        background: white !important;
        color: #6264A7 !important;
        border: 1px solid #6264A7 !important;
    }
    
    .fc-today-button:hover {
        background: #f5f5f9 !important;
    }
    
    /* Time grid */
    .fc-timegrid-slot {
        height: 3rem !important;
    }
    
    .fc-timegrid-slot-label {
        font-size: 0.875rem !important;
        color: #605E5C !important;
    }
    
    .fc-col-header-cell {
        padding: 1rem 0 !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        color: #252423 !important;
        background: #f5f5f9 !important;
    }
    
    .fc-day-today {
        background: #F3F2F1 !important;
    }
    
    /* Events */
    .fc-event {
        border-radius: 4px !important;
        border: none !important;
        padding: 2px 4px !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        cursor: pointer !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1) !important;
    }
    
    .fc-event:hover {
        box-shadow: 0 2px 4px rgba(0,0,0,0.15) !important;
    }
    
    .fc-event-time {
        font-weight: 600 !important;
    }
    
    /* Conflict warning */
    .conflict-event {
        border-left: 4px solid #C4314B !important;
        background: #FDE7E9 !important;
    }
    
    /* All-day events */
    .fc-daygrid-event {
        margin: 2px 4px !important;
        padding: 4px 8px !important;
        border-radius: 4px !important;
    }
    
    /* Streamlit components */
    .stButton > button {
        background: #6264A7;
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 4px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: #464775;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stTextInput > div > div > input {
        border-radius: 4px;
        border: 1px solid #D1D1D1;
        padding: 0.5rem;
    }
    
    .stSelectbox > div > div {
        border-radius: 4px;
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .block-container {
            padding: 0.5rem 1rem !important;
        }
        
        .calendar-header {
            padding: 1rem;
            flex-direction: column;
            gap: 1rem;
        }
        
        .calendar-title {
            font-size: 1.25rem;
        }
        
        .fc-toolbar {
            flex-direction: column !important;
            gap: 0.5rem !important;
        }
        
        .fc-toolbar-chunk {
            margin: 0.25rem 0 !important;
        }
        
        .fc-button {
            padding: 0.4rem 0.8rem !important;
            font-size: 0.875rem !important;
        }
        
        .fc-timegrid-slot {
            height: 2.5rem !important;
        }
        
        .fc-timegrid-slot-label {
            font-size: 0.75rem !important;
        }
    }
    
    /* Success/Error messages */
    .stSuccess, .stError, .stWarning {
        border-radius: 4px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Supabase client
@st.cache_resource
def init_supabase():
    """Initialize Supabase client with credentials"""
    supabase_url = os.environ.get("SUPABASE_URL") or st.secrets.get("SUPABASE_URL", "")
    supabase_key = os.environ.get("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY", "")
    
    if supabase_url and supabase_key:
        return create_client(supabase_url, supabase_key)
    return None

# Initialize session state
if 'events' not in st.session_state:
    st.session_state.events = []
if 'selected_event' not in st.session_state:
    st.session_state.selected_event = None
if 'show_conflict_warning' not in st.session_state:
    st.session_state.show_conflict_warning = False

# Event color palette (Teams-inspired)
EVENT_COLORS = {
    "Work": "#6264A7",
    "Personal": "#00B7C3",
    "Meeting": "#8764B8",
    "Important": "#C4314B",
    "Health": "#038387",
    "Other": "#107C10"
}

def check_event_conflict(new_event, existing_events):
    """Check if new event conflicts with existing events"""
    conflicts = []
    new_start = datetime.fromisoformat(new_event['start'].replace('Z', '+00:00'))
    new_end = datetime.fromisoformat(new_event['end'].replace('Z', '+00:00'))
    
    for event in existing_events:
        if event.get('id') == new_event.get('id'):
            continue
            
        event_start = datetime.fromisoformat(event['start'].replace('Z', '+00:00'))
        event_end = datetime.fromisoformat(event['end'].replace('Z', '+00:00'))
        
        # Check for overlap
        if (new_start < event_end and new_end > event_start):
            conflicts.append(event)
    
    return conflicts

def save_event_to_supabase(event):
    """Save event to Supabase database"""
    supabase = init_supabase()
    if supabase:
        try:
            response = supabase.table('calendar_events').upsert(event).execute()
            return True
        except Exception as e:
            st.error(f"Error saving to database: {str(e)}")
            return False
    return False

def load_events_from_supabase():
    """Load events from Supabase database"""
    supabase = init_supabase()
    if supabase:
        try:
            response = supabase.table('calendar_events').select("*").execute()
            return response.data
        except Exception as e:
            st.warning(f"Could not load from database: {str(e)}")
            return []
    return []

def delete_event_from_supabase(event_id):
    """Delete event from Supabase database"""
    supabase = init_supabase()
    if supabase:
        try:
            supabase.table('calendar_events').delete().eq('id', event_id).execute()
            return True
        except Exception as e:
            st.error(f"Error deleting from database: {str(e)}")
            return False
    return False

# Load events from Supabase on startup
if not st.session_state.events:
    st.session_state.events = load_events_from_supabase()

# Main app
def main():
    # Header
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("<h1 class='calendar-title'>📅 My Calendar</h1>", unsafe_allow_html=True)
    
    with col2:
        if st.button("➕ New Event", use_container_width=True):
            st.session_state.show_new_event = True
    
    with col3:
        if st.button("🔄 Refresh", use_container_width=True):
            st.session_state.events = load_events_from_supabase()
            st.rerun()
    
    st.markdown("---")
    
    # Sidebar for event creation/editing
    with st.sidebar:
        st.header("Event Details")
        
        if st.session_state.get('show_new_event', False) or st.session_state.selected_event:
            
            # Form for creating/editing event
            with st.form("event_form"):
                event_title = st.text_input("Event Title", 
                    value=st.session_state.selected_event.get('title', '') if st.session_state.selected_event else '')
                
                event_category = st.selectbox("Category", 
                    options=list(EVENT_COLORS.keys()),
                    index=0)
                
                is_all_day = st.checkbox("All-day event")
                
                col1, col2 = st.columns(2)
                with col1:
                    event_date = st.date_input("Date", 
                        value=datetime.now())
                
                if not is_all_day:
                    with col2:
                        event_start_time = st.time_input("Start Time", 
                            value=datetime.now().replace(minute=0, second=0))
                    
                    event_duration = st.selectbox("Duration", 
                        options=["15 min", "30 min", "1 hour", "2 hours", "3 hours", "Custom"],
                        index=2)
                    
                    if event_duration == "Custom":
                        event_end_time = st.time_input("End Time")
                    else:
                        duration_map = {"15 min": 15, "30 min": 30, "1 hour": 60, "2 hours": 120, "3 hours": 180}
                        minutes = duration_map[event_duration]
                        event_end_time = (datetime.combine(event_date, event_start_time) + 
                                        timedelta(minutes=minutes)).time()
                
                event_description = st.text_area("Description (optional)")
                
                col1, col2 = st.columns(2)
                with col1:
                    submitted = st.form_submit_button("💾 Save Event", use_container_width=True)
                with col2:
                    cancelled = st.form_submit_button("❌ Cancel", use_container_width=True)
                
                if submitted and event_title:
                    # Create event object
                    if is_all_day:
                        start_datetime = datetime.combine(event_date, datetime.min.time())
                        end_datetime = start_datetime + timedelta(days=1)
                    else:
                        start_datetime = datetime.combine(event_date, event_start_time)
                        end_datetime = datetime.combine(event_date, event_end_time)
                    
                    new_event = {
                        'id': st.session_state.selected_event.get('id', str(datetime.now().timestamp())) if st.session_state.selected_event else str(datetime.now().timestamp()),
                        'title': event_title,
                        'start': start_datetime.isoformat(),
                        'end': end_datetime.isoformat(),
                        'backgroundColor': EVENT_COLORS[event_category],
                        'borderColor': EVENT_COLORS[event_category],
                        'allDay': is_all_day,
                        'extendedProps': {
                            'category': event_category,
                            'description': event_description
                        }
                    }
                    
                    # Check for conflicts
                    conflicts = check_event_conflict(new_event, st.session_state.events)
                    
                    if conflicts:
                        st.warning(f"⚠️ Conflict Warning: This event overlaps with {len(conflicts)} existing event(s)")
                        if st.checkbox("Allow conflict and save anyway"):
                            # Add conflict indicator
                            new_event['className'] = 'conflict-event'
                            
                            # Update or add event
                            if st.session_state.selected_event:
                                st.session_state.events = [e for e in st.session_state.events 
                                                          if e['id'] != new_event['id']]
                            st.session_state.events.append(new_event)
                            
                            # Save to Supabase
                            save_event_to_supabase(new_event)
                            
                            st.success("✅ Event saved with conflict warning!")
                            st.session_state.show_new_event = False
                            st.session_state.selected_event = None
                            st.rerun()
                    else:
                        # Update or add event
                        if st.session_state.selected_event:
                            st.session_state.events = [e for e in st.session_state.events 
                                                      if e['id'] != new_event['id']]
                        st.session_state.events.append(new_event)
                        
                        # Save to Supabase
                        save_event_to_supabase(new_event)
                        
                        st.success("✅ Event saved successfully!")
                        st.session_state.show_new_event = False
                        st.session_state.selected_event = None
                        st.rerun()
                
                if cancelled:
                    st.session_state.show_new_event = False
                    st.session_state.selected_event = None
                    st.rerun()
        
        else:
            st.info("Click '➕ New Event' to create an event, or drag on the calendar to create one!")
            st.markdown("### Quick Tips")
            st.markdown("""
            - 🖱️ **Drag** on the calendar to create events
            - 👆 **Click** an event to edit or delete
            - 📱 Works great on mobile!
            - ⚠️ Conflicts are detected but allowed
            - 🔄 Auto-syncs with cloud database
            """)
    
    # Calendar configuration
    calendar_options = {
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "timeGridDay,timeGridWeek"
        },
        "initialView": "timeGridDay",
        "selectable": True,
        "selectMirror": True,
        "dayMaxEvents": True,
        "weekends": True,
        "nowIndicator": True,
        "editable": True,
        "droppable": True,
        "eventDurationEditable": True,
        "eventStartEditable": True,
        "slotMinTime": "06:00:00",
        "slotMaxTime": "22:00:00",
        "slotDuration": "00:30:00",
        "height": 650,
        "expandRows": True,
        "allDaySlot": True,
        "eventTimeFormat": {
            "hour": "2-digit",
            "minute": "2-digit",
            "meridiem": "short"
        }
    }
    
    # Custom JS for handling calendar interactions
    custom_css = """
        .fc-event {
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .fc-event:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.15) !important;
        }
    """
    
    # Render calendar
    calendar_events = st.session_state.events
    
    state = calendar(
        events=calendar_events,
        options=calendar_options,
        custom_css=custom_css,
        key="calendar"
    )
    
    # Handle calendar interactions
    if state.get("eventClick"):
        clicked_event = state["eventClick"]["event"]
        st.session_state.selected_event = clicked_event
        st.session_state.show_new_event = True
        st.rerun()
    
    if state.get("select"):
        selection = state["select"]
        
        # Create a new event from selection
        start_time = datetime.fromisoformat(selection["start"].replace('Z', '+00:00'))
        end_time = datetime.fromisoformat(selection["end"].replace('Z', '+00:00'))
        
        quick_event = {
            'id': str(datetime.now().timestamp()),
            'title': 'New Event',
            'start': start_time.isoformat(),
            'end': end_time.isoformat(),
            'backgroundColor': EVENT_COLORS["Work"],
            'borderColor': EVENT_COLORS["Work"],
            'allDay': selection.get("allDay", False),
            'extendedProps': {
                'category': 'Work',
                'description': ''
            }
        }
        
        st.session_state.selected_event = quick_event
        st.session_state.show_new_event = True
        st.rerun()
    
    # Delete event
    if st.session_state.selected_event and st.sidebar.button("🗑️ Delete Event", use_container_width=True):
        event_id = st.session_state.selected_event['id']
        st.session_state.events = [e for e in st.session_state.events if e['id'] != event_id]
        delete_event_from_supabase(event_id)
        st.session_state.selected_event = None
        st.session_state.show_new_event = False
        st.success("✅ Event deleted!")
        st.rerun()

if __name__ == "__main__":
    main()
