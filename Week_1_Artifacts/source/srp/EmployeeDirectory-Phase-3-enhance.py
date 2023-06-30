# Single Responsibility Principle ( Separation Of Concerns)
class EmployeeDirectory:
    def __init__(self):
        self.employeeDirectory = {}

    def add_entry(self, name, number):
        self.employeeDirectory[name] = number

    def delete_entry(self, name):
        self.employeeDirectory.pop(name)

    def update_entry(self, name, number):
        self.employeeDirectory[name] = number

    def lookup_number(self, name):
        return self.employeeDirectory[name]

    # This is similar to toString() to format the print statements
    def __str__(self):
        ret_dct = ""
        for key, value in self.employeeDirectory.items():
            ret_dct += f'{key} : {value}\n'
        return ret_dct

class PersistToDB:
    # functionality of the class
    def __init__(self, object_to_persist):
        pass

class PersistToFile:
    # functionality of the class
    def __init__(self, object_to_save):
        pass

if __name__ == '__main__':
    myEmployeeDirectory = EmployeeDirectory()
    myEmployeeDirectory.add_entry("Employee-1", 123456)
    myEmployeeDirectory.add_entry("Employee-2", 678452)
    print(myEmployeeDirectory)
    PersistToFile(myEmployeeDirectory)
    PersistToDB(myEmployeeDirectory)

    myEmployeeDirectory.delete_entry("Employee-1")
    myEmployeeDirectory.add_entry("Employee-1", 123456)
    myEmployeeDirectory.update_entry("Employee-2", 776589)
    print(myEmployeeDirectory.lookup_number("Employee-2"))
    print(myEmployeeDirectory)
    PersistToFile(myEmployeeDirectory)
    PersistToDB(myEmployeeDirectory)

    # 1. Implementation style for SRP
    PersistToFile(myEmployeeDirectory)
    PersistToDB(myEmployeeDirectory)

    # 2. Implementation style for SRP
    myEmployeeDirectory.persistToFile()

    # 3. Implementation style for SRP
    myEmployeeDirectory.save()