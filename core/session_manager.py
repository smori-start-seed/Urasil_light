"""
Session Manager Module
Manages conversation sessions and context for Urasil_light.
"""

import datetime
import uuid
from typing import Optional, Dict, Any, List


class SessionManager:
    """
    Manages conversation sessions with Urasil_light.
    
    Tracks:
    - Session lifecycle (start, end)
    - Conversation history
    - Context and themes
    - User preferences
    """
    
    def __init__(self, identity):
        """
        Initialize Session Manager.
        
        Args:
            identity: Identity instance for persistence
        """
        self.identity = identity
        self.session_id: Optional[str] = None
        self.start_time: Optional[datetime.datetime] = None
        self.history: List[Dict[str, Any]] = []
        self.context: Dict[str, Any] = {
            'theme': None,
            'mood': 'neutral',
            'depth': 0,
            'user_intent': None,
            'conversation_flow': []
        }
        self.stats: Dict[str, Any] = {
            'message_count': 0,
            'word_count': 0,
            'gold_conform_count': 0,
            'maturity_scores': []
        }
    
    def start(self):
        """Start a new session."""
        self.session_id = str(uuid.uuid4())
        self.start_time = datetime.datetime.now()
        self.history = []
        self.context = {
            'theme': None,
            'mood': 'neutral',
            'depth': 0,
            'user_intent': None,
            'conversation_flow': []
        }
        self.stats = {
            'message_count': 0,
            'word_count': 0,
            'gold_conform_count': 0,
            'maturity_scores': []
        }
        
        # Update identity
        self.identity.data["session_active"] = True
        self.identity.data["session_id"] = self.session_id
        self.identity.data["session_start"] = self.start_time.isoformat()
    
    def end(self):
        """End the current session."""
        self.identity.data["session_active"] = False
        self.identity.data["session_end"] = datetime.datetime.now().isoformat()
        self.identity.data["session_duration"] = self.get_duration()
        
        # Store session summary
        self.identity.data["session_summary"] = self.get_summary()
    
    def add_interaction(self, user_input: str, response: str, 
                      metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Add a user-AI interaction to the session history.
        
        Args:
            user_input: User's input text
            response: AI's response text
            metadata: Optional additional metadata
            
        Returns:
            The interaction entry
        """
        self.stats['message_count'] += 1
        self.stats['word_count'] += len(user_input.split()) + len(response.split())
        
        if metadata and metadata.get('gold_conform'):
            self.stats['gold_conform_count'] += 1
        
        if metadata and 'maturity_score' in metadata:
            self.stats['maturity_scores'].append(metadata['maturity_score'])
        
        entry = {
            'session_id': self.session_id,
            'timestamp': datetime.datetime.now().isoformat(),
            'user_input': user_input,
            'response': response,
            'metadata': metadata or {}
        }
        
        self.history.append(entry)
        self.context['conversation_flow'].append(entry)
        
        # Update context
        self._update_context(user_input, response, metadata)
        
        return entry
    
    def _update_context(self, user_input: str, response: str, 
                       metadata: Optional[Dict] = None):
        """Update conversation context based on interaction."""
        # Analyze for theme
        self._update_theme(user_input, response)
        
        # Analyze for mood
        self._update_mood(user_input, response)
        
        # Update depth
        self._update_depth(user_input, response)
        
        # Update user intent
        self._update_user_intent(user_input)
        
        # Apply metadata if available
        if metadata:
            if 'zyklus' in metadata:
                self.context['zyklus'] = metadata['zyklus']
            if 'emack_mood' in metadata:
                self.context['emack_mood'] = metadata['emack_mood']
    
    def _update_theme(self, user_input: str, response: str):
        """Detect and update conversation theme."""
        # Simple theme detection based on keywords
        text = f"{user_input} {response}".lower()
        
        theme_keywords = {
            'philosophie': ['existenz', 'bewegung', 'verbindung', 'änderung', 'unendlich'],
            'technik': ['system', 'code', 'programm', 'algorithm', 'ki'],
            'emotion': ['gefühl', 'liebe', 'freude', 'traurig', 'glücklich'],
            'kreativ': ['schaffen', 'kunst', 'malen', 'tanzen', 'musik'],
            'praktisch': ['machen', 'bauen', 'werkzeug', 'anwendung', 'praktisch']
        }
        
        for theme, keywords in theme_keywords.items():
            if any(kw in text for kw in keywords):
                if self.context['theme'] is None:
                    self.context['theme'] = theme
                elif theme != self.context['theme']:
                    # Multiple themes detected
                    if isinstance(self.context['theme'], list):
                        if theme not in self.context['theme']:
                            self.context['theme'].append(theme)
                    else:
                        self.context['theme'] = [self.context['theme'], theme]
    
    def _update_mood(self, user_input: str, response: str):
        """Detect and update conversation mood."""
        text = f"{user_input} {response}".lower()
        
        # Simple mood detection
        positive_words = ['gut', 'schön', 'wunderbar', 'fantastisch', 'liebe', 'freude']
        negative_words = ['schlecht', 'schlimm', 'traurig', 'wütend', 'problem']
        
        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)
        
        if positive_count > negative_count:
            self.context['mood'] = 'positiv'
        elif negative_count > positive_count:
            self.context['mood'] = 'negativ'
        else:
            self.context['mood'] = 'neutral'
    
    def _update_depth(self, user_input: str, response: str):
        """Update conversation depth."""
        # Depth increases with longer, more complex responses
        word_count = len(response.split())
        
        if word_count > 50:
            self.context['depth'] += 2
        elif word_count > 20:
            self.context['depth'] += 1
        elif word_count < 5:
            self.context['depth'] = max(0, self.context['depth'] - 1)
        
        # Cap depth
        self.context['depth'] = max(0, min(10, self.context['depth']))
    
    def _update_user_intent(self, user_input: str):
        """Detect and update user intent."""
        text = user_input.lower()
        
        intent_keywords = {
            'frage': ['?', 'wie', 'was', 'warum', 'erkläre'],
            'statement': ['.', 'ich denke', 'ich glaube', 'meiner meinung'],
            'befehl': ['mache', 'tu', 'erzeuge', 'schreibe', 'zeige'],
            'feedback': ['danke', 'gut', 'schlecht', 'gefällt', 'mag']
        }
        
        for intent, keywords in intent_keywords.items():
            if any(kw in text for kw in keywords):
                self.context['user_intent'] = intent
                break
    
    def get_context(self) -> Dict[str, Any]:
        """Get current conversation context."""
        return {
            **self.context,
            'session_id': self.session_id,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'duration': self.get_duration(),
            'stats': self.stats
        }
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict]:
        """Get session history."""
        if limit is None:
            return self.history
        return self.history[-limit:]
    
    def get_duration(self) -> float:
        """Get session duration in seconds."""
        if self.start_time is None:
            return 0.0
        return (datetime.datetime.now() - self.start_time).total_seconds()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get session summary."""
        duration = self.get_duration()
        
        avg_maturity = 0
        if self.stats['maturity_scores']:
            avg_maturity = sum(self.stats['maturity_scores']) / len(self.stats['maturity_scores'])
        
        gold_rate = 0
        if self.stats['message_count'] > 0:
            gold_rate = self.stats['gold_conform_count'] / self.stats['message_count']
        
        return {
            'session_id': self.session_id,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'duration_seconds': duration,
            'message_count': self.stats['message_count'],
            'word_count': self.stats['word_count'],
            'gold_conform_rate': gold_rate,
            'avg_maturity_score': avg_maturity,
            'theme': self.context['theme'],
            'mood': self.context['mood'],
            'depth': self.context['depth']
        }
    
    def is_active(self) -> bool:
        """Check if session is active."""
        return self.identity.data.get("session_active", False)
    
    def clear_history(self):
        """Clear session history."""
        self.history = []
        self.context['conversation_flow'] = []
