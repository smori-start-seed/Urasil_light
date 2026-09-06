"""
Urasil_light Core Module
A lightweight experimental AI core system with cyclic internal state and modular response pipeline.
"""

from .zyklus import Zyklus
from .interpretation import Interpretation
from .seed import Seed
from .silky_edge import SilkyEdge
from .erfahrung import Erfahrung
from .rueckmeldung import Rueckmeldung
from .mandate import Mandate
from .ininity import Ininity
from .identity import Identity
from .session_manager import SessionManager
from .pipeline import Pipeline
from .emack import EMACKCoordinator

__all__ = [
    'Zyklus',
    'Interpretation',
    'Seed',
    'SilkyEdge',
    'Erfahrung',
    'Rueckmeldung',
    'Mandate',
    'Ininity',
    'Identity',
    'SessionManager',
    'Pipeline',
    'EMACKCoordinator',
]

__version__ = "2.0.0"
