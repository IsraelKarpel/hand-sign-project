def get_distance(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)
def getSquraredDistancesSum(frame1,frame2):
    sum = 0
    distance  =0
    for i in range(0,NUMBER_OF_JOINTS):
        x1= frame1[i][0]
        y1 =frame1[i][1]
        x2 = frame2[i][0]
        y2=frame2[i][1]
        if x1 is float("nan"):
            x1= 0
        if y1 is float("nan"):
            y1= 0
        if x2 is float("nan"):
            x2= 0
        if y2 is float("nan"):
            y2= 0
        sum += get_distance(x1,y1,x2,y2)
    return sum


def get_best_connection_point(pose1,pose2):
    #rightnow it's a fixed window size but it should be dynamic and specific to the pose
    distancematrix= np.zeros(shape = (WINDOW_SIZE,WINDOW_SIZE))
    numberofpointspose1 = len(pose1.body.data)
    numberofpointspose2 = len(pose2.body.data)
    for i in range((numberofpointspose1-WINDOW_SIZE),numberofpointspose1):
        for j in range(0, WINDOW_SIZE):
            print(len(pose1.body.data[i][0]))
            print(len(pose2.body.data[j][0]))
            d = getSquraredDistancesSum(pose1.body.data[i][0], pose2.body.data[j][0])
            distancematrix[numberofpointspose1-i][j] = d


def find_connection_points_candidates(poses):
    number_of_poses  =len(poses)
    for i in range (0, number_of_poses-1):
        get_best_connection_point(poses[i],poses[i+1])
