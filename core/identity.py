import json
import os

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

# Default baseline identity for when files are missing
DEFAULT_BASELINE = {
    "erstellt": "2026-01-01T00:00:00Z",
    "beschreibung": "Baseline Identity",
    "werte": ["klarheit", "ehrlichkeit", "resonanz"],
    "grundton": "neutral",
    "mandate": [],
    "nodus": {},
    "erfahrung": [],
    "zyklus": {"sonne": 0, "mond": 0, "tag": 0}
}

class Identity:
    """
    Identity Module - Manages persistent state for Urasil_light.
    
    Handles loading, saving, and resetting the identity data.
    """
    
    def __init__(self, data):
        """
        Initialize Identity with data.
        
        Args:
            data: Dictionary containing identity data
        """
        self.data = data

    @staticmethod
    def load():
        """
        Load identity from file, or create from baseline.
        
        Returns:
            Identity instance
        """
        path = os.path.join(DATA_PATH, "identity.json")
        baseline_path = os.path.join(DATA_PATH, "baseline_identity.json")

        # Try to load baseline
        try:
            with open(baseline_path, "r") as f:
                baseline = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            baseline = DEFAULT_BASELINE.copy()

        # Try to load identity
        try:
            if os.path.exists(path):
                with open(path, "r") as f:
                    identity = json.load(f)
            else:
                identity = baseline.copy()
        except (json.JSONDecodeError, OSError):
            # If identity file is corrupted, start from baseline
            identity = baseline.copy()

        return Identity(identity)

    @staticmethod
    def save(data):
        """
        Save identity to file.
        
        Args:
            data: Dictionary to save
        """
        path = os.path.join(DATA_PATH, "identity.json")
        
        # Ensure directory exists
        os.makedirs(DATA_PATH, exist_ok=True)
        
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
    
    @staticmethod
    def reset_to_baseline():
        """
        Reset identity to baseline.
        
        Returns:
            New Identity instance with baseline data
        """
        baseline_path = os.path.join(DATA_PATH, "baseline_identity.json")
        
        try:
            with open(baseline_path, "r") as f:
                baseline = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            baseline = DEFAULT_BASELINE.copy()
        
        Identity.save(baseline)
        return Identity(baseline)
