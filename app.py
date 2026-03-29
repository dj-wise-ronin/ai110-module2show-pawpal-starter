import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# --- Phase 3: Manage Application Memory ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

owner = st.session_state.owner

# --- UI for Owner and Pets ---
with st.sidebar:
    st.header("Manage Pets")
    owner.name = st.text_input("Owner Name", value=owner.name)
    
    with st.form("add_pet_form"):
        st.subheader("Add a New Pet")
        new_pet_name = st.text_input("Pet Name")
        new_pet_species = st.selectbox("Species", ["Dog", "Cat", "Bird", "Other"])
        new_pet_age = st.number_input("Age", min_value=0, max_value=30, value=1)
        new_pet_breed = st.text_input("Breed", value="Unknown")
        
        if st.form_submit_button("Add Pet"):
            if new_pet_name:
                new_pet = Pet(name=new_pet_name, species=new_pet_species, age=new_pet_age, breed=new_pet_breed)
                owner.add_pet(new_pet)
                st.success(f"Added {new_pet_name}!")
                st.rerun()
            else:
                st.error("Pet name is required.")

    if owner.pets:
        st.subheader("Your Pets")
        for pet in owner.pets:
            st.write(f"- {pet.get_info()}")
    else:
        st.info("No pets added yet.")

# --- Task Management ---
st.subheader("Schedule a Task")
if not owner.pets:
    st.warning("Please add at least one pet in the sidebar before scheduling tasks.")
else:
    with st.form("add_task_form"):
        selected_pet_name = st.selectbox("Select Pet", [p.name for p in owner.pets])
        task_desc = st.text_input("Task Description", value="Morning Walk")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            duration = st.number_input("Duration (mins)", min_value=1, max_value=240, value=30)
        with col2:
            priority_label = st.selectbox("Priority", ["High (1)", "Medium (2)", "Low (3)"])
            priority_val = int(priority_label.split("(")[1][0])
        with col3:
            time_val = st.time_input("Scheduled Time", value=None)
            time_str = time_val.strftime("%H:%M") if time_val else "09:00"
        
        col4, col5 = st.columns(2)
        with col4:
            category = st.text_input("Category", value="Exercise")
        with col5:
            frequency = st.selectbox("Frequency", ["Once", "Daily"])
        
        if st.form_submit_button("Add Task to Schedule"):
            target_pet = next(p for p in owner.pets if p.name == selected_pet_name)
            new_task = Task(
                description=task_desc, 
                duration=duration, 
                priority=priority_val, 
                category=category,
                time=time_str,
                frequency=frequency
            )
            target_pet.add_task(new_task)
            st.success(f"Task '{task_desc}' added for {selected_pet_name} at {time_str}!")
            st.rerun()

# --- Display All Tasks with Filtering ---
all_tasks = owner.get_all_tasks()
if all_tasks:
    st.divider()
    st.subheader("Current Tasks")
    
    col1, col2 = st.columns(2)
    with col1:
        pet_filter = st.multiselect("Filter by Pet", options=[p.name for p in owner.pets])
    with col2:
        status_filter = st.radio("Status Filter", ["All", "Pending", "Completed"], horizontal=True)
    
    filtered_tasks = all_tasks
    if pet_filter:
        filtered_tasks = [t for t in filtered_tasks if t.pet_name in pet_filter]
    if status_filter == "Pending":
        filtered_tasks = [t for t in filtered_tasks if not t.is_completed]
    elif status_filter == "Completed":
        filtered_tasks = [t for t in filtered_tasks if t.is_completed]

    if filtered_tasks:
        task_data = []
        for t in filtered_tasks:
            task_data.append({
                "Time": t.time,
                "Pet": t.pet_name,
                "Description": t.description,
                "Duration": t.duration,
                "Priority": t.priority,
                "Status": "✅" if t.is_completed else "⏳"
            })
        st.table(task_data)
    else:
        st.info("No tasks match the current filters.")

# --- Build Schedule & Conflict Detection ---
st.divider()
st.subheader("Generate Daily Plan")

if all_tasks:
    scheduler = Scheduler(available_time=480, tasks=all_tasks)
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for conflict in conflicts:
            st.warning(conflict)

available_time = st.slider("How much time do you have today? (minutes)", min_value=15, max_value=480, value=120)

if st.button("Generate Optimized Schedule"):
    pending_tasks = [t for t in all_tasks if not t.is_completed]
    if not pending_tasks:
        st.info("No pending tasks to schedule. Add some tasks first!")
    else:
        scheduler = Scheduler(available_time=available_time, tasks=pending_tasks)
        plan = scheduler.generate_plan()
        
        if not plan:
            st.warning("No tasks could fit in the available time based on priorities.")
        else:
            st.success(f"Schedule generated! Total time: {scheduler.get_total_duration(plan)} mins")
            
            # Display the plan sorted by time
            plan_sorted = sorted(plan, key=lambda x: x.time)
            plan_data = []
            for t in plan_sorted:
                plan_data.append({
                    "Time": t.time,
                    "Pet": t.pet_name,
                    "Task": t.description,
                    "Duration": t.duration,
                    "Priority": t.priority
                })
            st.table(plan_data)
            
            st.markdown("### Why this plan?")
            st.write("The scheduler prioritized your tasks based on their importance (Priority 1 first) and then fit as many as possible into your available time. The plan above is displayed chronologically for your convenience!")
