
import unittest
from unittest.mock import patch
from io import StringIO

import stampnav
from stampnav import STAMPNavigator

class TestGetDirections(unittest.TestCase):

    def test_main_entrance_food_court(self):
        nav = STAMPNavigator("1")
        steps = nav.get_directions("1")
        self.assertTrue(any("Ground Floor" in s for s in steps))

    def test_main_entrance_book_center(self):
        nav = STAMPNavigator("1")
        steps = nav.get_directions("2")
        self.assertTrue(any("Ground Floor" in s for s in steps))

    def test_main_entrance_terpzone(self):
        nav = STAMPNavigator("1")
        steps = nav.get_directions("3")
        self.assertTrue(any("Basement" in s for s in steps))

    def test_main_entrance_coffee_bar(self):
        nav = STAMPNavigator("1")
        steps = nav.get_directions("4")
        self.assertTrue(any("First Floor" in s or "1F" in s for s in steps))

    def test_main_entrance_panera(self):
        nav = STAMPNavigator("1")
        steps = nav.get_directions("5")
        self.assertTrue(any("north" in s.lower() for s in steps))

    def test_south_entrance_food_court(self):
        nav = STAMPNavigator("2")
        steps = nav.get_directions("1")
        self.assertTrue(any("Ground Floor" in s for s in steps))

    def test_south_entrance_coffee_bar(self):
        nav = STAMPNavigator("2")
        steps = nav.get_directions("4")
        self.assertTrue(any("immediately" in s.lower() or "Cafe Lounge" in s for s in steps))

    def test_southwest_entrance_food_court(self):
        nav = STAMPNavigator("3")
        steps = nav.get_directions("1")
        self.assertTrue(any("Ground Floor" in s or "east" in s.lower() for s in steps))

    def test_southwest_entrance_terpzone(self):
        nav = STAMPNavigator("3")
        steps = nav.get_directions("3")
        self.assertTrue(any("Basement" in s for s in steps))

    def test_east_entrance_food_court(self):
        nav = STAMPNavigator("4")
        steps = nav.get_directions("1")
        self.assertTrue(any("west" in s.lower() for s in steps))

    def test_east_entrance_terpzone(self):
        nav = STAMPNavigator("4")
        steps = nav.get_directions("3")
        self.assertTrue(any("Basement" in s for s in steps))

    def test_northeast_entrance_terpzone(self):
        nav = STAMPNavigator("5")
        steps = nav.get_directions("3")
        self.assertTrue(any("west" in s.lower() or "TerpZone" in s for s in steps))

    def test_northeast_entrance_book_center(self):
        nav = STAMPNavigator("5")
        steps = nav.get_directions("2")
        self.assertTrue(any("Basement" in s or "Book Center" in s for s in steps))

    def test_unknown_destination_returns_empty(self):
        nav = STAMPNavigator("1")
        self.assertEqual(nav.get_directions("99"), [])

    def test_directions_are_list(self):
        nav = STAMPNavigator("1")
        self.assertIsInstance(nav.get_directions("1"), list)

    def test_all_combos_non_empty(self):
        for entrance in ("1", "2", "3", "4", "5"):
            for dest in ("1", "2", "3", "4", "5"):
                nav = STAMPNavigator(entrance)
                steps = nav.get_directions(dest)
                self.assertGreater(len(steps), 0,
                    msg=f"No steps for entrance={entrance}, dest={dest}")

class TestFormatDirections(unittest.TestCase):

    def test_valid_destination_contains_name(self):
        nav = STAMPNavigator("1")
        self.assertIn("FOOD COURT", nav.format_directions("1"))

    def test_valid_destination_numbered_steps(self):
        nav = STAMPNavigator("1")
        self.assertIn("1.", nav.format_directions("1"))

    def test_invalid_destination_returns_error(self):
        nav = STAMPNavigator("1")
        self.assertIn("Error: Destination not recognized", nav.format_directions("99"))

    def test_visit_count_increments_on_valid(self):
        nav = STAMPNavigator("1")
        nav.format_directions("1")
        nav.format_directions("2")
        self.assertEqual(nav.visit_count, 2)

    def test_visit_count_does_not_increment_on_invalid(self):
        nav = STAMPNavigator("1")
        nav.format_directions("99")
        self.assertEqual(nav.visit_count, 0)

    def test_terpzone_format(self):
        nav = STAMPNavigator("1")
        self.assertIn("TERPZONE", nav.format_directions("3"))

    def test_book_center_format(self):
        nav = STAMPNavigator("1")
        self.assertIn("UNIVERSITY BOOK CENTER", nav.format_directions("2"))

    def test_coffee_bar_format(self):
        nav = STAMPNavigator("1")
        self.assertIn("COFFEE BAR", nav.format_directions("4"))

    def test_panera_format(self):
        nav = STAMPNavigator("1")
        self.assertIn("PANERA", nav.format_directions("5"))

class TestSessionSummary(unittest.TestCase):

    def test_zero_visits(self):
        nav = STAMPNavigator("1")
        self.assertIn("0 destinations", nav.session_summary())

    def test_one_visit_singular(self):
        nav = STAMPNavigator("1")
        nav.format_directions("1")
        summary = nav.session_summary()
        self.assertIn("1 destination", summary)
        self.assertNotIn("destinations", summary)

    def test_multiple_visits_plural(self):
        nav = STAMPNavigator("1")
        nav.format_directions("1")
        nav.format_directions("2")
        self.assertIn("2 destinations", nav.session_summary())

    def test_summary_contains_go_terps(self):
        nav = STAMPNavigator("1")
        self.assertIn("Go Terps", nav.session_summary())

class TestRunNavigationLoop(unittest.TestCase):

    def _run_loop(self, inputs, entrance="1"):
        nav = STAMPNavigator(entrance)
        with patch("builtins.input", side_effect=iter(inputs)):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                stampnav.run_navigation_loop(nav)
                return fake_out.getvalue(), nav

    def test_exit_immediately(self):
        output, nav = self._run_loop(["0"])
        self.assertNotIn("Destination:", output)
        self.assertEqual(nav.visit_count, 0)

    def test_single_valid_destination(self):
        output, nav = self._run_loop(["1", "n"])
        self.assertIn("FOOD COURT", output)
        self.assertEqual(nav.visit_count, 1)

    def test_two_destinations_then_exit(self):
        output, nav = self._run_loop(["1", "y", "3", "n"])
        self.assertIn("FOOD COURT", output)
        self.assertIn("TERPZONE", output)
        self.assertEqual(nav.visit_count, 2)

    def test_invalid_destination_shows_error(self):
        output, _ = self._run_loop(["99", "0"])
        self.assertIn("Error: Destination not recognized", output)

    def test_south_entrance_coffee_bar_immediate(self):
        output, nav = self._run_loop(["4", "n"], entrance="2")
        self.assertTrue(
            "immediately" in output.lower() or "Cafe Lounge" in output
        )
        self.assertEqual(nav.visit_count, 1)

    def test_northeast_entrance_terpzone(self):
        output, nav = self._run_loop(["3", "n"], entrance="5")
        self.assertIn("TERPZONE", output)
        self.assertEqual(nav.visit_count, 1)

    def test_east_entrance_food_court_goes_west(self):
        output, _ = self._run_loop(["1", "n"], entrance="4")
        self.assertIn("west", output.lower())


class TestInputHelpers(unittest.TestCase):

    def test_get_entrance_choice_returns_input(self):
        with patch("builtins.input", return_value="2"):
            self.assertEqual(stampnav.get_entrance_choice(), "2")

    def test_get_destination_choice_returns_input(self):
        with patch("builtins.input", return_value="3"):
            self.assertEqual(stampnav.get_destination_choice(), "3")

    def test_get_entrance_choice_strips_whitespace(self):
        with patch("builtins.input", return_value="  1  "):
            self.assertEqual(stampnav.get_entrance_choice(), "1")

    def test_get_destination_choice_strips_whitespace(self):
        with patch("builtins.input", return_value="  2  "):
            self.assertEqual(stampnav.get_destination_choice(), "2")


if __name__ == "__main__":
    unittest.main()
