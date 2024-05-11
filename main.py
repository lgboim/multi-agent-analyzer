import os
import streamlit as st
from groq import Groq
import time

# Streamlit App Layout Enhancements
st.title("Dynamic and Intelligent Multi-Agent Topic Analysis")
st.write("Provide a topic, and watch as the manager dynamically creates roles and assigns tasks based on the topic analysis!")

# User input for API key
api_key = st.text_input("Enter your Groq API key:", type="password")

# Initialize Groq client
client = Groq(api_key=api_key)

def get_completion(messages, model="llama3-8b-8192"):
    try:
        chat_completion = client.chat.completions.create(messages=messages, model=model)
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def analyze_topic_with_groq(topic):
    messages = [
        {"role": "system", "content": "You are an intelligent agent tasked with analyzing topics and suggesting agent roles."},
        {"role": "user", "content": f"Analyze the topic '{topic}' and suggest 5 roles for agents and their task. Every line is a different role and task. Write just the points without any other text or explanations. start just with the first point: '1."}
    ]
    return get_completion(messages)

def generate_dynamic_agents(topic_analysis, topic, max_agents=5):
    lines = topic_analysis.split('\n')
    agents = {}
    task_instructions = {}

    for i, line in enumerate(lines):
        if line.strip() and i < max_agents:
            agent_name = f"Agent {i+1}"
            role = f"Agent specializing in {line.strip()}"
            agents[agent_name] = {
                "role": "assistant",
                "personality": f"{role} to provide insights about {topic}.",
            }
            task_instructions[agent_name] = f"Provide a detailed analysis and gather additional information about {line.strip()}."

    return agents, task_instructions

def delegate_tasks_linear_smart(agents, task_instructions, topic):
    responses = {}
    all_previous_content = ""
    agent_names = list(agents.keys())

    for i, agent in enumerate(agent_names):
        if i == 0:
            # The first agent gives a detailed analysis
            instruction = task_instructions[agent]
            messages = [
                {"role": "system", "content": agents[agent]["personality"]},
                {"role": "user", "content": instruction}
            ]
            response = get_completion(messages)
            responses[agent] = response
            all_previous_content += response
        else:
            # Subsequent agents analyze all prior content and add new insights
            context = all_previous_content + f"\n\nBased on the above, what are the deeper implications and related aspects of the topic '{topic}'? think smarter and deeper, from first principles, not Repeat things that have already been said."
            messages = [
                {"role": "system", "content": agents[agent]["personality"]},
                {"role": "user", "content": context}
            ]
            response = get_completion(messages)
            responses[agent] = response
            all_previous_content += "\n\n" + response

    return responses

def consolidate_responses(responses, topic):
    all_responses = "\n".join([f"{agent}: {response}" for agent, response in responses.items()])
    messages = [
        {"role": "system", "content": "You are an AI assistant that consolidates and summarizes responses from multiple agents on a given topic into a comprehensive report."},
        {"role": "user", "content": f"Here are the responses from various AI agents regarding '{topic}':\n\n{all_responses}\n\nPlease consolidate these findings into a comprehensive, very long, detailed, and structured summary of all responses. Use titles, bold, points, and long explanations."}
    ]
    return get_completion(messages)

# Predefined subject to start with
predefined_subject = "How will AGI change the world?"
topic = st.text_input("Enter a topic:", value=predefined_subject, key="topic")

if st.button("Analyze Topic"):
    if not api_key:
        st.warning("Please enter your Groq API key to proceed.")
    else:
        progress_text = "Analyzing the topic..."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.05)
            my_bar.progress(percent_complete + 1, text=progress_text)

        topic_analysis = analyze_topic_with_groq(topic)

        if not topic_analysis.startswith("Error"):
            with st.expander("Topic Analysis and Suggested Points", expanded=True):
                st.write(topic_analysis)
            
            agents, task_instructions = generate_dynamic_agents(topic_analysis, topic)

            with st.expander("Dynamic Agents and Their Tasks", expanded=True):
                for agent, info in agents.items():
                    st.markdown(f"**{agent} ({info['role']}):** Task: {task_instructions[agent]}")

            progress_text = "Agents are generating responses in a linear collaborative manner..."
            my_bar.progress(0, text=progress_text)

            for percent_complete in range(100):
                time.sleep(0.05)
                my_bar.progress(percent_complete + 1, text=progress_text)
                
            responses = delegate_tasks_linear_smart(agents, task_instructions, topic)

            with st.expander("Agent Responses in Linear Collaboration", expanded=False):
                for agent, response in responses.items():
                    st.markdown(f"**{agent}:** {response}")

            progress_text = "Generating comprehensive summary..."
            my_bar.progress(0, text=progress_text)

            for percent_complete in range(100):
                time.sleep(0.05)
                my_bar.progress(percent_complete + 1, text=progress_text)
                
            consolidated_summary = consolidate_responses(responses, topic)

            with st.expander("Comprehensive Summary", expanded=True):
                st.write(consolidated_summary)
        else:
            st.error("Failed to analyze the topic with Groq. Please check your API key and network connection.")
