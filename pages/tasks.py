import streamlit as st
import yaml
import os

# Ensure the tasks directory exists
if not os.path.exists('tasks'):
    os.makedirs('tasks')

def load_task_files():
    task_files = {}
    for filename in os.listdir('tasks'):
        if filename.endswith('.yaml'):
            with open(os.path.join('tasks', filename), 'r') as file:
                task_files[filename] = yaml.safe_load(file)
    return task_files

def save_task(filename, data):
    with open(os.path.join('tasks', filename), 'w') as file:
        yaml.dump(data, file)

def delete_task(filename):
    os.remove(os.path.join('tasks', filename))

def load_agent_files():
    agent_files = {}
    for filename in os.listdir('agents'):
        if filename.endswith('.yaml'):
            agent_files[filename.replace('.yaml', '')] = filename
    return agent_files

st.title("Task File Manager")

# Load existing agent files for the dropdown
agent_files = load_agent_files()

# Create new task
st.header("Create New Task")
new_task_name = st.text_input("New Task Name")
new_task_description = st.text_area("Description")
new_task_expected_output = st.text_input("Expected Output")
new_task_agent = st.selectbox("Select Agent", list(agent_files.keys()), key="new_task_agent")

if st.button("Create Task"):
    if new_task_name and new_task_description and new_task_expected_output and new_task_agent:
        filename = f"{new_task_name.lower().replace(' ', '_')}.yaml"
        new_task_data = {
            "description": new_task_description,
            "expected_output": new_task_expected_output,
            "agent": agent_files[new_task_agent]
        }
        save_task(filename, new_task_data)
        st.success(f"Task {new_task_name} created successfully!")
    else:
        st.error("Please fill in all fields")

# Load existing task files
task_files = load_task_files()

# Edit or delete existing tasks
st.header("Manage Existing Tasks")

if task_files:
    selected_task = st.selectbox("Select a task to edit or delete", list(task_files.keys()))
    
    if selected_task:
        task_data = task_files[selected_task]
        
        edited_data = {}
        edited_data['description'] = st.text_area("Description", task_data['description'], key=f"{selected_task}_description")
        edited_data['expected_output'] = st.text_input("Expected Output", task_data['expected_output'], key=f"{selected_task}_expected_output")
        edited_data['agent'] = st.selectbox("Select Agent", list(agent_files.keys()), 
                                            index=list(agent_files.values()).index(task_data['agent']), 
                                            key=f"{selected_task}_agent")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Update Task"):
                edited_data['agent'] = agent_files[edited_data['agent']]  # Convert back to filename
                save_task(selected_task, edited_data)
                st.success(f"Task {selected_task} updated successfully!")
        with col2:
            if st.button("Delete Task"):
                delete_task(selected_task)
                st.success(f"Task {selected_task} deleted successfully!")
                st.experimental_rerun()
else:
    st.info("No existing tasks found. Create a new task to get started.")