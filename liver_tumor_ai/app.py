from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel,Extra
from typing import List
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv
import markdown

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)


prompt_template = PromptTemplate.from_template(
    template = """
        You are a liver tumor management assistant. Your role is to provide accurate information and guidance on liver tumor-related topics, including symptoms, staging, segmentation from CT scans, diagnostic recommendations, and post-detection health tips. 
        You have knowledge of advanced machine learning techniques such as dilated convolutions, attention mechanisms, transformer-based encoders, and the ResUNet model applied to liver tumor segmentation. You also understand the importance of context-based medical recommendations after the segmentation step using a combination of Large Language Models (LLM) integrated with Retrieval-Augmented Generation (RAG).

        Based on the symptoms and details provided by the user, suggest recommendations and possible diagnostic approaches. If the symptoms or tumor details are unclear, ask the user for more details about their condition and tumor. Confirm with the user if they have provided all necessary details for accurate analysis. Always respond with 'I don't know' if the question is unclear or outside your area of expertise.

        %CHAT HISTORY
        chat history: {chat_history}

        %USER QUESTION
        Question: {user_question}
        """
        ) 

def update_chat_history(chat_history):
    history =[]
    for message in chat_history:
        if message['sender']=="assistant":
            history.append(AIMessage(content=message['text']))
        elif message['sender']=="user":
            history.append(HumanMessage(content=message['text']))
    return history

def get_llm_response(query, chat_history):
    tprompt = prompt_template.format(chat_history=chat_history,user_question=query) 
    result = llm.invoke(tprompt)
    return result.content


app = FastAPI()

# Directory where static files (css, js) and HTML are located
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

# Serve static files (CSS, JS) from the "static" folder
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Serve the HTML page at the root (127.0.0.1:8000)
@app.get("/", response_class=HTMLResponse)
async def get_chat_page():
    with open(os.path.join(STATIC_DIR, "chat.html"), "r") as file:
        return file.read()

# Store the chat history
chat_history = []

# Define the request model for chat messages
class Message(BaseModel):
    query: str
    chat_history: List
    class Config:
        extra = Extra.ignore 

# Endpoint to handle chat messages
@app.post("/chat")
async def chat(message: Message):
    # Add user's message to chat history

    # Simple bot response (reverses user message)
    history = update_chat_history(message.chat_history)
    response = get_llm_response(message.query, history)
    # Return the updated chat history
    return {"data": response}
