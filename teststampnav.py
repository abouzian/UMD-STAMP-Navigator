import unittest
from unittest.mock import patch
from io import StringIO
import os
import json

import stampnav
from stampnav import STAMPNavigator


# helper to run the navigation loop with fake inputs and capture output

def _run_loop(inputs, entrance="1"):
    """runs the navigation loop with a fake list of inputs, returns the output and navigator"""
    nav = STAMPNavigator(entrance)
    with patch("builtins.input", side_effect=iter(inputs)):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            stampnav.run_navigation_loop(nav, entrance)
            return fake_out.getvalue(), nav


# TestGetDirections

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
                self.assertGreater(
                    len(steps), 0,
                    msg=f"No steps for entrance={entrance}, dest={dest}"
                )


# TestFormatDirections

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


# TestUpdateEntrance

class TestUpdateEntrance(unittest.TestCase):

    def test_update_changes_entrance(self):
        nav = STAMPNavigator("1")
        nav.update_entrance("3")
        self.assertEqual(nav.entrance, "3")

    def test_update_affects_next_directions(self):
        # after updating to entrance 3, directions should reflect that new position
        nav = STAMPNavigator("1")
        nav.update_entrance("3")
        # now asking for Food Court directions from entrance 3 (SW entrance, Ground Floor)
        steps = nav.get_directions("1")
        self.assertTrue(any("Ground Floor" in s or "east" in s.lower() for s in steps))

    def test_update_does_not_change_visit_count(self):
        nav = STAMPNavigator("1")
        nav.update_entrance("2")
        self.assertEqual(nav.visit_count, 0)

    def test_multiple_updates(self):
        nav = STAMPNavigator("1")
        nav.update_entrance("2")
        nav.update_entrance("5")
        self.assertEqual(nav.entrance, "5")


# TestSessionSummary

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


# tests for run_navigation_loop

class TestRunNavigationLoop(unittest.TestCase):

    def test_exit_immediately(self):
        output, nav = _run_loop(["0"])
        self.assertNotIn("Destination:", output)
        self.assertEqual(nav.visit_count, 0)

    def test_single_valid_destination(self):
        # dest=1, no more, no save
        output, nav = _run_loop(["1", "n", "n"])
        self.assertIn("FOOD COURT", output)
        self.assertEqual(nav.visit_count, 1)

    def test_two_destinations_then_exit(self):
        # dest=1, continue, dest=3, no more, no save
        output, nav = _run_loop(["1", "y", "3", "n", "n"])
        self.assertIn("FOOD COURT", output)
        self.assertIn("TERPZONE", output)
        self.assertEqual(nav.visit_count, 2)

    def test_three_destinations(self):
        # dest=4, continue, dest=1, continue, dest=5, no more, no save
        output, nav = _run_loop(["4", "y", "1", "y", "5", "n", "n"])
        self.assertIn("COFFEE BAR", output)
        self.assertIn("FOOD COURT", output)
        self.assertIn("PANERA", output)
        self.assertEqual(nav.visit_count, 3)

    def test_invalid_destination_shows_error(self):
        output, _ = _run_loop(["99", "0"])
        self.assertIn("Invalid choice", output)

    def test_invalid_then_valid(self):
        # bad input, then valid, then quit
        output, nav = _run_loop(["99", "2", "n", "n"])
        self.assertIn("Invalid choice", output)
        self.assertIn("UNIVERSITY BOOK CENTER", output)
        self.assertEqual(nav.visit_count, 1)

    def test_route_summary_shown_after_session(self):
        # route summary should show up when the user is done navigating
        output, _ = _run_loop(["1", "y", "3", "n", "n"])
        self.assertIn("Route completed", output)

    def test_route_summary_shows_both_stops(self):
        output, _ = _run_loop(["2", "y", "4", "n", "n"])
        self.assertIn("Stop 1", output)
        self.assertIn("Stop 2", output)

    def test_save_favorite_on_yes(self):
        # saying yes to save should write the route to the file
        if os.path.exists(stampnav.FAVORITES_FILE):
            os.remove(stampnav.FAVORITES_FILE)
        _run_loop(["1", "n", "y"])  # dest=1, no more, save=yes
        fav = stampnav.load_favorite()
        self.assertIsNotNone(fav)
        self.assertIn("1", fav["destinations"])
        os.remove(stampnav.FAVORITES_FILE)

    def test_no_save_on_no(self):
        # saying no to save should not create a file
        if os.path.exists(stampnav.FAVORITES_FILE):
            os.remove(stampnav.FAVORITES_FILE)
        _run_loop(["1", "n", "n"])  # dest=1, no more, save=no
        self.assertIsNone(stampnav.load_favorite())

    def test_multi_stop_save_contains_all_destinations(self):
        # saving a multi-stop route should include all destinations in order
        if os.path.exists(stampnav.FAVORITES_FILE):
            os.remove(stampnav.FAVORITES_FILE)
        _run_loop(["4", "y", "2", "n", "y"])  # Coffee Bar > Book Center
        fav = stampnav.load_favorite()
        self.assertIsNotNone(fav)
        self.assertEqual(fav["destinations"], ["4", "2"])
        os.remove(stampnav.FAVORITES_FILE)

    def test_entrance_updates_between_stops(self):
        # after visiting Food Court (dest 1), entrance should update to East Entrance (4)
        nav = STAMPNavigator("3")
        with patch("builtins.input", side_effect=iter(["1", "n", "n"])):
            with patch("sys.stdout", new=StringIO()):
                stampnav.run_navigation_loop(nav, "3")
        self.assertEqual(nav.entrance, "4")

    def test_south_entrance_coffee_bar_immediate(self):
        output, nav = _run_loop(["4", "n", "n"], entrance="2")
        self.assertTrue("immediately" in output.lower() or "Cafe Lounge" in output)
        self.assertEqual(nav.visit_count, 1)

    def test_northeast_entrance_terpzone(self):
        output, nav = _run_loop(["3", "n", "n"], entrance="5")
        self.assertIn("TERPZONE", output)
        self.assertEqual(nav.visit_count, 1)

    def test_east_entrance_food_court_goes_west(self):
        output, _ = _run_loop(["1", "n", "n"], entrance="4")
        self.assertIn("west", output.lower())

    def test_chained_directions_use_last_destination_as_start(self):
        # after going to Food Court, the next directions shouldn't start from Main Entrance
        nav = STAMPNavigator("1")
        with patch("builtins.input", side_effect=iter(["1", "y", "3", "n", "n"])):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                stampnav.run_navigation_loop(nav, "1")
                output = fake_out.getvalue()
        legs = output.split("=" * 40)
        if len(legs) >= 4:
            second_leg = legs[3]
            self.assertNotIn("Main Entrance", second_leg)


# tests for save_favorite, load_favorite, and delete_favorite

class TestFavoritePersistence(unittest.TestCase):

    def setUp(self):
        # make sure there's no leftover file before each test
        if os.path.exists(stampnav.FAVORITES_FILE):
            os.remove(stampnav.FAVORITES_FILE)

    def tearDown(self):
        # clean up the file after each test
        if os.path.exists(stampnav.FAVORITES_FILE):
            os.remove(stampnav.FAVORITES_FILE)

    def test_save_and_load_single_stop(self):
        stampnav.save_favorite("2", ["3"])
        fav = stampnav.load_favorite()
        self.assertEqual(fav["entrance"], "2")
        self.assertEqual(fav["destinations"], ["3"])

    def test_save_and_load_multi_stop(self):
        stampnav.save_favorite("1", ["4", "2", "5"])
        fav = stampnav.load_favorite()
        self.assertEqual(fav["entrance"], "1")
        self.assertEqual(fav["destinations"], ["4", "2", "5"])

    def test_load_returns_none_when_no_file(self):
        self.assertIsNone(stampnav.load_favorite())

    def test_delete_removes_file(self):
        stampnav.save_favorite("1", ["1"])
        stampnav.delete_favorite()
        self.assertFalse(os.path.exists(stampnav.FAVORITES_FILE))

    def test_delete_when_no_file_does_not_raise(self):
        try:
            stampnav.delete_favorite()
        except Exception as e:
            self.fail(f"delete_favorite() raised an exception: {e}")

    def test_load_after_delete_returns_none(self):
        stampnav.save_favorite("3", ["2"])
        stampnav.delete_favorite()
        self.assertIsNone(stampnav.load_favorite())

    def test_overwrite_favorite(self):
        # saving again should replace the old favorite, not add to it
        stampnav.save_favorite("1", ["1"])
        stampnav.save_favorite("3", ["4", "5"])
        fav = stampnav.load_favorite()
        self.assertEqual(fav["entrance"], "3")
        self.assertEqual(fav["destinations"], ["4", "5"])

    def test_saved_file_is_valid_json(self):
        stampnav.save_favorite("2", ["1", "3"])
        with open(stampnav.FAVORITES_FILE) as f:
            data = json.load(f)
        self.assertIn("entrance", data)
        self.assertIn("destinations", data)


# tests for the DESTINATION_TO_ENTRANCE mapping we added

class TestDestinationToEntranceMapping(unittest.TestCase):
    """checks that every destination maps to a valid entrance on the right floor"""

    def test_all_destinations_have_mapping(self):
        for dest in stampnav.DESTINATIONS:
            self.assertIn(
                dest, stampnav.DESTINATION_TO_ENTRANCE,
                msg=f"Destination '{dest}' missing from DESTINATION_TO_ENTRANCE"
            )

    def test_all_mapped_entrances_are_valid(self):
        for dest, entrance in stampnav.DESTINATION_TO_ENTRANCE.items():
            self.assertIn(
                entrance, stampnav.ENTRANCES,
                msg=f"Destination '{dest}' maps to invalid entrance '{entrance}'"
            )

    def test_food_court_maps_to_ground_floor_entrance(self):
        # Food Court is on Ground Floor so it should map to a Ground Floor entrance
        entrance = stampnav.DESTINATION_TO_ENTRANCE["1"]
        self.assertIn("Ground Floor", stampnav.ENTRANCES[entrance])

    def test_terpzone_maps_to_basement_entrance(self):
        # TerpZone is in the Basement so it should map to a Basement entrance
        entrance = stampnav.DESTINATION_TO_ENTRANCE["3"]
        self.assertIn("Basement", stampnav.ENTRANCES[entrance])

    def test_coffee_bar_maps_to_first_floor_entrance(self):
        # Coffee Bar is on First Floor so it should map to a First Floor entrance
        entrance = stampnav.DESTINATION_TO_ENTRANCE["4"]
        self.assertIn("First Floor", stampnav.ENTRANCES[entrance])

    def test_panera_maps_to_first_floor_entrance(self):
        # Panera is on First Floor so it should map to a First Floor entrance
        entrance = stampnav.DESTINATION_TO_ENTRANCE["5"]
        self.assertIn("First Floor", stampnav.ENTRANCES[entrance])

    def test_book_center_maps_to_ground_floor_entrance(self):
        # Book Center is on Ground Floor so it should map to a Ground Floor entrance
        entrance = stampnav.DESTINATION_TO_ENTRANCE["2"]
        self.assertIn("Ground Floor", stampnav.ENTRANCES[entrance])


# TestInputHelpers

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