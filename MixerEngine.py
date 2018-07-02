import pygame, os, random

pygame.init()
pygame.mixer.init(48000, channels=1)


class Mixer:
    def __init__(self, folder):
        self.last_play_index = 0
        waves = [os.path.join(folder, n) for n in os.listdir(folder) if n.endswith("ogg")]
        pygame.mixer.set_num_channels(len(waves))
        self.sounds = [[pygame.mixer.Sound(n), False] for n in waves]

    def play_next_sound(self):
        if self.amount_playing() == len(self.sounds):
            return
        sound, playing = self.sounds[self.last_play_index]
        if playing:
            self.last_play_index = (self.last_play_index + 1) % len(self.sounds)
            return
        channel = pygame.mixer.find_channel()
        channel.play(sound, loops=-1, fade_ms=1000 + random.randint(0, 2000))
        self.sounds[self.last_play_index][1] = True
        self.last_play_index = (self.last_play_index + 1) % len(self.sounds)

    def amount_playing(self):
        playing = 0
        for n in range(0, len(self.sounds)):
            if self.sounds[n][1]:
                playing += 1
        return playing

    def stop_playing(self, soundId):
        if soundId not in range(0, len(self.sounds)):
            return False
        if self.sounds[soundId][1]:
            self.sounds[soundId][0].fadeout(1000 + random.randint(0, 2000))
            self.sounds[soundId][1] = False
            return True

    def is_playing(self, id):
        if id in range(0, len(self.sounds)):
            return self.sounds[id][1]
        return False

    def stop_playing_one(self):
        num_playing = self.amount_playing()
        if num_playing == 0:
            return
        for n in range(self.last_play_index + len(self.sounds), self.last_play_index + len(self.sounds) * 2):
            if self.is_playing(n % len(self.sounds)):
                self.stop_playing(n % len(self.sounds))
                return

    def set_playing(self, amount):
        if amount < 0:
            return
        if amount > len(self.sounds):
            amount = len(self.sounds)
        current_playing = self.amount_playing()
        if current_playing > amount:
            for n in range(0, current_playing - amount):
                self.stop_playing_one()
        if current_playing < amount:
            for n in range(0, amount - current_playing):
                self.play_next_sound()
