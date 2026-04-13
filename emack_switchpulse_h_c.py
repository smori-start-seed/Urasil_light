import time
import random
import os
import sys
import termios
import tty

# Startwerte
af = 0.5
pf = 0.5
rf = 0.5
score = 0.0

tick = 0
mutation_strength = 0.02
last_score = 0.0

mode = "harmonic"   # Startmodus

ACTIONS = ["harmonize", "explore", "stabilize"]

def bar(value, length=20):
    filled = int(value * length)
    return "█" * filled + "░" * (length - filled)

def trend_symbol(delta):
    if delta > 0.005:
        return "↑"
    elif delta < -0.005:
        return "↓"
    else:
        return "→"

def speak(action, score_delta, mode):
    if mode == "harmonic":
        if action == "harmonize":
            return "Ruhige Balance vertieft sich."
        if action == "explore":
            return "Sanfte Exploration."
        if action == "stabilize":
            return "Stabilität hält das System weich."
    else:
        if action == "harmonize":
            return "Chaos versucht sich zu ordnen."
        if action == "explore":
            return "Exploration entfesselt neue Muster."
        if action == "stabilize":
            return "Kurzzeitige Beruhigung im Sturm."
    return ""

def key_pressed():
    """Nicht-blockierendes Tastaturlesen."""
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        if select := sys.stdin.read(1):
            return select
    except:
        return None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

try:
    while True:
        tick += 1

        # Tastatur prüfen
        key = key_pressed()
        if key == "h":
            mode = "harmonic"
        elif key == "c":
            mode = "chaotic"

        # Action wählen
        action = random.choice(ACTIONS)

        # Basis-Delta
        base_delta = (random.random() - 0.5) * mutation_strength

        # Modus beeinflusst Verhalten
        if mode == "harmonic":
            mode_factor = 0.5
            evo_factor = 0.9
        else:
            mode_factor = 2.0
            evo_factor = 1.1

        # Action-spezifische Modulation
        if action == "harmonize":
            mean_f = (af + pf + rf) / 3.0
            af += (mean_f - af) * 0.1 * mode_factor
            pf += (mean_f - pf) * 0.1 * mode_factor
            rf += (mean_f - rf) * 0.1 * mode_factor
            score_delta = base_delta + 0.01 * (random.random() - 0.4)
        elif action == "explore":
            af += (random.random() - 0.5) * mutation_strength * mode_factor
            pf += (random.random() - 0.5) * mutation_strength * mode_factor
            rf += (random.random() - 0.5) * mutation_strength * mode_factor
            score_delta = base_delta + (random.random() - 0.5) * 0.02 * mode_factor
        elif action == "stabilize":
            af += (0.5 - af) * 0.05 * mode_factor
            pf += (0.5 - pf) * 0.05 * mode_factor
            rf += (0.5 - rf) * 0.05 * mode_factor
            score_delta = base_delta * 0.5

        # Score aktualisieren
        score += score_delta

        # Frequenzen clampen
        af = max(0.0, min(1.0, af))
        pf = max(0.0, min(1.0, pf))
        rf = max(0.0, min(1.0, rf))

        # Mikro-Evolution
        if tick % 50 == 0:
            if score < last_score:
                mutation_strength *= evo_factor
            else:
                mutation_strength *= (2 - evo_factor)
            mutation_strength = max(0.001, min(0.1, mutation_strength))
            last_score = score

        os.system("clear")

        # Trend-Symbole
        af_trend = trend_symbol(af - 0.5)
        pf_trend = trend_symbol(pf - 0.5)
        rf_trend = trend_symbol(rf - 0.5)

        # Ausgabe
        print(f"EMACK PULSE  |  TICK {tick:06d}  |  MODE: {mode.upper()}")
        print("-" * 60)
        print(f"AF: {bar(af)} {af:5.3f} {af_trend}")
        print(f"PF: {bar(pf)} {pf:5.3f} {pf_trend}")
        print(f"RF: {bar(rf)} {rf:5.3f} {rf_trend}")
        print("-" * 60)
        print(f"ACTION      : {action}")
        print(f"SCORE       : {score: .4f}  (Δ {score_delta:+.4f})")
        print(f"MUTATION    : {mutation_strength: .4f}")
        print("-" * 60)
        print("SYSTEM NOTE : " + speak(action, score_delta, mode))
        print("-" * 60)
        print("Tasten: [h] harmonisch   |   [c] chaotisch")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nEMACK PULSE beendet.")
