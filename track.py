import streamlit as st
import json
from datetime import datetime, timedelta

# Configure the page
st.set_page_config(
    page_title="60-Day ML Plan",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for mobile-friendly responsive design
st.markdown("""
<style>
    /* Base styles */
    .today-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .day-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #6c757d;
    }
    .completed-day {
        border-left: 4px solid #28a745 !important;
        background-color: #d4edda !important;
    }
    .overdue-day {
        border-left: 4px solid #dc3545 !important;
        background-color: #f8d7da !important;
    }
    .current-day {
        border-left: 4px solid #007bff !important;
        background-color: #cce7ff !important;
    }
    .task-item {
        margin: 0.3rem 0;
        padding: 0.2rem;
        word-wrap: break-word;
    }
    .completed-task {
        text-decoration: line-through;
        color: #6c757d;
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .today-card {
            padding: 1rem;
            margin: 0.5rem 0;
        }
        .day-card {
            padding: 0.8rem;
            margin: 0.3rem 0;
        }
        .task-item {
            font-size: 0.9rem;
            margin: 0.2rem 0;
        }
    }
    
    /* Checkbox styling for mobile */
    .stCheckbox > label {
        font-size: 1rem;
    }
    
    @media (max-width: 768px) {
        .stCheckbox > label {
            font-size: 0.9rem;
        }
    }
    
    /* Sidebar mobile optimization */
    @media (max-width: 768px) {
        .sidebar .sidebar-content {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'tasks' not in st.session_state:
    st.session_state.tasks = {}
if 'start_date' not in st.session_state:
    st.session_state.start_date = datetime.now().date()
if 'carry_over' not in st.session_state:
    st.session_state.carry_over = {}
if 'view_day' not in st.session_state:
    st.session_state.view_day = None

# Load the 60-day plan
def load_plan():
    return {
        1: ["Python setup, NumPy basics", "SQL SELECT basics", "GitHub repo setup"],
        2: ["Pandas operations, merge, groupby", "SQL WHERE, ORDER BY", "EDA on small dataset"],
        3: ["ML pipeline intro", "Linear Regression", "SQL JOINS"],
        4: ["Logistic Regression", "Encoding & scaling", "SQL Window Functions"],
        5: ["Decision Trees, Random Forest", "Feature Engineering", "SQL practice (10 problems)"],
        6: ["XGBoost", "GridSearchCV", "Mini ML project"],
        7: ["Week revision", "SQL mini test", "Resume improvement"],
        8: ["SVM, kernels", "SQL subqueries", "Resume polishing"],
        9: ["KMeans, PCA", "SQL GROUP BY", "Add ML project to resume"],
        10: ["Feature engineering masterclass", "SQL scenarios (10 questions)"],
        11: ["End-to-end ML pipeline", "Model comparison notebook"],
        12: ["Time-series ML basics", "SQL Window deep dive"],
        13: ["FastAPI basics", "Deploy simple ML API"],
        14: ["Full revision of ML+SQL", "Apply to 5 jobs"],
        15: ["Start Major ML Project (Anomaly Detection/RAG)"],
        16: ["Neural Networks basics", "Build 1 NN classifier"],
        17: ["CNN theory", "CIFAR10 CNN"],
        18: ["Augmentation + tuning CNN", "Deploy CNN API"],
        19: ["RNN/LSTM models", "Sequence modeling"],
        20: ["Transformers intro", "Attention mechanism"],
        21: ["HuggingFace pipelines", "Embeddings practice"],
        22: ["Build RAG pipeline (FAISS)", "PDF → Embedding ingestion"],
        23: ["Query → Vector search → LLM response flow"],
        24: ["Add Streamlit UI", "Connect with FastAPI backend"],
        25: ["Improve chatbot responses", "GitHub cleanup"],
        26: ["SQL intermediate test", "ETL basics"],
        27: ["Build ETL script (API → Transform)"],
        28: ["Airflow setup", "First DAG"],
        29: ["Build full pipeline", "Load data to SQL DB"],
        30: ["Finalize Data Eng project", "Write README"],
        31: ["Improve RAG chatbot", "Add history memory"],
        32: ["Dockerize RAG chatbot"],
        33: ["ML interview Q&A practice"],
        34: ["DE interview Q&A practice"],
        35: ["Mock interview #1"],
        36: ["SQL intensive practice"],
        37: ["Dashboard creation (Optional)"],
        38: ["Optimize pipelines"],
        39: ["Apply to 20 companies", "LinkedIn networking"],
        40: ["Week revision + cleanup"],
        41: ["Daily: Apply 20 jobs", "SQL practice", "ML questions", "Improve projects"],
        42: ["Daily: Apply 20 jobs", "SQL practice", "ML questions", "Improve projects"],
        43: ["Daily: Apply 20 jobs", "SQL practice", "ML questions", "Improve projects"],
        44: ["Daily: Apply 20 jobs", "SQL practice", "ML questions", "Improve projects"],
        45: ["Daily: Apply 20 jobs", "SQL practice", "ML questions", "Improve projects"],
        46: ["20 Applications/day", "5 Recruiter Messages/day", "1 Mock Interview/day", "SQL (20 problems/day)", "ML (1 hour/day)", "Project explanation practice", "GitHub push daily"],
        47: ["20 Applications/day", "5 Recruiter Messages/day", "1 Mock Interview/day", "SQL (20 problems/day)", "ML (1 hour/day)", "Project explanation practice", "GitHub push daily"],
        48: ["20 Applications/day", "5 Recruiter Messages/day", "1 Mock Interview/day", "SQL (20 problems/day)", "ML (1 hour/day)", "Project explanation practice", "GitHub push daily"],
        49: ["20 Applications/day", "5 Recruiter Messages/day", "1 Mock Interview/day", "SQL (20 problems/day)", "ML (1 hour/day)", "Project explanation practice", "GitHub push daily"],
        50: ["20 Applications/day", "5 Recruiter Messages/day", "1 Mock Interview/day", "SQL (20 problems/day)", "ML (1 hour/day)", "Project explanation practice", "GitHub push daily"],
        51: ["20 Applications/day", "5 Recruiter Messages/day", "1 Mock Interview/day", "SQL (20 problems/day)", "ML (1 hour/day)", "Project explanation practice", "GitHub push daily"],
        52: ["20 Applications/day", "5 Recruiter Messages/day", "1 Mock Interview/day", "SQL (20 problems/day)", "ML (1 hour/day)", "Project explanation practice", "GitHub push daily"],
        53: ["20 Applications/day", "5 Recruiter Messages/day", "1 Mock Interview/day", "SQL (20 problems/day)", "ML (1 hour/day)", "Project explanation practice", "GitHub push daily"],
        54: ["20 Applications/day", "5 Recruiter Messages/day", "1 Mock Interview/day", "SQL (20 problems/day)", "ML (1 hour/day)", "Project explanation practice", "GitHub push daily"],
        55: ["20 Applications/day", "5 Recruiter Messages/day", "1 Mock Interview/day", "SQL (20 problems/day)", "ML (1 hour/day)", "Project explanation practice", "GitHub push daily"],
        56: ["HR interview prep", "Final resume polish", "Project presentations", "Final mock interview"],
        57: ["HR interview prep", "Final resume polish", "Project presentations", "Final mock interview"],
        58: ["HR interview prep", "Final resume polish", "Project presentations", "Final mock interview"],
        59: ["HR interview prep", "Final resume polish", "Project presentations", "Final mock interview"],
        60: ["HR interview prep", "Final resume polish", "Project presentations", "Final mock interview"]
    }

# Initialize tasks
def initialize_tasks():
    plan = load_plan()
    for day, day_tasks in plan.items():
        day_key = f"Day {day}"
        if day_key not in st.session_state.tasks:
            st.session_state.tasks[day_key] = {task: False for task in day_tasks}

# Save progress
def save_progress():
    progress_data = {
        'tasks': st.session_state.tasks,
        'start_date': st.session_state.start_date.isoformat(),
        'carry_over': st.session_state.carry_over
    }
    with open('learning_progress.json', 'w') as f:
        json.dump(progress_data, f)

# Load progress
def load_progress():
    try:
        with open('learning_progress.json', 'r') as f:
            data = json.load(f)
            st.session_state.tasks = data.get('tasks', {})
            st.session_state.start_date = datetime.fromisoformat(data.get('start_date', datetime.now().date().isoformat())).date()
            st.session_state.carry_over = data.get('carry_over', {})
    except FileNotFoundError:
        initialize_tasks()
        save_progress()

# Calculate current day and overdue tasks
def get_current_status():
    today = datetime.now().date()
    start_date = st.session_state.start_date
    days_passed = (today - start_date).days + 1  # +1 because Day 1 is the start date
    
    current_day = min(days_passed, 60)
    is_overdue = days_passed > 60
    
    # Calculate overdue days
    overdue_days = max(0, days_passed - 60)
    
    return current_day, is_overdue, overdue_days, days_passed

# Handle task carry-over
def handle_carry_over(current_day):
    plan = load_plan()
    
    # Carry over incomplete tasks from previous days
    for day in range(1, current_day + 1):
        day_key = f"Day {day}"
        if day_key in st.session_state.tasks:
            incomplete_tasks = [task for task, completed in st.session_state.tasks[day_key].items() if not completed]
            
            if incomplete_tasks and day < current_day:
                # Add incomplete tasks to carry_over
                st.session_state.carry_over[day_key] = incomplete_tasks

# Display tasks for a specific day
def display_day_tasks(day_number, is_current_day=False, show_checkboxes=True):
    plan = load_plan()
    day_key = f"Day {day_number}"
    
    if day_number in plan:
        # Combine original tasks with carried-over tasks
        all_tasks = plan[day_number].copy()
        
        # Add carried-over tasks from previous days
        if day_key in st.session_state.carry_over:
            carry_over_tasks = [f"🔁 {task} (from Day {day_number})" for task in st.session_state.carry_over[day_key]]
            all_tasks.extend(carry_over_tasks)
        
        # Ensure tasks exist in session state
        if day_key not in st.session_state.tasks:
            st.session_state.tasks[day_key] = {}
        
        # Initialize any new tasks
        for task in all_tasks:
            if task not in st.session_state.tasks[day_key]:
                st.session_state.tasks[day_key][task] = False
        
        # Display tasks
        day_completed = all(st.session_state.tasks[day_key].values())
        
        if is_current_day:
            card_class = "day-card completed-day" if day_completed else "day-card current-day"
            day_title = f"🎯 Day {day_number} - TODAY"
        else:
            card_class = "day-card completed-day" if day_completed else "day-card"
            day_title = f"📅 Day {day_number}"
        
        st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
        st.subheader(day_title)
        
        for task in all_tasks:
            task_completed = st.session_state.tasks[day_key].get(task, False)
            task_class = "completed-task" if task_completed else ""
            
            if show_checkboxes:
                col1, col2 = st.columns([1, 20])
                with col1:
                    new_status = st.checkbox("", value=task_completed, key=f"check_{day_number}_{task}")
                    if new_status != task_completed:
                        st.session_state.tasks[day_key][task] = new_status
                        save_progress()
                        st.rerun()
                
                with col2:
                    st.markdown(f'<div class="task-item {task_class}">{task}</div>', unsafe_allow_html=True)
            else:
                # Just display without checkboxes for view mode
                checkbox_icon = "✅" if task_completed else "⬜"
                st.markdown(f'<div class="task-item {task_class}">{checkbox_icon} {task}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        return day_completed
    return False

# Main app
def main():
    # Load progress
    load_progress()
    
    # Header
    st.title("📚 60-Day ML & Data Engineering Plan")
    
    # Calculate current status
    current_day, is_overdue, overdue_days, days_passed = get_current_status()
    
    # Handle task carry-over
    handle_carry_over(current_day)
    
    # Today's card
    today_date = datetime.now().strftime("%B %d, %Y")
    
    if is_overdue:
        st.markdown(f"""
        <div class="today-card" style="background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);">
            <h2>📅 Day {current_day} - {today_date}</h2>
            <h3>🚨 OVERDUE! - {overdue_days} day(s) behind schedule</h3>
            <p>You need to catch up on {overdue_days} day(s) of work.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="today-card">
            <h2>📅 Day {current_day} - {today_date}</h2>
            <h3>{"🎉 Final Day! Complete your journey!" if current_day == 60 else "Keep going! You're on track!" if current_day == days_passed else "Catch up! You have pending work!"}</h3>
            <p>Started on {st.session_state.start_date.strftime('%B %d, %Y')} • {60 - current_day} days remaining</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Navigation tabs for different views
    tab1, tab2 = st.tabs(["🎯 Today's Tasks", "📅 View Other Days"])
    
    with tab1:
        # Display current day's tasks with checkboxes
        display_day_tasks(current_day, is_current_day=True, show_checkboxes=True)
        
        # Show carried-over tasks section
        if st.session_state.carry_over:
            st.subheader("📋 Pending Tasks from Previous Days")
            
            for day, tasks in st.session_state.carry_over.items():
                if tasks:  # Only show if there are pending tasks
                    day_num = int(day.split()[1])
                    if day_num < current_day:  # Only from previous days
                        st.markdown(f'<div class="day-card overdue-day">', unsafe_allow_html=True)
                        st.write(f"**{day}**")
                        for task in tasks:
                            st.markdown(f'<div class="task-item">🔁 {task}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.subheader("View Tasks for Any Day")
        
        # Day selector
        col1, col2 = st.columns([1, 2])
        
        with col1:
            selected_day = st.selectbox(
                "Select Day to View",
                options=list(range(1, 61)),
                index=current_day-1,
                key="day_selector"
            )
        
        with col2:
            # Calculate the date for the selected day
            selected_date = st.session_state.start_date + timedelta(days=selected_day-1)
            st.write(f"**Date:** {selected_date.strftime('%B %d, %Y')}")
            
            # Status indicator
            if selected_day == current_day:
                st.success("🟢 This is today")
            elif selected_day < current_day:
                st.warning("🟡 This is a past day")
            else:
                st.info("🔵 This is a future day")
        
        # Display selected day's tasks (read-only mode)
        display_day_tasks(selected_day, is_current_day=(selected_day == current_day), show_checkboxes=False)
    
    # Simple controls in sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Start date selector
        new_start_date = st.date_input(
            "Plan Start Date",
            value=st.session_state.start_date,
            help="Change if you started on a different date"
        )
        
        if new_start_date != st.session_state.start_date:
            st.session_state.start_date = new_start_date
            save_progress()
            st.rerun()
        
        # Simple reset buttons
        st.subheader("🔄 Reset Options")
        
        if st.button("Reset Today's Tasks", use_container_width=True):
            current_day_key = f"Day {current_day}"
            if current_day_key in st.session_state.tasks:
                for task in st.session_state.tasks[current_day_key]:
                    st.session_state.tasks[current_day_key][task] = False
                save_progress()
                st.rerun()
        
        if st.button("Reset All Progress", use_container_width=True):
            st.session_state.tasks = {}
            st.session_state.carry_over = {}
            initialize_tasks()
            save_progress()
            st.rerun()
        
        # Quick stats
        st.subheader("📊 Quick Stats")
        total_completed = 0
        total_tasks = 0
        
        for day in range(1, 61):
            day_key = f"Day {day}"
            if day_key in st.session_state.tasks:
                day_tasks = st.session_state.tasks[day_key]
                total_tasks += len(day_tasks)
                total_completed += sum(day_tasks.values())
        
        if total_tasks > 0:
            completion_rate = (total_completed / total_tasks) * 100
            st.write(f"**Overall Progress:** {completion_rate:.1f}%")
            st.write(f"**Tasks Completed:** {total_completed}/{total_tasks}")
        
        # Mobile-friendly tips
        st.subheader("📱 Mobile Tips")
        st.info(
            "• Tap checkboxes to mark tasks complete\n"
            "• Swipe left/right to navigate\n"
            "• Use sidebar for settings\n"
            "• Progress saves automatically"
        )

if __name__ == "__main__":
    main()