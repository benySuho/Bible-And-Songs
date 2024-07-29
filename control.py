import projector_screen.projector as pj


class Controller:
    def __init__(self):
        self.projector = pj.Projector()
        self.verses = None
        self.songs = None
        self.songs_edit = None
        self.settings = None
        self.tabs = None

    def set_verses(self, verses):
        self.verses = verses

    def set_songs(self, songs):
        self.songs = songs

    def set_songs_edit(self, songs_edit):
        self.songs_edit = songs_edit

    def set_settings(self, settings):
        self.settings = settings

    def set_tabs(self, tabs):
        self.tabs = tabs

    def get_projector_settings(self):
        return self.projector.get_settings()

    def set_projector_settings(self, settings):
        self.projector.set_settings(settings)

    def set_effective_area(self):
        self.projector.set_effective_area()

    def show_verse(self, text, *args):
        self.projector.show_verse(text, *args)

    def verses_active(self):
        return self.projector.verses_active()

    def picture_active(self):
        return self.projector.picture_active()

    def song_active(self):
        return self.projector.song_active()

    def hide(self):
        self.projector.hide()

    def show_slide(self, text):
        self.projector.show_slide(text)

    def show_picture(self, image, scale):
        self.projector.show_picture(image, scale)

    def get_verses_settings(self):
        return self.verses.get_settings()

    def set_verses_settings(self, settings):
        self.verses.set_settings(settings)

    def get_songs_settings(self):
        return self.songs.get_settings()

    def set_songs_settings(self, settings):
        self.songs.set_settings(settings)

    def refresh_songs(self):
        self.songs.rearrange_frames()

    def edit_songs(self, song):
        self.songs_edit.song_chosen(name=song)
        self.tabs.select(self.songs_edit)

    def update_song(self, old_song=None, new_song=None):
        if old_song and new_song:
            self.songs.update_song(old_song, new_song)
        else:
            self.songs.update_songs()

    def delete_song(self, song):
        self.songs.delete_song(song)

    def get_interface_font(self):
        if self.settings:
            return self.settings.interface_font
        else:
            return None
    def apply_interface_font(self, font=None, widget_holder=None):
        if not font:
            font = self.settings.interface_font
        else:
            self.settings.interface_font = font
        if not widget_holder:
            widget_holder = self.tabs

        for widget in widget_holder.winfo_children():
            try:
                widget.configure(font=font)
            except:
                pass
            if widget.winfo_children():
                self.apply_interface_font(font=font, widget_holder=widget)

        self.songs.apply_interface_font(font=font)

    def update_translation_order(self):
        self.settings.update_translation_order()

    def get_all_translation(self):
        return self.verses.get_all_translation()
