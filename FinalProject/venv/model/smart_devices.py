import requests
import json
from abc import ABC, abstractmethod

def getAPITemp(zipcode):
    url = "http://api.weatherstack.com/current"
    access_key = "ea31b1e93ebfb5007496a6974d55e072" # Note: This is NOT a secure way of doing this
    query = str(zipcode)
    units = "f"
    response = requests.get(url + "?access_key=" + access_key + "&query=" + query + "&units=" + units).json()
    return response['current']['temperature']

class SmartDevice(ABC):
    def __init__(self, name, manufacturer):
        self._name = name
        self._manufacturer = manufacturer


    # Getters
    def get_name(self):
        return self._name
    
    def get_manufacturer(self):
        return self._manufacturer
    

    # Setters
    def set_name(self, name):
        self._name = name

    def set_manufacturer(self, manufacturer):
        self._manufacturer = manufacturer


    @abstractmethod
    def to_json(self):
        pass

    @abstractmethod
    def to_string(self):
        pass
      
# + Brightness
class LightBulb(SmartDevice):
    def __init__(self, name, manufacturer, brightness):
        super().__init__(name, manufacturer)
        self._brightness = int(brightness)


    # Getter
    def get_brightness(self):
        return self._brightness
    

    # Setter
    def adjust_brightness(self, brightness):
        self._brightness = float(brightness)
        print("Brightness is set to " + str(brightness))

    def to_json(self):
        dict_str = {"Type":"LightBulb", "Name":self._name, "Manufacturer":self._manufacturer, "Brightness":self._brightness}
        return json.dumps(dict_str)
    
    def to_string(self):
        return (self.get_name() + " made by " + self.get_manufacturer() + " is at " + str(self.get_brightness()) + "% brightness " + MakeBar(self.get_brightness()))


# + Brightness
# + Color
class ColorBulb(LightBulb):
    def __init__(self, name, manufacturer, brightness, color):
        super().__init__(name, manufacturer, brightness)
        self._color = color


    # Getter
    def get_color(self):
        return self._color
    

    # Setter
    def adjust_color(self, color):
        self._color = color
        print("Color is set to " + color)


    def to_json(self):
        dict_str = {"Type":"ColorBulb", "Name":self._name, "Manufacturer":self._manufacturer, "Brightness":self._brightness, "Color":self._color}
        return json.dumps(dict_str)
    
    def to_string(self):
        return (self.get_name() + " made by " + self.get_manufacturer() + " is at " + str(self.get_brightness()) + "% brightness " + MakeBar(self.get_brightness()) + " and is " + self.get_color())

# + Temperature
class Thermostat(SmartDevice):
    def __init__(self, name, manufacturer, temperature):
        super().__init__(name, manufacturer)
        self._temperature = int(temperature)


    # Getter
    def get_temperature(self):
        return self._temperature
    

    # Setter
    def adjust_temperature(self, temperature):
        self._brightness = float(temperature)
        print("Temperature is set to " + str(temperature))

    
    def to_json(self):
        dict_str = {"Type":"Thermostat", "Name":self._name, "Manufacturer":self._manufacturer, "Temperature":self._temperature}
        return json.dumps(dict_str)
    
    def to_string(self):
        return (self.get_name() + " made by " + self.get_manufacturer() + " is at " + str(self.get_temperature()) + " degrees " + MakeBar(self.get_temperature()))
    
# + Battery
# + Charging
class Vacuum(SmartDevice):
    def __init__(self, name, manufacturer, battery, charging):
        super().__init__(name, manufacturer)
        self._battery = int(battery)
        self._charging = bool(charging)


    # Getter    
    def get_battery(self):
        return self._battery
    
    def get_charging(self):
        return self._charging
    

    # Setter
    # Charges the vacuum to a certain percentage
    def charge(self, target_percent):
        if target_percent > 100:
            print("Cannot charge above 100%")
        elif self._charging == True:
            print("Vacuum is already charging...")
        else:
            self._charging = True
            self._battery = target_percent

            # Doesn't actually charge the vacuum, just simulates it
            print("Vacuum will take " + str(self._battery * 1.25) + " minutes to charge to " + str(target_percent) + "%")


    def unplug(self):
        self._charging = False
        print("Vacuum is unplugged...")
        print("Vacuum is at " + str(self._battery) + "% battery")

        if self._battery < 20:
            print("Vacuum is low on battery, charge it soon!")


    
    def to_json(self):
        dict_str = {"Type":"Vacuum", "Name":self._name, "Manufacturer":self._manufacturer, "Battery":self._battery, "Charging":self._charging}
        return json.dumps(dict_str)
    
    def to_string(self):
        return (self.get_name() + " made by " + self.get_manufacturer() + " is at " + str(self.get_battery()) + "% battery " + MakeBar(self.get_battery()))
    
# + Volume
class SmartSpeaker(SmartDevice):
    def __init__(self, name, manufacturer, volume):
        super().__init__(name, manufacturer)
        self._volume = int(volume)


    # Getter
    def get_volume(self):
        return self._volume
    

    # Setter
    def adjust_volume(self, volume):
        self._volume = float(volume)
        print("Volume is set to " + str(volume))


    def to_json(self):
        dict_str = {"Type":"SmartSpeaker", "Name":self._name, "Manufacturer":self._manufacturer, "Volume":self._volume}
        return json.dumps(dict_str)
    
    def to_string(self):
        return (self.get_name() + " made by " + self.get_manufacturer() + " is at " + str(self.get_volume()) + "% volume " + MakeBar(self.get_volume()))

# + Volume
# + Song
class Alexa(SmartSpeaker):
    def __init__(self, name, manufacturer, volume, song):
        super().__init__(name, manufacturer, volume)
        self._song = song


    # Getter
    def get_song(self):
        return self._song
    

    # Setter
    def adjust_song(self, song):
        self._song = song
        print("Song is set to " + song)


    def to_json(self):
        dict_str = {"Type":"Alexa", "Name":self._name, "Manufacturer":self._manufacturer, "Volume":self._volume, "Song":self._song}
        return json.dumps(dict_str)
    
    def to_string(self):
        return (self.get_name() + " made by " + self.get_manufacturer() + " is at " + str(self.get_volume()) + "% volume " + MakeBar(self.get_volume()) + " and is playing " + self.get_song())
# + Volume
# + Song
class GoogleHome(SmartSpeaker):
    def __init__(self, name, manufacturer, volume, song):
        super().__init__(name, manufacturer, volume)
        self._song = song


    # Getter
    def get_song(self):
        return self._song
    

    # Setter
    def adjust_song(self, song):
        self._song = song
        print("Song is set to " + song)


    def to_json(self):
        dict_str = {"Type":"GoogleHome", "Name":self._name, "Manufacturer":self._manufacturer, "Volume":self._volume, "Song":self._song}
        return json.dumps(dict_str)
    
    def to_string(self):
        return (self.get_name() + " made by " + self.get_manufacturer() + " is at " + str(self.get_volume()) + "% volume " + MakeBar(self.get_volume()) + " and is playing " + self.get_song())
    
class Home:
    # Doesnt need a constructor for smart_devices because it should start empty (as far as im aware)
    def __init__(self, street, city, state, zipcode):
        self._street = street
        self._city = city
        self._state = state
        self._zipcode = zipcode

        self._address = str(self._street) + ", " + str(self._city) + ", " + str(self._state) + ", " + str(self._zipcode)

        self._smart_devices = []

    # Getters
    def get_address(self):
        return self._address
    
    def get_smart_devices(self):
        return self._smart_devices
    

    # Setters
    def set_address(self, address):
        self._address = address

    def add_device(self, device):
        self._smart_devices.append(device)

    # Deleter
    def remove_device(self, device):
        self._smart_devices.remove(device)


    def print_devices(self):
        print("=============Devices in " + self._address + "=============\n")
        for device in self._smart_devices:
            print(device.to_string())

        
    def temperature_difference(self, thermostat):
        print("The temperature difference between the inside and outside is: " + str(thermostat._temperature - int(getAPITemp(self._zipcode))) + " degrees")
    
    

# Used to make visual percent bars
def MakeBar(percent):
        bar = "["
        if percent > 20:
            bar += "|"
        else:
            bar += " "


        if percent > 40:
            bar += "|"
        else:
            bar += " "


        if percent > 60:
            bar += "|"
        else:
            bar += " "


        if percent > 80:
            bar += "|"
        else:
            bar += " "


        if percent == 100:
            bar += "|"
        else:
            bar += " "

            
        bar += "]"
        return bar



