"""
Urasil_light Pipeline
Unified processing pipeline for the AI core system.
"""

import datetime
from typing import Optional, Dict, Any, List
from .identity import Identity
from .zyklus import Zyklus
from .interpretation import Interpretation
from .seed import Seed
from .silky_edge import SilkyEdge
from .erfahrung import Erfahrung
from .rueckmeldung import Rueckmeldung
from .mandate import Mandate
from .ininity import Ininity
from .session_manager import SessionManager
from .emack import EMACKCoordinator


class Pipeline:
    """
    Unified Pipeline for Urasil_light
    
    Coordinates all core modules to process user input and generate responses.
    Implements the complete flow:
    User Input -> Interpretation -> Seed -> Silky Edge -> Rueckmeldung -> Erfahrung -> Identity
    
    With EMACK coordination for adaptive behavior.
    """
    
    def __init__(self, identity: Optional[Identity] = None):
        """
        Initialize the pipeline.
        
        Args:
            identity: Optional Identity instance. If None, loads from file.
        """
        # Load or use provided identity
        if identity is None:
            self.identity = Identity.load()
        else:
            self.identity = identity
        
        # Initialize all components
        self.zyklus = Zyklus(self.identity.data)
        self.interpretation = Interpretation(self.identity, self.zyklus)
        self.seed = Seed(self.identity, self.zyklus)
        self.silky_edge = SilkyEdge(self.identity, self.zyklus)
        self.erfahrung = Erfahrung(self.identity, self.zyklus)
        self.rueckmeldung = Rueckmeldung(self.identity, self.zyklus)
        self.mandate = Mandate(self.identity)
        self.ininity = Ininity()
        self.session = SessionManager(self.identity)
        self.emack = EMACKCoordinator("Urasil")
        
        # Pipeline configuration
        self.config = {
            'store_experience': True,
            'use_emack': True,
            'use_feedback': True,
            'min_maturity_score': 0.3,
            'max_history': 100
        }
        
        # Conversation history
        self.history: List[Dict[str, Any]] = []
    
    def process(self, user_input: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Process user input through the complete pipeline.
        
        Args:
            user_input: User input text
            context: Optional additional context
            
        Returns:
            Dictionary containing:
            - response: Generated response text
            - bedeutung: Extracted meaning
            - rohantwort: Raw response before styling
            - metadata: Processing metadata
        """
        # Start session if not active
        if not self.identity.data.get("session_active", False):
            self.session.start()
        
        # Advance EMACK if enabled
        if self.config['use_emack']:
            action = self._select_action()
            self.emack.tick_forward(action)
            emack_mood = self.emack.current_mood()
        else:
            emack_mood = "harmonisierend"
        
        # Advance Zyklus
        self.zyklus.fortschritt()
        self.zyklus.speichern(self.identity.data)
        
        # Get current matrix (state)
        matrix = self.zyklus.matrix()
        
        # Step 1: Interpretation
        bedeutung = self.interpretation.verarbeite(user_input)
        
        # Step 2: Seed (Raw response generation)
        rohantwort = self.seed.generiere(bedeutung)
        
        # Step 3: Silky Edge (Stylistic refinement)
        antwort = self.silky_edge.veredeln(rohantwort, bedeutung)
        
        # Step 4: Rueckmeldung (Self-evaluation)
        self.rueckmeldung.verarbeite(antwort)
        
        # Step 5: Erfahrung (Store mature experiences)
        if self.config['store_experience']:
            # Check maturity before storing
            maturity_score = self.ininity.reife_score(bedeutung)
            if maturity_score >= self.config['min_maturity_score']:
                self.erfahrung.speichern(bedeutung)
        
        # Save identity
        Identity.save(self.identity.data)
        
        # Store in history
        self._add_to_history(user_input, antwort, bedeutung, rohantwort, matrix, emack_mood)
        
        # Build response
        response = {
            'response': antwort,
            'bedeutung': bedeutung,
            'rohantwort': rohantwort,
            'metadata': {
                'timestamp': datetime.datetime.now().isoformat(),
                'zyklus': matrix,
                'emack_mood': emack_mood,
                'emack_echo': self.emack.current_echo(),
                'resonance': self.emack.get_resonance(),
                'maturity_score': self.ininity.reife_score(bedeutung),
                'gold_conform': self.mandate.passt(antwort),
                'session_active': self.identity.data.get("session_active", False)
            }
        }
        
        return response
    
    def _select_action(self) -> str:
        """Select action based on EMACK mood."""
        mood = self.emack.current_mood()
        
        # Map mood to preferred actions
        mood_actions = {
            "balanciert": ["harmonize", "harmonize", "explore"],
            "neugierig": ["explore", "explore", "harmonize"],
            "harmonisierend": ["harmonize", "explore", "stabilize"],
            "chaotisch": ["stabilize", "stabilize", "harmonize"],
            "überreizt": ["stabilize", "stabilize", "stabilize"],
            "erschöpft": ["harmonize", "stabilize", "stabilize"]
        }
        
        import random
        return random.choice(mood_actions.get(mood, ["harmonize", "explore", "stabilize"]))
    
    def _add_to_history(self, user_input: str, response: str, bedeutung: str, 
                      rohantwort: str, matrix: Dict, emack_mood: str):
        """Add conversation to history."""
        entry = {
            'user_input': user_input,
            'response': response,
            'bedeutung': bedeutung,
            'rohantwort': rohantwort,
            'timestamp': datetime.datetime.now().isoformat(),
            'zyklus': matrix,
            'emack_mood': emack_mood
        }
        
        self.history.append(entry)
        
        # Trim history if too long
        if len(self.history) > self.config['max_history']:
            self.history = self.history[-self.config['max_history']:]
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict]:
        """Get conversation history."""
        if limit is None:
            return self.history
        return self.history[-limit:]
    
    def get_state(self) -> Dict[str, Any]:
        """Get current pipeline state."""
        return {
            'zyklus': self.zyklus.als_dict(),
            'emack': self.emack.get_summary(),
            'session_active': self.identity.data.get("session_active", False),
            'history_count': len(self.history),
            'gold_values': self.mandate.ideal(),
            'maturity_criteria': self.ininity.kriterien
        }
    
    def reset(self):
        """Reset the pipeline."""
        self.emack.reset()
        self.history = []
    
    def end_session(self):
        """End the current session."""
        self.session.end()
        Identity.save(self.identity.data)


class AsyncPipeline(Pipeline):
    """
    Asynchronous version of the pipeline for async contexts.
    (Placeholder for future async implementation)
    """
    pass
