from datetime import datetime
from unittest import TestCase
from unittest.mock import patch
from unittest.mock import Mock
from mock import GPIO
from mock.SDL_DS3231 import SDL_DS3231
from src.parking_garage import ParkingGarage
from src.parking_garage import ParkingGarageError

class TestParkingGarage(TestCase):

    @patch.object(GPIO, "input")
    def test_check_occupancy(self, mock_distance_radar: Mock):
        mock_distance_radar.return_value = True
        system = ParkingGarage()
        occupied = system.check_occupancy(system.INFRARED_PIN1)
        self.assertTrue(occupied)

    def test_check_occupancy_raises_error(self):
        system = ParkingGarage()
        self.assertRaises(ParkingGarageError, system.check_occupancy, -1)

    @patch.object(GPIO, "input")
    def test_get_number_occupied_spots(self,mock_distance_sensor: Mock):
        mock_distance_sensor.side_effect = [True, False, True]
        system = ParkingGarage()
        number = system.get_number_occupied_spots()
        self.assertEqual(2, number)

    @patch.object(SDL_DS3231, "read_datetime")
    def test_calculate_regular_parking_fee_same_minutes(self, mock_exit_time: Mock):
        mock_exit_time.return_value = datetime(2024, 11, 6, 16, 0)
        system = ParkingGarage()
        fee = system.calculate_parking_fee(datetime(2024, 11, 6, 14, 0))
        self.assertEqual(5,fee)

    @patch.object(SDL_DS3231, "read_datetime")
    def test_calculate_regular_parking_fee_different_minutes(self, mock_exit_time: Mock):
        mock_exit_time.return_value = datetime(2024, 11, 3, 16, 1)
        system = ParkingGarage()
        fee = system.calculate_parking_fee(datetime(2024, 11, 3, 14, 0))
        self.assertEqual(9.375,fee)

    @patch.object(ParkingGarage, "change_servo_angle")
    def test_open_garage_door(self, mock_servo: Mock):
        system = ParkingGarage()
        system.open_garage_door()
        mock_servo.assert_called_with(12)

    @patch.object(GPIO, "output")
    def test_turn_on_red_light(self, mock_light: Mock):
        system = ParkingGarage()
        system.turn_on_red_light()
        mock_light.assert_called_with(system.LED_PIN, True)
        self.assertTrue(system.red_light_on)

    @patch.object(GPIO, "output")
    def test_turn_off_red_light(self, mock_light: Mock):
        system = ParkingGarage()
        system.turn_off_red_light()
        mock_light.assert_called_with(system.LED_PIN, False)
        self.assertFalse(system.red_light_on)

    @patch.object(GPIO, "output")
    @patch.object(ParkingGarage, "get_number_occupied_spots")
    def test_manage_red_light(self, mock_spots: Mock, mock_light: Mock):
        mock_spots.return_value = 3
        system = ParkingGarage()
        system.manage_red_light()
        mock_light.assert_called_with(system.LED_PIN, True)
        self.assertTrue(system.red_light_on)






