from flask import Flask
from flask import render_template
from flask import request

import json

# Import from models folder
from model.smart_devices import Home
from model.smart_devices import SmartDevice
from model.smart_devices import LightBulb



app = Flask(__name__)

# Adding home object here as a global variable
# This is so its able to be used in the post request
House = Home("9912 Home Lane")


@app.route("/", methods=['GET'])
def index():
    Light = LightBulb("Smart Light", "Phillips Hue", 50)
    House.add_device(Light)

    devices_list = House.get_smart_devices()

    return render_template('home.html', 
                           devices = devices_list,
                           house_obj = House)

@app.route("/add-bulb", methods=['POST'])
def add_lightbulb():
    data = request.get_json()

    bulb = LightBulb(data['name'], data['manufacturer'], data['brightness'])
    House.add_device(bulb)

    newFile = open("light.json", "w")
    newFile.write(json.dumps(bulb.to_json()))

    return("LightBulb added to light.json!\n")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)