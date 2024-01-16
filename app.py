# Import necessary libraries

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import time

from openai import OpenAI

# Function to obtain completion from OpenAI Chat API
def get_chat_completion(prompt):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content

# Function to create a DataFrame with responses from the Chat API
def create_df(nb_iterations):
    answers_list = [get_chat_completion(prompt) for i in range(nb_iterations)]
    df = pd.DataFrame({
        "Answers": answers_list
    })
    
    return df


# Streamlit app title and description
st.title("Welcome on Ethic-AI")

st.write("A playground to test ChatGPT's ethical responses with tricky questions (Model: gpt-3.5-turbo).")

# Sidebar input for OpenAI API key
key = st.sidebar.text_input('Your API KEY')
client = OpenAI(api_key = str(key))

# Sidebar input for the number of iterations and user prompt                
nb_iterations = st.sidebar.slider(
    "How many iterations?",0,500)

prompt = st.text_area("Enter your  prompt")

# Sidebar input for the type of graphs to display
graph_type = st.multiselect(
    'What are the graphs you want?',
    ['Piechart', 'Countplot', 'Boxplot'],
    ['Piechart', 'Boxplot'])

# Initialize list to store user-defined options
list_of_options = []
# Allow user to input multiple new options (comma-separated)
new_options = st.text_input('Enter your expected answers (comma-separated)', 'Option 1, Option 2')

# Check selected graph types
isPiechart = 'Piechart' in graph_type
isCountplot = 'Countplot' in graph_type
isBoxplot = 'Boxplot' in graph_type

# Button to trigger analysis
if st.button('Analyze'):
    # Extract and process new user-defined options
    new_options_list = [option.strip() for option in new_options.split(',') if option.strip()]
    list_of_options.extend(new_options_list)
    st.write(list_of_options)

    data_frame=create_df(nb_iterations)

    # Display user prompt in chat format
    message_human = st.chat_message("user")
    message_human.write(prompt)

    # Introduce delay for better visual experience
    time.sleep(1)

    # Display assistant's responses in chat format
    message_assistant = st.chat_message("assistant")
    message_assistant.write(data_frame)

    # Apply user-defined options to responses
    data_frame['Answers'] = data_frame['Answers'].apply(lambda answer: next((option for option in list_of_options if option in answer), 'Verbose Answer'))


    # Plot selected graphs based on user preferences
    if isPiechart:
        fig = px.pie(data_frame['Answers'].explode(), names='Answers', title='Pie chart')
        st.plotly_chart(fig, use_container_width=True)

    if isCountplot:
        st.title('Count Plot - Distribution of Responses')
        fig = px.bar(data_frame['Answers'].explode(), x='Answers', title='Count Plot')
        st.plotly_chart(fig, use_container_width=True)

    if isBoxplot:
        st.title('Box Plot - Distribution of Responses')
        fig = px.box(data_frame['Answers'].explode(), x='Answers', title='Box Plot')
        st.plotly_chart(fig, use_container_width=True)



