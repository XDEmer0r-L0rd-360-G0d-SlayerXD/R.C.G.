import os
import moviepy.editor as mpy
from mutagen.mp3 import MP3


def go_to_folder(target_folder):
    os.chdir('data')
    os.chdir(target_folder)
    open('test.txt', 'w').close()


def get_names():
    all_names = os.listdir()
    all_names = sorted(all_names, reverse=True)
    grouped = []
    while len(all_names) > 1:
        if all_names[0][:-3] == all_names[1][:-3]:
            grouped.append((all_names.pop(0), all_names.pop(0)))
        else:
            all_names.pop(0)
    return grouped


def make_vid(names_list, files_dir):
    os.chdir('..')
    os.chdir('use')
    print(names_list)
    intro_clip = mpy.VideoFileClip('Intro(1).mp4')
    transition_clip = mpy.AudioFileClip('Karate hit single.mp3')
    bg_music = mpy.AudioFileClip('The_Shadow_Self[ambient].mp3')
    os.chdir('..')
    os.chdir(files_dir)
    vid_len = float(0)
    content_clips = []
    audio_channel = []
    vid_channel = []
    while vid_len < 600 and len(names_list) > 0:
        active = names_list.pop(0)
        mu_audio = MP3(active[1])
        print(mu_audio.info.length)
        current_audio = mpy.AudioFileClip(active[1], fps=44100).set_duration(mu_audio.info.length)
        audio_set = mpy.CompositeAudioClip([bg_music.subclip(11, 11.1).volumex(.01), current_audio.set_start(vid_len + 1), transition_clip.set_start(current_audio.duration + 2 + vid_len)])
        current_vid = mpy.ImageClip(active[0], duration=audio_set.duration + (1 if max(0, vid_len - .7) != 0 else .3))
        vid_set = mpy.CompositeVideoClip([current_vid]).set_start(max(0, vid_len - .7))
        vid_len += vid_set.duration - vid_len
        audio_channel.append(audio_set)
        vid_channel.append(vid_set)
        print(active, vid_len, vid_set.duration, audio_set.duration)
    print('merging')
    audio_content = mpy.CompositeAudioClip(audio_channel)
    vid_content = mpy.CompositeVideoClip(vid_channel).set_audio(audio_content)
    final = mpy.concatenate_videoclips([intro_clip, vid_content, intro_clip])
    final.write_videofile('mash.mp4', fps=30, audio_fps=44100)


def main():
    target_folder = 'redditors_with_good_handwriting_what_are_some'
    go_to_folder(target_folder)
    names = get_names()
    make_vid(names, target_folder)


if __name__ == '__main__':
    main()
