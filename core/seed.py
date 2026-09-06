from core.mandate import Mandate


class Seed:
    """
    Seed Module - Generates raw responses based on meaning and context.
    
    The seed is the core of the response, containing the essential meaning
    before stylistic refinement by Silky Edge.
    """
    
    def __init__(self, identity, zyklus):
        self.identity = identity
        self.zyklus = zyklus
        self.mandate = Mandate(identity)

    def generiere(self, bedeutung):
        """
        Generate a raw response based on meaning and current state.
        
        Args:
            bedeutung: The extracted meaning from interpretation
            
        Returns:
            Raw response text
        """
        modus = self.zyklus.matrix()

        # Zyklus-Fokus bestimmt die Art der Antwort
        if modus["fokus"] == "fokus":
            antwort = f"Direkt: {bedeutung}"

        elif modus["fokus"] == "variation":
            antwort = f"Alternative Sicht: {bedeutung}"

        else:
            antwort = f"Zusammenhang: {bedeutung}"

        # Reflexionssignal aus der Identitaet
        reflex = self.identity.data.get("letzte_korrektur", "ok")

        # Wenn letzte Antwort nicht gold-konform war -> mehr Klarheit
        if reflex == "gold":
            # Enhance with GOLD values for better alignment
            gold_values = self.mandate.ideal()
            if gold_values:
                # Add relevant GOLD value to guide the response
                relevant_value = gold_values[0] if gold_values else "Klarheit"
                antwort = f"Klarer [{relevant_value}]: {antwort}"
            else:
                antwort = "Klarer: " + antwort

        # Apply EMACK mood influence if available
        emack_mood = self.identity.data.get("emack_mood", "harmonisierend")
        if emack_mood == "chaotisch" or emack_mood == "uberreizt":
            # Add stability in chaotic states
            antwort = f"[Stabil] {antwort}"
        elif emack_mood == "balanciert":
            # Add harmony marker
            antwort = f"[Harmonie] {antwort}"

        return antwort
    
    def generiere_mit_kontext(self, bedeutung, kontext=None):
        """
        Generate response with additional context.
        
        Args:
            bedeutung: The extracted meaning
            kontext: Additional context dictionary
            
        Returns:
            Enhanced raw response
        """
        # For now, just use the basic generation
        # Can be extended to use context
        return self.generiere(bedeutung)
