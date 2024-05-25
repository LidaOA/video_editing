import random

from moviepy.editor import VideoFileClip,AudioFileClip,CompositeAudioClip,vfx,afx,concatenate_videoclips
import os
import numpy as np
from PIL import Image

def fade_voice_video(link_video:str,fade = True) -> VideoFileClip :
    audio = AudioFileClip(link_video).fx(afx.audio_fadein, 2).fx(afx.audio_fadeout, 5)
    video = VideoFileClip(link_video).set_audio(audio)
    if fade :
        video = video.fx(vfx.fadein,1).fx(vfx.fadeout,1)
    return video

def backsound_processing(link_backsound: str) -> AudioFileClip:
    backsound = AudioFileClip(link_backsound)
    backsound = backsound.fx(afx.volumex,0.04)
    return backsound

def mixing_video_and_backsound(video : VideoFileClip,backsound : AudioFileClip) -> VideoFileClip:
    if backsound.duration > video.duration:
        backsound = backsound.set_duration(video.duration)
    
    backsound = backsound.fx(afx.audio_fadein, 2).fx(afx.audio_fadeout, 5)
    audio_end = CompositeAudioClip([video.audio, backsound])
    video_mixed = video.set_audio(audio_end)
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


def tune_db(link_backsound: str,factor_tune : float) -> AudioFileClip:
    sound = AudioFileClip(link_backsound)
    soud = sound.fx(afx.volumex,factor_tune)
    return sound



def merger(link_video:str, link_sound:str):
    videoclip = fade_voice_video(link_video)
    backsoundclip = backsound_processing(link_sound)
    videoclip_mixed = mixing_video_and_backsound(videoclip, backsoundclip)
    videoclip_mixed.set_duration(videoclip_mixed.duration)
    videoclip_mixed.write_videofile(f'{os.getcwd()}\output\processed_{random_with_N_digits(5)}.mp4', fps=25, threads=1, codec="libx264")
    videoclip_mixed.reader.close()
    videoclip.reader.close()


def append_or_insert(path_origin_video : str, path_insert_video : str, time_insert : float = None):

    videoclip_origin = VideoFileClip(path_origin_video)
    videoclip_insert = VideoFileClip(path_origin_video)

    if ((videoclip_insert.w != videoclip_origin.w) and (videoclip_insert.h != videoclip_origin.h)):
        raise ValueError("Size of Video1 and Video2 are different")

    if time_insert != None and time_insert > 0:
        videoclip_origin_first = videoclip_origin.set_duration(time_insert)

    videoclip_origin_last = videoclip_origin.set_start(time_insert+videoclip_insert.duration)
    clips = [videoclip_origin_first,videoclip_insert.crossfadein(0.3),
              videoclip_origin_last.crossfadein(0.3)]
    final_video = concatenate_videoclips(clips,method='compose')
    return final_video


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return random.randint(range_start, range_end)
