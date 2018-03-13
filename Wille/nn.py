import numpy as np
from keras.models import Sequential
from keras.layers import Dense

# fix random seed for reproducibility
np.random.seed(7)

#---- CONSTANTS ----


interval = 6


#---- HELPER FUNCTIONS ----


def loadData():
    dataset = np.loadtxt("../finalData.csv", delimiter=",")

    # split into input (X) and output (Y) variables
    X = dataset[:,0:interval]
    Y = dataset[:,interval]
    return [X,Y]


model = Sequential()
model.add(Dense(12, input_dim=interval, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Fit the model
X = loadData()[0]
Y = loadData()[1]
model.fit(X, Y, epochs=150, batch_size=10)

# evaluate the model
scores = model.evaluate(X, Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
