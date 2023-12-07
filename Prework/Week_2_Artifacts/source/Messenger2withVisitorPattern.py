standard_emotion = {
    'HAPPY': 0,
    'SAD': 1,
    'ANGRY': 2
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

    def accept(self, renderer):
        if renderer:
            renderer.render_emoticon(self)


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

    def accept(self, renderer):
        if renderer:
            renderer.render_caption(self)


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


class Renderer:
    def render_caption(self, caption):
        pass

    def render_emoticon(self, emoticon):
        pass


class NormalRenderer(Renderer):
    def render_caption(self, caption):
        if caption:
            caption.text = 'NORMAL:: ' + caption.text + ' ::NORMAL'
            print(f'{caption.text}')

    def render_emoticon(self, emoticon):
        if emoticon:
            emoticon.emotion = 'NORMAL:: ' + emoticon.emotion + ' ::NORMAL'
            print(f'{emoticon.emotion}')


class EmphasisRenderer(Renderer):
    def render_caption(self, caption):
        if caption:
            caption.text = 'EMPHASIS:: ' + caption.text + ' ::EMPHASIS'
            print(f'{caption.text}')

    def render_emoticon(self, emoticon):
        if emoticon:
            emoticon.emotion = 'EMPHASIS:: ' + emoticon.emotion + ' ::EMPHASIS'
            print(f'{emoticon.emotion}')

class NewRenderer(Renderer):
    def render_caption(self, caption):
        if caption:
            caption.text = 'New:: ' + caption.text + ' ::New'
            print(f'{caption.text}')

    def render_emoticon(self, emoticon):
        if emoticon:
            emoticon.emotion = 'New:: ' + emoticon.emotion + ' ::New'
            print(f'{emoticon.emotion}')

class LatestLogic(Renderer):
    def render_caption(self, caption):
        if caption:
            caption.text = 'LatestLogic:: ' + caption.text + ' ::LatestLogic'
            print(f'{caption.text}')

    def render_emoticon(self, emoticon):
        if emoticon:
            emoticon.emotion = 'New:: ' + emoticon.emotion + ' ::New'
            print(f'{emoticon.emotion}')


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

    def render_message(self, renderer):
        if len(self.caption_list) == len(self.emoticon_list):
            size = len(self.caption_list)
            for index in range(0, size):
                # Implement a new Functionality on Caption
                # without changing Caption Concerete Class.
                # Please accept a new functionality on this object.
                self.caption_list[index].accept(renderer)
                # Implement a new Functionality on Emoticon
                # without changing Emoticon Concerete Class.
                self.emoticon_list[index].accept(renderer)

        self.caption_list.clear()
        self.emoticon_list.clear()


if __name__ == '__main__':
    keyboard = Keyboard()

    caption_builder = CaptionBuilder(keyboard)
    normal_renderer = NormalRenderer()
    emphasis_renderer = EmphasisRenderer()
    #new_renderer = NewRenderer()

    # Message 1
    keyboard.reset()
    keyboard.input([standard_emotion['HAPPY']])
    caption_builder.build_message()
    caption_builder.render_message(emphasis_renderer)
    print('\n\n')

    keyboard.reset()
    keyboard.input([standard_emotion['HAPPY']])
    caption_builder.build_message()
    caption_builder.render_message(new_renderer)
    print('\n\n')

    keyboard.reset()
    keyboard.input([standard_emotion['SAD'], standard_emotion['HAPPY']])
    caption_builder.build_message()
    caption_builder.render_message(normal_renderer)
    print('\n\n')

    keyboard.reset()
    keyboard.input([standard_emotion['ANGRY'], standard_emotion['SAD'], standard_emotion['HAPPY']])
    caption_builder.build_message()
    caption_builder.render_message(emphasis_renderer)
    print('\n\n')

    keyboard.reset()
    keyboard.input([-1])
    caption_builder.build_message()
    caption_builder.render_message(normal_renderer)