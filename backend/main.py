from fastapi import FastAPI, HTTPException
from pydantic import BaseModel  # Add this import
import random
import os
from dotenv import load_dotenv
from langchain_community.tools import DuckDuckGoSearchRun

# Load environment variables from .env file
load_dotenv()

# Get AI21 API key (ensure you set this in your .env file)
AI21_API_KEY = os.getenv("AI21_API_KEY")
ROOT_URL = "https://api.ai21.com/studio/v1/"

# Create FastAPI app
app = FastAPI()

# Pydantic model to parse incoming data for MCQ generation
class MCQRequest(BaseModel):
    topic: str  # The topic for which we will generate MCQs

# Function to generate random MCQ options and diversify question types
def generate_mcq_options_and_question(topic: str):
    # Different possible question templates
    question_templates = [
        f"What is the importance of the topic '{topic}'?",
        f"What are the key challenges related to {topic}?",
        f"What are the benefits of {topic}?",
        f"Why is {topic} relevant in today's context?"
    ]
 # Randomly choose one of the question templates
    question = random.choice(question_templates)
    
    # Options based on the topic
    options = [
        f"Importance of {topic} in society",
        f"{topic} and its relevance",
        f"Key challenges of {topic}",
        f"Benefits of {topic}"
    ]
    
    # Shuffle options to randomize the answer order
    random.shuffle(options)
    
    # Randomly select one of the options to be the correct answer
    correct_option = random.choice(options)
    
    return question, options, correct_option

# Route for generating MCQs
@app.post("/generate_mcq/")
async def generate_mcq(mcq_request: MCQRequest):
    topic = mcq_request.topic
    question, options, correct_option = generate_mcq_options_and_question(topic)
    
    mcq_data = {
        "question": question,
        "options": options,
        "correct_option": correct_option
 }
    
    return {"mcq": mcq_data};
