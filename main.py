import cv2
import numpy as np
import numpy.ma as ma

import sys
from Dictionaries import Dictionaries
import Dictionary
import PoseObj

from PoseN import PoseN

sys.path.append("/")

from pose_format import Pose
from pose_format.numpy import NumPyPoseBody
from pose_format.pose_visualizer import PoseVisualizer


#from pose_formatloc.pose_format.pose import Pose
#from pose_format.pose_body import PoseBody as NumPyPoseBody
#from pose_formatloc.pose_format.pose_visualizer import PoseVisualizer
import json
import Parser
import PoseLoader
import TTMLParser
import SmoothingAlgorithm
#import SubsAnalyse
import PoseObj

BASE_PATH = "pose_en_files/"




def create_languages_to_suffix_dictionary(filePath="langs.txt"):
    languages = {}
    file = open(filePath, 'r', encoding='utf-8')
    pose_dic = []
    if file:
        for line in file.readlines():
            parts = line.split()
            languages[parts[0]] = parts[1]
        file.close()
        return languages
    return None


#def craeate_ID_to_WORD_dicts():




def draw_words_on_frames(frames, words):
    for frame, word in zip(frames, words):
        frame = cv2.putText(frame, word, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
        yield frame


def create_pose_for_video(dict):
    list =[]
    #dict = PoseObj.PoseDictionary("en-us")
    subsarray,suffix,language = TTMLParser.getArrfromCaptions("data.xml")
    for line in subsarray:
        basic_words, all_list = Parser.parse_captions1(language,line[1])
        if len(basic_words)!=0:
            poses = PoseLoader.find_poses(BASE_PATH, dict, basic_words,suffix)
            if len(poses) != 0:
                new_pose,lenarray = SmoothingAlgorithm.runSmoothingAlgorithm(poses,line[0])
                list.append(new_pose)
        #break
    #
    #
    # padding = NumPyPoseBody(25, data=np.zeros(shape=(20, 1, 137, 2)),
    #                          confidence=np.zeros(shape=(20, 1, 137)))
    # # Join videos with padding
    # pose_body_data = ma.concatenate([ma.concatenate([p.body.data, padding.data]) for p in list])
    # pose_body_confidence = np.concatenate([np.concatenate([p.body.confidence, padding.confidence]) for p in list])
    #
    # # Create joint pose
    # new_pose_body = NumPyPoseBody(25, data=pose_body_data, confidence=pose_body_confidence)
    # new_pose = Pose(header=poses[0].header, body=new_pose_body)

    # Draw video
    #
    # new_pose.header.dimensions.width*=0.5
    # new_pose.header.dimensions.height*=0.5
    # po
    # new_pose.header.dimensions.height = int(new_pose.header.dimensions.height/2)
    # new_pose.header.dimensions.width =int(new_pose.header.dimensions.width/2)
    # new_pose.body.data/=2
    # new_pose.body.fps=20
    words = []
    for i in range(0,len(lenarray)):
        for j in range(0,lenarray[i]+10):
            words.append(basic_words[i])


    # v = PoseVisualizer(new_pose)
    # frames = v.draw()
    # v.save_video("jointwithwordsmatrix.mp4", draw_words_on_frames(frames, words))
    # v.save_video("jointWithMatrix.mp4", frames)
    # #,custom_ffmpeg="C:/Users/User/ffmpeg/bin")
    # frames = v.draw()
    f = open("po.pose","wb")
    new_pose.write(f)
    f.close()


def main():
    langs = create_languages_to_suffix_dictionary()
    dictionaries = Dictionaries()
    for l in langs:
        dict = Dictionary.PoseDictionary(l, langs[l])
        dictionaries.add_dictionary(dict)
    dictionaries.createAllWordToID()
    print("loaded index file and all dictionaries")
    suf = "en.us"
    dict = dictionaries.getdictionarybysuffix(suf)
    create_pose_for_video(dict)



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

if __name__ == '__main__':
    main()


