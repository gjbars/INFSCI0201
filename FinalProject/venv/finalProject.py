from flask import Flask
from flask import render_template
from flask import request

import json

# Import from models folder
from model.smart_devices import Home
from model.smart_devices import SmartDevice

from model.smart_devices import LightBulb
from model.smart_devices import ColorBulb

from model.smart_devices import Thermostat
from model.smart_devices import Vacuum

from model.smart_devices import SmartSpeaker
from model.smart_devices import Alexa
from model.smart_devices import GoogleHome

app = Flask(__name__)

# Adding home object here as a global variable
House = Home("3312 Sutherland Dr", "Pittsburgh", "PA", 15213)
activitiesList = []

# Home page
@app.route("/", methods=['GET'])
def index():
    devices_list = House.get_smart_devices()

    return render_template('home.html', 
                           devices = devices_list,
                           house_obj = House)

# Adds a colored light bulb to the house
@app.route("/add-color-bulb")
def add_color_bulb():
    ColorLight = ColorBulb("Color Light", "Phillips Hue", 100, "Red")
    House.add_device(ColorLight)

    activitiesList.append("Added Color Light to home")
    return render_template('coloradd.html')

# Shows all color bulbs
@app.route("/color-list", methods=['GET'])
def color_list():
    devices_list = House.get_smart_devices()
    bulb_list = []
    for device in devices_list:
        if isinstance(device, ColorBulb):
            bulb_list.append(device)

    activitiesList.append("Viewed all color bulbs")
    return render_template('color.html', 
                           devices = bulb_list,
                           house_obj = House)

# Adds examples to the house
@app.route("/add-examples")
def add_examples():
    House.add_device(Alexa("Alexa", "Amazon", 100, "Big Difference"))
    House.add_device(GoogleHome("Google Home", "Google", 25, "Beep Beep"))
    House.add_device(Thermostat("Thermostat", "Nest", 70))

    activitiesList.append("Added examples to home")
    return render_template('add.html')

# Put request to change the volume of all smart speakers
@app.route("/change-volume", methods=['PUT'])
def change_volume():
    data = request.get_json()

    for device in House.get_smart_devices():
        if isinstance(device, SmartSpeaker):
            device.adjust_volume(data['volume'])

    activitiesList.append("Changed volume of all Smart Speakers to " + str(data['volume']) + "%")
    return("Volume changed!\n")

# Post request to add device
# Can take any device type
@app.route("/add-device", methods=['POST'])
def add_device():
    data = request.get_json()
    activitiesList.append("Added " + data['type'] + " to home")

    if data['type'] == "LightBulb":
        bulb = LightBulb(data['name'], data['manufacturer'], data['brightness'])
        House.add_device(bulb)
        return("LightBulb added!\n")
    elif data['type'] == "ColorBulb":
        bulb = ColorBulb(data['name'], data['manufacturer'], data['brightness'], data['color'])
        House.add_device(bulb)
        return("ColorBulb added!\n")
    elif data['type'] == "Thermostat":
        thermostat = Thermostat(data['name'], data['manufacturer'], data['temperature'])
        House.add_device(thermostat)
        return("Thermostat added!\n")
    elif data['type'] == "Vacuum":
        vacuum = Vacuum(data['name'], data['manufacturer'], data['battery'])
        House.add_device(vacuum)
        return("Vacuum added!\n")
    elif data['type'] == "Alexa":
        alexa = Alexa(data['name'], data['manufacturer'], data['volume'], data['song'])
        House.add_device(alexa)
        return("Alexa added!\n")
    elif data['type'] == "GoogleHome":
        google = GoogleHome(data['name'], data['manufacturer'], data['volume'], data['song'])
        House.add_device(google)
        return("Google Home added!\n")
    elif data['type'] == "SmartSpeaker":
        speaker = SmartSpeaker(data['name'], data['manufacturer'], data['volume'])
        House.add_device(speaker)
        return("Smart Speaker added!\n")
    else:
        return("Device type not found!\n")
   
    
# Delete request to remove all devices of a certain type
@app.route("/remove-device", methods=['DELETE'])
def remove_device():
    data = request.get_json()
    data_type = data['type']
    if data_type == "LightBulb":
        data_type = LightBulb
    elif data_type == "ColorBulb":
        data_type = ColorBulb
    elif data_type == "Thermostat":
        data_type = Thermostat
    elif data_type == "Vacuum":
        data_type = Vacuum
    elif data_type == "Alexa":
        data_type = Alexa
    elif data_type == "GoogleHome":
        data_type = GoogleHome
    elif data_type == "SmartSpeaker":
        data_type = SmartSpeaker

    for device in House.get_smart_devices():
        if isinstance(device, data_type):
            House.remove_device(device)

    activitiesList.append("Removed all " + data['type'] + "s from home")

    return("Devices removed!\n")

@app.route("/remove-all")
def remove_all():
    House._smart_devices = []
    activitiesList.append("Removed all devices from home")

    return render_template('remove.html')

@app.route("/activities")
def activities():
    return render_template('activities.html',
                           house_obj = House,
                           activities = activitiesList)

@app.route("/save")
def save():
    devices = House.get_smart_devices()
    newFile = open("house.json", "w")
    json.dump([device.to_json() for device in devices], newFile)

    activitiesList.append("Saved home to house.json")
    return render_template('save.html')

@app.route("/load")
def load():
    with open("house.json", 'r') as newFile:
        data = json.load(newFile)
        devices = [json.loads(device) for device in data]

    for device in devices:
        if device['Type'] == "LightBulb":
            House.add_device(LightBulb(device['Name'], device['Manufacturer'], device['Brightness']))
        elif device['Type'] == "ColorBulb":
            House.add_device(ColorBulb(device['Name'], device['Manufacturer'], device['Brightness'], device['Color']))
        elif device['Type'] == "Thermostat":
            House.add_device(Thermostat(device['Name'], device['Manufacturer'], device['Temperature']))
        elif device['Type'] == "Vacuum":
            House.add_device(Vacuum(device['Name'], device['Manufacturer'], device['Battery']))
        elif device['Type'] == "Alexa":
            House.add_device(Alexa(device['Name'], device['Manufacturer'], device['Volume'], device['Song']))
        elif device['Type'] == "GoogleHome":
            House.add_device(GoogleHome(device['Name'], device['Manufacturer'], device['Volume'], device['Song']))
        elif device['Type'] == "SmartSpeaker":
            House.add_device(SmartSpeaker(device['Name'], device['Manufacturer'], device['Volume']))
        else:
            return("Device type not found!\n")

    activitiesList.append("Loaded home from house.json")
    return render_template('load.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)