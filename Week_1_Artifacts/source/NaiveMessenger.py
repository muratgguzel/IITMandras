import random

message_type = {
    'PLAIN_POST': 0,
    'RESPONSE_POST': 1,
    'MENTION_POST': 2
}

message_attribute = {
    'TAG': 0,
    'ANCHOR': 1
}

texts = [
    'Veni, Vidi, Vici',
    'Eureka! Eureka!',
    'The Eagle Has Landed!',
    'Let Them Have Cake',
    'Swaraj Is My Birthright!'
]

users = [
    (1001, 'Charles'),
    (1002, 'Jane'),
    (1003, 'Mary')
]


class NaiveMessage:
    def __init__(self, msg_type, text, tag, anchor, target_user):
        self.msg_type = msg_type
        self._text = text
        self.target_user = target_user
        self.tag = tag
        self.anchor = anchor

    def is_response(self):
        return self.msg_type == message_type['RESPONSE_POST']

    def is_mention(self):
        return self.msg_type == message_type['MENTION_POST']

    def has_tag(self):
        return self.tag

    def has_anchor(self):
        return self.anchor

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    def get_target_user(self):
        return self.target_user


class ErrorLogger:
    def log(self, message):
        print(f'Exception occurred while posting message: [ {message.text} ]')


class FormattedLogger:
    def log(self, message):
        print(f'ALERT!!! Exception occurred while posting MESSAGE: [** {message.text} **]')


class Console:
    def display(self, message):
        print(f'DISPLAYING ON WEB INTERFACE: [<< {message.text} >>]')


class Database:
    def insert(self, message):
        print(f'INSERTING DOCUMENT INTO DATABASE: [%% {message.text} %%]')


class User:
    def __init__(self, identity, name):
        self.identity = identity
        self.name = name

    def notify(self, alert):
        print(f'User {self.name} with ID {self.identity} received NOTIFICATION: [ {alert} ]')

    def superpose(self, message):
        print(f'User {self.name} with ID {self.identity} SUPERPOSED with message: [ {message.text} ]')


class Engine:
    def __init__(self, console, database): # Dependency Injection...
        self.console = console # HAS-A-Relationship (Composition) and Loose Coupling
        self.database = database # Loose Coupling

    def dispatch(self, message):
        self.console.display(message)
        self.database.insert(message)

    def add(self, message):
        self.dispatch(message)

    def add_as_tag(self, message):
        text = "ADDING AS A TAG:" + message.text
        message.text = text
        self.dispatch(message)

    def add_as_anchor(self, message):
        text = "IN ANCHOR MODE: " + message.text
        message.text = text
        self.dispatch(message)

    def add_as_response(self, message):
        text = "POSTING AS A RESPONSE: " + message.text
        message.text = text
        self.dispatch(message)

    def notify_user(self, user):
        alert = "Creating a Mention!"
        user.notify(alert)

    def superpose_mention(self, user, message):
        user.superpose(message)


class File:
    def backup(self, message):
        print(f'WRITING BACKUP RECORD INTO FILE: [$$ {message} $$]')


class NaiveRegularPost:
    def create_post(self, message):
        pass


# class RegularPost:
#     def create_post(self, message):
#         pass
#     def broadcast_post(self, message):
#         pass


class NaivePost(NaiveRegularPost):
    def __init__(self, engine):
        self.error_logger = ErrorLogger() # Composition (NaivePost HasA Relationship with ErrorLogger)
                                         # NativePost is Tightly Coupled with ErrorLogger
        self.engine = engine # Composition (NaivePost HasA Relationship with Engine) and Loose Coupling
        self.file = File() # Composition and Tight Coupling

    def create_post(self, message):
        try:
            if message.has_tag():
                self.engine.add_as_tag(message)
            elif message.has_anchor():
                self.engine.add_as_anchor(message)
            else:
                self.engine.add(message)
        except Exception:
            self.error_logger.log(message)
            self.file.backup(message)


class NaiveResponsePost(NaivePost):
    def __init__(self, engine):
        super().__init__(engine)

    def create_response_post(self, message):
        try:
            self.engine.add_as_response(message)
        except Exception:
            self.error_logger.log(message)
            self.file.backup(message)


class NaiveMentionPost(NaivePost):
    def __init__(self, engine):
        super().__init__(engine)

    def create_mention_post(self, message):
        try:
            user = message.get_target_user()

            self.engine.notify_user(user)
            self.engine.superpose_mention(user, message)
            self.create_post(message)
        except Exception:
            self.error_logger.log(message)
            self.file.backup(message)


class NaiveMessageStream:
    def get_next_message(self):
        target_user = None
        tag = False
        anchor = False

        # randint (0, len of message_type ) - We could also do something like,
        # random.randint(0, len(message_type)-1)
        msg_type = random.randint(0, message_type['MENTION_POST'])
        text_index = random.randint(0, len(texts)-1)

        if type == message_type['MENTION_POST']:
            index = random.randint(0, len(users)-1)
            target_user = User(users[index][0], users[index][1])
        elif type == message_type['PLAIN_POST']:
            ind = random.randint(0, len(message_attribute)-1)
            if ind == message_attribute['TAG']:
                tag = True
            else:
                anchor = True

        return NaiveMessage(msg_type, texts[text_index], tag, anchor, target_user)


class NaiveMessenger:
    def __init__(self):
        self.engine = Engine(Console(), Database())
        self.file = File()

    def process_message(self, message):
            if message.is_response():
                post = NaiveResponsePost(self.engine)
            elif message.is_mention():
                post = NaiveMentionPost(self.engine)
            else:
                post = NaivePost(self.engine)

            post.create_post(message)