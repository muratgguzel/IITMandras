class Singleton:
    __instance = None  # private attribute

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Singleton.__instance is None:
            Singleton()
        return Singleton.__instance

    def __init__(self):
        if Singleton.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Singleton.__instance = self

class SingletonExample:
    @staticmethod
    def doJob1():
        Singleton.getInstance()

    @staticmethod
    def doJob2():
        Singleton.getInstance().job()

class SingletonAnotherExample:
    def doJob1(self, instance):
        # Perform some logic using attributes of an instance

if __name__ == '__main__':
    #newInstance = Singleton()
    #print(newInstance)

    anotherInstance = Singleton.getInstance()
    print(anotherInstance)

    oneMoreInstance = Singleton.getInstance()
    print(oneMoreInstance)

    SingletonExample.doJob1()
    SingletonExample.doJob2()

    object = SingletonAnotherExample()
    object.doJob1(Singleton.getInstance())

