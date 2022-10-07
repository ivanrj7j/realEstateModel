import pickle
import numpy as np

with open("model.sav", "rb") as f:
    model = pickle.load(f)

testData = np.array([[1,2500,0.38,1,0,0,0,0,0.31,0,0,0,0.67,0.9,0,0.5554100675763941,0,1,0]])
prediction = model.predict(testData)
print(prediction)