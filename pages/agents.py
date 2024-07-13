import streamlit as st
import yaml
import os

# Ensure the agents directory exists
if not os.path.exists('agents'):
    os.makedirs('agents')

def load_agent_files():
    agent_files = {}
    for filename in os.listdir('agents'):
        if filename.endswith('.yaml'):
            with open(os.path.join('agents', filename), 'r') as file:
                agent_files[filename] = yaml.safe_load(file)
    return agent_files

def save_agent(filename, data):
    with open(os.path.join('agents', filename), 'w') as file:
        yaml.dump(data, file)

def delete_agent(filename):
    os.remove(os.path.join('agents', filename))

st.title("Agent File Manager")

# Create new agent
st.header("Create New Agent")
new_agent_name = st.text_input("New Agent Name")
new_agent_goal = st.text_area("Goal")
new_agent_backstory = st.text_area("Backstory")
new_agent_model = st.text_input("Model", value="openhermes")
new_agent_allow_delegation = st.checkbox("Allow Delegation", key="new_allow_delegation")
new_agent_verbose = st.checkbox("Verbose", value=True, key="new_verbose")

if st.button("Create Agent"):
    if new_agent_name and new_agent_goal and new_agent_backstory:
        filename = f"{new_agent_name.lower().replace(' ', '_')}.yaml"
        new_agent_data = {
            "goal": new_agent_goal,
            "backstory": new_agent_backstory,
            "model": new_agent_model,
            "allow_delegation": new_agent_allow_delegation,
            "verbose": new_agent_verbose
        }
        save_agent(filename, new_agent_data)
        st.success(f"Agent {new_agent_name} created successfully!")
    else:
        st.error("Please fill in all fields")

# Load existing agent files
agent_files = load_agent_files()

# Edit or delete existing agents
st.header("Manage Existing Agents")

if agent_files:
    selected_agent = st.selectbox("Select an agent to edit or delete", list(agent_files.keys()))
    
    if selected_agent:
        agent_data = agent_files[selected_agent]
        
        edited_data = {}
        edited_data['goal'] = st.text_area("Goal", agent_data['goal'], key=f"{selected_agent}_goal")
        edited_data['backstory'] = st.text_area("Backstory", agent_data['backstory'], key=f"{selected_agent}_backstory")
        edited_data['model'] = st.text_input("Model", agent_data.get('model', 'llama2'), key=f"{selected_agent}_model")
        edited_data['allow_delegation'] = st.checkbox("Allow Delegation", agent_data.get('allow_delegation', False), key=f"{selected_agent}_allow_delegation")
        edited_data['verbose'] = st.checkbox("Verbose", agent_data.get('verbose', True), key=f"{selected_agent}_verbose")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Update Agent"):
                save_agent(selected_agent, edited_data)
                st.success(f"Agent {selected_agent} updated successfully!")
        with col2:
            if st.button("Delete Agent"):
                delete_agent(selected_agent)
                st.success(f"Agent {selected_agent} deleted successfully!")
                st.experimental_rerun()
else:
    st.info("No existing agents found. Create a new agent to get started.")