# Code Walk through.
from termcolor import colored
from Inheritance import OpticStopWatch, QuartzStopWatch
from NaiveInheritance import NaiveOpticStopWatch, NaiveQuartzStopWatch
from NaiveMessenger import NaiveMessenger, NaiveMessageStream
from Messenger import Messenger, MessageStream

def NaiveWatchImplementation():
    optic_watch = NaiveOpticStopWatch()
    optic_time = optic_watch.find_interval(0, 10)
    print(optic_time)

    quartz_watch = NaiveQuartzStopWatch()
    quartz_time = quartz_watch.find_interval(10, 20)
    print(quartz_time)

def StandardWatchImplementation():
    optic_watch = OpticStopWatch()
    optic_time = optic_watch.find_interval(0, 10)
    print(optic_time)

    quartz_watch = QuartzStopWatch()
    quartz_time = quartz_watch.find_interval(10, 20)
    print(quartz_time)

def NaiveMessengerImplementation():
    message_stream = NaiveMessageStream()
    messenger = NaiveMessenger()

    for count in range(1, 8):
        message = message_stream.get_next_message()
        messenger.process_message(message)

def StandardMessengerImplementation():
    message_stream = MessageStream()
    messenger = Messenger()

    for count in range(1, 8):
        message = message_stream.get_next_message()
        messenger.process_message(message)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #NaiveWatchImplementation()
    #StandardWatchImplementation()

    NaiveMessengerImplementation()
    #StandardMessengerImplementation()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
