import os
import random
import numpy as np
import argparse
import PIL
from functions import fade_voice_video,backsound_processing,mixing_video_and_backsound,get_screenshots_adjusted

parser = argparse.ArgumentParser()

parser.add_argument('--folder_videos','-f_v', type = str,help='Path to the input video folder')
parser.add_argument('--folder_audios','-f_a',type = str, help='Path to the input audio folder')

args = parser.parse_args()

if __name__== "__main__":
    check_arg_1,check_arg_2 = False,False
    if args.folder_videos is not None and os.path.isdir(args.folder_videos):
    	check_arg_1 = True
    if args.folder_audios is not None and os.path.isdir(args.folder_audios):
    	check_arg_2 = True

    dir1 = os.scandir(args.folder_videos) if check_arg_1 else os.scandir(f'{os.getcwd()}\input_data')
    dir2 = os.scandir(args.folder_audios) if check_arg_2 else os.scandir(f'{os.getcwd()}\input_backsound')

    input_links_videos = [obj_dir.path for obj_dir in dir1]
    input_links_backsounds = [obj_dir.path for obj_dir in dir2]

    if not input_links_videos:
        raise FileNotFoundError("The videos list is empty")

    for i,link in enumerate(input_links_videos, start = 1):
        file_name = os.path.basename(link)
        video_name = os.path.splitext(file_name)[0]
        videoclip = fade_voice_video(link)
        link_sound = random.choice(input_links_backsounds)
        backsoundclip = backsound_processing(link_sound)
        videoclip_mixed = mixing_video_and_backsound(videoclip,backsoundclip)
        videoclip_mixed.with_duration(videoclip_mixed.duration)
        videoclip_mixed.write_videofile(f'{os.getcwd()}\output\processed_{video_name}_{i}.mp4', fps=25, threads = 1, codec="libx264")
        imgs_link = get_screenshots_adjusted(videoclip_mixed)
        for k,img in enumerate(imgs_link,start = 1):
            img.save(f'{os.getcwd()}\images\Frame_{i}_{k}_rand{random.randint(100, 999)}_.png')

        videoclip_mixed.close()
        videoclip.close()
