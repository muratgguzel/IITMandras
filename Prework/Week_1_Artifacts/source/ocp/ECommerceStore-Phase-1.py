from enum import Enum

class Products(Enum):
    ELECTRONICS = 1
    CLOTHES = 2
    BOOKS = 3
    TOYS = 4
    ACCESSORIES = 5
    TravelKit = 6


class DiscountCalculator:
    def __init__(self, product_type, cost):
        self.product_type = product_type
        self.cost = cost

    def get_discounted_price(self):
        if self.product_type == Products.ELECTRONICS:
            return self.cost - (self.cost * 0.10) # Rigidity
        elif self.product_type == Products.CLOTHES:
            return self.cost - (self.cost * 0.15)
        elif self.product_type == Products.BOOKS:
            return self.cost - (self.cost * 0.25)
        elif self.product_type == Products.TOYS:
            return self.cost - (self.cost * 0.50)
        elif self.product_type == Products.ACCESSORIES:
            return self.cost - (self.cost * 0.30)
        elif self.product_type == Products.TravelKit:
            return self.cost - (self.cost * 0.50)

if __name__ == '__main__':
    dc_Electronics = DiscountCalculator(Products.ELECTRONICS, 100)
    print(dc_Electronics.get_discounted_price())

    dc_Clothes = DiscountCalculator(Products.CLOTHES, 100)
    print(dc_Clothes.get_discounted_price())

    dc_Clothes = DiscountCalculator(Products.BOOKS, 100)
    print(dc_Clothes.get_discounted_price())

    dc_Toys = DiscountCalculator(Products.TOYS, 100)
    print(dc_Toys.get_discounted_price())

    dc_Acc = DiscountCalculator(Products.ACCESSORIES, 100)
    print(dc_Acc.get_discounted_price())

    dc_TravelKit = DiscountCalculator(Products.TravelKit, 100)
    print(dc_TravelKit.get_discounted_price())