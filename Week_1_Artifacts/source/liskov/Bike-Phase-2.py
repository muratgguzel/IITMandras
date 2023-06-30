class Bike():
    def __init__(self, type):
        self.type = type
        self.bike_properties = {}

    def set_properties(self, color, gear, capacity):
        self.bike_properties = {"Color": color, "Gear": gear, "Capacity": capacity}

    def get_properties(self):
        return self.bike_properties

class PetrolBike(Bike):
    def __init__(self, type):
        self.type = type
        self.bike_properties = {}
    def set_mileage(self, mileage):
        self.mileage = mileage


def find_red_bikes(bikes):
    red_bikes = 0
    for bike in bikes:
        if bike.properties['Color'] == "Red":
            red_bikes += 1
    print(f'Number of Red bikes = {red_bikes}')

if __name__ == '__main__':
    bike = Bike("Sports")
    #bike.properties = {"Color": "Red", "Gear": "Auto", "Capacity": 1}
    bike.set_properties("Red", "Auto", 1)
    print(bike.bike_properties)

    petrol_bike = PetrolBike("Mountain Bike")
    #petrol_bike.properties = {'Color': "Blue", 'Gear': "Manual", 'Capacity': 2, 'Mileage': 50}
    petrol_bike.set_properties("Blue", "Manual", 2)
    print(petrol_bike.bike_properties)
    petrol_bike.set_mileage(50)
    #bikes = [bike, petrol_bike]

    #find_red_bikes(bikes)
