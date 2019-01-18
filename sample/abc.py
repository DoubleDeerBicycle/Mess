import abc
class Animal(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get(self, key, value):
        pass

    @abc.abstractmethod
    def set(self, key, value):
        pass

class Dog(Animal):
    def get(self, key, value):
        pass
    
    def set(self, key, value):
        pass

dog1 = Dog()
dog1.get('key', 'value')