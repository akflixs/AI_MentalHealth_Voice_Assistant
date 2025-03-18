import sqlite3
from typing import Optional, List
from dataclasses import dataclass
from contextlib import contextmanager
from datetime import datetime

@dataclass
class User:
    user_id: str
    name: str
    created_at: str
    last_session: str

@dataclass
class Conversation:
    conversation_id: int
    user_id: str
    timestamp: str
    mood_rating: Optional[int]
    notes: Optional[str]

@dataclass
class Message:
    message_id: int
    conversation_id: int
    sender: str  # 'user' or 'assistant'
    content: str
    timestamp: str

class DatabaseDriver:
    def __init__(self, db_path: str = "mental_health_db.sqlite"):
        self.db_path = db_path
        self._init_db()

    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    last_session TEXT NOT NULL
                )
            """)
            
            # Create conversations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    conversation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    mood_rating INTEGER,
                    notes TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)
            
            # Create messages table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id INTEGER NOT NULL,
                    sender TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY (conversation_id) REFERENCES conversations (conversation_id)
                )
            """)
            
            conn.commit()

    def create_user(self, user_id: str, name: str) -> User:
        current_time = datetime.now().isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (user_id, name, created_at, last_session) VALUES (?, ?, ?, ?)",
                (user_id, name, current_time, current_time)
            )
            conn.commit()
            return User(user_id=user_id, name=name, created_at=current_time, last_session=current_time)

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            if not row:
                return None
            
            return User(
                user_id=row[0],
                name=row[1],
                created_at=row[2],
                last_session=row[3]
            )
    
    def update_user_session(self, user_id: str) -> bool:
        current_time = datetime.now().isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET last_session = ? WHERE user_id = ?",
                (current_time, user_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    def create_conversation(self, user_id: str, mood_rating: Optional[int] = None, notes: Optional[str] = None) -> Optional[Conversation]:
        current_time = datetime.now().isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO conversations (user_id, timestamp, mood_rating, notes) VALUES (?, ?, ?, ?)",
                (user_id, current_time, mood_rating, notes)
            )
            conversation_id = cursor.lastrowid
            conn.commit()
            
            # Update user's last session time
            self.update_user_session(user_id)
            
            return Conversation(
                conversation_id=conversation_id,
                user_id=user_id,
                timestamp=current_time,
                mood_rating=mood_rating,
                notes=notes
            )

    def add_message(self, conversation_id: int, sender: str, content: str) -> Optional[Message]:
        current_time = datetime.now().isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO messages (conversation_id, sender, content, timestamp) VALUES (?, ?, ?, ?)",
                (conversation_id, sender, content, current_time)
            )
            message_id = cursor.lastrowid
            conn.commit()
            
            return Message(
                message_id=message_id,
                conversation_id=conversation_id,
                sender=sender,
                content=content,
                timestamp=current_time
            )

    def get_user_conversations(self, user_id: str, limit: int = 5) -> List[Conversation]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM conversations WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
                (user_id, limit)
            )
            rows = cursor.fetchall()
            
            return [
                Conversation(
                    conversation_id=row[0],
                    user_id=row[1],
                    timestamp=row[2],
                    mood_rating=row[3],
                    notes=row[4]
                )
                for row in rows
            ]

    def get_conversation_messages(self, conversation_id: int) -> List[Message]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM messages WHERE conversation_id = ? ORDER BY timestamp ASC",
                (conversation_id,)
            )
            rows = cursor.fetchall()
            
            return [
                Message(
                    message_id=row[0],
                    conversation_id=row[1],
                    sender=row[2],
                    content=row[3],
                    timestamp=row[4]
                )
                for row in rows
            ]