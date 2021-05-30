class PoseObj:
    def __init__(self, pose, id, text):
        self.id = id
        self.word = text
        self.pose= pose
        self.length = len(pose.body.data)
        self.start = None
        self.end = None

    def is_end_calculated(self):
        if self.end is None:
            return False

    def is_start_calculated(self):
        if self.start is None:
            return False

    def set_start(self, value):
        self.start=value

    def set_end(self, value):
        self.end = value

    @staticmethod
    def find_end(wristarr, elbowarr):
        lenarr = len(elbowarr)
        endindex = 0
        above = False  # in the start the wrists are below the elbows
        for i in range(0, lenarr):
            if wristarr[i] >= elbowarr[i] and above == True:
                rendindex = i
                above = False
            elif wristarr[i] < elbowarr[i]:
                above = True
        return endindex

    @staticmethod
    def find_start(wristarr, elbowarr):
        lenarr = len(elbowarr)
        startindex = 0
        above = False  # in the start the wrists are below the elbows
        for i in range(0, lenarr):
            if wristarr[i] <= elbowarr[i] and above == False:
                startindex = i
                above = True
        return startindex

    def find_points(self,rWristarr, rElbowarr, lWristarr, lElbowarr):
        lenarr = len(rElbowarr)
        rend = self.find_end(rWristarr, rElbowarr)
        lend = self.find_end(lWristarr, lElbowarr)
        rstart = self.find_start(rWristarr, rElbowarr)
        lstart = self.find_start(lWristarr, lElbowarr)
        startpoint = 0
        endpoint = max(rend, lend)
        if endpoint == 0:
            endpoint = lenarr - 15
        startpoint = check_start(rstart, lstart)
        #print("num points: " + str(lenarr) + " start: " + str(startpoint) + " end: " + str(endpoint))
        return startpoint, endpoint

    def find_start_end_points(self):
        rWristYpoints = []
        lWristYpoints = []
        rElbowYpoints = []
        lElbowYpoints = []
        number_of_points = len(self.pose.body.data)
        for i in range(0, number_of_points):
            rWristYpoints.append(self.pose.body.data[i][0][4][1])
            lWristYpoints.append(self.pose.body.data[i][0][7][1])
            rElbowYpoints.append(self.pose.body.data[i][0][3][1])
            lElbowYpoints.append(self.pose.body.data[i][0][6][1])
        st, en = self.find_points(rWristYpoints, rElbowYpoints, lWristYpoints, lElbowYpoints)
        self.set_start(st)
        self.set_end(en)


def check_start(rstart, lstart):
    if rstart == 0 and lstart != 0:
        startpoint = lstart
    elif lstart == 0 and rstart != 0:
        startpoint = rstart
    else:
        startpoint = min(rstart, lstart)
    return startpoint
























