import streamlit as st
import requests

# FastAPI backend URL
FASTAPI_URL = "http://127.0.0.1:8000/generate_mcq/"

# Streamlit app setup
st.title("AI Question Generator")
st.write("Enter a topic to generate a multiple-choice question:")

# Input for topic
topic_input = st.text_input("Topic:", "")

# Initialize session_state variables if they don't exist
if "question_data" not in st.session_state:
    st.session_state.question_data = {}
if "user_answer" not in st.session_state:
    st.session_state.user_answer = None
if "feedback_message" not in st.session_state:
    st.session_state.feedback_message = ""

# If the user clicks the "Generate Question" button
if st.button("Generate Question"):
    if topic_input:
        try:
            # Make a request to the FastAPI backend
            response = requests.post(FASTAPI_URL, json={"topic": topic_input})
            response.raise_for_status()

            # Store the question data in session_state
            st.session_state.question_data = response.json()
            st.session_state.user_answer = None
            st.session_state.feedback_message = ""
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching data from backend: {e}")
    else:
        st.write("Please enter a topic to generate the question.")

# Display question and options if available
if "question_data" in st.session_state and st.session_state.question_data:
    question_data = st.session_state.question_data.get("mcq", {})
    question = question_data.get("question", "")
    options = question_data.get("options", [])
    correct_answer = question_data.get("correct_option", "")

    if question:
        st.subheader(question)
        
        # Display radio buttons for the options
        user_answer = st.radio("Choose an option:", options)

        # Submit button to check answer
        if st.button("Submit Answer"):
            if user_answer:
                if user_answer == correct_answer:
                    st.session_state.feedback_message = "Correct Answer!"
                else:
                    st.session_state.feedback_message = "Incorrect Answer. Try again."
            else:
                st.session_state.feedback_message = "Please select an answer."

            # Display feedback message
            st.write(st.session_state.feedback_message)

else:
    st.write("Please generate a question first.")
