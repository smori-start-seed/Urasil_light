import os
import functools


class Mandate:
    """
    Mandate Module - Manages GOLD values and their application.
    
    GOLD (Grounded Oneness, Living Democracy) provides the value system
    that guides response generation and evaluation.
    """
    
    def __init__(self, identity):
        self.identity = identity
        self.gold = self._lade_gold()

    @functools.lru_cache(maxsize=128)
    def _lade_gold(self):
        """Load GOLD values from file with caching."""
        pfad = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data",
            "gold.txt"
        )

        if not os.path.exists(pfad):
            return []

        with open(pfad, "r", encoding='utf-8') as f:
            inhalt = f.read().strip()

        # gold.txt wird in einzelne Leitlinien zerlegt
        lines = [zeile.strip() for zeile in inhalt.split("\n") if zeile.strip()]
        
        # Filter out comments and empty lines
        gold_values = []
        for line in lines:
            # Skip comment lines
            if line.startswith('#') or line.startswith('---'):
                continue
            # Skip title lines (all caps, short)
            if line.isupper() and len(line.split()) <= 3:
                continue
            # Add non-empty lines
            if line:
                gold_values.append(line)
        
        return gold_values[:50]  # Limit to first 50 values

    def ideal(self):
        """
        Get the list of ideal GOLD mandates.
        
        Returns:
            List of GOLD value strings
        """
        return self.gold

    def passt(self, text):
        """
        Check if text conforms to GOLD values.
        
        Args:
            text: Text to check
            
        Returns:
            True if text contains any GOLD value, False otherwise
        """
        text_lower = text.lower()
        for wert in self.gold:
            if wert.lower() in text_lower:
                return True
        return False
    
    def score(self, text) -> float:
        """
        Score text based on GOLD value alignment.
        
        Args:
            text: Text to score
            
        Returns:
            Score between 0 and 1 (higher is better alignment)
        """
        if not self.gold:
            return 0.5
        
        text_lower = text.lower()
        matches = 0
        total_weight = 0
        
        for wert in self.gold:
            # Weight values by position (earlier = more important)
            weight = 1.0 / (self.gold.index(wert) + 1)
            total_weight += weight
            
            if wert.lower() in text_lower:
                matches += weight
        
        if total_weight > 0:
            return matches / total_weight
        return 0.0
    
    def guide_response(self, text: str, strength: float = 0.3) -> str:
        """
        Guide/enhance a response to better align with GOLD values.
        
        Args:
            text: Original response text
            strength: How strongly to apply guidance (0-1)
            
        Returns:
            Enhanced response with GOLD alignment
        """
        if not self.gold:
            return text
        
        # Check which GOLD values are missing
        text_lower = text.lower()
        missing_values = []
        
        for wert in self.gold[:10]:  # Only consider first 10 values
            if wert.lower() not in text_lower:
                missing_values.append(wert)
        
        # Add missing values if any
        if missing_values and strength > 0:
            # Select a relevant value to add
            import random
            value_to_add = random.choice(missing_values[:3])
            
            # Add it in a natural way
            # Determine if we should prepend or append
            if len(text.split()) > 10:
                # Long response: prepend
                text = f"[{value_to_add}] {text}"
            else:
                # Short response: append
                text = f"{text} [{value_to_add}]"
        
        return text
    
    def get_value_by_category(self, category: str) -> list:
        """
        Get GOLD values by category.
        
        Args:
            category: Category to filter by (e.g., "Klarheit", "Integritaet")
            
        Returns:
            List of values in that category
        """
        category_lower = category.lower()
        return [v for v in self.gold if category_lower in v.lower()]
    
    def clear_cache(self):
        """Clear the loading cache."""
        self._lade_gold.cache_clear()
