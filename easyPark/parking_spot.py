#parking_spot.py
from datetime import datetime

class ParkingSpot:
    def __init__(self, id):
        self.id = id
        self.is_occupied = False
        self.vehicle = None
        self.start_time = None
        self.duration = None
        self.user = None

class ParkingLot:
    def __init__(self, num_spots):
        self.spots = [ParkingSpot(f"A{i+1}") for i in range(num_spots)]

    def get_available_spots(self):
        return [spot for spot in self.spots if not spot.is_occupied]

    def occupy_spot(self, spot_id, vehicle, duration, user):
        for spot in self.spots:
            if spot.id == spot_id:
                spot.is_occupied = True
                spot.vehicle = vehicle
                spot.start_time = datetime.now()
                spot.duration = duration
                spot.user = user
                break

    def vacate_spot(self, spot_id):
        for spot in self.spots:
            if spot.id == spot_id:
                spot.is_occupied = False
                spot.vehicle = None
                spot.start_time = None
                spot.duration = None
                spot.user = None
                break
