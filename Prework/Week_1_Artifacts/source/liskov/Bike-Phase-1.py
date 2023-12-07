class Bike:
    def __init__(self, type):
        self.type = type


class PetrolBike(Bike):
    def __init__(self, type):
        super().__init__(type)
        self.type = type


def find_red_bikes(bikes):
    red_bikes = 0
    for bike in bikes:
        if bike.properties['Color'] == "Red":
            red_bikes += 1
    print(f'Number of Red bikes = {red_bikes}')

if __name__ == '__main__':
    bike = Bike("Sports")
    bike.properties = {'Color': "Red", 'Gear': "Auto", 'Capacity': 1}
    print(bike.properties)

    #if bike.properties['Color'] == "Red":
        #print(1)

    petrol_bike = PetrolBike("Mountain Bike")
    petrol_bike.properties = {'Color': "Blue", 'Gear': "Manual", 'Capacity': 2, 'Milage': 50}
    print(petrol_bike.properties)

    #bikes = [bike, petrol_bike]

    #find_red_bikes(bikes)
