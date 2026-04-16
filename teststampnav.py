import unittest
from unittest.mock import patch
from io import StringIO
import sys

import stampnav 

class TestUMDStampNavigator(unittest.TestCase):

    def run_test_with_input(self, user_input):
            """Helper method to simulate input and capture output."""
            with patch('builtins.input', return_value=user_input):
                with patch('sys.stdout', new=StringIO()) as fake_out:
                    stampnav.main() 
                    return fake_out.getvalue()

    def test_food_court_directions(self):
        output = self.run_test_with_input('1')
        self.assertIn("Destination: FOOD COURT", output)
        self.assertIn("Go DOWN one level", output)

    def test_bookstore_directions(self):
        output = self.run_test_with_input('2')
        self.assertIn("UNIVERSITY BOOK CENTER", output)
        self.assertIn("IMMEDIATELY to your right", output)

    def test_terpzone_directions(self):
        output = self.run_test_with_input('3')
        self.assertIn("TERPZONE", output)
        self.assertIn("Basement Level (B)", output)

    def test_invalid_input(self):
        output = self.run_test_with_input('99')
        self.assertIn("Error: Destination not recognized", output)

if __name__ == '__main__':
    unittest.main()