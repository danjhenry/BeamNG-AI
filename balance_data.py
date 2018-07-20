import numpy as np
from random import shuffle
from collections import Counter

files = 22

AW = [1, 0, 0, 0, 0, 0, 0, 0]
DW = [0, 1, 0, 0, 0, 0, 0, 0]
AS = [0, 0, 1, 0, 0, 0, 0, 0]
DS = [0, 0, 0, 1, 0, 0, 0, 0]
W  = [0, 0, 0, 0, 1, 0, 0, 0]
S  = [0, 0, 0, 0, 0, 1, 0, 0]
A  = [0, 0, 0, 0, 0, 0, 1, 0]
D  = [0, 0, 0, 0, 0, 0, 0, 1]



for i in range(1, files+1):
    file_name = 'data/training_data-{}.npy'.format(i)
    # full file info
    train_data = np.load(file_name)
    print('training_data-{}.npy'.format(i),len(train_data))

    lefts = []
    rights = []
    forwards = []
    
    for data in train_data:
        img = data[0]
        choice = data[1]

        if choice == AW or choice == A:
            lefts.append([img,choice])
        elif choice == W:
            forwards.append([img,choice])
        elif choice == DW or choice == D:
            rights.append([img,choice])
        else:
            print('no matches')

    length = min(len(lefts), len(rights), len(forwards))

    final_data = lefts[:length] + rights[:length] + forwards[:length]

    shuffle(final_data)

    np.save('balance_data/training_data-{}.npy'.format(i), final_data)

    final_data = list()














            
