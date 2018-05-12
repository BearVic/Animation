import re
import os
import pickle
# import math

walk_path = '/Users/victor/Desktop/8110/project_final/file_classified/walk'
other_path = '/Users/victor/Desktop/8110/project_final/file_classified/other'

joints = [
'root',
'lowerback',
'upperback',
'thorax',
'lowerneck',
'upperneck',
'head',
'rclavicle',
'rhumerus',
'rradius',
'rwrist',
'rhand',
'rfingers',
'rthumb',
'lclavicle',
'lhumerus',
'lradius',
'lwrist',
'lhand',
'lfingers',
'lthumb',
'rfemur',
'rtibia',
'rfoot',
'rtoes',
'lfemur',
'ltibia',
'lfoot',
'ltoes']

low_in_frame = 0
# joints = set(['root', 'thorax', 'head', 'rhumerus', 'rradius', 'lhumerus', 'lradius', 'rfemur', 'rtibia', 'lfemur', 'ltibia'])


from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import cross_val_score
import numpy as np

def rfClassifier(X_train, y_train):
    rf = RandomForestClassifier(n_estimators = 100)
    
    scores = cross_val_score(rf, X_train, y_train, cv = 10, scoring = 'accuracy')

    # print(scores.mean())

    return scores.mean()
    # rf.fit(X_train, y_train)

    # y_predict = rf.predict(X_test)

    # print("Accuracy of random forests:", rf.score(X_test, y_test))

def mixAndShuffle(walk, other):
    # walk = np.asarray(walk, dtype=np.float32)
    # other = np.asarray(other, dtype=np.float32)

    dataset = walk + other

    label_pos = [1 for _ in range(len(walk))]
    label_neg = [0 for _ in range(len(other))]

    labels = label_pos + label_neg

    index = [i for i in range(len(dataset))]
    np.random.shuffle(index)

    dataset = [dataset[i] for i in index]
    labels = [labels[i] for i in index]

    dataset = np.asarray(dataset, dtype=np.float32)
    labels = np.asarray(labels, dtype=int)

    return dataset, labels

def main():

    global joints
    global lowthan280

    res = []

    cur_path = os.getcwd()

    i = 0
    while i < len(joints):
        temp = joints[i]
        flag, s1, s2 = isDelete(i)
        if not flag:
            i += 1
        else:
            res.append([temp, s1, s2])

    # print("lower in frame:", low_in_frame)
    os.chdir(cur_path)

    for w in res:
        print(w)

    return res


def saveFile(name, file):
    with open(name, 'wb') as f:
        pickle.dump(file, f)
        f.close()


def isDelete(i):

    global joints
    jointcopy = joints[:]
    del jointcopy[i]

    not_delete_score = getScoreByJoints(joints)
    after_delete_score = getScoreByJoints(jointcopy)

    print('feature #', i,' ',joints[i],' s1:', not_delete_score, ' s2:',after_delete_score)

    if after_delete_score>not_delete_score or abs(after_delete_score- not_delete_score)<0.001:
        print(joints[i], ' not very well, deleting...')
        del joints[i]
        return True, not_delete_score, after_delete_score 
    else:
        return False, None, None


def genData(joints):

    os.chdir(walk_path)
    walk_list = os.listdir('.')

    walk_data = []

    for name in walk_list:
        if len(name)>80:
            continue

        data = genOneData(name, 'walk', joints)
        if data:
            walk_data.append(data)
        # print(name)
    
    other_data = []

    os.chdir(other_path)
    other_list = os.listdir('.')
    n = len(walk_data)
    for idx, name in enumerate(other_list):
        if idx > n:
            break
        data = genOneData(name, 'other', joints)
        if data:
            other_data.append(data)

    return walk_data, other_data

def getScoreByJoints(joints):
    walk_data, other_data = genData(joints)
    X, y = mixAndShuffle(walk_data, other_data)
    score = rfClassifier(X, y)
    return score

def genOneData(name, label, joints):

    start_frame_idx = 0
    time_gap = 0.25
    frame_num = 12
    frame = int(name.split('#')[1])
    gap = int(frame*time_gap)

    raw_features_num = 30
    
    src_file = open(name, 'r')
    raws = src_file.read().strip()
    src_file.close()

    data = raws.split('\n')
    # delete the header(file decription) & last line(empty)
    del data[0]
    del data[0]
    del data[0]
    del data[-1]

    if (start_frame_idx+(frame_num)*gap*raw_features_num) > len(data):
        global low_in_frame
        low_in_frame += 1
        return None
    
    res = []
                
    for i in range(frame_num):
        for j in range((i*gap+start_frame_idx)*raw_features_num,(i*gap+start_frame_idx+1)*raw_features_num):
            if j==0:
                continue
            line = data[j]
            line = line.split()
            if line[0] not in joints:
                continue
            # skip the first name element
            for c in line[1:]:
                res.append(float(c))

    return res


def analyzeData(datas):
    total_len = []
    larger80 = []
    for data in datas:
        total_len.append(len(data))
        if len(data)>80:
            larger80.append(data)
            print(data)



    print(total_len[::50])
    print("avg:",sum(total_len)/len(total_len))
    print("max:",max(total_len))
    print("min:",min(total_len))

    # len(name) > 80 output:
    # 86_05$5#120#walking, jumping, jumping jacks,  jumping on one foot, punching, chopping,<TD><TD>.amc
    # 86_07$7#120#walking, swinging arms, stretching, jumping on one leg, and jumping<TD><TD>.amc
    # 19_07$7#120#navigate busy sidewalk; A leads the way, takes B by the arm (2 subjects - subject B).amc
    # 56_05$5#120#vignettes - walk, drink water, runjog, jump, wipe window, lift open window, throw punches, yawn, stretch.amc
    # 56_06$6#120#vignettes - throw punches, grab, skip, yawn, stretch, leap, lift open window, walk, jumpbound.amc
    # 15_12$12#120#wash windows; basketball - dribble, lay-up shot, pass; throw ball; dance - Egyptian walk, the Dive, the Twist; strew.amc
    # 18_09$9#120#conversation - explain with hand gestures, walk (2 subjects - subject A).amc
    # 56_08$8#120#vignettes - lift open window, smash against wall, hop, walk, runjog, yawn, stretch.amc
    # 18_07$7#120#navigate busy sidewalk; A leads the way, takes B by the arm (2 subjects - subject A).amc
    # 19_09$9#120#conversation - explain with hand gestures, walk (2 subjects - subject B).amc
    # 86_06$6#120#walking, running, kicking, punching, knee kicking, and stretching<TD><TD>.amc
    # 56_04$4#120#vignettes - fists up, wipe window, grab, lift open window, throw punches, yawn, stretch, walk, jump.amc
    # 86_12$12#120#walking, dragging, sweeping, dustpan, wipe window, and wipe mirror<TD><TD>.amc
    # 15_05$5#120#wash windows, paint; hand signals; dance - Egyptian walk, the Dive, the Twist, the Cabbage Patch; boxing.amc
    # 15_04$4#120#wash windows, paint; hand signals; dance - Egyptian walk, the Dive, the Twist, the Cabbage Patch; boxing.amc
    # 56_07$7#120#vignettes - yawn, stretch, walk, runjog, angrily grab, jump, skip, halt.amc

    # [39, 20, 30, 50, 31, 98, 20, 46, 34, 36, 87]
    # avg: 39.641263940520446
    # max: 133
    # min: 20

def readFile(name):
    with open(name, 'rb') as f:
        file = pickle.load(f)
        f.close()
        return file

def resAnalysis():
    res = []
    for i in range(5):
        temp = readFile('del_feature_no'+str(i))
        res.append(np.array(temp))

    record = []
    for name in joints:
      count = 0
      for i in range(5):
          if name in res[i][:,0]:
              count += 1
      record.append([name, count])

    record = np.array(record)
    print(record)



if __name__=='__main__':

    # for i in range(5):
    #     res = main()
    #     saveFile('del_feature_no'+str(i), res)
    resAnalysis()
    

