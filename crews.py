import streamlit as st
import yaml
import os
from enum import Enum

class Process(Enum):
    sequential = "sequential"
    hierarchical = "hierarchical"

# Ensure the crews directory exists
if not os.path.exists('crews'):
    os.makedirs('crews')

def load_yaml_files(directory):
    files = {}
    for filename in os.listdir(directory):
        if filename.endswith('.yaml'):
            with open(os.path.join(directory, filename), 'r') as file:
                files[filename.replace('.yaml', '')] = filename
    return files

def save_crew(filename, data):
    with open(os.path.join('crews', filename), 'w') as file:
        yaml.dump(data, file)

def delete_crew(filename):
    os.remove(os.path.join('crews', filename))

def load_crew_files():
    return load_yaml_files('crews')

st.title("Crew File Manager")

# Load existing agent and task files for the dropdowns
agent_files = load_yaml_files('agents')
task_files = load_yaml_files('tasks')

# Create new crew
st.header("Create New Crew")
new_crew_name = st.text_input("New Crew Name")
new_crew_agents = st.multiselect("Select Agents", list(agent_files.keys()), key="new_crew_agents")
new_crew_tasks = st.multiselect("Select Tasks", list(task_files.keys()), key="new_crew_tasks")
new_crew_verbose = st.slider("Verbose Level", 0, 2, 2, key="new_crew_verbose")
new_crew_process = st.selectbox("Process", [p.value for p in Process], key="new_crew_process")

if st.button("Create Crew"):
    if new_crew_name and new_crew_agents and new_crew_tasks:
        filename = f"{new_crew_name.lower().replace(' ', '_')}.yaml"
        new_crew_data = {
            "agents": [agent_files[agent] for agent in new_crew_agents],
            "tasks": [task_files[task] for task in new_crew_tasks],
            "verbose": new_crew_verbose,
            "process": new_crew_process
        }
        save_crew(filename, new_crew_data)
        st.success(f"Crew {new_crew_name} created successfully!")
    else:
        st.error("Please fill in all fields")

# Load existing crew files
crew_files = load_crew_files()

# Edit or delete existing crews
st.header("Manage Existing Crews")

if crew_files:
    selected_crew = st.selectbox("Select a crew to edit or delete", list(crew_files.keys()))
    
    if selected_crew:
        with open(os.path.join('crews', crew_files[selected_crew]), 'r') as file:
            crew_data = yaml.safe_load(file)
        
        edited_data = {}
        edited_data['agents'] = st.multiselect("Select Agents", list(agent_files.keys()),
                                               default=[key for key, value in agent_files.items() if value in crew_data['agents']],
                                               key=f"{selected_crew}_agents")
        edited_data['tasks'] = st.multiselect("Select Tasks", list(task_files.keys()),
                                              default=[key for key, value in task_files.items() if value in crew_data['tasks']],
                                              key=f"{selected_crew}_tasks")
        edited_data['verbose'] = st.slider("Verbose Level", 0, 2, crew_data['verbose'], key=f"{selected_crew}_verbose")
        edited_data['process'] = st.selectbox("Process", [p.value for p in Process], 
                                              index=[p.value for p in Process].index(crew_data['process']),
                                              key=f"{selected_crew}_process")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Update Crew"):
                edited_data['agents'] = [agent_files[agent] for agent in edited_data['agents']]
                edited_data['tasks'] = [task_files[task] for task in edited_data['tasks']]
                save_crew(crew_files[selected_crew], edited_data)
                st.success(f"Crew {selected_crew} updated successfully!")
        with col2:
            if st.button("Delete Crew"):
                delete_crew(crew_files[selected_crew])
                st.success(f"Crew {selected_crew} deleted successfully!")
                st.experimental_rerun()
else:
    st.info("No existing crews found. Create a new crew to get started.")