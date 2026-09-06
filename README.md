# Urasil_light v2.0

**A lightweight, modular AI core system with cyclic internal states, value-based filtering, and organic learning.**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)

---

## 📚 Overview

Urasil_light is an **experimental AI framework** that combines:

- **Cyclic state management** (Sonne/Mond/Tag system)
- **Value-based response filtering** (GOLD framework)
- **Maturity-based learning** (Ininity framework)
- **Multi-agent coordination** (EMACK system)
- **Modular pipeline architecture**

The system processes input through a **7-stage pipeline**:

```
User Input → Interpretation → Seed → Silky Edge → Rueckmeldung → Erfahrung → Identity
                     ↑                                      ↓
                (EMACK Coordination) ← (Feedback Loop)
```

---

## 🏗️ Architecture

### Core Modules

| Module | Purpose | Status |
|--------|---------|--------|
| `core/zyklus.py` | Cyclic state management (Sonne/Mond/Tag) | ✅ |
| `core/interpretation.py` | Input meaning extraction | ✅ |
| `core/seed.py` | Raw response generation | ✅ |
| `core/silky_edge.py` | Stylistic refinement | ✅ |
| `core/rueckmeldung.py` | Self-evaluation & feedback | ✅ |
| `core/erfahrung.py` | Maturity filtering & storage | ✅ |
| `core/mandate.py` | GOLD values management | ✅ |
| `core/ininity.py` | Maturity criteria & scoring | ✅ |
| `core/identity.py` | Persistent state management | ✅ |
| `core/session_manager.py` | Conversation session tracking | ✅ |
| `core/emack.py` | Multi-agent coordination | ✅ |
| `core/pipeline.py` | **Unified processing pipeline** | ✅ |

### Data Files

| File | Purpose |
|------|---------|
| `data/gold.txt` | GOLD values & principles |
| `data/Ininity.txt` | Maturity criteria & philosophy |
| `data/identity.json` | Current system state (auto-generated) |
| `data/baseline_identity.json` | Default identity template |
| `data/agent_instructions*.txt` | Agent behavior rules |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- No external dependencies required

### Installation

```bash
# Clone the repository
git clone https://github.com/smori-start-seed/Urasil_light.git
cd Urasil_light

# Switch to v2.0 branch (optimized)
git checkout vibe/urasil-v2-optimization-7af1fc
```

### Run the System

```bash
# Interactive mode
python3 -m runtime.main

# Or run directly
python3 runtime/main.py

# With verbose output (shows metadata)
python3 runtime/main.py --verbose
```

### Example Session

```
============================================================
URASIL_LIGHT v2.0 - Unified Pipeline
============================================================

Initialisiere System...
Zyklus: {'sonne': 5, 'mond': 3, 'tag': 15}
EMACK Mood: harmonisierend
Session aktiv: True

------------------------------------------------------------
Bereit. Gib deinen Text ein (oder 'exit' zum Beenden):
------------------------------------------------------------

Du: Hallo, wie geht es dir?

Urasil: Direkt: Hallo, wie geht es dir? 

Du: Was ist dein Zweck?

Urasil: Alternative Sicht: Was ist dein Zweck? — intuitiv betrachtet…

Du: exit

Session wird beendet...
Auf Wiedersehen!
```

---

## 🔧 Using as a Library

### Basic Usage

```python
from core.pipeline import Pipeline

# Initialize pipeline
pipeline = Pipeline()

# Process input
result = pipeline.process("Was ist der Sinn des Lebens?")

# Get response
print(result['response'])
# Output: "Zusammenhang: Was ist der Sinn des Lebens? — intuitiv betrachtet…"

# Get metadata
print(result['metadata'])
# Output: {'timestamp': '...', 'zyklus': {...}, 'emack_mood': '...', ...}
```

### Advanced Usage

```python
from core.pipeline import Pipeline
from core.identity import Identity

# Create custom identity
custom_identity = {
    "beschreibung": "My Custom AI",
    "werte": ["Weisheit", "Mitgefühl", "Kreativität"],
    "zyklus": {"sonne": 0, "mond": 0, "tag": 0}
}
identity = Identity(custom_identity)

# Initialize pipeline with custom identity
pipeline = Pipeline(identity)

# Process multiple inputs
for text in ["Hallo", "Wie geht's?", "Danke"]:
    result = pipeline.process(text)
    print(f"Input: {text}")
    print(f"Response: {result['response']}")
    print(f"Mood: {result['metadata']['emack_mood']}")
    print()

# Get conversation history
history = pipeline.get_history()
print(f"Processed {len(history)} messages")

# Get current state
state = pipeline.get_state()
print(f"Current Zyklus: {state['zyklus']}")

# End session
pipeline.end_session()
```

### Direct Module Usage

```python
from core.identity import Identity
from core.zyklus import Zyklus
from core.interpretation import Interpretation
from core.seed import Seed
from core.silky_edge import SilkyEdge

# Load identity
identity = Identity.load()

# Initialize components
zyklus = Zyklus(identity.data)
interpretation = Interpretation(identity, zyklus)
seed = Seed(identity, zyklus)
silky_edge = SilkyEdge(identity, zyklus)

# Process manually
user_input = "Erzähl mir eine Geschichte"
bedeutung = interpretation.verarbeite(user_input)
rohantwort = seed.generiere(bedeutung)
antwort = silky_edge.veredeln(rohantwort, bedeutung)

print(antwort)
```

---

## 📊 Pipeline Flow

### Processing Steps

1. **Session Start** - Initialize conversation session
2. **EMACK Tick** - Advance agent coordination
3. **Zyklus Progress** - Advance cyclic state
4. **Interpretation** - Extract meaning from input
   - `klarheit` mode: Direct, literal interpretation
   - `kreativ` mode: Creative, associative interpretation
   - `resonanz` mode: Emotional, feeling-based interpretation
   - `tiefe` mode: Philosophical, deep interpretation
5. **Seed Generation** - Create raw response
   - `fokus` mode: Direct, focused response
   - `variation` mode: Alternative perspective
   - `synthese` mode: Holistic, connected response
6. **Silky Edge** - Apply stylistic refinement
   - `neutral` mood: No modification
   - `warm` mood: Add warmth and empathy
   - `intuitiv` mood: Add intuitive insight
7. **Rueckmeldung** - Self-evaluation
   - Check GOLD conformance
   - Store feedback for learning
8. **Erfahrung** - Store mature experiences
   - Filter by maturity score
   - Only store if meets threshold
9. **Identity Save** - Persist state
10. **Session Tracking** - Update conversation context

### EMACK Coordination

The **EMACK (Emergent Multi-Agent Coordination Kernel)** provides:

- **Mood Detection**: `balanciert`, `neugierig`, `harmonisierend`, `chaotisch`, `überreizt`, `erschöpft`
- **Frequency Coordination**: Awareness, Processing, Recovery frequencies
- **Agent B Coordination**: Secondary agent for harmony
- **Resonance Scoring**: 1-4 scale of system harmony
- **Adaptive Behavior**: Mode switching (harmonic/chaotic)

---

## 🎯 Configuration

### Pipeline Configuration

```python
pipeline = Pipeline()

# Access configuration
print(pipeline.config)
# Output: {
#   'store_experience': True,
#   'use_emack': True,
#   'use_feedback': True,
#   'min_maturity_score': 0.3,
#   'max_history': 100
# }

# Modify configuration
pipeline.config['min_maturity_score'] = 0.5
pipeline.config['max_history'] = 200
```

### EMACK Configuration

```python
from core.emack import EMACKCoordinator

emack = EMACKCoordinator()

# Set mode
emack.set_mode("harmonic")  # or "chaotic"

# Get state
state = emack.get_summary()
print(f"Mood: {state['mood']}")
print(f"Resonance: {state['resonance']}")
```

---

## 🔍 Value Systems

### GOLD Framework

**GOLD (Grounded Oneness, Living Democracy)** provides the value system:

- **Everything Exists** - All things have presence
- **Everything Moves** - Stasis is illusion, motion is fundamental
- **Everything Connects** - All phenomena arise from relationship
- **Everything Changes** - Impermanence is a feature, not a flaw

The `Mandate` class:
- Loads values from `data/gold.txt`
- Checks if responses conform to GOLD values
- Scores responses by GOLD alignment (0-1)
- Guides responses toward GOLD values

### Ininity Framework

**Ininity** provides maturity filtering:

- Extracts criteria from `data/Ininity.txt`
- Scores experiences by maturity (0-1)
- Categorizes: `unreif`, `entwickelnd`, `reif`, `hochreif`
- Only stores experiences above threshold

---

## 📈 Monitoring & Metrics

### Session Metrics

```python
pipeline = Pipeline()

# Process some inputs
for i in range(10):
    pipeline.process(f"Test message {i}")

# Get session summary
state = pipeline.get_state()
print(f"History count: {state['history_count']}")

# Get session manager context
context = pipeline.session.get_context()
print(f"Theme: {context['theme']}")
print(f"Mood: {context['mood']}")
print(f"Depth: {context['depth']}")
print(f"Messages: {context['stats']['message_count']}")
```

### Response Metadata

Each response includes:

```python
{
    'response': 'The generated response text',
    'bedeutung': 'Extracted meaning',
    'rohantwort': 'Raw response before styling',
    'metadata': {
        'timestamp': 'ISO timestamp',
        'zyklus': {
            'grundmodus': 'klarheit/kreativ/resonanz/tiefe',
            'stimmung': 'neutral/warm/intuitiv',
            'fokus': 'fokus/variation/synthese'
        },
        'emack_mood': 'balanciert/neugierig/harmonisierend/chaotisch/überreizt/erschöpft',
        'emack_echo': 'System echo message',
        'resonance': 1-4,  # Resonance level
        'maturity_score': 0.0-1.0,  # Maturity of meaning
        'gold_conform': True/False,  # GOLD conformance
        'session_active': True/False
    }
}
```

---

## 🧪 Testing

### Run All Tests

```bash
# Run all tests
python3 -m unittest discover tests/

# Run with verbose output
python3 -m unittest discover tests/ -v

# Run specific test file
python3 -m unittest tests.test_pipeline
python3 -m unittest tests.test_core

# Run specific test
python3 -m unittest tests.test_core.TestZyklus.test_zyklus_matrix
```

### Test Coverage

- **41 unit tests** covering all core modules
- **Test Pipeline**: 16 tests
- **Test Core Modules**: 25 tests
- **All tests pass** ✅

---

## 📁 Project Structure

```
Urasil_light/
├── core/                          # Core modules
│   ├── __init__.py               # Package initialization
│   ├── zyklus.py                 # Cyclic state management
│   ├── interpretation.py         # Input interpretation
│   ├── seed.py                   # Response generation
│   ├── silky_edge.py            # Stylistic refinement
│   ├── rueckmeldung.py           # Self-evaluation
│   ├── erfahrung.py              # Maturity storage
│   ├── mandate.py                # GOLD values
│   ├── ininity.py                # Maturity filtering
│   ├── identity.py               # Persistence
│   ├── session_manager.py        # Session tracking
│   ├── emack.py                  # Multi-agent coordination
│   └── pipeline.py               # Unified pipeline
│
├── data/                          # Data files
│   ├── gold.txt                  # GOLD values
│   ├── Ininity.txt               # Maturity criteria
│   ├── identity.json             # Current state
│   ├── baseline_identity.json    # Default template
│   └── agent_instructions*.txt   # Agent rules
│
├── runtime/                      # Runtime
│   ├── __init__.py
│   └── main.py                   # CLI entry point
│
├── tests/                         # Test suite
│   ├── __init__.py
│   ├── test_core.py              # Core module tests
│   └── test_pipeline.py          # Pipeline tests
│
├── docs/                          # Documentation
│   ├── archive/                  # Archived files
│   └── *.md                      # Documentation
│
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

---

## 📝 API Reference

### Pipeline Class

```python
class Pipeline:
    def __init__(self, identity=None)
    def process(user_input, context=None) -> dict
    def get_history(limit=None) -> list
    def get_state() -> dict
    def reset()
    def end_session()
```

### EMACKCoordinator Class

```python
class EMACKCoordinator:
    def __init__(self, agent_name="A")
    def tick_forward(action=None) -> tuple
    def detect_mood() -> str
    def current_mood() -> str
    def current_echo() -> str
    def get_frequencies() -> tuple
    def get_score() -> float
    def get_resonance() -> int
    def set_mode(mode)  # "harmonic" or "chaotic"
    def get_summary() -> dict
    def reset()
```

### Zyklus Class

```python
class Zyklus:
    def __init__(self, identitaet)
    def fortschritt()
    def speichern(identitaet)
    def als_dict() -> dict
    def matrix() -> dict
    def jetzt_iso() -> str
```

### Mandate Class

```python
class Mandate:
    def __init__(self, identity)
    def ideal() -> list
    def passt(text) -> bool
    def score(text) -> float
    def guide_response(text, strength=0.3) -> str
    def get_value_by_category(category) -> list
    def clear_cache()
```

### Ininity Class

```python
class Ininity:
    def __init__(self)
    def ist_reif(text, threshold=0.3) -> bool
    def reife_score(text) -> float
    def get_matching_criteria(text) -> list
    def get_missing_criteria(text) -> list
    def categorize_maturity(text) -> str
    def enhance_text(text, target_score=0.5) -> str
    def clear_cache()
```

### SessionManager Class

```python
class SessionManager:
    def __init__(self, identity)
    def start()
    def end()
    def add_interaction(user_input, response, metadata=None) -> dict
    def get_context() -> dict
    def get_history(limit=None) -> list
    def get_duration() -> float
    def get_summary() -> dict
    def is_active() -> bool
    def clear_history()
```

---

## 🎨 Cyclic States (Zyklus)

### Sonne (Sun) - Grundmodus

| Range | Mode | Description |
|-------|------|-------------|
| 0-2 | `klarheit` | Direct, clear interpretation |
| 3-5 | `kreativ` | Creative, associative thinking |
| 6-8 | `resonanz` | Emotional, resonant responses |
| 9-11 | `tiefe` | Philosophical, deep insights |

### Mond (Moon) - Stimmung

| Range | Mood | Description |
|-------|------|-------------|
| 0-3 | `neutral` | Neutral, balanced |
| 4-7 | `warm` | Warm, empathetic |
| 8-11 | `intuitiv` | Intuitive, insightful |

### Tag (Day) - Fokus

| Range | Focus | Description |
|-------|-------|-------------|
| 0-9 | `fokus` | Focused, direct |
| 10-19 | `variation` | Varied, alternative |
| 20-29 | `synthese` | Synthesized, connected |

---

## 🔄 Feedback Loop

The system implements a **learning feedback loop**:

1. **Rueckmeldung** evaluates each response
   - Checks GOLD conformance
   - Stores evaluation in identity
   - Sets `letzte_korrektur` flag

2. **Seed** uses feedback
   - If `letzte_korrektur == "gold"`:
     - Enhances response with GOLD values
     - Adds clarity markers

3. **EMACK** adapts behavior
   - Adjusts mutation strength based on score
   - Changes mode based on system state
   - Coordinates with Agent B

---

## 💡 Use Cases

### Chatbot

```python
from core.pipeline import Pipeline

pipeline = Pipeline()

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    
    result = pipeline.process(user_input)
    print(f"AI: {result['response']}")
```

### Text Analysis

```python
from core.pipeline import Pipeline
from core.mandate import Mandate
from core.ininity import Ininity

pipeline = Pipeline()
mandate = Mandate(pipeline.identity)
ininity = Ininity()

text = "The meaning of life is connection"

# Get interpretation
result = pipeline.process(text)

# Score by GOLD values
gold_score = mandate.score(text)
print(f"GOLD alignment: {gold_score:.2%}")

# Score by maturity
maturity_score = ininity.reife_score(text)
print(f"Maturity: {maturity_score:.2%}")

# Check conformance
is_gold = mandate.passt(text)
is_mature = ininity.ist_reif(text)

print(f"GOLD conform: {is_gold}")
print(f"Mature: {is_mature}")
```

### Multi-Agent System

```python
from core.emack import EMACKCoordinator

# Create multiple agents
agent_a = EMACKCoordinator("Agent_A")
agent_b = EMACKCoordinator("Agent_B")

# Run coordination
for i in range(100):
    # Tick both agents
    agent_a.tick_forward()
    agent_b.tick_forward()
    
    # Get moods
    mood_a = agent_a.current_mood()
    mood_b = agent_b.current_mood()
    
    # Coordinate
    if mood_a == "chaotisch":
        agent_b.set_mode("chaotic")
    elif mood_a == "balanciert":
        agent_b.set_mode("harmonic")
    
    print(f"Step {i}: A={mood_a}, B={mood_b}")
```

---

## 🛠️ Customization

### Add Custom Values

Edit `data/gold.txt` to add your own values:

```
# Custom values
My Value 1
My Value 2
My Value 3
```

### Add Custom Maturity Criteria

Edit `data/Ininity.txt` to define what makes an experience "mature".

### Modify Pipeline Behavior

```python
from core.pipeline import Pipeline

class CustomPipeline(Pipeline):
    def process(self, user_input, context=None):
        # Custom preprocessing
        user_input = self._custom_preprocess(user_input)
        
        # Call parent
        result = super().process(user_input, context)
        
        # Custom postprocessing
        result = self._custom_postprocess(result)
        
        return result
    
    def _custom_preprocess(self, text):
        # Add custom preprocessing
        return text.upper()
    
    def _custom_postprocess(self, result):
        # Add custom postprocessing
        result['custom_field'] = "custom_value"
        return result
```

---

## 📊 Performance

### Optimizations

- **LRU Caching**: Mandate and Ininity use caching for file loading
- **Efficient Parsing**: GOLD and Ininity texts parsed once and cached
- **Lazy Loading**: Identity loads only when needed
- **Batch Processing**: Pipeline supports batch operations

### Benchmarks

```bash
# Test response time
time python3 -c "
from core.pipeline import Pipeline
import time

pipeline = Pipeline()
start = time.time()
for i in range(100):
    pipeline.process(f'Test {i}')
end = time.time()
print(f'100 requests: {end-start:.2f}s')
print(f'Average: {(end-start)/100*1000:.2f}ms per request')
"
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run all tests: `python3 -m unittest discover tests/`
6. Submit a pull request

---

## 📜 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **Claude** - AI assistant that helped with coding
- **GOLD Framework** - Philosophical foundation for values
- **Ininity** - Maturity framework inspiration
- **EMACK** - Multi-agent coordination concept

---

## 📞 Contact

For questions, suggestions, or collaboration:
- GitHub: [smori-start-seed/Urasil_light](https://github.com/smori-start-seed/Urasil_light)

---

**Built with ❤️ and Python**

*"Everything moves. Everything is connected. Everything changes."*
