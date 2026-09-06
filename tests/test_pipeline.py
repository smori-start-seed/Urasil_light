"""
Test Pipeline Module
Tests for the unified pipeline functionality.
"""

import sys
import os

# Setup path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

import unittest
import tempfile
import json
from core.pipeline import Pipeline
from core.identity import Identity


class TestPipeline(unittest.TestCase):
    """Test cases for the Pipeline class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary identity file
        self.temp_dir = tempfile.mkdtemp()
        self.original_data_path = os.path.join(
            project_root, "data", "identity.json"
        )
        self.temp_identity_path = os.path.join(self.temp_dir, "identity.json")
        
        # Create baseline identity for testing
        self.test_baseline = {
            "erstellt": "2026-01-01T00:00:00Z",
            "beschreibung": "Test Identity",
            "werte": ["klarheit", "ehrlichkeit", "resonanz"],
            "grundton": "neutral",
            "mandate": [],
            "nodus": {},
            "erfahrung": [],
            "zyklus": {"sonne": 0, "mond": 0, "tag": 0}
        }
        
        # Backup original identity if it exists
        if os.path.exists(self.original_data_path):
            with open(self.original_data_path, 'r') as f:
                self.original_identity = json.load(f)
        else:
            self.original_identity = None
        
        # Create test identity file
        with open(self.temp_identity_path, 'w') as f:
            json.dump(self.test_baseline, f)
        
        # Patch data path
        self.original_data_dir = os.path.join(project_root, "data")
        self.temp_data_dir = self.temp_dir
        
        # Update Identity.DATA_PATH for testing
        import core.identity
        self.original_data_path_attr = core.identity.DATA_PATH
        core.identity.DATA_PATH = self.temp_data_dir
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Restore original identity
        if self.original_identity is not None:
            with open(self.original_data_path, 'w') as f:
                json.dump(self.original_identity, f)
        
        # Restore original DATA_PATH
        import core.identity
        core.identity.DATA_PATH = self.original_data_path_attr
        
        # Clean up temp files
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_pipeline_initialization(self):
        """Test that pipeline initializes correctly."""
        pipeline = Pipeline()
        
        self.assertIsNotNone(pipeline.identity)
        self.assertIsNotNone(pipeline.zyklus)
        self.assertIsNotNone(pipeline.interpretation)
        self.assertIsNotNone(pipeline.seed)
        self.assertIsNotNone(pipeline.silky_edge)
        self.assertIsNotNone(pipeline.erfahrung)
        self.assertIsNotNone(pipeline.rueckmeldung)
        self.assertIsNotNone(pipeline.mandate)
        self.assertIsNotNone(pipeline.ininity)
        self.assertIsNotNone(pipeline.session)
        self.assertIsNotNone(pipeline.emack)
    
    def test_pipeline_process(self):
        """Test basic pipeline processing."""
        pipeline = Pipeline()
        
        # Process a simple input
        result = pipeline.process("Hallo, wie geht es dir?")
        
        # Check that we got a response
        self.assertIn('response', result)
        self.assertIn('bedeutung', result)
        self.assertIn('rohantwort', result)
        self.assertIn('metadata', result)
        
        # Response should not be empty
        self.assertTrue(len(result['response']) > 0)
        
        # Meaning should not be empty
        self.assertTrue(len(result['bedeutung']) > 0)
    
    def test_pipeline_metadata(self):
        """Test that pipeline returns proper metadata."""
        pipeline = Pipeline()
        
        result = pipeline.process("Test input")
        
        metadata = result['metadata']
        
        # Check required metadata fields
        self.assertIn('timestamp', metadata)
        self.assertIn('zyklus', metadata)
        self.assertIn('emack_mood', metadata)
        self.assertIn('emack_echo', metadata)
        self.assertIn('resonance', metadata)
        self.assertIn('maturity_score', metadata)
        self.assertIn('gold_conform', metadata)
        self.assertIn('session_active', metadata)
        
        # Check that zyklus has required fields
        zyklus = metadata['zyklus']
        self.assertIn('grundmodus', zyklus)
        self.assertIn('stimmung', zyklus)
        self.assertIn('fokus', zyklus)
    
    def test_pipeline_history(self):
        """Test that pipeline maintains history."""
        pipeline = Pipeline()
        
        # Process multiple inputs
        pipeline.process("Erste Nachricht")
        pipeline.process("Zweite Nachricht")
        pipeline.process("Dritte Nachricht")
        
        # Get history
        history = pipeline.get_history()
        
        # Should have 3 entries
        self.assertEqual(len(history), 3)
        
        # Test limit parameter
        limited_history = pipeline.get_history(limit=2)
        self.assertEqual(len(limited_history), 2)
    
    def test_pipeline_state(self):
        """Test that pipeline state is accessible."""
        pipeline = Pipeline()
        
        state = pipeline.get_state()
        
        # Check required state fields
        self.assertIn('zyklus', state)
        self.assertIn('emack', state)
        self.assertIn('session_active', state)
        self.assertIn('history_count', state)
        self.assertIn('gold_values', state)
        self.assertIn('maturity_criteria', state)
    
    def test_pipeline_reset(self):
        """Test that pipeline can be reset."""
        pipeline = Pipeline()
        
        # Process some inputs
        pipeline.process("Test 1")
        pipeline.process("Test 2")
        
        # Check history exists
        self.assertGreater(len(pipeline.get_history()), 0)
        
        # Reset
        pipeline.reset()
        
        # History should be empty
        self.assertEqual(len(pipeline.get_history()), 0)


class TestPipelineComponents(unittest.TestCase):
    """Test individual pipeline components."""
    
    def test_zyklus_matrix(self):
        """Test zyklus matrix generation."""
        from core.zyklus import Zyklus
        
        zyklus = Zyklus({"sonne": 0, "mond": 0, "tag": 0})
        matrix = zyklus.matrix()
        
        self.assertIn('grundmodus', matrix)
        self.assertIn('stimmung', matrix)
        self.assertIn('fokus', matrix)
    
    def test_interpretation(self):
        """Test interpretation module."""
        from core.interpretation import Interpretation
        from core.zyklus import Zyklus
        from core.identity import Identity
        
        identity = Identity(self._create_test_identity())
        zyklus = Zyklus(identity.data)
        interpretation = Interpretation(identity, zyklus)
        
        # Test interpretation
        result = interpretation.verarbeite("Test input")
        
        self.assertIsNotNone(result)
        self.assertTrue(len(result) > 0)
    
    def test_seed(self):
        """Test seed module."""
        from core.seed import Seed
        from core.zyklus import Zyklus
        from core.identity import Identity
        
        identity = Identity(self._create_test_identity())
        zyklus = Zyklus(identity.data)
        seed = Seed(identity, zyklus)
        
        # Test seed generation
        result = seed.generiere("Test bedeutung")
        
        self.assertIsNotNone(result)
        self.assertTrue(len(result) > 0)
    
    def test_silky_edge(self):
        """Test silky edge module."""
        from core.silky_edge import SilkyEdge
        from core.zyklus import Zyklus
        from core.identity import Identity
        
        identity = Identity(self._create_test_identity())
        zyklus = Zyklus(identity.data)
        silky_edge = SilkyEdge(identity, zyklus)
        
        # Test refinement
        result = silky_edge.veredeln("Test rohantwort", "Test bedeutung")
        
        self.assertIsNotNone(result)
        self.assertTrue(len(result) > 0)
    
    def _create_test_identity(self):
        """Create a test identity dictionary."""
        return {
            "erstellt": "2026-01-01T00:00:00Z",
            "beschreibung": "Test Identity",
            "werte": ["klarheit", "ehrlichkeit", "resonanz"],
            "grundton": "neutral",
            "mandate": [],
            "nodus": {},
            "erfahrung": [],
            "zyklus": {"sonne": 0, "mond": 0, "tag": 0}
        }


class TestEMACKIntegration(unittest.TestCase):
    """Test EMACK integration."""
    
    def test_emack_initialization(self):
        """Test EMACK coordinator initialization."""
        from core.emack import EMACKCoordinator
        
        emack = EMACKCoordinator()
        
        self.assertIsNotNone(emack.state)
        self.assertIsNotNone(emack.agent_b)
        self.assertEqual(emack.tick, 0)
    
    def test_emack_tick(self):
        """Test EMACK tick forward."""
        from core.emack import EMACKCoordinator
        
        emack = EMACKCoordinator()
        
        # Tick forward
        af, pf, rf, score_delta = emack.tick_forward()
        
        # Check that values are returned
        self.assertIsInstance(af, float)
        self.assertIsInstance(pf, float)
        self.assertIsInstance(rf, float)
        self.assertIsInstance(score_delta, float)
        
        # Check that tick counter increased
        self.assertEqual(emack.tick, 1)
    
    def test_emack_mood_detection(self):
        """Test EMACK mood detection."""
        from core.emack import EMACKCoordinator
        
        emack = EMACKCoordinator()
        
        # Tick a few times
        for _ in range(10):
            emack.tick_forward()
        
        # Get mood
        mood = emack.current_mood()
        
        # Mood should be one of the valid options
        valid_moods = ["balanciert", "neugierig", "harmonisierend", 
                      "chaotisch", "uberreizt", "erschopft"]
        self.assertIn(mood, valid_moods)
    
    def test_emack_resonance(self):
        """Test EMACK resonance calculation."""
        from core.emack import EMACKCoordinator
        
        emack = EMACKCoordinator()
        
        # Tick a few times
        for _ in range(10):
            emack.tick_forward()
        
        # Get resonance
        resonance = emack.get_resonance()
        
        # Resonance should be between 1 and 4
        self.assertGreaterEqual(resonance, 1)
        self.assertLessEqual(resonance, 4)


if __name__ == '__main__':
    unittest.main()
