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

