# Yair
# This is a program that gets:
# sentence "I go to work"
# Length of time - optional (e.g. 2 seconds)
# Target sign language (e.g., American Sign Language)
# output path
# and generates the new pose sequence file, and saves it to the path specified.
import sys
import random

from pose_format.pose_visualizer import PoseVisualizer

import Dictionary
import Parser
import PoseCreator
import PoseLoader
import SmoothingAlgorithm
import os

SAVE_PATH_SENTENCES = "sentence_results"


def main():
    dictionaries = PoseCreator.create_languages_to_suffix_dictionary()
    dictionaries.createAllWordToID()
    for dic in dictionaries.dictionaries:
        dic.dict_array = Dictionary.create_length_Array(dic.wordToID)
    print("loaded index file and all dictionaries")

    sentence = input("Please enter the sentence you want to translate:")
    if sentence == "":
        print("Invalid input, please enter a valid input")
        sentence = input()
        if sentence == "":
            print("Invalid input")
            exit(-1)
    output_path = SAVE_PATH_SENTENCES
    isDirectory = os.path.isdir(output_path)
    if isDirectory is False:
        output_path = input("Please enter a valid output path")
        isDirectory = os.path.isdir(output_path)
        if isDirectory is False:
            print("Invalid input")
            exit(-1)
    sourcelang = input("Please enter source lang:")
    destlang = input("Please enter dest lang:")
    fps = 40
    n = random.randint(0, 2002)
    dictoptimum = dictionaries.getdictionarybysuffix(sourcelang + '.' + destlang)
    if dictoptimum:
        filename, sentence_found = PoseCreator.create_pose_for_sentence(dictoptimum, sentence,
                                                                        (sourcelang + '.' + destlang),
                                                                        sourcelang, n, fps)
    else:
        dicts = dictionaries.get_dictionaries_by_lang(sourcelang)
        if dicts is None:
            print("source language doesn't match")
            exit(-1)
        else:
            dict_dest = dictionaries.getdictionarybysuffix2(destlang)
            if dict_dest is None:
                print("dest language doesn't match")
                exit(-1)
            filename, sentence_found = PoseCreator.create_pose_for_sentence_dest_lang(dicts, sentence, sourcelang,
                                                                                      dict_dest,
                                                                                      sourcelang, n, fps)
    if sentence_found is None:
        print("not successful")
    else:
        print("successful")


if __name__ == "__main__":
    main()
