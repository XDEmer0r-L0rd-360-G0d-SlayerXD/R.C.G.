import os
import moviepy.editor as mpy
import sys


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
    transition_clip = mpy.AudioFileClip('Karate_hit[transition].mp3').set_end(.8)
    silence = mpy.AudioFileClip('1-second-of-silence.mp3').set_end(1)
    os.chdir('..')
    os.chdir(files_dir)
    vid_len = 0
    content_clips = []
    audio_channel = []
    vid_channel = []
    # todo make 600 again
    while vid_len < 600 and len(names_list) > 0:
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
        del current_audio
        del audio_set
    print('merging')
    audio_content = mpy.concatenate_audioclips(audio_channel)
    vid_content = mpy.concatenate_videoclips(vid_channel).set_audio(audio_content).resize((1280, 720))
    # todo working write here
    vid_content.write_videofile(files_dir + '.mp4', fps=30)
    print(os.getcwd())
    exit()


def main():
    target_folder = 'who_here_has_actually_married_their_lets_get'
    if len(sys.argv) > 1:
        target_folder = sys.argv[1]
    go_to_folder(target_folder)
    names = get_names()
    make_vid(names, target_folder)


if __name__ == '__main__':
    main()
