import projector_screen.SecondWindow as sw


class Projector(sw.SecondWindow):
    def __init__(self):
        self._window = sw.SecondWindow()
        self._window.hide_second_screen()

    def show_verse(self, text, *args):
        if not self._window:
            self.__init__()
        self._window.show_text(text, *args)

    def verses_active(self):
        return self._window.verses_active

    def song_active(self):
        return self._window.song_active

    def picture_active(self):
        return self._window.picture_active

    def hide(self):
        self._window.hide_second_screen()

    def show_slide(self, text, *args):
        self._window.show_slide(text)

    def show_picture(self, image, scale=1):
        self._window.show_picture(image, scale)

    def get_settings(self):
        return self._window.get_settings()

    def set_settings(self, settings):
        self._window.set_settings(settings)

    def set_effective_area(self):
        self._window.set_effective_area()
