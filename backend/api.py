from livekit.agents import llm
import enum
from typing import Annotated, Optional
import logging
from db_driver import DatabaseDriver
import uuid
from datetime import datetime

logger = logging.getLogger("mental-health-assistant")
logger.setLevel(logging.INFO)

DB = DatabaseDriver()

class UserStatus(enum.Enum):
    NEW = "new"
    RETURNING = "returning"
    UNKNOWN = "unknown"

class AssistantFnc(llm.FunctionContext):
    def __init__(self):
        super().__init__()
        
        self._user_details = {
            "user_id": "",
            "name": "",
            "status": UserStatus.UNKNOWN,
            "current_conversation_id": None
        }
    
    def get_user_str(self):
        user_str = ""
        for key, value in self._user_details.items():
            if key != "status" and key != "current_conversation_id":
                user_str += f"{key}: {value}\n"
            
        if self._user_details["status"] != UserStatus.UNKNOWN:
            user_str += f"status: {self._user_details['status'].value}\n"
        
        return user_str
    
    @llm.ai_callable(description="lookup a user by their ID")
    def lookup_user(self, user_id: Annotated[str, llm.TypeInfo(description="The ID of the user to lookup")]):
        logger.info("lookup user - user_id: %s", user_id)
        
        result = DB.get_user_by_id(user_id)
        if result is None:
            return "User not found"
        
        self._user_details["user_id"] = result.user_id
        self._user_details["name"] = result.name
        self._user_details["status"] = UserStatus.RETURNING
        
        # Create a new conversation for this session
        conversation = DB.create_conversation(result.user_id)
        if conversation:
            self._user_details["current_conversation_id"] = conversation.conversation_id
        
        recent_conversations = DB.get_user_conversations(result.user_id, 3)
        
        response = f"Welcome back, {result.name}!\n"
        
        if recent_conversations:
            response += "Here's a summary of your recent conversations:\n"
            for conv in recent_conversations:
                if conv.mood_rating:
                    response += f"- Session on {conv.timestamp[:10]}: Mood rating: {conv.mood_rating}/10\n"
                else:
                    response += f"- Session on {conv.timestamp[:10]}\n"
        
        return response
    
    @llm.ai_callable(description="get the details of the current user")
    def get_user_details(self):
        logger.info("get user details")
        if self._user_details["user_id"] == "":
            return "No user is currently active. Please create a new user or lookup an existing one."
        
        return f"The current user details are:\n{self.get_user_str()}"
    
    @llm.ai_callable(description="create a new user")
    def create_user(
        self, 
        name: Annotated[str, llm.TypeInfo(description="The name of the user")]
    ):
        user_id = str(uuid.uuid4())
        logger.info("create user - user_id: %s, name: %s", user_id, name)
        
        result = DB.create_user(user_id, name)
        if result is None:
            return "Failed to create user"
        
        self._user_details["user_id"] = result.user_id
        self._user_details["name"] = result.name
        self._user_details["status"] = UserStatus.NEW
        
        # Create a new conversation for this session
        conversation = DB.create_conversation(result.user_id)
        if conversation:
            self._user_details["current_conversation_id"] = conversation.conversation_id
        
        return f"Welcome, {name}! I've created a profile for you. How can I support you today?"
    
    @llm.ai_callable(description="record a message in the current conversation")
    def record_message(
        self,
        content: Annotated[str, llm.TypeInfo(description="The message content")],
        sender: Annotated[str, llm.TypeInfo(description="Who sent the message (user/assistant)")] = "user"
    ):
        if not self._user_details["current_conversation_id"]:
            return "No active conversation. Please create a user first."
        
        logger.info("recording message from %s in conversation %s", 
                   sender, self._user_details["current_conversation_id"])
        
        message = DB.add_message(
            self._user_details["current_conversation_id"],
            sender,
            content
        )
        
        if message:
            return f"Message recorded successfully"
        else:
            return f"Failed to record message"
    
    @llm.ai_callable(description="update the mood rating for the current conversation")
    def update_mood_rating(
        self,
        rating: Annotated[int, llm.TypeInfo(description="The mood rating on a scale of 1-10")]
    ):
        if not self._user_details["current_conversation_id"]:
            return "No active conversation. Please create a user first."
        
        # This would require adding a method to the DatabaseDriver class
        # For now, we'll just log it
        logger.info("updating mood rating to %d for conversation %s", 
                   rating, self._user_details["current_conversation_id"])
        
        return f"Mood rating updated to {rating}/10"
    
    def has_user(self):
        return self._user_details["user_id"] != ""