from abc import abstractmethod, ABC


class CallingDevice(ABC):
    @abstractmethod
    def make_calls(self):
        #1. Fetch Contact Number (SRP)
        #2. Dial Number (SRP)
        #3. Connect to the Provider (SRP)
        pass

class MessagingDevice(ABC):
    @abstractmethod
    def send_sms(self):
        pass

class InternetbrowsingDevice(ABC):
    @abstractmethod
    def browse_internet(self):
        pass

class SmartPhone(CallingDevice, MessagingDevice, InternetbrowsingDevice):
    def make_calls(self):
        # implementation
        pass

    def send_sms(self):
        # implementation
        pass

    def browse_internet(self):
        # implementation
        pass

class LandlinePhone(CallingDevice):
    def make_calls(self):
        # implementation
        pass

class Pager(MessagingDevice):
    def send_sms(self):
        # implementation
        pass