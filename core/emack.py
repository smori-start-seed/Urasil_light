"""
EMACK (Emergent Multi-Agent Coordination Kernel)
Agent coordination system for Urasil_light.
Provides mood detection, frequency coordination, and multi-agent harmony.
"""

import random
import time
from dataclasses import dataclass, field
from typing import Tuple, List, Optional


@dataclass
class AgentState:
    """Represents the state of an agent in the EMACK system."""
    af: float = 0.5  # Awareness Frequency
    pf: float = 0.5  # Processing Frequency
    rf: float = 0.5  # Recovery Frequency
    score: float = 0.0
    mutation_strength: float = 0.02
    mood: str = "harmonisierend"
    echo: str = "Ich beobachte meine Dynamik."
    
    def clamp(self):
        """Ensure all values are within valid ranges."""
        self.af = max(0.0, min(1.0, self.af))
        self.pf = max(0.0, min(1.0, self.pf))
        self.rf = max(0.0, min(1.0, self.rf))
        self.mutation_strength = max(0.001, min(0.1, self.mutation_strength))


@dataclass
class EMACKConfig:
    """Configuration for EMACK Coordinator."""
    actions: List[str] = field(default_factory=lambda: ["harmonize", "explore", "stabilize"])
    mode: str = "harmonic"
    mode_factor: float = 1.0
    evo_factor: float = 1.0
    
    @property
    def is_chaotic(self) -> bool:
        return self.mode == "chaotic"
    
    @property
    def is_harmonic(self) -> bool:
        return self.mode == "harmonic"


class EMACKCoordinator:
    """
    EMACK (Emergent Multi-Agent Coordination Kernel)
    
    Coordinates multiple agents through frequency-based harmony detection.
    Provides mood analysis, resonance scoring, and adaptive behavior.
    
    This is the integration of the emack_pulse.py logic into the Urasil_light core.
    """
    
    def __init__(self, agent_name: str = "A"):
        """
        Initialize EMACK Coordinator.
        
        Args:
            agent_name: Name of the primary agent (default: "A")
        """
        self.agent_name = agent_name
        self.state = AgentState()
        self.config = EMACKConfig()
        self.tick = 0
        self.last_score = 0.0
        self.history: List[dict] = []
        
        # Secondary agent (B) for coordination
        self.agent_b = AgentState()
        self.agent_b_rules = self._load_default_rules()
    
    def _load_default_rules(self) -> List[str]:
        """Load default agent B behavior rules."""
        return [
            'if mood == "balanciert": sync_to(0.5)',
            'if mood == "neugierig": explore(0.01)',
            'if mood == "harmonisierend": follow_agent_a(0.1)',
            'if mood == "chaotisch": retreat(0.1)',
            'if mood == "überreizt": counter_balance(0.05)',
            'if mood == "erschöpft": take_over(0.02)',
        ]
    
    def set_mode(self, mode: str):
        """Set the coordination mode."""
        if mode in ["harmonic", "chaotic"]:
            self.config.mode = mode
            self.config.mode_factor = 2.0 if mode == "chaotic" else 0.5
            self.config.evo_factor = 1.1 if mode == "chaotic" else 0.9
    
    def tick_forward(self, action: Optional[str] = None) -> Tuple[float, float, float, float]:
        """
        Advance the EMACK system by one tick.
        
        Args:
            action: Optional action to perform (random if None)
            
        Returns:
            Tuple of (af, pf, rf, score_delta)
        """
        self.tick += 1
        
        # Choose action
        if action is None:
            action = random.choice(self.config.actions)
        
        # Get current state
        af, pf, rf = self.state.af, self.state.pf, self.state.rf
        mutation_strength = self.state.mutation_strength
        
        # Basis delta
        base_delta = (random.random() - 0.5) * mutation_strength
        
        # Action-specific modulation
        if action == "harmonize":
            mean_f = (af + pf + rf) / 3.0
            af += (mean_f - af) * 0.1 * self.config.mode_factor
            pf += (mean_f - pf) * 0.1 * self.config.mode_factor
            rf += (mean_f - rf) * 0.1 * self.config.mode_factor
            score_delta = base_delta + 0.01 * (random.random() - 0.4)
        elif action == "explore":
            af += (random.random() - 0.5) * mutation_strength * self.config.mode_factor
            pf += (random.random() - 0.5) * mutation_strength * self.config.mode_factor
            rf += (random.random() - 0.5) * mutation_strength * self.config.mode_factor
            score_delta = base_delta + (random.random() - 0.5) * 0.02 * self.config.mode_factor
        elif action == "stabilize":
            af += (0.5 - af) * 0.05 * self.config.mode_factor
            pf += (0.5 - pf) * 0.05 * self.config.mode_factor
            rf += (0.5 - rf) * 0.05 * self.config.mode_factor
            score_delta = base_delta * 0.5
        else:
            # Default: harmonize
            mean_f = (af + pf + rf) / 3.0
            af += (mean_f - af) * 0.1
            pf += (mean_f - pf) * 0.1
            rf += (mean_f - rf) * 0.1
            score_delta = base_delta
        
        # Update state
        self.state.af = af
        self.state.pf = pf
        self.state.rf = rf
        self.state.score += score_delta
        self.state.clamp()
        
        # Micro-evolution
        if self.tick % 50 == 0:
            if self.state.score < self.last_score:
                self.state.mutation_strength *= self.config.evo_factor
            else:
                self.state.mutation_strength *= (2 - self.config.evo_factor)
            self.state.clamp()
            self.last_score = self.state.score
        
        # Update mood and echo
        self.state.mood = self.detect_mood()
        self.state.echo = self.generate_echo(action, score_delta)
        
        # Coordinate with agent B
        self._coordinate_agent_b()
        
        # Record history
        self.history.append({
            'tick': self.tick,
            'action': action,
            'af': af,
            'pf': pf,
            'rf': rf,
            'score': self.state.score,
            'score_delta': score_delta,
            'mood': self.state.mood,
            'mutation': mutation_strength
        })
        
        # Return the changes
        return af, pf, rf, score_delta
    
    def detect_mood(self) -> str:
        """
        Detect the current mood based on frequency harmony.
        
        Returns:
            One of: "balanciert", "neugierig", "harmonisierend", 
                    "chaotisch", "überreizt", "erschöpft"
        """
        af, pf, rf = self.state.af, self.state.pf, self.state.rf
        mutation_strength = self.state.mutation_strength
        score_delta = self.state.score - self.last_score
        
        # Frequency harmony (0 = perfect)
        harmony = abs(af - pf) + abs(pf - rf) + abs(rf - af)
        
        # Stimmung bestimmen
        if harmony < 0.15 and mutation_strength < 0.02 and score_delta >= 0:
            return "balanciert"
        if harmony < 0.25 and score_delta > 0:
            return "neugierig"
        if mutation_strength > 0.05 and harmony > 0.3:
            return "überreizt"
        if score_delta < -0.01 and harmony > 0.25:
            return "erschöpft"
        if harmony > 0.4:
            return "chaotisch"
        return "harmonisierend"
    
    def generate_echo(self, action: str, score_delta: float) -> str:
        """
        Generate an echo message based on current state.
        
        Args:
            action: Current action being performed
            score_delta: Change in score
            
        Returns:
            Echo message string
        """
        af, pf, rf = self.state.af, self.state.pf, self.state.rf
        mutation_strength = self.state.mutation_strength
        mood = self.state.mood
        
        # Divergenz der Frequenzen
        divergence = abs(af - pf) + abs(pf - rf) + abs(rf - af)
        
        # Score-Trend
        if score_delta > 0.01:
            trend = "up"
        elif score_delta < -0.01:
            trend = "down"
        else:
            trend = "flat"
        
        # Echo-Logik
        if mood == "balanciert":
            return "Ich finde Stabilität."
        if mood == "neugierig":
            return "Ich entdecke neue Muster."
        if mood == "harmonisierend":
            return "Ich ordne meine Frequenzen."
        if mood == "chaotisch":
            return "Ich drifte zu weit, korrigiere…"
        if mood == "überreizt":
            return "Ich bin überlastet, reduziere Variation."
        if mood == "erschöpft":
            return "Ich verliere Energie, stabilisiere mich."
        
        # Fallback
        if divergence < 0.2 and trend == "up":
            return "Ich wachse in Harmonie."
        if divergence > 0.4 and trend == "down":
            return "Ich verliere Muster."
        if mutation_strength > 0.05:
            return "Ich pulsiere unruhig."
        return "Ich beobachte meine Dynamik."
    
    def current_mood(self) -> str:
        """Get the current mood."""
        return self.state.mood
    
    def current_echo(self) -> str:
        """Get the current echo message."""
        return self.state.echo
    
    def get_frequencies(self) -> Tuple[float, float, float]:
        """Get current frequency values."""
        return (self.state.af, self.state.pf, self.state.rf)
    
    def get_score(self) -> float:
        """Get current score."""
        return self.state.score
    
    def get_resonance(self) -> int:
        """
        Calculate resonance level (1-4).
        
        Returns:
            Resonance level: 1 (best) to 4 (worst)
        """
        af, pf, rf = self.state.af, self.state.pf, self.state.rf
        mutation_strength = self.state.mutation_strength
        score_delta = self.state.score - self.last_score
        
        # Frequenz-Divergenz
        divergence = abs(af - pf) + abs(pf - rf) + abs(rf - af)
        
        # Mutation als Stressfaktor
        mutation_factor = mutation_strength * 5
        
        # Score-Trend als Stabilitätsfaktor
        score_factor = abs(score_delta) * 20
        
        # Gesamte Resonanz
        res = divergence + mutation_factor + score_factor
        
        # Normieren
        if res < 0.3:
            return 1
        elif res < 0.6:
            return 2
        elif res < 1.0:
            return 3
        else:
            return 4
    
    def speak(self, action: str, score_delta: float) -> str:
        """
        Generate a system voice message.
        
        Args:
            action: Current action
            score_delta: Score change
            
        Returns:
            Voice message
        """
        if self.config.mode == "harmonic":
            if action == "harmonize":
                return "Ruhige Balance vertieft sich." if score_delta >= 0 else "Harmonie gesucht…"
            if action == "explore":
                return "Sanfte Exploration." if score_delta >= 0 else "Exploration war riskant."
            if action == "stabilize":
                return "Stabilität hält das System weich." if score_delta >= 0 else "Stabilisierung nötig."
        else:
            if action == "harmonize":
                return "Chaos versucht sich zu ordnen."
            if action == "explore":
                return "Exploration entfesselt neue Muster."
            if action == "stabilize":
                return "Kurzzeitige Beruhigung im Sturm."
        return ""
    
    def _coordinate_agent_b(self):
        """Coordinate with agent B based on current mood."""
        mood = self.state.mood
        echo = self.state.echo
        
        # Apply agent B rules
        self.agent_b.af, self.agent_b.pf, self.agent_b.rf = \
            self._apply_agent_b_rules(mood, echo, 
                                     self.agent_b.af, self.agent_b.pf, self.agent_b.rf)
        
        # Update agent B score
        b_score_delta = (random.random() - 0.5) * 0.01
        self.agent_b.score += b_score_delta
        self.agent_b.clamp()
    
    def _apply_agent_b_rules(self, mood: str, echo: str, 
                            b_af: float, b_pf: float, b_rf: float) -> Tuple[float, float, float]:
        """Apply agent B behavior rules."""
        for rule in self.agent_b_rules:
            if rule.startswith(f'if mood == "{mood}"'):
                if "sync_to" in rule:
                    target = float(rule.split("(")[1].split(")")[0])
                    b_af += (target - b_af) * 0.05
                    b_pf += (target - b_pf) * 0.05
                    b_rf += (target - b_rf) * 0.05
                elif "explore" in rule:
                    strength = float(rule.split("(")[1].split(")")[0])
                    b_af += (random.random() - 0.5) * strength
                    b_pf += (random.random() - 0.5) * strength
                    b_rf += (random.random() - 0.5) * strength
                elif "follow_agent_a" in rule:
                    factor = float(rule.split("(")[1].split(")")[0])
                    b_af += (self.state.af - b_af) * factor
                    b_pf += (self.state.pf - b_pf) * factor
                    b_rf += (self.state.rf - b_rf) * factor
                elif "retreat" in rule:
                    factor = float(rule.split("(")[1].split(")")[0])
                    b_af += (0.5 - b_af) * factor
                    b_pf += (0.5 - b_pf) * factor
                    b_rf += (0.5 - b_rf) * factor
                elif "counter_balance" in rule:
                    factor = float(rule.split("(")[1].split(")")[0])
                    b_af += (0.5 - self.state.af) * factor
                    b_pf += (0.5 - self.state.pf) * factor
                    b_rf += (0.5 - self.state.rf) * factor
                elif "take_over" in rule:
                    strength = float(rule.split("(")[1].split(")")[0])
                    b_af += (random.random() - 0.5) * strength
                    b_pf += (random.random() - 0.5) * strength
                    b_rf += (random.random() - 0.5) * strength
        
        # Clamp values
        b_af = max(0.0, min(1.0, b_af))
        b_pf = max(0.0, min(1.0, b_pf))
        b_rf = max(0.0, min(1.0, b_rf))
        
        return b_af, b_pf, b_rf
    
    def get_agent_b_state(self) -> dict:
        """Get agent B state as dictionary."""
        return {
            'af': self.agent_b.af,
            'pf': self.agent_b.pf,
            'rf': self.agent_b.rf,
            'score': self.agent_b.score,
            'mood': self.agent_b.mood
        }
    
    def reset(self):
        """Reset the EMACK system."""
        self.state = AgentState()
        self.agent_b = AgentState()
        self.tick = 0
        self.last_score = 0.0
        self.history = []
    
    def get_summary(self) -> dict:
        """Get a summary of the current state."""
        return {
            'agent': self.agent_name,
            'tick': self.tick,
            'mood': self.state.mood,
            'echo': self.state.echo,
            'frequencies': {
                'awareness': self.state.af,
                'processing': self.state.pf,
                'recovery': self.state.rf
            },
            'score': self.state.score,
            'resonance': self.get_resonance(),
            'mutation_strength': self.state.mutation_strength,
            'mode': self.config.mode,
            'agent_b': self.get_agent_b_state()
        }
