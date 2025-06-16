import keras
from keras import datasets, layers, models

data_dir = "./images/"

dataset = data_dir

classes = ["bolsonaro", "lula", "marcos"]
print(f"classes {classes}")

model = models.Sequential()
model.add(layers.Conv2D(32, (3,3), activation="relu", input_shape=(32, 32, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))

model.compile(optimizer='adam',
              loss = keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              )

history = model.fit(dataset, classes, epochs=10)