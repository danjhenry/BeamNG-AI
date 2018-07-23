import numpy as np
import time
import os
from Inception_net import inception_v3 as googlenet
from random import shuffle

# last data file
FILE_I_END = 19

WIDTH = 200
HEIGHT = 150
LR = 0.001
EPOCHS = 9

MODEL_NAME = 'BeamNG_1.0'
PREV_MODEL = 'BeamNG_1.0'

LOAD_MODEL = False

model = googlenet(WIDTH, HEIGHT, 3, LR, output=9, model_name=MODEL_NAME)

if LOAD_MODEL:
    model.load('model/{}'.format(PREV_MODEL))
    print('We have loaded a previous model!!!!')

for e in range(EPOCHS):
    data_order = [i for i in range(1,FILE_I_END+1)]
    shuffle(data_order)
    for count,i in enumerate(data_order):
        
        try:
            file_name = 'balanced_data/training_data-{}.npy'.format(i)
            # full file info
            train_data = np.load(file_name)
            print('training_data-{}.npy'.format(i),len(train_data))
<<<<<<< HEAD

            testlen = int(len(train_data) * 0.1)

            train = train_data[:-testlen]
            test = train_data[-testlen:]
=======
            
            train = train_data[:-200]
            test = train_data[-200:]
>>>>>>> f8a82f2f91b94e97652126f5927a8f513249a479

            X = np.array([i[0] for i in train]).reshape(-1,WIDTH,HEIGHT,3)
            Y = [i[1] for i in train]

            test_x = np.array([i[0] for i in test]).reshape(-1,WIDTH,HEIGHT,3)
            test_y = [i[1] for i in test]
            # batch_size=128,
            model.fit({'input': X}, {'targets': Y}, n_epoch=1, validation_set=({'input': test_x}, {'targets': test_y}), 
                snapshot_step=2000, show_metric=True, run_id=MODEL_NAME)

            if True: #count%10 == 0:
                print('SAVING MODEL!')
                model.save('model/{}'.format(MODEL_NAME))
                    
        except Exception as e:
            print(str(e))
            
