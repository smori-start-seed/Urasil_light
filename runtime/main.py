#!/usr/bin/env python3
"""
Urasil_light Main Runtime
Entry point for the Urasil_light AI core system.
"""

import sys
import os

# Ensure the project root is in the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now we can import from core
from core.identity import Identity
from core.zyklus import Zyklus
from core.seed import Seed
from core.silky_edge import SilkyEdge
from core.erfahrung import Erfahrung
from core.interpretation import Interpretation
from core.rueckmeldung import Rueckmeldung
from core.mandate import Mandate
from core.ininity import Ininity
from core.session_manager import SessionManager
from core.pipeline import Pipeline
from core.emack import EMACKCoordinator


def main():
    """
    Main entry point for Urasil_light CLI.
    
    Processes user input through the complete pipeline and outputs responses.
    """
    # Method 1: Use the unified Pipeline (recommended)
    print("=" * 60)
    print("URASIL_LIGHT v2.0 - Unified Pipeline")
    print("=" * 60)
    print("\nInitialisiere System...")
    
    # Initialize pipeline
    pipeline = Pipeline()
    
    # Get initial state
    state = pipeline.get_state()
    print(f"Zyklus: {state['zyklus']}")
    print(f"EMACK Mood: {state['emack']['mood']}")
    print(f"Session aktiv: {state['session_active']}")
    print("\n" + "-" * 60)
    print("Bereit. Gib deinen Text ein (oder 'exit' zum Beenden):")
    print("-" * 60 + "\n")
    
    # Main interaction loop
    try:
        while True:
            try:
                # Get user input
                user_input = input("Du: ").strip()
            except EOFError:
                # Handle end of input (e.g., from pipe)
                print("\nSession wird beendet...")
                pipeline.end_session()
                print("Auf Wiedersehen!")
                break
            
            # Exit condition
            if user_input.lower() in ['exit', 'quit', 'beenden', 'ende']:
                print("\nSession wird beendet...")
                pipeline.end_session()
                print("Auf Wiedersehen!")
                break
            
            # Skip empty input
            if not user_input:
                continue
            
            # Process through pipeline
            result = pipeline.process(user_input)
            
            # Display response
            print(f"\nUrasil: {result['response']}")
            
            # Display metadata if verbose
            if "--verbose" in sys.argv or "-v" in sys.argv:
                print(f"\n  Bedeutung: {result['bedeutung']}")
                print(f"  Rohantwort: {result['rohantwort']}")
                print(f"  Zyklus: {result['metadata']['zyklus']}")
                print(f"  EMACK Mood: {result['metadata']['emack_mood']}")
                print(f"  EMACK Echo: {result['metadata']['emack_echo']}")
                print(f"  Resonanz: {result['metadata']['resonance']}")
                print(f"  Reife: {result['metadata']['maturity_score']:.2f}")
                print(f"  GOLD-konform: {result['metadata']['gold_conform']}")
            
            print()
            
    except KeyboardInterrupt:
        print("\n\nSession wird beendet...")
        pipeline.end_session()
        print("Auf Wiedersehen!")
    except Exception as e:
        print(f"\nFehler: {e}")
        import traceback
        traceback.print_exc()


def legacy_main():
    """
    Legacy main method using individual components.
    
    This is kept for backwards compatibility.
    """
    print("URASIL_LIGHT - Legacy Mode")
    print("-" * 40)
    
    # 1. Identitaet laden
    identity = Identity.load()

    # 2. Session starten
    session = SessionManager(identity)
    session.start()

    # 3. Zyklus laden + fortschreiben
    zyklus = Zyklus(identity.data)
    zyklus.fortschritt()
    zyklus.speichern(identity.data)

    # 4. Seed initialisieren
    seed = Seed(identity, zyklus)

    # 5. Silky Edge initialisieren
    se = SilkyEdge(identity, zyklus)

    # 6. Input holen
    user_input = input("Du: ")

    # 7. Interpretation
    interpretation = Interpretation(identity, zyklus)
    bedeutung = interpretation.verarbeite(user_input)

    # 8. Seed generiert Rohantwort
    rohantwort = seed.generiere(bedeutung)

    # 9. Silky Edge veredelt Antwort
    antwort = se.veredeln(rohantwort, bedeutung)

    # 10. Ruckmeldung / Reflexion
    rueck = Rueckmeldung(identity, zyklus)
    rueck.verarbeite(antwort)

    # 11. Erfahrung speichern (NACH der Antwort, nicht vorher!)
    erfahrung = Erfahrung(identity, zyklus)
    erfahrung.speichern(bedeutung)

    # 12. Identitaet speichern
    Identity.save(identity.data)

    # 13. Session beenden
    session.end()

    print("Urasil:", antwort)


if __name__ == "__main__":
    # Use new pipeline by default
    main()
