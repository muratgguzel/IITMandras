import random

message_type = {
    'PLAIN_POST': 0,
    'TAG_POST': 1,
    'ANCHOR_POST': 2,
    'RESPONSE_POST': 3,
    'MENTION_POST': 4
}

texts = [
    'Veni, Vidi, Vici',
    'Eureka! Eureka!',
    'The Eagle Has Landed!',
    'Let Them Have Cake',
    'Swaraj Is My Birthright!',
    'Proletariat Of The World, Unite!',
    'Fact Is Stranger Than Fiction'
]

users = [
    (1001, 'Charles'),
    (1002, 'Jane'),
    (1003, 'Mary')
]


class Message:
    def __init__(self, msg_type, text, target_user):
        self.msg_type = msg_type
        self._text = text
        self.target_user = target_user

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    def is_response(self):
        return self.msg_type == message_type['RESPONSE_POST']

    def is_mention(self):
        return self.msg_type == message_type['MENTION_POST']

    def is_tag(self):
        return self.msg_type == message_type['TAG_POST']

    def is_anchor(self):
        return self.msg_type == message_type['ANCHOR_POST']

    def get_target_user(self):
        return self.target_user


class Logger:
    def __init__(self, file):
        self.file = file

    def log(self, message):
        pass


class ErrorLogger(Logger):
    def __init__(self, file):
        super().__init__(file)

    def log(self, message):
        print(f'Exception occurred while posting message: [ {message.text} ]')
        self.file.backup(message)


class FormattedLogger(Logger):
    def __init__(self, file):
        super().__init__(file)

    def log(self, message):
        print(f'ALERT!!! Exception occurred while posting MESSAGE: [** {message.text} **]')
        self.file.backup(message)


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

# SRP - Eliminate the User Notification Logic which
# existed in Naive Implementation.
class Engine:
    def __init__(self, console, database):
        self.console = console
        self.database = database

    def dispatch(self, message):
        self.console.display(message)
        self.database.insert(message)

    def add(self, message):
        self.dispatch(message)

    def add_as_tag(self, message):
        self.dispatch(message)

    def add_as_anchor(self, message):
        self.dispatch(message)

    def add_as_response(self, message):
        self.dispatch(message)


class File:
    def backup(self, message):
        print(f'WRITING BACKUP RECORD INTO FILE: [$$ {message.text} $$]')


class RegularPost:
    def create_post(self, message):
        pass


class BroadcastPost:
    def broadcast_post(self, message):
        pass

# OCP - AnchorPost, TagPost Creation
class Post(RegularPost):
    def __init__(self, engine, logger):
        self.logger = logger
        self.engine = engine

    def create_post(self, message):
        try:
            self.engine.add(message)
        except Exception:
            self.logger.log(message)

class TagPost(RegularPost):
    def __init__(self, engine, logger):
        self.logger = logger
        self.engine = engine

    def create_post(self, message):
        try:
            self.engine.add_as_tag(message)
        except Exception:
            self.logger.log(message)


class AnchorPost(RegularPost):
    def __init__(self, engine, logger):
        self.logger = logger
        self.engine = engine

    def create_post(self, message):
        try:
            self.engine.add_as_anchor(message)
        except Exception:
            self.logger.log(message)


class ResponsePost(Post):
    def __init__(self, engine, logger):
        super().__init__(engine, logger)

    def create_post(self, message):
        try:
            self.engine.add_as_response(message)
        except Exception:
            self.logger.log(message)


class UserMentioner:
    def notify_user(self, user):
        alert = "Creating a Mention!"
        user.notify(alert)

    def superpose_mention(self, user, message):
        user.superpose(message)


class MentionPost(Post):
    def __init__(self, engine, logger, user_mentioner):
        super().__init__(engine, logger)
        self.user_mentioner = user_mentioner #Composition and loose coupling.

    def create_post(self, message):
        try:
            user = message.get_target_user()

            self.user_mentioner.notify_user(user)
            self.user_mentioner.superpose_mention(user, message)
            self.create_post(message)
        except Exception:
            self.logger.log(message)


class MessageStream:
    def get_next_message(self):
        target_user = None

        msg_type = random.randint(0, message_type['MENTION_POST'])
        text_index = random.randint(0, len(texts) - 1)

        if type == message_type['MENTION_POST']:
            index = random.randint(0, len(users) - 1)
            target_user = User(users[index][0], users[index][1])

        return Message(msg_type, texts[text_index], target_user)


class Messenger:
    def __init__(self):
        # Dependency Injection.
        self.engine = Engine(Console(), Database())
        self.logger = ErrorLogger(File())
        self.file = File()

    def process_message(self, message):
        # ISP -> Creating Independent Interfaces.
        if message.is_response():
            post = ResponsePost(self.engine, self.logger)
        elif message.is_mention():
            post = MentionPost(self.engine, self.logger, UserMentioner())
        elif message.is_tag():
            post = TagPost(self.engine, self.logger)
        elif message.is_anchor():
            post = AnchorPost(self.engine, self.logger)
        else:
            post = Post(self.engine, self.logger)

        post.create_post(message)
