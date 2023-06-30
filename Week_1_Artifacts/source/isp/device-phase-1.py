from abc import abstractmethod, ABC


# Another style of implementing Abstract class.
class CommunicationDevice():
    @abstractmethod
    def make_calls(self):
        pass

    @abstractmethod
    def send_sms(self):
        pass

    @abstractmethod
    def browse_internet(self):
        pass

class SmartPhone(CommunicationDevice):
    def make_calls(self):
        # implementation
        pass

    def send_sms(self):
        # implementation
        pass

    def browse_internet(self):
        # implementation
        pass

class LandlinePhone(CommunicationDevice):
    def make_calls(self):
        # implementation
        pass

    def send_sms(self):
        # just pass or raise exception as this feature is not supported
        pass

    def browse_internet(self):
        # just pass or raise exception as this feature is not supported
        pass