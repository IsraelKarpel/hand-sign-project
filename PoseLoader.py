# Yair
import json
from typing import List
from pose_format import Pose
from pose_format.numpy import NumPyPoseBody
import pose_format.utils.openpose as op

import Dictionary
import PoseObj


def load_pose(path, lang):
    file = open(path, 'r', encoding='utf-8')
    pose_dic = []
    if file:
        for line in file.readlines():
            pose = json.loads(line)
            if str(pose["id"]).__contains__(lang):
                pose_dic.append(pose)
        file.close()
        return pose_dic


# def find_poses(BASE_PATH, dictionary, basic_words, suffix):
#     FILES = []
#     texts = []
#     poses: List[Pose] = []
#     countwords =0
#     countnot =0
#     for word in basic_words:
#         countwords+=1
#         pose = dictionary.find_pose(word)
#         if pose:
#             poses.append(pose)
#         else:
#             countnot+=1
#     print("words total:" +str(countwords))
#     print("words not found " +str(countnot))
#     return poses


def spellWord(dictionary, word):
    word = word.upper()
    newWord = []
    for char in word:
        newWord.append('$' + char + '$')
    poses = []
    for letter in newWord:
        cur_pose = dictionary.find_pose(letter)
        if cur_pose:
            poses.append(cur_pose)
    return poses


def find_poses(BASE_PATH, dictionary, basic_words, suffix):
    sentence = " "
    sentence_found = ""
    for i in range(0, len(basic_words)):
        sentence += basic_words[i] + " "
    sentece_len = len(sentence)
    i = min(sentece_len, len(dictionary.dict_array) - 1)
    while i > 0:
        for phrase in dictionary.dict_array[i]:
            index = sentence.find(" " + phrase + " ")
            if index != -1:
                cur_pose = dictionary.find_pose(phrase)
                if cur_pose:
                    sentence = sentence.replace(phrase, phrase.replace(" ", "-"))
        i -= 1
    new_basic_words = sentence.split()
    poses: List[Pose] = []
    countwords = 0
    countnot = 0
    for word in new_basic_words:
        countwords += 1
        pose = dictionary.find_pose(word.replace("-", " "))
        if pose:
            sentence_found += word + " "
            poses.append(pose)
        else:
            if dictionary.suffix == "en.us":
                letter_pose = spellWord(dictionary, word)
                if len(letter_pose) > 0:
                    sentence_found += word + " "
                for po in letter_pose:
                    poses.append(po)
            else:
                countnot += 1
    return poses, sentence_found


def find_poses_dest_lang(BASE_PATH, dictionary, basic_words, suffix):
    sentence = " "
    sentence_found = ""
    for i in range(0, len(basic_words)):
        sentence += basic_words[i] + " "
    sentence_len = len(sentence)
    i = min(sentence_len, len(dictionary.dict_array) - 1)
    while i > 0:
        for phrase in dictionary.dict_array[i]:
            index = sentence.find(" " + phrase + " ")
            if index != -1:
                cur_pose = dictionary.find_pose(phrase)
                if cur_pose:
                    sentence = sentence.replace(phrase, phrase.replace(" ", "-"))
        i -= 1
    new_basic_words = sentence.split()
    poses: List[Pose] = []
    countwords = 0
    countnot = 0
    for word in new_basic_words:
        countwords += 1
        pose = dictionary.find_pose(word.replace("-", " "))
        if pose:
            sentence_found += word + " "
            poses.append(pose)
        else:
            if dictionary.suffix == "en.us":
                letter_pose = spellWord(dictionary, word)
                if len(letter_pose) > 0:
                    sentence_found += word + " "
                for po in letter_pose:
                    poses.append(po)
            else:
                countnot += 1
    return poses, sentence_found


# def get_unified_dictionary(dics):
#     unified_dict = Dictionary.PoseDictionary(dics[0].lang,"--",None)
#     unified_dict.
def find_poses_in_lang(BASE_PATH, dics, basic_words, suffix):
    sentence = " "
    sentence_found = ""
    for i in range(0, len(basic_words)):
        sentence += basic_words[i] + " "
    sentece_len = len(sentence)
    i = min(sentece_len, len(dics[0].dict_array) - 1)
    while i > 0:
        for phrase in dics[0].dict_array[i]:
            index = sentence.find(" " + phrase + " ")
            if index != -1:
                cur_pose = dics[0].find_pose(phrase)
                if cur_pose:
                    sentence = sentence.replace(phrase, phrase.replace(" ", "-"))
        i -= 1
    new_basic_words = sentence.split()
    poses: List[Pose] = []
    countwords = 0
    countnot = 0
    for word in new_basic_words:
        countwords += 1
        pose = dics[0].find_pose(word.replace("-", " "))
        if pose:
            sentence_found += word + " "
            poses.append(pose)
        else:
            if dics[0].suffix == "en.us":
                letter_pose = spellWord(dics[0], word)
                if len(letter_pose) > 0:
                    sentence_found += word + " "
                for po in letter_pose:
                    poses.append(po)
            else:
                countnot += 1
    return poses, sentence_found
