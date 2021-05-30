class PoseN:
    def __init__(self,pose):
        self.pose = pose
        self.default_start = 0
        self.default_end = len(self.pose.body.data)
        self.c_start = None
        self.c_end = None
    def set_c_start(self,val):
        self.c_start = val
    def set_c_end(self,val):
        self.c_end = val
