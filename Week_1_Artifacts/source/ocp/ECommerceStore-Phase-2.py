from abc import abstractmethod


class DiscountCalculator:
    # Abstraction
    @abstractmethod
    def get_discounted_price(self):
        pass


class DiscountCalculatorElectronics(DiscountCalculator):
    def __init__(self, cost):
        self.cost = cost

    # Abstraction
    def get_discounted_price(self):
        return self.cost - (self.cost * 0.30) #Rigidity


class DiscountCalculatorClothes(DiscountCalculator):
    def __init__(self, cost):
        self.cost = cost

    def get_discounted_price(self):
        return self.cost - (self.cost * 0.15)

class DiscountCalculatorBooks(DiscountCalculator):
    def __init__(self, cost):
        self.cost = cost

    def get_discounted_price(self):
        return self.cost - (self.cost * 0.25)


class DiscountCalculatorToys(DiscountCalculator):
    def __init__(self, cost):
        self.cost = cost

    def get_discounted_price(self):
        return self.cost - (self.cost * 0.50)


class DiscountCalculatorAcc(DiscountCalculator):
    def __init__(self, cost):
        self.cost = cost

    def get_discounted_price(self):
        return self.cost - (self.cost * 0.30)

class DiscountCalculatorTravelKit(DiscountCalculator):
    def __init__(self, cost):
        self.cost = cost

    def get_discounted_price(self):
        return self.cost - (self.cost * 0.50)


if __name__ == '__main__':
    # Assume the price is 100/- (Avoid Opacity -:) )
    dc_Electronic = DiscountCalculatorElectronics(100)
    print(dc_Electronic.get_discounted_price())

    dc_Clothes = DiscountCalculatorClothes(100)
    print(dc_Clothes.get_discounted_price())

    dc_Books = DiscountCalculatorBooks(100)
    print(dc_Books.get_discounted_price())

    dc_Books = DiscountCalculatorToys(100)
    print(dc_Books.get_discounted_price())

    dc_Acc = DiscountCalculatorAcc(100)
    print(dc_Acc.get_discounted_price())

    dc_Tkit = DiscountCalculatorTravelKit(100)
    print(dc_Tkit.get_discounted_price())
