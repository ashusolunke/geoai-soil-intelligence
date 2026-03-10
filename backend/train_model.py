import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

data = ImageDataGenerator(rescale=1./255)

train = data.flow_from_directory(
    "dataset",
    target_size=(128,128),
    batch_size=32,
    class_mode='categorical'
)

model = Sequential([
tf.keras.layers.Input(shape=(128,128,3)),

Conv2D(32,(3,3),activation='relu'),
MaxPooling2D(),

Conv2D(64,(3,3),activation='relu'),
MaxPooling2D(),

Flatten(),

Dense(128,activation='relu'),

Dense(7,activation='softmax')   # ← IMPORTANT FIX
])

model.compile(
optimizer='adam',
loss='categorical_crossentropy',
metrics=['accuracy']
)

model.fit(train,epochs=10)

model.save("backend/model.h5")