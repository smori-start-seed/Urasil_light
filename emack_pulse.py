import time
import random
import os
import math

# Startwerte
af = 0.5   # Awareness-Frequency
pf = 0.5   # Processing-Frequency
rf = 0.5   # Recovery-Frequency
score = 0.0

tick = 0
mutation_strength = 0.02
last_score = 0.0

ACTIONS = ["harmonize", "explore", "stabilize"]

def bar(value, length=20):
    """ASCII-Balken für Visualisierung."""
    filled = int(value * length)
    return "█" * filled + "░" * (length - filled)

def trend_symbol(delta):
    if delta > 0.005:
        return "↑"
    elif delta < -0.005:
        return "↓"
    else:
        return "→"

def speak(action, score_delta):
    """Kleine 'Stimme' des Systems."""
    if action == "harmonize":
        if score_delta >= 0:
            return "Harmonie vertieft."
        else:
            return "Harmonie gesucht…"
    elif action == "explore":
        if score_delta >= 0:
            return "Neue Muster lohnen sich."
        else:
            return "Exploration war riskant."
    elif action == "stabilize":
        if score_delta >= 0:
            return "Stabilität trägt."
        else:
            return "Stabilisierung nötig."
    return ""

try:
    while True:
        tick += 1

        # Action wählen
        action = random.choice(ACTIONS)

        # Basis-Delta
        base_delta = (random.random() - 0.5) * mutation_strength

        # Action-spezifische Modulation
        if action == "harmonize":
            # Frequenzen aneinander angleichen
            mean_f = (af + pf + rf) / 3.0
            af += (mean_f - af) * 0.1
            pf += (mean_f - pf) * 0.1
            rf += (mean_f - rf) * 0.1
            score_delta = base_delta + 0.01 * (random.random() - 0.4)
        elif action == "explore":
            # Frequenzen stärker streuen
            af += (random.random() - 0.5) * mutation_strength * 2
            pf += (random.random() - 0.5) * mutation_strength * 2
            rf += (random.random() - 0.5) * mutation_strength * 2
            score_delta = base_delta + (random.random() - 0.5) * 0.02
        elif action == "stabilize":
            # Frequenzen leicht dämpfen Richtung Mitte
            af += (0.5 - af) * 0.05
            pf += (0.5 - pf) * 0.05
            rf += (0.5 - rf) * 0.05
            score_delta = base_delta * 0.5

        # Score aktualisieren
        score += score_delta

        # Frequenzen in [0,1] halten
        af = max(0.0, min(1.0, af))
        pf = max(0.0, min(1.0, pf))
        rf = max(0.0, min(1.0, rf))

        # Mikro-Evolution: Mutation anpassen
        if tick % 50 == 0:
            if score < last_score:
                mutation_strength *= 1.1   # mehr Exploration
            else:
                mutation_strength *= 0.9   # mehr Stabilität
            mutation_strength = max(0.001, min(0.1, mutation_strength))
            last_score = score

        # Terminal „klar“ machen (optional)
        os.system("clear")

        # Trend-Symbole
        af_trend = trend_symbol(af - 0.5)
        pf_trend = trend_symbol(pf - 0.5)
        rf_trend = trend_symbol(rf - 0.5)

        # Ausgabe
        print(f"EMACK PULSE  |  TICK {tick:06d}")
        print("-" * 60)
        print(f"AF: {bar(af)} {af:5.3f} {af_trend}")
        print(f"PF: {bar(pf)} {pf:5.3f} {pf_trend}")
        print(f"RF: {bar(rf)} {rf:5.3f} {rf_trend}")
        print("-" * 60)
        print(f"ACTION      : {action}")
        print(f"SCORE       : {score: .4f}  (Δ {score_delta:+.4f})")
        print(f"MUTATION    : {mutation_strength: .4f}")
        print("-" * 60)
        print("SYSTEM NOTE : " + speak(action, score_delta))

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nEMACK PULSE beendet.")
