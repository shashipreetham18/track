import streamlit as st
import json
from datetime import datetime, timedelta

# Configure the page
st.set_page_config(
    page_title="60-Day ML Plan",
    page_icon="📚",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
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
        border-left: 4px solid #28a745;
        background-color: #d4edda;
    }
    .current-day {
        border-left: 4px solid #007bff;
        background-color: #cce7ff;
    }
    .task-item {
        margin: 0.3rem 0;
        padding: 0.2rem;
    }
    .completed-task {
        text-decoration: line-through;
        color: #6c757d;
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

# Load the plan
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

def initialize_tasks():
    plan = load_plan()
    for day, day_tasks in plan.items():
        day_key = f"Day {day}"
        if day_key not in st.session_state.tasks:
            st.session_state.tasks[day_key] = {task: False for task in day_tasks}

def save_progress():
    progress_data = {
        'tasks': st.session_state.tasks,
        'start_date': st.session_state.start_date.isoformat(),
        'carry_over': st.session_state.carry_over
    }
    with open('learning_progress.json', 'w') as f:
        json.dump(progress_data, f)

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

def get_current_status():
    today = datetime.now().date()
    start_date = st.session_state.start_date
    days_passed = (today - start_date).days + 1
    
    current_day = min(days_passed, 60)
    is_overdue = days_passed > 60
    overdue_days = max(0, days_passed - 60)
    
    return current_day, is_overdue, overdue_days, days_passed

def handle_carry_over(current_day):
    for day in range(1, current_day + 1):
        day_key = f"Day {day}"
        if day_key in st.session_state.tasks:
            incomplete_tasks = [task for task, completed in st.session_state.tasks[day_key].items() if not completed]
            if incomplete_tasks and day < current_day:
                st.session_state.carry_over[day_key] = incomplete_tasks

def display_day_tasks(day_number, is_current_day=False, show_checkboxes=True):
    plan = load_plan()
    day_key = f"Day {day_number}"
    
    if day_number in plan:
        all_tasks = plan[day_number].copy()
        
        if day_key in st.session_state.carry_over:
            carry_over_tasks = [f"🔁 {task} (from Day {day_number})" for task in st.session_state.carry_over[day_key]]
            all_tasks.extend(carry_over_tasks)
        
        if day_key not in st.session_state.tasks:
            st.session_state.tasks[day_key] = {}
        
        for task in all_tasks:
            if task not in st.session_state.tasks[day_key]:
                st.session_state.tasks[day_key][task] = False
        
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
                # Simple checkbox without complex key
                checked = st.checkbox(task, value=task_completed, key=f"{day_number}_{task}")
                if checked != task_completed:
                    st.session_state.tasks[day_key][task] = checked
                    save_progress()
                    st.rerun()
            else:
                checkbox_icon = "✅" if task_completed else "⬜"
                st.markdown(f'<div class="task-item {task_class}">{checkbox_icon} {task}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    load_progress()
    
    st.title("📚 60-Day ML & Data Engineering Plan")
    
    current_day, is_overdue, overdue_days, days_passed = get_current_status()
    handle_carry_over(current_day)
    
    today_date = datetime.now().strftime("%B %d, %Y")
    
    if is_overdue:
        st.markdown(f"""
        <div class="today-card">
            <h2>📅 Day {current_day} - {today_date}</h2>
            <h3>🚨 OVERDUE! - {overdue_days} day(s) behind</h3>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="today-card">
            <h2>📅 Day {current_day} - {today_date}</h2>
            <h3>{"🎉 Final Day!" if current_day == 60 else "Keep going!"}</h3>
            <p>{60 - current_day} days remaining</p>
        </div>
        """, unsafe_allow_html=True)
    
    # SIMPLE navigation without tabs that might cause issues
    view_option = st.radio("What do you want to view?", ["Today's Tasks", "Other Day's Tasks"])
    
    if view_option == "Today's Tasks":
        display_day_tasks(current_day, is_current_day=True, show_checkboxes=True)
        
        if st.session_state.carry_over:
            st.subheader("📋 Pending Tasks")
            for day, tasks in st.session_state.carry_over.items():
                if tasks:
                    st.write(f"**{day}**")
                    for task in tasks:
                        st.write(f"🔁 {task}")
    
    else:  # Other Day's Tasks
        st.subheader("View Tasks for Any Day")
        
        # ULTRA SIMPLE day selector - no index, no complex options
        selected_day = st.number_input(
            "Select Day (1-60):", 
            min_value=1, 
            max_value=60, 
            value=current_day
        )
        
        selected_date = st.session_state.start_date + timedelta(days=selected_day-1)
        st.write(f"**Date:** {selected_date.strftime('%B %d, %Y')}")
        
        if selected_day == current_day:
            st.info("This is today")
        elif selected_day < current_day:
            st.warning("This is a past day")
        else:
            st.success("This is a future day")
        
        display_day_tasks(selected_day, is_current_day=(selected_day == current_day), show_checkboxes=False)
    
    # Sidebar
    with st.sidebar:
        st.header("Settings")
        
        new_start_date = st.date_input("Plan Start Date", value=st.session_state.start_date)
        if new_start_date != st.session_state.start_date:
            st.session_state.start_date = new_start_date
            save_progress()
            st.rerun()
        
        if st.button("Reset Today's Tasks"):
            current_day_key = f"Day {current_day}"
            if current_day_key in st.session_state.tasks:
                for task in st.session_state.tasks[current_day_key]:
                    st.session_state.tasks[current_day_key][task] = False
                save_progress()
                st.rerun()
        
        if st.button("Reset All Progress"):
            st.session_state.tasks = {}
            st.session_state.carry_over = {}
            initialize_tasks()
            save_progress()
            st.rerun()

if __name__ == "__main__":
    main()
