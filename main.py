
import os
import spacy


import numpy as np
import numpy.ma as ma
from typing import List
from pose_format import Pose
from pose_format.numpy import NumPyPoseBody
from pose_format.pose_visualizer import PoseVisualizer

import Parser
import PoseLoader
import json
BASE_PATH = "pose_en_files/"
txt = "we study computer science"
basic_words,all_list = Parser.parse_captions1(txt)
pose_dict= PoseLoader.load_poses("index.jsonl","en.us")
poses = PoseLoader.find_poses(BASE_PATH,pose_dict,basic_words)


# Create a padding
padding = NumPyPoseBody(fps=poses[0].body.fps, data=np.zeros(shape=(10, 1, 137, 2)),
                        confidence=np.zeros(shape=(10, 1, 137)))

# Join videos with padding
pose_body_data = ma.concatenate([ma.concatenate([p.body.data, padding.data]) for p in poses])
pose_body_confidence = np.concatenate([np.concatenate([p.body.confidence, padding.confidence]) for p in poses])

# Create joint pose
new_pose_body = NumPyPoseBody(fps=poses[0].body.fps, data=pose_body_data, confidence=pose_body_confidence)
new_pose = Pose(header=poses[0].header, body=new_pose_body.interpolate(kind='linear'))
new_pose.focus()  # Focus pose to not be on 0,0

# Draw video
v = PoseVisualizer(new_pose)
v.save_video("joint.mp4", v.draw())