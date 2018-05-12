import re
import os
import pickle

from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import classification_report
import numpy as np

from sklearn.model_selection import train_test_split

walk_path = '/Users/victor/Desktop/8110/project_final/file_classified/walk'
other_path = '/Users/victor/Desktop/8110/project_final/file_classified/other'

joints = set(['root', 'thorax', 'head', 'rhumerus', 'rradius', 'lhumerus', 'lradius', 'rfemur', 'rtibia', 'lfemur', 'ltibia'])


low_in_frame = 0
tree_num = 0
frame_num_g = 0

def main():
    # global maxScore
    global joints1
    global joints2
    global low_in_frame

    # res = []

    cur_path = os.getcwd()
    
    walk_data, other_data = genData(joints)

    print('walk_data len:', len(walk_data))
    print('other_data len:', len(other_data))
    # X, y = mixAndShuffle(walk_data, other_data)
    X_train, y_train, X_test, y_test  = mixAndShuffle(walk_data, other_data)
    # X_train, y_train, X_test, y_test = train_test_split(X,y, test_size=0.33,random_state=42)
    score = rfClassifier(X_train, y_train)
    # rfClassifier(X_train, y_train, X_test, y_test)


    os.chdir(cur_path)

    # print('score:', score)
    # res.append(maxScore)

    # print("lower in frame:", low_in_frame)
    # return score
    return 0


def genData(joints):

    os.chdir(walk_path)
    walk_list = os.listdir('.')

    walk_data = []

    for name in walk_list:
        if len(name)>80:
            continue
        for i in range(5):
            data = genOneData(name,'walk', joints,i*5)
            # data = genOneData(name, 'walk', joints)
            if data:
                walk_data.append(data)
        # print(name)
    
    other_data = []

    os.chdir(other_path)
    other_list = os.listdir('.')
    n = len(walk_data)
    for idx, name in enumerate(other_list):
        if len(other_data) > n:
            break
        # data = genOneData(name, 'other', joints,0)
        for i in range(2):
            data = genOneData(name,'other', joints,i*5)
            if data:
                other_data.append(data)

    return walk_data, other_data

def genOneData(name, label, joints, start_frame):
    if name.split('.')[-1]!='amc':
        return

    global frame_num_g

    start_frame_idx = start_frame
    time_gap = 0.25
    frame_num = frame_num_g
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

    # print(len(data)//30)

    # for i in range(30):
    #     print(data[i])



    if (start_frame_idx+(frame_num)*gap*raw_features_num) > len(data):
        global low_in_frame
        low_in_frame += 1
        return None
    
    res = []
                
    for i in range(frame_num):
        # temp = []
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
            # print(pre_frame)

    return res


def saveFile(name, file):
    with open(name, 'wb') as f:
        pickle.dump(file, f)
        f.close()

def rfClassifier(X_train, y_train):
    global tree_num
    rf = RandomForestClassifier(n_estimators = tree_num)
    
    scores = cross_val_score(rf, X_train, y_train, cv = 10, scoring = 'accuracy')

    # print(scores.mean())

    return scores.mean()


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

    # dataset = np.asarray(dataset, dtype=np.float32)
    # labels = np.asarray(labels, dtype=int)
    length = int(len(dataset)*0.7)

    return dataset[:length], labels[:length], dataset[length:], labels[length:]

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

def rfNAnalyze():
    temp = readFile('n_in_rf_vs_acc')
    a = np.array(temp)
    # print(temp)
    # print(a[:,0])
    plt.plot(a[:,0], a[:,1])
    plt.xlabel('n_estimator')
    plt.ylabel('Accuracy')
    plt.show()

def kfAnalyze():
    temp = readFile('frames_num_vs_acc')
    a = np.array(temp)
    # print(temp)
    # print(a[:,0])
    print(a)
    plt.plot(a[:,0], a[:,1])
    plt.xlabel('Number of Keyframe')
    plt.ylabel('Accuracy')
    plt.show()

if __name__=='__main__':
    # global tree_num
    # global frame_num_g
    

    # ==========find best n_estimator=============

    # frame_num_g = 8
    # rfNumXRes = []
    # for i in range(5,200,10):
    #     tree_num = i
    #     score = main()
    #     print('rf n:',i, ' acc:', score)
    #     rfNumXRes.append([i, score])
    # saveFile('n_in_rf_vs_acc', rfNumXRes)
    
    # ===========find best keyframes number======================

    # tree_num = 100
    # frameNumXAcc = []
    # for i in range(3,20):
    #     frame_num_g = i
    #     score = main()
    #     print('frames:', i, ' filtered frames:', low_in_frame, ' acc:', score)
    #     frameNumXAcc.append([i, score, low_in_frame])
    #     low_in_frame = 0

    # saveFile('frames_num_vs_acc', frameNumXAcc)
    # print('done!')

    # main()
    
    # ===============draw results==========================
    # rfNAnalyze()
    # kfAnalyze()

    tree_num = 50
    frame_num_g = 10
    main()




