# The emoticon base class that can be customized

standard_emotion = {
                    'HAPPY': 0,
                    'SAD': 1,
                    'ANGRY': 2}


class Emoticon:
    def __init__(self, emotion):
        self._emotion = emotion

    def __str__(self):
        pass

    @property
    def emotion(self):
        return self._emotion

    @emotion.setter
    def emotion(self, emotion):
        self._emotion = emotion


class Happy(Emoticon):
    def __init__(self):
        super().__init__(':-)')

    def __str__(self):
        print(f'{self.emotion}')


class Angry(Emoticon):
    def __init__(self):
        super().__init__(';-#')

    def __str__(self):
        print(f'{self.emotion}')


class Sad(Emoticon):
    def __init__(self):
        super().__init__(':-(')

    def __str__(self):
        print(f'{self.emotion}')


class CaptionText:
    def __init__(self, text):
        self._text = text

    def __str__(self):
        print(f'{self.text}')

    @property
    def text(self):
        return self._text


class HappyCaption(CaptionText):
    def __init__(self):
        super().__init__('What a beautiful day!')


class SadCaption(CaptionText):
    def __init__(self):
        super().__init__('The world is so difficult!')


class AngryCaption(CaptionText):
    def __init__(self):
        super().__init__('I will put an end to all misery!')


class Keyboard:
    def __init__(self):
        self._typed_text = ''
        self._emotion = -1

    @property
    def typed_text(self):
        return self._typed_text

    @typed_text.setter
    def typed_text(self, typed_text):
        self._typed_text = typed_text

    @property
    def emotion(self):
        return self._emotion

    @emotion.setter
    def emotion(self, emotion):
        self._emotion = emotion

    def input(self, input_text, emotion):
        self.typed_text = input_text
        self.emotion = emotion


class CaptionBuilder:
    def __init__(self, keyboard):
        self.keyboard = keyboard

    def build_message(self):
        full_message = ''
        full_message += self.keyboard.typed_text
        full_message += '\n'

        if self.keyboard.emotion == standard_emotion['HAPPY']:
            caption_text = HappyCaption()
            emoticon = Happy()
        elif self.keyboard.emotion == standard_emotion['SAD']:
            caption_text = SadCaption()
            emoticon = Sad()
        elif self.keyboard.emotion == standard_emotion['ANGRY']:
            caption_text = AngryCaption()
            emoticon = Angry()
        else:
            print('Unsupported emotion experienced!')
            return

        full_message += caption_text.text
        full_message += '\n'
        full_message += emoticon.emotion

        print(f'{full_message}')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    keyboard = Keyboard()

    caption_builder = CaptionBuilder(keyboard)

    # Message 1

    keyboard.input('Today is a Monday', standard_emotion['HAPPY'])
    caption_builder.build_message()

    keyboard.input('Today is a Monday', standard_emotion['SAD'])
    caption_builder.build_message()

    keyboard.input('Today is a Monday', standard_emotion['ANGRY'])
    caption_builder.build_message()

    keyboard.input('Today is a Monday', -1)
    caption_builder.build_message()

    keyboard.input('Today is a Monday', 3)
    caption_builder.build_message()