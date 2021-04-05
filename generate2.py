# Yair
# NOTE: works only in US English
# This is a program that gets:
# sentence "I go to work"
# Length of time - optional (e.g. 2 seconds)
# Target sign language (e.g., American Sign Language)
# output path
# and generates the new pose sequence file, and saves it to the path specified.
import sys

from pose_format.pose_visualizer import PoseVisualizer

import Parser
import PoseLoader
import SmoothingAlgorithm

BASE_PATH = "pose_en_files/"


def main():
    sentence = input("Please enter the sentence you want to translate:")
    output_path = input("Please enter output path")
    basic_words, all_list = Parser.parse_captions1(sentence)
    pose_dict = PoseLoader.load_poses("index.jsonl", "en.us")
    poses = PoseLoader.find_poses(BASE_PATH, pose_dict, basic_words)
    new_pose = SmoothingAlgorithm.runSmoothingAlgorithm(poses)
    f = open("{0}".format(output_path + "/" + sentence), "wb")
    new_pose.write(f)
    f.close()
    # v = PoseVisualizer(new_pose)
    # v.save_video("{0}.mp4".format((output_path+"/"+sentence)), v.draw())


if __name__ == "__main__":
    main()
