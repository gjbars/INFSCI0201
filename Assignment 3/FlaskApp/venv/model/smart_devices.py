import json
from abc import ABC, abstractmethod

class SmartDevice:
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
        dict_str = {"Name":self._name, "Manufacturer":self._manufacturer, "Brightness":self._brightness}
        return json.dumps(dict_str)

class Home:
    # Doesnt need a constructor for smart_devices because it should start empty (as far as im aware)
    def __init__(self, address):
        self._address = address
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


    def print_devices(self):
        print("=============Devices in " + self._address + "=============\n")
        for device in self._smart_devices:
            if isinstance(device, LightBulb):
                print(device.get_name() + " made by " + device.get_manufacturer() + " is at " + str(device.get_brightness()) + "% brightness")
            else:
                print(device.get_name() + " made by " + device.get_manufacturer() + " is connected to the network")