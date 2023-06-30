


standard_emotion = {
    'HAPPY': 0,
    'SAD': 1,
    'ANGRY': 2
}

rendering_types = {
    'NORMAL': 0,
    'EMPHASIS': 1
}


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

    def normal_rendering(self):
        if self.emotion:
            self.emotion = 'NORMAL:: ' + self.emotion + ' ::NORMAL'
            print(f'{self.emotion}')

    def emphasis_rendering(self):
        if self.emotion:
            self.emotion = 'EMPHASIS:: ' + self.emotion + ' ::EMPHASIS'
            print(f'{self.emotion}')


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


class Caption:
    def __init__(self, text):
        self._text = text

    def __str__(self):
        print(f'{self.text}')

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    def normal_rendering(self):
        if self.text:
            self.text = 'NORMAL:: ' + self.text + ' ::NORMAL'
            print(f'{self.text}')

    def emphasis_rendering(self):
        if self.text:
            self.text = 'EMPHASIS:: ' + self.text + ' ::EMPHASIS'
            print(f'{self.text}')


class HappyCaption(Caption):
    def __init__(self):
        super().__init__('What a beautiful day!')


class SadCaption(Caption):
    def __init__(self):
        super().__init__('The world is so difficult!')


class AngryCaption(Caption):
    def __init__(self):
        super().__init__('I will put an end to all misery!')


class Keyboard:
    def __init__(self):
        self.emotion_list = []

    def input(self, emotions):
        self.emotion_list.extend(emotions)

    def reset(self):
        self.emotion_list.clear()


class CaptionBuilder:
    def __init__(self, keyboard):
        self.keyboard = keyboard
        self.caption_list = []
        self.emoticon_list = []

    def build_message(self):
        for emotion in self.keyboard.emotion_list:
            if emotion == standard_emotion['HAPPY']:
                caption = HappyCaption()
                emoticon = Happy()
            elif emotion == standard_emotion['SAD']:
                caption = SadCaption()
                emoticon = Sad()
            elif emotion == standard_emotion['ANGRY']:
                caption = AngryCaption()
                emoticon = Angry()
            else:
                print('Unsupported emotion experienced!')
                continue

            if caption:
                self.caption_list.append(caption)

            if emoticon:
                self.emoticon_list.append(emoticon)

    def render_message(self, rendering):
        if len(self.caption_list) == len(self.emoticon_list):
            size = len(self.caption_list)
            for index in range(0, size):
                if rendering == rendering_types['NORMAL']:
                    self.caption_list[index].normal_rendering() # Car.LiftThroughHeliCopter()
                    self.emoticon_list[index].normal_rendering()
                elif rendering == rendering_types['EMPHASIS']:
                    self.caption_list[index].emphasis_rendering() # Car.CreateWings()
                    self.emoticon_list[index].emphasis_rendering()
                else:
                    print('Rendering Type Not Supported')
                    return

        self.caption_list.clear()
        self.emoticon_list.clear()


if __name__ == '__main__':

    keyboard = Keyboard()

    caption_builder = CaptionBuilder(keyboard)

    # Message 1
    keyboard.reset()
    keyboard.input([standard_emotion['HAPPY']])
    caption_builder.build_message()
    caption_builder.render_message(rendering_types['EMPHASIS'])
    print('\n\n')

    keyboard.reset()
    keyboard.input([standard_emotion['SAD'], standard_emotion['HAPPY']])
    caption_builder.build_message()
    caption_builder.render_message(rendering_types['NORMAL'])
    print('\n\n')

    keyboard.reset()
    keyboard.input([standard_emotion['ANGRY'], standard_emotion['SAD'], standard_emotion['HAPPY']])
    caption_builder.build_message()
    caption_builder.render_message(rendering_types['EMPHASIS'])
    print('\n\n')

    keyboard.reset()
    keyboard.input([-1])
    caption_builder.build_message()
    caption_builder.render_message(rendering_types['NORMAL'])