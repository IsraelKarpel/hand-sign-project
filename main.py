import cv2
import numpy as np
import numpy.ma as ma

import sys
from Dictionaries import Dictionaries
import Dictionary
import PoseObj

sys.path.append("/")

from pose_format import Pose
from pose_format.numpy import NumPyPoseBody
from pose_format.pose_visualizer import PoseVisualizer

# from pose_formatloc.pose_format.pose import Pose
# from pose_format.pose_body import PoseBody as NumPyPoseBody
# from pose_formatloc.pose_format.pose_visualizer import PoseVisualizer
import json
import Parser
import PoseLoader
import TTMLParser
import SmoothingAlgorithm
import SquareDistanceMatrix

import PoseObj

BASE_PATH = "pose_en_files/pose_files"
from Dictionaries import Dictionaries


def create_languages_to_suffix_dictionary(filePath="langs.txt"):
    file = open(filePath, 'r', encoding='utf-8')
    dictionaries = Dictionaries()
    if file:
        for line in file.readlines():
            parts = line.split()
            dict = Dictionary.PoseDictionary(parts[0], parts[1], parts[2])
            dictionaries.add_dictionary(dict)
        file.close()
        return dictionaries
    return None


def draw_words_on_frames(frames, words):
    for frame, word in zip(frames, words):
        frame = cv2.putText(frame, word, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
        yield frame


def weighted_fps(fpsarr, timearr, totaltime):
    sum = 0
    for i in range(0, len(fpsarr)):
        sum += timearr[i] * fpsarr[i]
    return int(sum / totaltime)


def create_pose_for_video(dict, subsarray, suffix, language, totaltime, draw_words=False, draw_video=False):
    list = []
    totalframes = 0
    timearr = []
    fpsarr = []
    count = 0
    for line in subsarray:
        basic_words, all_list = Parser.parse_captions(language, suffix, line[1], dict)
        if len(basic_words) != 0:
            poses, sentence_found = PoseLoader.find_poses(BASE_PATH, dict, basic_words, suffix)
            if count == 0:
                first_pose = poses[0]
            if len(poses) != 0:
                new_pose, lenarray = SmoothingAlgorithm.runSmoothingAlgorithmVideo(poses, first_pose, True, line[0])
                timearr.append(float(line[0]))
                fpsarr.append(int(len(new_pose.body.data) / float(line[0])))
                totalframes += len(new_pose.body.data)

                list.append(new_pose)
        count += 1

    if (len(list) > 1):
        frames_per_seconds = int(totalframes / totaltime)
        padding = NumPyPoseBody(frames_per_seconds, data=np.zeros(shape=(10, 1, 137, 2)),
                                confidence=np.zeros(shape=(10, 1, 137)))
        # Join videos with padding
        pose_body_data = ma.concatenate([ma.concatenate([p.body.data, padding.data]) for p in list])
        pose_body_confidence = np.concatenate([np.concatenate([p.body.confidence, padding.confidence]) for p in list])

        # Create joint pose
        new_pose_body = NumPyPoseBody(frames_per_seconds, data=pose_body_data, confidence=pose_body_confidence)
        new_pose = Pose(header=list[0].header, body=new_pose_body)
    if draw_video:
        words = []
        for i in range(0, len(lenarray)):
            for j in range(0, lenarray[i] + 10):
                words.append(basic_words[i])
        v = PoseVisualizer(new_pose)
        frames = v.draw()
        v.save_video("sentence2.mp4", draw_words_on_frames(frames, words))

    # f = open("C:\\Users\\User\\Documents\\GitHub\\pose-format\\pose_viewer\\www\\sample-data\\video\\po.pose","wb")
    print("try new")
    new_pose.body.data -= new_pose.body.data[:, :, 1:2, :]
    new_pose.focus()
    new_pose = SmoothingAlgorithm.smooth_final_pose(new_pose)
    f = open("C:\\Users\\User\\PycharmProjects\\FINAL\\po.pose", "wb")
    new_pose.write(f)
    f.close()


def create_pose_for_sentence(dict, sentence, suffix, language, index):
    basic_words, all_list = Parser.parse_captions(language, suffix, sentence, dict)
    if len(basic_words) != 0:
        poses, sentence_found = PoseLoader.find_poses(BASE_PATH, dict, basic_words, suffix)
        if len(poses) != 0:
            new_pose, lenarray = SmoothingAlgorithm.runSmoothingAlgorithmSetence(poses, True)
            new_pose.body.data -= new_pose.body.data[:, :, 1:2, :]
            new_pose.focus()
            filename = "sentence{0}.pose".format(index)
            f = open(filename, "wb")
            new_pose.write(f)
            f.close()
            return filename, sentence_found
        else:
            return None, None
    else:
        return None, None


def translate2dest(src_poses, dic_dest):
    dest_poses = []
    sentence = ""
    for pose in src_poses:
        id = pose.pose_id
        p, word = dic_dest.find_pose_by_ID(id)
        if p:
            dest_poses.append(p)
            sentence += word + " "
    return dest_poses, sentence


def create_pose_for_sentence_dest_lang(dict, sentence, suffix, dic_dest, language, index):
    basic_words, all_list = Parser.parse_captions(language, suffix, sentence, dict)
    if len(basic_words) != 0:
        poses, sentence_found = PoseLoader.find_poses(BASE_PATH, dict, basic_words, suffix)
        # new
        poses_dest, sentence_dest = translate2dest(poses, dic_dest)
        if len(poses_dest) != 0:
            new_pose, lenarray = SmoothingAlgorithm.runSmoothingAlgorithmSetence(poses_dest, True)
            new_pose.body.data -= new_pose.body.data[:, :, 1:2, :]
            new_pose.focus()
            filename = "sentence{0}.pose".format(index)
            f = open(filename, "wb")
            new_pose.write(f)
            f.close()
            return filename, sentence_dest
        else:
            return None, None
    else:
        return None, None

#
#
# def main():
#     langs = create_languages_to_suffix_dictionary()
#     dictionaries = Dictionaries()
#     for l in langs:
#         dict = Dictionary.PoseDictionary(l, langs[l])
#         dictionaries.add_dictionary(dict)
#     dictionaries.createAllWordToID()
#     print("loaded index file and all dictionaries")
#     suf = "en.us"
#     dict = dictionaries.getdictionarybysuffix(suf)
#     create_pose_for_video(dict)
#
#
# if __name__ == '__main__':
#     import cProfile
#     cProfile.run("main()","output.dat")
#     import pstats
#     from pstats import SortKey
#     with open("output_time.txt","w") as f:
#         p = pstats.Stats("output.dat",stream=f)
#         p.sort_stats("time").print_stats()
#     with open("outputcalls.txt","w") as f:
#         p = pstats.Stats("output.dat", stream=f)
#         p.sort_stats("calls").print_stats()

# if __name__ == '__main__':
#     main()