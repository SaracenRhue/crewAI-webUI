import streamlit as st
import yaml
import os
from crewai import Agent, Task, Crew, Process
from langchain_community.llms import Ollama

env = {}
if os.path.exists('.env'):
    with open('.env', 'r') as f:
        for line in f:
            key, value = line.strip().split('=')
            env[key] = value
else:
    env['OLLAMA_URL'] = os.getenv('OLLAMA_URL')

# Load YAML files
def load_yaml_files(directory):
    files = {}
    for filename in os.listdir(directory):
        if filename.endswith('.yaml'):
            with open(os.path.join(directory, filename), 'r') as file:
                files[filename.replace('.yaml', '')] = yaml.safe_load(file)
    return files

# Load crew, agent, and task files
crews = load_yaml_files('crews')
agents = load_yaml_files('agents')
tasks = load_yaml_files('tasks')

# Streamlit app
st.title("CrewAI Task Runner")

# Select crew
selected_crew = st.selectbox("Select a Crew", list(crews.keys()))

if selected_crew:
    crew_data = crews[selected_crew]
    st.write(f"Selected Crew: {selected_crew}")
    st.write(f"Agents: {', '.join([agent.split('.')[0] for agent in crew_data['agents']])}")
    st.write(f"Tasks: {', '.join([task.split('.')[0] for task in crew_data['tasks']])}")
    st.write(f"Verbose Level: {crew_data['verbose']}")
    st.write(f"Process: {crew_data['process']}")

    if st.button("Run Crew"):
        if 1 == 0:
            pass
        else:
            # Set environment variables
            os.environ["OPENAI_API_KEY"] = "NA"

            # Create agents
            crew_agents = []
            for agent_file in crew_data['agents']:
                agent_data = agents[agent_file.replace('.yaml', '')]
                print(agent_data)
                agent = Agent(
                    role=agent_file.replace('.yaml', '').replace('_',' '),
                    goal=agent_data['goal'],
                    backstory=agent_data['backstory'],
                    allow_delegation=agent_data['allow_delegation'],
                    verbose=agent_data['verbose'],
                    llm = Ollama(model = agent_data['model'],base_url = env['OLLAMA_URL'])
                )
                crew_agents.append(agent)

            # Create tasks
            crew_tasks = []
            for task_file in crew_data['tasks']:
                task_data = tasks[task_file.replace('.yaml', '')]
                print(crew_data)
                task = Task(
                    description=task_data['description'],
                    expected_output=task_data['expected_output'],
                    agent=crew_agents[crew_data['agents'].index(task_data['agent'])]
                )
                crew_tasks.append(task)

            # Create crew
            crew = Crew(
                agents=crew_agents,
                tasks=crew_tasks,
                verbose=crew_data['verbose'],
                process=Process[crew_data['process']]
            )

            # Run crew
            with st.spinner("Crew is working..."):
                result = crew.kickoff()

            st.success("Crew has completed its tasks!")
            st.write("Result:")
            st.write(result)

else:
    st.info("No crews found. Please create a crew using the Crew Manager.")