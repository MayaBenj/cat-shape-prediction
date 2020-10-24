import os
import pathlib

import pandas as pd
from keras_preprocessing.image import ImageDataGenerator
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from tensorflow.keras import Input
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.layers import Flatten, Dense
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.optimizers import SGD
from tensorflow.python.keras.applications.vgg16 import preprocess_input

categories = ["cat_loaf", "cats_sitting_down", "cats_standing_up"]
size = 224, 224

df = pd.DataFrame(columns=['file', 'label'])
for category in categories:
    filenames = os.listdir(category)
    labels = [str(categories.index(category))] * len(filenames)
    path = "%s\\%s\\" % (pathlib.Path().absolute(), category)
    df = df.append(pd.DataFrame({
        'file': [path + filename for filename in filenames],
        'label': labels
    }))

# Split the data
X_train, X_test = train_test_split(df, test_size=0.2, random_state=42)

# Training generator
train_datagen = ImageDataGenerator(
    rotation_range=30,
    shear_range=0.1,
    zoom_range=0.25,
    horizontal_flip=True,
    width_shift_range=0.2,
    height_shift_range=0.2,
    preprocessing_function=preprocess_input)

train_generator = train_datagen.flow_from_dataframe(
    X_train,
    x_col='file',
    y_col='label',
    target_size=size,
    class_mode='categorical',
    batch_size=128)

validation_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
validation_generator = validation_datagen.flow_from_dataframe(
    X_test,
    x_col='file',
    y_col='label',
    target_size=size,
    class_mode='categorical',
    batch_size=128)

# callback
earlystop = EarlyStopping(patience=10)
learning_rate_reduction = ReduceLROnPlateau(monitor='val_loss',
                                            patience=2,
                                            verbose=1,
                                            factor=0.5,
                                            min_lr=0.00001)
callbacks = [earlystop, learning_rate_reduction]

# input
new_input = Input(shape=(224, 224, 3))

# model
vgg = VGG16(include_top=False, input_tensor=new_input, pooling="avg")
# Freeze all the layers
for layer in vgg.layers[:-7]:
    layer.trainable = False

# define new model
model = Sequential()
model.add(vgg)
model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(3, activation='softmax'))

# optimizer
opt = Adam(lr=0.0001)

model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=["accuracy"])

history = model.fit(
    train_generator,
    epochs=100,
    validation_data=validation_generator,
    callbacks=callbacks)

model.save("model")

# plot learning curve
pyplot.subplot(211)
pyplot.title('Cross Entropy Loss')
pyplot.plot(history.history['loss'], color='blue', label='train')
pyplot.plot(history.history['val_loss'], color='orange', label='test')
pyplot.legend(loc="best")

# plot accuracy
pyplot.subplot(212)
pyplot.title('Classification Accuracy')
pyplot.plot(history.history['accuracy'], color='blue', label='train')
pyplot.plot(history.history['val_accuracy'], color='orange', label='test')
pyplot.legend(loc="best")

pyplot.tight_layout()
# save plot
pyplot.savefig("pyplot.jpg")