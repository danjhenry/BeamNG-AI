import numpy as np
from random import shuffle
from collections import Counter

files = 46

AW = [1, 0, 0, 0, 0, 0, 0, 0, 0]
DW = [0, 1, 0, 0, 0, 0, 0, 0, 0]
SW = [0, 0, 1, 0, 0, 0, 0, 0, 0]
SW = [0, 0, 0, 1, 0, 0, 0, 0, 0]
W  = [0, 0, 0, 0, 1, 0, 0, 0, 0]
A  = [0, 0, 0, 0, 0, 1, 0, 0, 0]
S  = [0, 0, 0, 0, 0, 0, 1, 0, 0]
D  = [0, 0, 0, 0, 0, 0, 0, 1, 0]
NA = [0, 0, 0, 0, 0, 0, 0, 0, 1]

left_over = list()

j = 0
for i in range(1, files+1):
    file_name = 'data/training_data-{}.npy'.format(i)
    # full file info
    train_data = np.load(file_name)
    print('training_data-{}.npy'.format(i),len(train_data))

    lefts = []
    rights = []
    forwards = []
    No_move = []
    final_data = []
    
    for data in train_data:
        img = data[0]
        choice = data[1]

        if choice == AW or choice == A:
            lefts.append([img,choice])

        elif choice == W:
            forwards.append([img,choice])
            
        elif choice == DW or choice == D:
            rights.append([img,choice])
            
        elif choice == NA:
            No_move.append([img,choice])
        
        else:
            final_data.append([img,choice])
            
    length = min(len(lefts), len(rights), len(forwards), len(No_move))
    print('min ', length)
    final_data += lefts[:length] + rights[:length] + forwards[:length] + No_move[:length] + left_over
    shuffle(final_data)

    if len(final_data) < 2000:
        left_over = final_data
        
    else:
        j += 1
        np.save('balanced_data/training_data-{}.npy'.format(j), final_data[:2000])
        left_over = final_data[2000:]

    if i == files:
        np.save('balanced_data/training_data-{}.npy'.format(j+1), final_data)
