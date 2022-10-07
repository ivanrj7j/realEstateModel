from flask import Flask, request, render_template
import requests as x
import pickle
import numpy as np 

app = Flask(__name__)
app.debug = True


with open('model.sav', "rb") as file:
    model = pickle.load(file)

@app.route('/api', methods=['GET','POST'])
def hello_world():
    req = request.form
    return '₹'+getPrice(req)

@app.route('/')
def hi():
    
    return render_template('index.html')


def findAvgDistance(places: list) -> float:
    if len(places) == 0:
        return 0
    totalDistance = 0
    for distance in places:
        totalDistance += distance
    return totalDistance/len(places)



def getPrice(data):
    area = float(data.get('area'))
    latitude = float(data.get('latitude'))
    longitude = float(data.get('longitude'))
    age = float(data.get('age'))
    status = float(data.get('status'))

    r = x.get(f"https://www.makaan.com/apis/getAmenities?latitude={str(latitude)}&longitude={str(longitude)}&distance=5&start=0&rows=999&format=json")

    if 'school' in r.json():
        avgSchoolDistance = 1 / findAvgDistance([school['geoDistance'] for school in r.json()['school']])
    else:
        avgSchoolDistance = 0

    if 'restaurant' in r.json():
        avgRestrauntDistance = 1 / findAvgDistance([restaurant['geoDistance'] for restaurant in r.json()['restaurant']])
    else:
        avgRestrauntDistance = 0

    if 'hospital' in r.json():
         avgHospitalDistance = 1 / findAvgDistance([hospital['geoDistance'] for hospital in r.json()['hospital']])
    else:
        avgHospitalDistance = 0

    if 'atm' in r.json():
        avgATMDistance = 1 / findAvgDistance([atm['geoDistance'] for atm in r.json()['atm']])
    else:
        avgATMDistance = 0

    if 'shopping_mall' in r.json():
        avgShoppingMallDistance = 1 / findAvgDistance([shopping_mall['geoDistance'] for shopping_mall in r.json()['shopping_mall']])
    else:
        avgShoppingMallDistance = 0
        # finding the reciprocal of the average distance between the house and amneties

    data = np.array([[age,0,area,avgATMDistance,avgHospitalDistance,avgRestrauntDistance,avgSchoolDistance,avgShoppingMallDistance,status]])
    prediction = model.predict(data)
    return str(round(float(prediction[0]), 2))
    
    



if __name__ == '__main__':
   app.run(port=80)