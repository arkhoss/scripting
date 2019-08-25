#!/usr/bin/python3
#Usage: 9.oop-inheritance.py
#Author: David Caballero <d@dcaballero.net>
#Version: 1.0

#OOP
class Vehicle:
    def __init__(self, VIN, weight, manufacturer):
        self.vin_number = VIN
        self.weight = weight
        self.manufacturer = manufacturer
    def GetWeight(self):
        return self.weight
    def GetManufacturer(self):
        return self.manufacturer
    def VehicleType(self):
        pass

class Car(Vehicle):
    def __init__(self, VIN, weight, manufacturer, seats):
        self.vin_number = VIN
        self.weight = weight
        self.seats = seats
        self.manufacturer = manufacturer
    def NumberOfSeats(self):
        return self.seats
    def VehicleType(self):
        return 'CAR'

class Truck(Vehicle):
    def __init__(self, VIN, weight, manufacturer, capacity):
        self.vin_number = VIN
        self.weight = weight
        self.capacity = capacity
        self.manufacturer = manufacturer
    def TransportCapacity(self):
        return self.capacity
    def VehicleType(self):
        return 'TRUCK'


a = Car('ABC1',1000,'BMW',4)
b = Truck('BCD2',1000,'MAN',10000)
c = Car('DEF3',1200,'FORD',4)
d = Truck('EFG4',11000,'MERCEDES',15000)


print(a.GetWeight(), b.GetManufacturer(), c.NumberOfSeats(), d.TransportCapacity())

for v in [a,b,c,d]:
    print(v.GetManufacturer(),v.VehicleType())
