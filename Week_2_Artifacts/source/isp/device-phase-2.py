rendering_language = {
    'ENGLISH': 0,
    'FRENCH': 1,
    'GERMAN': 2,
    'SPANISH': 3,
}

standard_greeting_type = {
    'HELLO': 0,
    'THANKS': 1,
    'GOODBYE': 2
}

english_greetings = {
    'HELLO': 'Hello!',
    'THANKS': 'Thanks!',
    'GOODBYE': 'Goodbye!'
}

french_greetings = {
    'HELLO': 'Bonjour!',
    'THANKS': 'Merci!',
    'GOODBYE': 'Au revoir!'
}

german_greetings = {
    'HELLO': 'Hallo!',
    'THANKS': 'Vielen Dank!',
    'GOODBYE': 'Auf Wiedersehen!'
}

spanish_greetings = {
    'HELLO': 'Hola!',
    'THANKS': 'Gracias!',
    'GOODBYE': 'Adios!'
}


class RenderingLanguage:
    def render_text(self, typed_text):
        pass


class FrenchRendering(RenderingLanguage):
    def render_text(self, typed_text, greeting_type):
        text = ''

        if greeting_type == standard_greeting_type['HELLO']:
            text = french_greetings['HELLO']
        elif greeting_type == standard_greeting_type['THANKS']:
            text = french_greetings['THANKS']
        elif greeting_type == standard_greeting_type['GOODBYE']:
            text = french_greetings['GOODBYE']
        else:
            print('Incompatible greeting type passed!')
            return

        print(f'Translated to French: {text}')


class GermanRendering(RenderingLanguage):
    def render_text(self, typed_text, greeting_type):
        text = ''

        if greeting_type == standard_greeting_type['HELLO']:
            text = german_greetings['HELLO']
        elif greeting_type == standard_greeting_type['THANKS']:
            text = german_greetings['THANKS']
        elif greeting_type == standard_greeting_type['GOODBYE']:
            text = german_greetings['GOODBYE']
        else:
            print('Incompatible greeting type passed!')
            return

        print(f'Translated to German: {text}')


class SpanishRendering(RenderingLanguage):
    def render_text(self, typed_text, greeting_type):
        text = ''

        if greeting_type == standard_greeting_type['HELLO']:
            text = spanish_greetings['HELLO']
        elif greeting_type == standard_greeting_type['THANKS']:
            text = spanish_greetings['THANKS']
        elif greeting_type == standard_greeting_type['GOODBYE']:
            text = spanish_greetings['GOODBYE']
        else:
            print('Incompatible greeting type passed!')
            return

        print(f'Translated to Spanish: {text}')


class EnglishKeyboard:
    def __init__(self):
        self._typed_text = ''
        self._greeting_type = -1

    @property
    def typed_text(self):
        return self._typed_text

    @typed_text.setter
    def typed_text(self, typed_text):
        self._typed_text = typed_text

    @property
    def greeting_type(self):
        return self._greeting_type

    @greeting_type.setter
    def greeting_type(self, greeting_type):
        self._greeting_type = greeting_type

    def input_text(self, typed_text, greeting_type):
        self.typed_text = typed_text
        self.greeting_type = greeting_type

    def display_text(self, language_type):
        print(f'Greetings in English: {self.typed_text}')

        rendering = None

        if language_type == rendering_language['FRENCH']:
            rendering = FrenchRendering()
            rendering.render_text(self.typed_text, self.greeting_type)
        elif language_type == rendering_language['GERMAN']:
            rendering = GermanRendering()
            rendering.render_text(self.typed_text, self.greeting_type)
        elif language_type == rendering_language['SPANISH']:
            rendering = SpanishRendering()
            rendering.render_text(self.typed_text, self.greeting_type)
        else:
            print(f'Remain in English: {self.typed_text}')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    english_keyboard = EnglishKeyboard()

    english_keyboard.input_text(english_greetings['HELLO'], standard_greeting_type['HELLO'])
    english_keyboard.display_text(rendering_language['FRENCH'])

    english_keyboard.input_text(english_greetings['THANKS'], standard_greeting_type['THANKS'])
    english_keyboard.display_text(rendering_language['SPANISH'])

    english_keyboard.input_text(english_greetings['GOODBYE'], standard_greeting_type['GOODBYE'])
    english_keyboard.display_text(rendering_language['GERMAN'])

    english_keyboard.input_text(english_greetings['GOODBYE'], standard_greeting_type['GOODBYE'])
    english_keyboard.display_text(rendering_language['ENGLISH'])