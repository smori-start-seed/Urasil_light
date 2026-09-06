import os
import functools


class Ininity:
    """
    Ininity Module - Maturity filtering system.
    
    Uses criteria from Ininity.txt to filter and score experiences
    based on their maturity level before storing in the identity.
    """
    
    def __init__(self):
        self.kriterien = self._lade_kriterien()

    @functools.lru_cache(maxsize=128)
    def _lade_kriterien(self):
        """Load maturity criteria from file with caching."""
        pfad = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data",
            "Ininity.txt"
        )

        if not os.path.exists(pfad):
            return []

        with open(pfad, "r", encoding='utf-8') as f:
            inhalt = f.read().strip()

        # Extract meaningful criteria from the text
        # The Ininity.txt contains philosophical text, so we need to
        # extract key concepts that indicate maturity
        lines = inhalt.split('\n')
        
        # Look for specific maturity indicators
        kriterien = []
        maturity_indicators = [
            'honoring existence',
            'everything moves',
            'everything is connected',
            'everything changes',
            'honor existence',
            'becoming what moves you',
            'full capacity',
            'complete presence',
            'authenticity',
            'totality',
            'fluidity',
            'integrity',
            'surrender to process',
            'motion',
            'infinity',
            'connection',
            'love',
            'truth',
            'good',
            'valuable',
            'understanding',
            'wisdom',
            'presence',
            'conscious',
            'alive',
        ]
        
        # Add indicators that appear in the text
        for indicator in maturity_indicators:
            if indicator.lower() in inhalt.lower():
                if indicator not in kriterien:
                    kriterien.append(indicator.lower())
        
        # Also extract significant phrases from the text
        # Look for lines that are short and meaningful
        for line in lines:
            line = line.strip().lower()
            if line and len(line.split()) <= 5 and len(line) > 3:
                # Check if it's a meaningful phrase
                if any(word in line for word in ['honor', 'motion', 'connection', 'existence', 'becoming', 'truth', 'love']):
                    if line not in kriterien:
                        kriterien.append(line)
        
        return kriterien[:100]  # Limit to first 100 criteria

    def ist_reif(self, text, threshold: float = 0.3) -> bool:
        """
        Check if text is mature enough to be stored.
        
        Args:
            text: Text to check
            threshold: Minimum score to be considered mature (0-1)
            
        Returns:
            True if text meets maturity threshold, False otherwise
        """
        return self.reife_score(text) >= threshold

    def reife_score(self, text) -> float:
        """
        Calculate maturity score for text.
        
        Args:
            text: Text to score
            
        Returns:
            Maturity score between 0 and 1
        """
        if not self.kriterien:
            return 0.5
        
        text_lower = text.lower()
        matches = 0
        total_criteria = len(self.kriterien)
        
        for kriterium in self.kriterien:
            if kriterium in text_lower:
                matches += 1
        
        return matches / total_criteria if total_criteria > 0 else 0.0
    
    def get_matching_criteria(self, text) -> list:
        """
        Get list of maturity criteria that match the text.
        
        Args:
            text: Text to check
            
        Returns:
            List of matching criteria
        """
        text_lower = text.lower()
        return [k for k in self.kriterien if k in text_lower]
    
    def get_missing_criteria(self, text) -> list:
        """
        Get list of maturity criteria NOT present in the text.
        
        Args:
            text: Text to check
            
        Returns:
            List of missing criteria
        """
        text_lower = text.lower()
        return [k for k in self.kriterien if k not in text_lower]
    
    def categorize_maturity(self, text) -> str:
        """
        Categorize text maturity level.
        
        Args:
            text: Text to categorize
            
        Returns:
            One of: "unreif", "entwickelnd", "reif", "hochreif"
        """
        score = self.reife_score(text)
        
        if score < 0.2:
            return "unreif"
        elif score < 0.4:
            return "entwickelnd"
        elif score < 0.7:
            return "reif"
        else:
            return "hochreif"
    
    def clear_cache(self):
        """Clear the loading cache."""
        self._lade_kriterien.cache_clear()
    
    def enhance_text(self, text: str, target_score: float = 0.5) -> str:
        """
        Enhance text to improve its maturity score.
        
        Args:
            text: Original text
            target_score: Target maturity score to achieve
            
        Returns:
            Enhanced text with improved maturity
        """
        current_score = self.reife_score(text)
        
        if current_score >= target_score:
            return text
        
        # Get missing criteria
        missing = self.get_missing_criteria(text)
        
        if not missing:
            return text
        
        # Add one missing criterion
        import random
        criterion_to_add = random.choice(missing[:5])
        
        # Add it naturally
        if len(text.split()) > 15:
            # Long text: insert in middle
            words = text.split()
            mid = len(words) // 2
            text = ' '.join(words[:mid]) + f" [{criterion_to_add}] " + ' '.join(words[mid:])
        else:
            # Short text: append
            text = f"{text} [{criterion_to_add}]"
        
        return text
