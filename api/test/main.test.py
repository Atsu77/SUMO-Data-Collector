import unittest
import requests

class TestMain(unittest.TestCase):
    URL = 'http://localhost:8000'

    def test_root_page(self):
        response = requests.get(self.URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hello World"})

    def test_create_net_file(self):
        params = {
            "number_of_lanes": "2",
            "road_length": "1000"
        }
        response = requests.get(self.URL + '/net/create', params=params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Net file created"})

    def test_create_row_file(self):
        params = {
            "maxSpeed": "13.89",
            "vehcle_per_hour": "1800",
            "begin": "0",
            "end": "3600",
        }
        response = requests.get(self.URL + '/row/create', params=params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Row file created"})

    def test_create_sumocfg_file(self):
        params = {
            "net_file": "net.net.xml",
            "rou_file": "rou.rou.xml",
            "begin": "0",
            "end": "3600",
            "step_length": "0.1",
        }
        response = requests.get(self.URL + '/sumocfg/create', params=params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Sumocfg file created"})


    def test_simuration_start(self):
        response = requests.get(self.URL + '/simulation/start')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Simulation start"})

if __name__ == '__main__':
    unittest.main()
