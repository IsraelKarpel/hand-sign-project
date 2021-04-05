# Yair
# NOTE: works only in US English
# This is a program that gets:
# Words and their POS tags (e.g. “I_NOUN go_VERB work_NOUN”, or “work_NOUN I_NOUN go_VERB”)
# Length of time - optional (e.g. 2 seconds)
# Target sign language (e.g., American Sign Language)
# output path
# and generates the new pose sequence file, and saves it to the path specified.
import os

import Parser
import PoseLoader
import SmoothingAlgorithm
from pose_format.pose_visualizer import PoseVisualizer

BASE_PATH = "pose_en_files/"


# this function parses the words and their POS's input into a string(sentence) and returns it.
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
    output_path = input("Please enter output path")
    isDirectory = os.path.isdir(output_path)
    if isDirectory is False:
        output_path = input("Please enter a valid output path")
        isDirectory = os.path.isdir(output_path)
        if isDirectory is False:
            print("Invalid input")
            exit(-1)
    sentence = parsePOS(wordsPOS)
    basic_words, all_list = Parser.parse_captions1(sentence)
    pose_dict = PoseLoader.load_poses("index.jsonl", "en.us")
    poses = PoseLoader.find_poses(BASE_PATH, pose_dict, basic_words)
    if isTime:
        new_pose = SmoothingAlgorithm.runSmoothingAlgorithmwithtime(poses, length)
    else:
        new_pose = SmoothingAlgorithm.runSmoothingAlgorithm(poses)
    f = open("{0}".format(output_path + "/" + sentence), "wb")
    if f:
        new_pose.write(f)
        f.close()
    else:
        print("couldn't open file")
        exit(-2)


if __name__ == "__main__":
    main()
