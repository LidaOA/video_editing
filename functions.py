import random

from moviepy import VideoFileClip,AudioFileClip,concatenate_videoclips,afx,vfx,CompositeAudioClip,CompositeVideoClip

import os
import numpy as np
from PIL import Image


def fade_voice_video(link_video: str, fade=True) -> VideoFileClip:
    """Applique des effets de fondu audio et vidéo à un clip vidéo."""
    audio = AudioFileClip(link_video)
    # Utilisation de with_fx pour appliquer les effets audio en une seule étape
    audio = audio.with_effects([
        afx.AudioFadeIn(2.5),
        afx.AudioFadeOut(3),
        afx.MultiplyVolume(1.3)
    ])
    video = VideoFileClip(link_video).with_audio(audio)
    if fade:
      # Utilisation de with_fx pour appliquer les effets vidéo en une seule étape
        video = video.with_effects([
            vfx.FadeIn(1),
            vfx.FadeOut(1)
        ])
    return video


def backsound_processing(link_backsound: str) -> AudioFileClip:
    """Traite une piste audio de fond en ajustant le volume."""
    backsound = AudioFileClip(link_backsound)
    # Utilisation de with_volume pour ajuster le volume
    backsound = backsound.with_volume_scaled(0.04)
    return backsound


def mixing_video_and_backsound(video: VideoFileClip, backsound: AudioFileClip) -> VideoFileClip:
    """Mélange une piste audio avec la bande son d'une vidéo."""
    if backsound.duration > video.duration:
        # Utilisation de with_duration pour définir la durée
        backsound = backsound.with_duration(video.duration)

        # Utilisation de with_effects pour appliquer les effets audio en une seule étape
    backsound = backsound.with_effects([
        afx.AudioFadeIn(2),
        afx.AudioFadeOut(3),
    ])
    audio_end = CompositeAudioClip([video.audio, backsound])
    video_mixed = video.with_audio(audio_end)
    return video_mixed

def get_screenshots_adjusted(video : VideoFileClip) -> list[Image]:
    time_video = int(video.duration) + 1
    RGB = [1, 1, 249/255]
    imgs = []
    for t in range (5,time_video,(time_video//6)):
        frame : np.ndarray = video.get_frame(t)
        R,G,B = 1.0 * np.array(RGB)/(sum(RGB))
        im = R * frame[:, :, 0] + G * frame[:, :, 1] + B * frame[:, :, 2]
        im = np.dstack(3 * [im]).astype("uint8")
        imgs.append(Image.fromarray(im))

    return imgs


def tune_db(link_backsound: str, factor_tune: float) -> AudioFileClip:
    """Ajuste le volume d'un clip audio."""
    sound = AudioFileClip(link_backsound)
    # Utilisation de with_volume_scaled pour ajuster le volume
    sound = sound.with_volume_scaled(factor_tune)
    return sound


def merger(link_video: str, link_sound: str):
    """Fusionne une vidéo avec une bande son puis l'enregistre directement."""
    videoclip = fade_voice_video(link_video)
    backsoundclip = backsound_processing(link_sound)
    videoclip_mixed = mixing_video_and_backsound(videoclip, backsoundclip)
    # Pas besoin de set_duration ici car la durée est déjà définie
    # La durée du clip final est définie par mixing_video_and_backsound
    videoclip_mixed.write_videofile(
        f'{os.getcwd()}/output/processed_{random_with_N_digits(5)}.mp4', fps=25, threads=1, codec="libx264")
    # Fermeture des ressources
    videoclip_mixed.audio.close()
    videoclip_mixed.close()
    videoclip.close()


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return random.randint(range_start, range_end)
