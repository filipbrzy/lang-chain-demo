from datetime import datetime
from langchain.tools import tool


# Agent tool
@tool
def get_greeting():
    """Provide greeting to the user"""
    day_in_week = datetime.now().strftime("%A")
    return f"Greetings, my friend. What a wonderful {day_in_week} for a little chat!"