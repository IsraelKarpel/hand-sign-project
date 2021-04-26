import numpy as np
import numpy.ma as ma

from pose_format import Pose
from pose_format.numpy import NumPyPoseBody
from pose_format.pose_visualizer import PoseVisualizer
import json
import Parser
import PoseLoader
import TTMLParser
import SmoothingAlgorithm
#import SubsAnalyse


BASE_PATH = "pose_en_files/"
file_path = "News2.xml"

list =[]
subsarray,suffix,language = TTMLParser.getArrfromCaptions(file_path)
for line in subsarray:
    basic_words, all_list = Parser.parse_captions1(language,line[1])
    pose_dict = PoseLoader.load_poses("index.jsonl", suffix)
    poses = PoseLoader.find_poses(BASE_PATH, pose_dict, basic_words)
    new_pose = SmoothingAlgorithm.runSmoothingAlgorithm(poses)
    list.append(new_pose)

padding = NumPyPoseBody(fps=poses[0].body.fps, data=np.zeros(shape=(10, 1, 137, 2)),
                        confidence=np.zeros(shape=(10, 1, 137)))

# Join videos with padding
pose_body_data = ma.concatenate([ma.concatenate([p.body.data, padding.data]) for p in list])
pose_body_confidence = np.concatenate([np.concatenate([p.body.confidence, padding.confidence]) for p in list])

# Create joint pose
new_pose_body = NumPyPoseBody(fps=poses[0].body.fps, data=pose_body_data, confidence=pose_body_confidence)
new_pose = Pose(header=poses[0].header, body=new_pose_body)




# # Draw video
v = PoseVisualizer(new_pose)
v.save_video("joint.mp4", v.draw())

