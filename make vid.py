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

    def wrap_audio(sound):
        edges = mpy.AudioFileClip(r'C:\Dump\git\reddit content grabber\data\Use\The_Shadow_Self[ambient].mp3').subclip(11, 11.01)
        clip = mpy.concatenate_audioclips([edges, sound.subclip(edges.duration, sound.duration - edges.duration), edges])
        # vid_content.reader.close()
        # vid_content.audio.reader.close_proc()
        return clip

    os.chdir('..')
    os.chdir('use')
    print(names_list)
    # intro_audio = mpy.AudioFileClip('Intro(2).wav').set_end(5.7)
    intro_clip = mpy.VideoFileClip('Intro(1).mp4').set_end(5.6)
    print(intro_clip.audio.duration, intro_clip.duration)
    transition_clip = mpy.AudioFileClip('Karate_hit[transition].mp3').set_end(.8)
    bg_music = mpy.AudioFileClip('The_Shadow_Self[ambient].mp3').set_end(162)
    silence = mpy.AudioFileClip('1-second-of-silence.mp3').set_end(1)
    quiet_time = 0
    intro_silent_cat = []
    while quiet_time < intro_clip.duration:
        if quiet_time + silence.duration < intro_clip.duration:
            intro_silent_cat.append(silence)
            quiet_time += silence.duration
            print(quiet_time)
        else:
            intro_silent_cat.append(silence.subclip(0, intro_clip.duration - quiet_time))
            quiet_time += silence.duration
    print(0)
    intro_clip_audio = mpy.CompositeAudioClip([mpy.concatenate_audioclips(intro_silent_cat), intro_clip.audio])
    print(1)
    intro_clip = intro_clip.set_audio(intro_clip_audio)
    print(mpy.AudioFileClip('Karate_durration.mp3').duration, intro_clip.duration, transition_clip.duration, bg_music.duration, silence.duration)
    os.chdir('..')
    os.chdir(files_dir)
    vid_len = float(0)
    content_clips = []
    audio_channel = []
    vid_channel = []
    # todo make 600 again
    while vid_len < 110 and len(names_list) > 0:
        active = names_list.pop(0)
        content_clips.append(active[0])
        current_audio = mpy.AudioFileClip(active[1], fps=44100)
        audio_set = mpy.concatenate_audioclips([silence, current_audio, silence, transition_clip])
        if len(str(audio_set.duration)) > 6:
            print('ran shortener')
            audio_set = audio_set.set_end(float(str(audio_set.duration)[:6]))
        vid_set = mpy.ImageClip(active[0], duration=audio_set.duration + (-.7 if vid_len == 0 else (.7 if vid_len + audio_set.duration > 600 else 0)))
        vid_len += audio_set.duration
        audio_channel.append(audio_set)
        vid_channel.append(vid_set)
        print(active, vid_len, current_audio.duration, audio_set.duration)
        # try:
        #     audio_set.write_audiofile('__' + active[1])
        # except IndexError:
        #     print('ran exception')
        #     audio_set = audio_set.subclip(t_end=(audio_set.duration - 1.0/audio_set.fps))
        #     audio_set.write_audiofile('__' + active[1])
        del current_audio
        del audio_set
    print('merging')
    audio_content = mpy.concatenate_audioclips(audio_channel)
    bg_content = []
    bg_len = 0
    while bg_len < audio_content.duration:
        if bg_len + bg_music.duration > audio_content.duration:
            bg_content.append(bg_music.set_end(audio_content.duration - bg_len))
        else:
            bg_content.append(bg_music)
        bg_len += bg_music.duration
    bg_channel = mpy.concatenate_audioclips(bg_content).volumex(.1)
    # all_sound = mpy.CompositeAudioClip([audio_content, bg_channel])
    vid_content = mpy.concatenate_videoclips(vid_channel).set_audio(audio_content).resize((1280, 720))
    # todo working write here
    vid_content.write_videofile('__del later.mp4', fps=30)
    print(os.getcwd())
    exit()
    final = mpy.concatenate_videoclips([intro_clip, vid_content.subclip(1, 2), intro_clip.subclip(1, 5)])
    # if len(str(final.duration)) > 6:
    #     print('ran shortener')
    #     final = final.set_end(float(str(final.duration)[:6]))
    print(intro_clip.duration, audio_content.duration, vid_content.duration, final.duration, intro_clip.duration * 2 + audio_content.duration)
    print(audio_content.duration, bg_channel.duration, final.duration)
    final.write_videofile('mash.mp4', fps=30, audio_fps=44100)
    exit()
    intro_clip.reader.close()
    intro_clip.audio.reader.close_proc()
    vid_content.reader.close()
    vid_content.audio.reader.close_proc()


def main():
    target_folder = 'who_here_has_actually_married_their_lets_get'
    go_to_folder(target_folder)
    names = get_names()
    make_vid(names, target_folder)


if __name__ == '__main__':
    main()
