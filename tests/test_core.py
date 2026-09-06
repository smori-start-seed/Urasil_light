"""
Test Core Modules
Tests for individual core modules.
"""

import sys
import os

# Setup path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

import unittest
from core.zyklus import Zyklus
from core.interpretation import Interpretation
from core.seed import Seed
from core.silky_edge import SilkyEdge
from core.mandate import Mandate
from core.ininity import Ininity
from core.identity import Identity


class TestZyklus(unittest.TestCase):
    """Test Zyklus module."""
    
    def test_zyklus_initialization(self):
        """Test Zyklus initialization."""
        identity_data = {"zyklus": {"sonne": 5, "mond": 3, "tag": 15}}
        zyklus = Zyklus(identity_data)
        
        self.assertEqual(zyklus.sonne, 5)
        self.assertEqual(zyklus.mond, 3)
        self.assertEqual(zyklus.tag, 15)
    
    def test_zyklus_defaults(self):
        """Test Zyklus with default values."""
        zyklus = Zyklus({})
        
        self.assertEqual(zyklus.sonne, 0)
        self.assertEqual(zyklus.mond, 0)
        self.assertEqual(zyklus.tag, 0)
    
    def test_zyklus_fortschritt(self):
        """Test Zyklus progression."""
        identity_data = {"zyklus": {"sonne": 0, "mond": 0, "tag": 0}}
        zyklus = Zyklus(identity_data)
        
        # Initial values
        self.assertEqual(zyklus.sonne, 0)
        self.assertEqual(zyklus.mond, 0)
        self.assertEqual(zyklus.tag, 0)
        
        # Progress
        zyklus.fortschritt()
        
        # Values should have incremented
        self.assertEqual(zyklus.sonne, 1)
        self.assertEqual(zyklus.mond, 1)
        self.assertEqual(zyklus.tag, 1)
    
    def test_zyklus_wrap_around(self):
        """Test Zyklus wrap-around."""
        identity_data = {"zyklus": {"sonne": 11, "mond": 11, "tag": 29}}
        zyklus = Zyklus(identity_data)
        
        # Progress
        zyklus.fortschritt()
        
        # Should wrap around
        self.assertEqual(zyklus.sonne, 0)
        self.assertEqual(zyklus.mond, 0)
        self.assertEqual(zyklus.tag, 0)
    
    def test_zyklus_matrix(self):
        """Test Zyklus matrix generation."""
        identity_data = {"zyklus": {"sonne": 0, "mond": 0, "tag": 0}}
        zyklus = Zyklus(identity_data)
        
        matrix = zyklus.matrix()
        
        self.assertIn('grundmodus', matrix)
        self.assertIn('stimmung', matrix)
        self.assertIn('fokus', matrix)
    
    def test_zyklus_matrix_values(self):
        """Test specific matrix values."""
        # Test all sonne ranges
        for sonne in range(12):
            identity_data = {"zyklus": {"sonne": sonne, "mond": 0, "tag": 0}}
            zyklus = Zyklus(identity_data)
            matrix = zyklus.matrix()
            
            # Sonne 0-2: klarheit
            if sonne < 3:
                self.assertEqual(matrix['grundmodus'], 'klarheit')
            # Sonne 3-5: kreativ
            elif sonne < 6:
                self.assertEqual(matrix['grundmodus'], 'kreativ')
            # Sonne 6-8: resonanz
            elif sonne < 9:
                self.assertEqual(matrix['grundmodus'], 'resonanz')
            # Sonne 9-11: tiefe
            else:
                self.assertEqual(matrix['grundmodus'], 'tiefe')
    
    def test_zyklus_speichern(self):
        """Test Zyklus speichern."""
        identity_data = {}
        zyklus = Zyklus(identity_data)
        
        zyklus.sonne = 5
        zyklus.mond = 3
        zyklus.tag = 15
        
        zyklus.speichern(identity_data)
        
        self.assertIn('zyklus', identity_data)
        self.assertEqual(identity_data['zyklus']['sonne'], 5)
        self.assertEqual(identity_data['zyklus']['mond'], 3)
        self.assertEqual(identity_data['zyklus']['tag'], 15)
    
    def test_zyklus_als_dict(self):
        """Test Zyklus als_dict."""
        identity_data = {"zyklus": {"sonne": 5, "mond": 3, "tag": 15}}
        zyklus = Zyklus(identity_data)
        
        result = zyklus.als_dict()
        
        self.assertIn('sonne', result)
        self.assertIn('mond', result)
        self.assertIn('tag', result)
        self.assertEqual(result['sonne'], 5)


class TestInterpretation(unittest.TestCase):
    """Test Interpretation module."""
    
    def test_interpretation_initialization(self):
        """Test Interpretation initialization."""
        identity = Identity(self._create_test_identity())
        zyklus = Zyklus(identity.data)
        interpretation = Interpretation(identity, zyklus)
        
        self.assertIsNotNone(interpretation.identity)
        self.assertIsNotNone(interpretation.zyklus)
    
    def test_interpretation_klarheit(self):
        """Test interpretation in klarheit mode."""
        identity_data = {"zyklus": {"sonne": 0, "mond": 0, "tag": 0}}
        identity = Identity(identity_data)
        zyklus = Zyklus(identity_data)
        interpretation = Interpretation(identity, zyklus)
        
        result = interpretation.verarbeite("Test input")
        
        # In klarheit mode, should return stripped text
        self.assertEqual(result, "Test input")
    
    def test_interpretation_kreativ(self):
        """Test interpretation in kreativ mode."""
        identity_data = {"zyklus": {"sonne": 3, "mond": 0, "tag": 0}}
        identity = Identity(identity_data)
        zyklus = Zyklus(identity_data)
        interpretation = Interpretation(identity, zyklus)
        
        result = interpretation.verarbeite("Test input")
        
        # In kreativ mode, should add prefix
        self.assertIn("Kreativer Impuls:", result)
    
    def test_interpretation_resonanz(self):
        """Test interpretation in resonanz mode."""
        identity_data = {"zyklus": {"sonne": 6, "mond": 0, "tag": 0}}
        identity = Identity(identity_data)
        zyklus = Zyklus(identity_data)
        interpretation = Interpretation(identity, zyklus)
        
        result = interpretation.verarbeite("Test input")
        
        # In resonanz mode, should add emotional prefix (with umlaut)
        self.assertTrue("Gefuhl dahinter:" in result or "Gef\u00fchl dahinter:" in result)
    
    def test_interpretation_tiefe(self):
        """Test interpretation in tiefe mode."""
        identity_data = {"zyklus": {"sonne": 9, "mond": 0, "tag": 0}}
        identity = Identity(identity_data)
        zyklus = Zyklus(identity_data)
        interpretation = Interpretation(identity, zyklus)
        
        result = interpretation.verarbeite("Test input")
        
        # In tiefe mode, should add philosophical prefix
        self.assertIn("Tiefer Gedanke:", result)
    
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


class TestSeed(unittest.TestCase):
    """Test Seed module."""
    
    def test_seed_initialization(self):
        """Test Seed initialization."""
        identity = Identity(self._create_test_identity())
        zyklus = Zyklus(identity.data)
        seed = Seed(identity, zyklus)
        
        self.assertIsNotNone(seed.identity)
        self.assertIsNotNone(seed.zyklus)
        self.assertIsNotNone(seed.mandate)
    
    def test_seed_fokus(self):
        """Test seed in fokus mode."""
        identity_data = {"zyklus": {"sonne": 0, "mond": 0, "tag": 0}}
        identity = Identity(identity_data)
        zyklus = Zyklus(identity_data)
        seed = Seed(identity, zyklus)
        
        result = seed.generiere("Test bedeutung")
        
        # In fokus mode, should add "Direkt:" prefix
        self.assertIn("Direkt:", result)
    
    def test_seed_variation(self):
        """Test seed in variation mode."""
        identity_data = {"zyklus": {"sonne": 0, "mond": 0, "tag": 10}}
        identity = Identity(identity_data)
        zyklus = Zyklus(identity_data)
        seed = Seed(identity, zyklus)
        
        result = seed.generiere("Test bedeutung")
        
        # In variation mode, should add "Alternative Sicht:" prefix
        self.assertIn("Alternative Sicht:", result)
    
    def test_seed_synthese(self):
        """Test seed in synthese mode."""
        identity_data = {"zyklus": {"sonne": 0, "mond": 0, "tag": 20}}
        identity = Identity(identity_data)
        zyklus = Zyklus(identity_data)
        seed = Seed(identity, zyklus)
        
        result = seed.generiere("Test bedeutung")
        
        # In synthese mode, should add "Zusammenhang:" prefix
        self.assertIn("Zusammenhang:", result)
    
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


class TestSilkyEdge(unittest.TestCase):
    """Test Silky Edge module."""
    
    def test_silky_edge_initialization(self):
        """Test Silky Edge initialization."""
        identity = Identity(self._create_test_identity())
        zyklus = Zyklus(identity.data)
        silky_edge = SilkyEdge(identity, zyklus)
        
        self.assertIsNotNone(silky_edge.identity)
        self.assertIsNotNone(silky_edge.zyklus)
    
    def test_silky_edge_neutral(self):
        """Test Silky Edge in neutral mode."""
        identity_data = {"zyklus": {"sonne": 0, "mond": 0, "tag": 0}}
        identity = Identity(identity_data)
        zyklus = Zyklus(identity_data)
        silky_edge = SilkyEdge(identity, zyklus)
        
        result = silky_edge.veredeln("Test rohantwort", "Test bedeutung")
        
        # In neutral mode, should return unchanged
        self.assertEqual(result, "Test rohantwort")
    
    def test_silky_edge_warm(self):
        """Test Silky Edge in warm mode."""
        identity_data = {"zyklus": {"sonne": 0, "mond": 4, "tag": 0}}
        identity = Identity(identity_data)
        zyklus = Zyklus(identity_data)
        silky_edge = SilkyEdge(identity, zyklus)
        
        result = silky_edge.veredeln("Test rohantwort", "Test bedeutung")
        
        # In warm mode, should add warm suffix (with umlaut)
        self.assertTrue("ich spure da etwas Warmes" in result or "ich sp\u00fcre da etwas Warmes" in result)
    
    def test_silky_edge_intuitiv(self):
        """Test Silky Edge in intuitiv mode."""
        identity_data = {"zyklus": {"sonne": 0, "mond": 8, "tag": 0}}
        identity = Identity(identity_data)
        zyklus = Zyklus(identity_data)
        silky_edge = SilkyEdge(identity, zyklus)
        
        result = silky_edge.veredeln("Test rohantwort", "Test bedeutung")
        
        # In intuitiv mode, should add intuitive suffix
        self.assertIn("intuitiv betrachtet", result)
    
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


class TestMandate(unittest.TestCase):
    """Test Mandate module."""
    
    def test_mandate_initialization(self):
        """Test Mandate initialization."""
        identity = Identity(self._create_test_identity())
        mandate = Mandate(identity)
        
        self.assertIsNotNone(mandate.identity)
        self.assertIsNotNone(mandate.gold)
    
    def test_mandate_ideal(self):
        """Test Mandate ideal method."""
        identity = Identity(self._create_test_identity())
        mandate = Mandate(identity)
        
        ideals = mandate.ideal()
        
        # Should return a list
        self.assertIsInstance(ideals, list)
    
    def test_mandate_passt(self):
        """Test Mandate passt method."""
        identity = Identity(self._create_test_identity())
        mandate = Mandate(identity)
        
        # Test with text containing a value
        # This depends on what's in gold.txt
        # We'll just test that it doesn't crash
        result = mandate.passt("Test text")
        self.assertIsInstance(result, bool)
    
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


class TestIninity(unittest.TestCase):
    """Test Ininity module."""
    
    def test_ininity_initialization(self):
        """Test Ininity initialization."""
        ininity = Ininity()
        
        self.assertIsNotNone(ininity.kriterien)
    
    def test_ininity_ist_reif(self):
        """Test Ininity ist_reif method."""
        ininity = Ininity()
        
        # Test with some text
        result = ininity.ist_reif("Test text")
        self.assertIsInstance(result, bool)
    
    def test_ininity_reife_score(self):
        """Test Ininity reife_score method."""
        ininity = Ininity()
        
        # Test with some text
        score = ininity.reife_score("Test text")
        
        # Score should be between 0 and 1
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 1)


if __name__ == '__main__':
    unittest.main()
