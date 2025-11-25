import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="My Calendar",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Dark Theme CSS
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Dark Theme */
    :root {
        --bg-primary: #1a1a1a;
        --bg-secondary: #242424;
        --bg-tertiary: #2d2d2d;
        --text-primary: #ffffff;
        --text-secondary: #b0b0b0;
        --accent-primary: #6366f1;
        --accent-hover: #4f46e5;
        --border-color: #3d3d3d;
        --success: #10b981;
        --warning: #f59e0b;
        --error: #ef4444;
    }
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main container */
    .main {
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }
    
    .block-container {
        padding: 2rem !important;
        max-width: 100% !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border-color);
    }
    
    [data-testid="stSidebar"] * {
        color: var(--text-primary) !important;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }
    
    /* Calendar container */
    .calendar-wrapper {
        background: var(--bg-secondary);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        border: 1px solid var(--border-color);
    }
    
    /* FullCalendar Dark Theme Overrides */
    .fc {
        background: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        border-radius: 12px !important;
    }
    
    .fc-theme-standard .fc-scrollgrid {
        border-color: var(--border-color) !important;
    }
    
    .fc-theme-standard td, 
    .fc-theme-standard th {
        border-color: var(--border-color) !important;
    }
    
    .fc-toolbar-title {
        font-size: 1.75rem !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
    }
    
    /* Calendar buttons */
    .fc-button {
        background: var(--accent-primary) !important;
        border: none !important;
        padding: 0.6rem 1.2rem !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        text-transform: capitalize !important;
        color: white !important;
    }
    
    .fc-button:hover {
        background: var(--accent-hover) !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
    }
    
    .fc-button:active {
        transform: translateY(0);
    }
    
    .fc-button-primary:not(:disabled).fc-button-active {
        background: var(--accent-hover) !important;
    }
    
    .fc-today-button {
        background: var(--bg-tertiary) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
    }
    
    .fc-today-button:hover {
        background: var(--border-color) !important;
    }
    
    /* Calendar header cells */
    .fc-col-header-cell {
        background: var(--bg-tertiary) !important;
        color: var(--text-secondary) !important;
        padding: 1rem 0 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        border-color: var(--border-color) !important;
    }
    
    /* Time slots */
    .fc-timegrid-slot {
        height: 3.5rem !important;
        border-color: var(--border-color) !important;
    }
    
    .fc-timegrid-slot-label {
        color: var(--text-secondary) !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }
    
    .fc-timegrid-axis {
        background: var(--bg-tertiary) !important;
    }
    
    /* Day cells */
    .fc-daygrid-day, .fc-timegrid-col {
        background: var(--bg-secondary) !important;
    }
    
    .fc-day-today {
        background: rgba(99, 102, 241, 0.1) !important;
        border: 1px solid var(--accent-primary) !important;
    }
    
    .fc-daygrid-day-number {
        color: var(--text-primary) !important;
        font-weight: 500 !important;
        padding: 0.5rem !important;
    }
    
    /* Events */
    .fc-event {
        border-radius: 6px !important;
        border: none !important;
        padding: 4px 8px !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
    }
    
    .fc-event:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5) !important;
    }
    
    .fc-event-time {
        font-weight: 600 !important;
    }
    
    .fc-event-title {
        font-weight: 500 !important;
    }
    
    /* All-day events */
    .fc-daygrid-event {
        margin: 2px 4px !important;
        padding: 4px 8px !important;
    }
    
    /* Now indicator */
    .fc-timegrid-now-indicator-line {
        border-color: var(--error) !important;
        border-width: 2px !important;
    }
    
    .fc-timegrid-now-indicator-arrow {
        border-color: var(--error) !important;
    }
    
    /* Selection highlighting */
    .fc-highlight {
        background: rgba(99, 102, 241, 0.2) !important;
    }
    
    /* Streamlit components dark theme */
    .stButton > button {
        background: var(--accent-primary) !important;
        color: white !important;
        border: none !important;
        padding: 0.6rem 1.5rem !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: var(--accent-hover) !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    
    /* Text inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: var(--bg-tertiary) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        padding: 0.6rem !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
    }
    
    /* Select boxes */
    .stSelectbox > div > div,
    .stDateInput > div > div,
    .stTimeInput > div > div {
        background: var(--bg-tertiary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
    }
    
    .stSelectbox div[data-baseweb="select"] > div {
        background: var(--bg-tertiary) !important;
        color: var(--text-primary) !important;
    }
    
    /* Checkbox */
    .stCheckbox {
        color: var(--text-primary) !important;
    }
    
    /* Form */
    .stForm {
        background: var(--bg-tertiary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
    }
    
    /* Success/Warning/Error messages */
    .stSuccess {
        background: rgba(16, 185, 129, 0.1) !important;
        color: var(--success) !important;
        border: 1px solid var(--success) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    .stWarning {
        background: rgba(245, 158, 11, 0.1) !important;
        color: var(--warning) !important;
        border: 1px solid var(--warning) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.1) !important;
        color: var(--error) !important;
        border: 1px solid var(--error) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    .stInfo {
        background: rgba(99, 102, 241, 0.1) !important;
        color: var(--accent-primary) !important;
        border: 1px solid var(--accent-primary) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    /* Divider */
    hr {
        border-color: var(--border-color) !important;
        margin: 1.5rem 0 !important;
    }
    
    /* Labels */
    label {
        color: var(--text-primary) !important;
        font-weight: 500 !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border-color);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .block-container {
            padding: 1rem !important;
        }
        
        .fc-toolbar {
            flex-direction: column !important;
            gap: 0.5rem !important;
        }
        
        .fc-toolbar-chunk {
            margin: 0.25rem 0 !important;
        }
        
        .fc-button {
            padding: 0.5rem 1rem !important;
            font-size: 0.875rem !important;
        }
        
        .fc-timegrid-slot {
            height: 3rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'events' not in st.session_state:
    st.session_state.events = []
if 'selected_event' not in st.session_state:
    st.session_state.selected_event = None
if 'show_form' not in st.session_state:
    st.session_state.show_form = False

# Event color palette - Dark theme friendly
EVENT_COLORS = {
    "Work": "#6366f1",
    "Personal": "#06b6d4",
    "Meeting": "#8b5cf6",
    "Important": "#ef4444",
    "Health": "#10b981",
    "Social": "#f59e0b",
    "Other": "#6b7280"
}

def check_event_conflict(new_event, existing_events):
    """Check if new event conflicts with existing events"""
    conflicts = []
    new_start = datetime.fromisoformat(new_event['start'].replace('Z', ''))
    new_end = datetime.fromisoformat(new_event['end'].replace('Z', ''))
    
    for event in existing_events:
        if event.get('id') == new_event.get('id'):
            continue
        
        if event.get('allDay', False) or new_event.get('allDay', False):
            continue
            
        event_start = datetime.fromisoformat(event['start'].replace('Z', ''))
        event_end = datetime.fromisoformat(event['end'].replace('Z', ''))
        
        if (new_start < event_end and new_end > event_start):
            conflicts.append(event)
    
    return conflicts

# Main app
def main():
    # Header
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("# 📅 My Calendar")
        st.markdown("*Create events by dragging on the calendar or using the sidebar*")
    
    with col2:
        if st.button("🔄 Refresh View"):
            st.rerun()
    
    st.markdown("---")
    
    # Sidebar for event creation/editing
    with st.sidebar:
        st.markdown("### Event Manager")
        
        # Show form when needed
        if st.session_state.show_form or st.session_state.selected_event:
            
            # Get event data if editing
            editing_event = st.session_state.selected_event
            is_editing = editing_event is not None
            
            st.markdown(f"#### {'✏️ Edit Event' if is_editing else '➕ New Event'}")
            
            # Form for creating/editing event
            with st.form("event_form", clear_on_submit=True):
                event_title = st.text_input(
                    "Event Title *", 
                    value=editing_event.get('title', '') if is_editing else '',
                    placeholder="e.g., Team Meeting"
                )
                
                event_category = st.selectbox(
                    "Category", 
                    options=list(EVENT_COLORS.keys()),
                    index=list(EVENT_COLORS.keys()).index(
                        editing_event.get('extendedProps', {}).get('category', 'Work')
                    ) if is_editing else 0
                )
                
                is_all_day = st.checkbox(
                    "All-day event",
                    value=editing_event.get('allDay', False) if is_editing else False
                )
                
                # Date and time selection
                if is_editing:
                    default_date = datetime.fromisoformat(editing_event['start'].replace('Z', '')).date()
                    default_start_time = datetime.fromisoformat(editing_event['start'].replace('Z', '')).time()
                    default_end_time = datetime.fromisoformat(editing_event['end'].replace('Z', '')).time()
                else:
                    default_date = datetime.now().date()
                    default_start_time = datetime.now().replace(minute=0, second=0, microsecond=0).time()
                    default_end_time = (datetime.now().replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)).time()
                
                event_date = st.date_input("Date *", value=default_date)
                
                if not is_all_day:
                    col1, col2 = st.columns(2)
                    with col1:
                        event_start_time = st.time_input("Start Time *", value=default_start_time)
                    with col2:
                        event_end_time = st.time_input("End Time *", value=default_end_time)
                else:
                    event_start_time = datetime.min.time()
                    event_end_time = datetime.min.time()
                
                event_description = st.text_area(
                    "Description (optional)",
                    value=editing_event.get('extendedProps', {}).get('description', '') if is_editing else '',
                    placeholder="Add details about this event..."
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    submitted = st.form_submit_button("💾 Save", use_container_width=True)
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
                        'id': editing_event.get('id', str(datetime.now().timestamp())) if is_editing else str(datetime.now().timestamp()),
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
                    
                    if conflicts and not is_all_day:
                        conflict_titles = ", ".join([c['title'] for c in conflicts[:2]])
                        st.warning(f"⚠️ Warning: Overlaps with {conflict_titles}")
                    
                    # Update or add event
                    if is_editing:
                        st.session_state.events = [e for e in st.session_state.events if e['id'] != new_event['id']]
                    
                    st.session_state.events.append(new_event)
                    
                    st.success("✅ Event saved successfully!")
                    st.session_state.show_form = False
                    st.session_state.selected_event = None
                    st.rerun()
                
                if cancelled:
                    st.session_state.show_form = False
                    st.session_state.selected_event = None
                    st.rerun()
            
            # Delete button for existing events
            if is_editing:
                st.markdown("---")
                if st.button("🗑️ Delete Event", use_container_width=True, type="secondary"):
                    st.session_state.events = [e for e in st.session_state.events if e['id'] != editing_event['id']]
                    st.session_state.selected_event = None
                    st.session_state.show_form = False
                    st.success("✅ Event deleted!")
                    st.rerun()
        
        else:
            # Show instructions when no form is active
            if st.button("➕ Create New Event", use_container_width=True):
                st.session_state.show_form = True
                st.session_state.selected_event = None
                st.rerun()
            
            st.markdown("---")
            st.info("""
            **Quick Tips:**
            
            🖱️ **Drag** on the calendar to create events quickly
            
            👆 **Click** an event to edit or delete it
            
            📱 **Responsive** design works on all devices
            
            ⚠️ **Conflict detection** warns about overlaps
            
            🎨 **Color coding** helps organize by category
            """)
            
            # Event statistics
            if st.session_state.events:
                st.markdown("---")
                st.markdown("### 📊 Your Events")
                st.metric("Total Events", len(st.session_state.events))
                
                # Count by category
                categories = {}
                for event in st.session_state.events:
                    cat = event.get('extendedProps', {}).get('category', 'Other')
                    categories[cat] = categories.get(cat, 0) + 1
                
                for cat, count in categories.items():
                    st.markdown(f"**{cat}:** {count}")
    
    # Calendar configuration with improved settings
    calendar_options = {
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,timeGridDay"
        },
        "initialView": "timeGridWeek",
        "selectable": True,
        "selectMirror": True,
        "dayMaxEvents": True,
        "weekends": True,
        "nowIndicator": True,
        "editable": True,
        "eventStartEditable": True,
        "eventDurationEditable": True,
        "slotMinTime": "06:00:00",
        "slotMaxTime": "22:00:00",
        "slotDuration": "00:30:00",
        "height": 700,
        "expandRows": True,
        "allDaySlot": True,
        "selectMinDistance": 5,
        "eventTimeFormat": {
            "hour": "2-digit",
            "minute": "2-digit",
            "meridiem": "short"
        },
        "slotLabelFormat": {
            "hour": "2-digit",
            "minute": "2-digit",
            "meridiem": "short"
        }
    }
    
    # Custom CSS for better event display
    custom_css = """
        .fc-event {
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .fc-event:hover {
            transform: translateY(-2px);
        }
        .fc-daygrid-event-dot {
            display: none;
        }
    """
    
    # Render calendar with wrapper
    st.markdown('<div class="calendar-wrapper">', unsafe_allow_html=True)
    
    state = calendar(
        events=st.session_state.events,
        options=calendar_options,
        custom_css=custom_css,
        key="calendar_component"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle calendar interactions
    if state.get("eventClick"):
        clicked_event = state["eventClick"]["event"]
        st.session_state.selected_event = clicked_event
        st.session_state.show_form = True
        st.rerun()
    
    if state.get("select"):
        selection = state["select"]
        
        # Parse the selection dates
        start_str = selection["start"]
        end_str = selection["end"]
        
        # Remove timezone info if present
        if start_str.endswith('Z'):
            start_str = start_str[:-1]
        if end_str.endswith('Z'):
            end_str = end_str[:-1]
        
        start_time = datetime.fromisoformat(start_str)
        end_time = datetime.fromisoformat(end_str)
        is_all_day = selection.get("allDay", False)
        
        # Create a quick event from drag selection
        quick_event = {
            'id': str(datetime.now().timestamp()),
            'title': 'New Event',
            'start': start_time.isoformat(),
            'end': end_time.isoformat(),
            'backgroundColor': EVENT_COLORS["Work"],
            'borderColor': EVENT_COLORS["Work"],
            'allDay': is_all_day,
            'extendedProps': {
                'category': 'Work',
                'description': ''
            }
        }
        
        st.session_state.selected_event = quick_event
        st.session_state.show_form = True
        st.rerun()
    
    # Handle event drag/resize (update event times)
    if state.get("eventChange"):
        changed_event = state["eventChange"]["event"]
        event_id = changed_event["id"]
        
        # Update the event in session state
        for i, event in enumerate(st.session_state.events):
            if event["id"] == event_id:
                st.session_state.events[i]["start"] = changed_event["start"]
                st.session_state.events[i]["end"] = changed_event["end"]
                break
        
        st.success("✅ Event time updated!")
        st.rerun()

if __name__ == "__main__":
    main()