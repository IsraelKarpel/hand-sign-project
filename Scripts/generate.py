import sys

from pose_format.pose_visualizer import PoseVisualizer

import Parser
import PoseLoader
import SmoothingAlgorithm

BASE_PATH = "../pose_en_files/"
# def parseargs(args):
#     # "hey may name is Danny" o:pathe
#     strargs = str(args)
#     strargs = strargs.split("o:")
#     path = strargs[1]
#     sentence  = str.split('"')
def secondtool():
    sentence = input("Please enter the sentence you want to translate:")
    output_path = input("Please enter output path")
    basic_words, all_list = Parser.parse_captions1(sentence)
    pose_dict = PoseLoader.load_poses("../index.jsonl", "en.us")
    poses = PoseLoader.find_poses(BASE_PATH, pose_dict, basic_words)
    new_pose = SmoothingAlgorithm.runSmoothingAlgorithm(poses)
    f = open("{0}".format(output_path+"/"+sentence),"wb")
    new_pose.write(f)
    f.close()
    # v = PoseVisualizer(new_pose)
    # v.save_video("{0}.mp4".format((output_path+"/"+sentence)), v.draw())

def parsePOS(sentence):
    list = sentence.split()
    words = ""
    for pos in list:
        words = words + " " + pos.split('_')[0]
    return words


def main():
    isTime = True
    wordsPOS = input("Please enter Words with POS:")
    if wordsPOS == "":
        print("Invalid input, please enter a valid input")
        wordsPOS = input()
        if wordsPOS == "":
            print("Invalid input")
            exit(-1)
    length = input("Please enter length in seconds:")
    if length == "":
        isTime = False
    else:
        length = int(length)

    #Targetlang =  input("Please enter output path")
    output_path = input("Please enter output path")
    sentence = parsePOS(wordsPOS)
    basic_words, all_list = Parser.parse_captions1(sentence)
    pose_dict = PoseLoader.load_poses("../index.jsonl", "en.us")
    poses = PoseLoader.find_poses(BASE_PATH, pose_dict, basic_words)
    if isTime:
        new_pose = SmoothingAlgorithm.runSmoothingAlgorithmwithtime(poses,length)
    else:
        new_pose = SmoothingAlgorithm.runSmoothingAlgorithm(poses)
    f = open("{0}".format(output_path+"/"+sentence),"wb")
    new_pose.write(f)
    f.close()

if __name__ == "__main__":
    main()