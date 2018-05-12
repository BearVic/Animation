import re
import pickle
import os

from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import cross_val_score
import numpy as np
import matplotlib.pyplot as plt

walk_path = '/Users/victor/Desktop/8110/project_final/file_classified/walk'
other_path = '/Users/victor/Desktop/8110/project_final/file_classified/other'

joints = set(['root', 'thorax', 'head', 'rhumerus', 'rradius', 'lhumerus', 'lradius', 'rfemur', 'rtibia', 'lfemur', 'ltibia'])


def rfClassifier(X_train, y_train):
    rf = RandomForestClassifier(n_estimators = 50)
    
    scores = cross_val_score(rf, X_train, y_train, cv = 5, scoring = 'accuracy')

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

    dataset = np.asarray(dataset, dtype=np.float32)
    labels = np.asarray(labels, dtype=int)

    return dataset, labels

def main():

    # global maxScore
    global joints

    # res = []

    cur_path = os.getcwd()

    walk_data1, other_data1 = genData1(joints)
    print('walk_data len:', len(walk_data1))
    print('other_data len:', len(other_data1))
    # X, y = mixAndShuffle(walk_data, other_data)
    X1, y1 = mixAndShuffle(walk_data1, other_data1)

    walk_data2, other_data2 = genData2(joints)
    print('walk_data len:', len(walk_data2))
    print('other_data len:', len(other_data2))
    # X, y = mixAndShuffle(walk_data, other_data)
    X2, y2 = mixAndShuffle(walk_data2, other_data2)

    walk_data3, other_data3 = genData3(joints)
    print('walk_data len:', len(walk_data3))
    print('other_data len:', len(other_data3))
    # X, y = mixAndShuffle(walk_data, other_data)
    X3, y3 = mixAndShuffle(walk_data3, other_data3)
    
    os.chdir(cur_path)
    res = []

    for i in range(20):
        num = 500 + i*100
        acc1 = rfClassifier(X1[:num], y1[:num])
        acc2 = rfClassifier(X2[:num], y2[:num])
        acc3 = rfClassifier(X3[:num], y3[:num])
        print(num,' ', acc1, ' ', acc2, ' ', acc3)
        res.append([num, acc1, acc2, acc3])
    

    saveFile('phases_3_comparison', res)
    # print('score:', score)
    # res.append(maxScore)


def saveFile(name, file):
    with open(name, 'wb') as f:
        pickle.dump(file, f)
        f.close()

def genData1(joints):

    os.chdir(walk_path)
    walk_list = os.listdir('.')

    walk_data = []

    for name in walk_list:
        if len(name)>80:
            continue

        for i in range(5):
            data = genOneData1(name,'walk', joints,i*5)
            # data = genOneData(name, 'walk', joints)
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
        for i in range(2):
            data = genOneData1(name,'other', joints,i*5)
            if data:
                other_data.append(data)

    return walk_data, other_data


def genData2(joints):

    os.chdir(walk_path)
    walk_list = os.listdir('.')

    walk_data = []

    for name in walk_list:
        if len(name)>80:
            continue

        for i in range(5):
            data = genOneData2(name,'walk', joints,i*5)
            # data = genOneData(name, 'walk', joints)
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
        for i in range(2):
            data = genOneData2(name,'other', joints,i*5)
            if data:
                other_data.append(data)

    return walk_data, other_data

def genData3(joints):

    os.chdir(walk_path)
    walk_list = os.listdir('.')

    walk_data = []

    for name in walk_list:
        if len(name)>80:
            continue

        for i in range(5):
            data = genOneData3(name,'walk', joints,i*5)
            # data = genOneData(name, 'walk', joints)
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
        for i in range(2):
            data = genOneData3(name,'other', joints,i*5)
            if data:
                other_data.append(data)

    return walk_data, other_data

def genOneData1(name, label, joints, start_frame):
    if name.split('.')[-1]!='amc':
        return

    start_frame_idx = start_frame
    time_gap = 0.25
    frame_num = 10
    frame = int(name.split('#')[1])

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
    
    if len(data)<301:
        return None

    gap = len(data)//raw_features_num//(frame_num+3)


    if (start_frame_idx+(frame_num)*gap*raw_features_num) > len(data):
        return None
    # print(len(data))
    # print(gap)
    
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


def genOneData2(name, label, joints, start_frame):
    if name.split('.')[-1]!='amc':
        return


    start_frame_idx = start_frame
    time_gap = 0.25
    frame_num = 10
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

def genOneData3(name, label, joints, start_frame):
    if name.split('.')[-1]!='amc':
        return

    start_frame_idx = start_frame
    time_gap = 0.25
    frame_num = 10
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
        return None
    
    pre_frame = []
    res = []

    for k in range(start_frame_idx*raw_features_num, (start_frame_idx+1)*raw_features_num):
        if k == 0:
            continue
        line = data[k]
        line = line.split()
        if line[0] not in joints:
            continue
        # skip the first name element
        for c in line[1:]:
            res.append(float(c))
            pre_frame.append(float(c))
                
    for i in range(1, frame_num):
        count = 0
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
                temp = float(c)
                res.append(temp-pre_frame[count])
                pre_frame[count] = temp
                count += 1
            # print(pre_frame)

    return res

def readFile(name):
    with open(name, 'rb') as f:
        file = pickle.load(f)
        f.close()
        return file


def resultAnalyze():
    temp = readFile('phases_3_comparison')
    a = np.array(temp)
    # print(temp)
    # print(a[:,0])
    print(a)
    plt.plot(a[:,0], a[:,1], 'r', label='type 1')
    plt.plot(a[:,0], a[:,2], 'g', label='type 2')
    plt.plot(a[:,0], a[:,3], 'b', label='type 3')
    plt.legend()
    plt.xlabel('Number of Train Dataset')
    plt.ylabel('Accuracy')
    plt.show()


if __name__=='__main__':

    resultAnalyze()

    # main()


