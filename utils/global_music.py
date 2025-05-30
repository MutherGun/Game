from kivy.core.audio import SoundLoader

class GlobalMusicPlayer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GlobalMusicPlayer, cls).__new__(cls)
            cls._instance.music = None
        return cls._instance

    def play_music(self, path):
        if self.music:
            return  # Už hraje

        self.music = SoundLoader.load(path)
        if self.music:
            self.music.loop = True
            self.music.play()

    def stop_music(self):
        if self.music:
            self.music.stop()
            self.music = None
