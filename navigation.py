# navigation.py
# Vision-Link AI Smart Glass - GPS Navigation Module
# Provides voice-guided navigation in Hausa

import serial
import requests
import math
import time
import config
from TTS import speak_hausa

class NavigationSystem:
    def __init__(self):
        self.gps_port = config.GPS_SETTINGS['port']
        self.baudrate = config.GPS_SETTINGS['baudrate']
        self.api_key = config.GOOGLE_MAPS_API_KEY
        self.current_location = None
        self.destination = None
        
    def get_gps_location(self):
        """
        Read GPS coordinates from GPS module
        Returns: dict with 'latitude' and 'longitude'
        """
        try:
            with serial.Serial(self.gps_port, self.baudrate, timeout=1) as ser:
                # Read NMEA sentences
                line = ser.readline().decode('ascii', errors='replace')
                
                if line.startswith('$GPGGA') or line.startswith('$GPRMC'):
                    # Parse GPS data
                    parts = line.split(',')
                    
                    if len(parts) > 5 and parts[2] and parts[4]:
                        # Convert NMEA format to decimal degrees
                        lat = self._nmea_to_decimal(parts[2], parts[3])
                        lon = self._nmea_to_decimal(parts[4], parts[5])
                        
                        location = {
                            'latitude': lat,
                            'longitude': lon
                        }
                        self.current_location = location
                        return location
            
            return self.current_location
            
        except Exception as e:
            print(f"GPS Error: {e}")
            speak_hausa("Akwai matsala da GPS. Sake gwadawa.")
            return None
    
    def _nmea_to_decimal(self, value, direction):
        """
        Convert NMEA coordinate format to decimal degrees
        """
        if not value or not direction:
            return 0.0
            
        degrees = float(value[:2]) if direction in ['N', 'S'] else float(value[:3])
        minutes = float(value[2:]) if direction in ['N', 'S'] else float(value[3:])
        decimal = degrees + (minutes / 60.0)
        
        if direction in ['S', 'W']:
            decimal = -decimal
            
        return decimal
    
    def get_directions(self, destination_address):
        """
        Get directions from current location to destination
        Args:
            destination_address: str (e.g., "Babura Market, Jigawa")
        Returns: list of direction steps
        """
        if not self.current_location:
            self.get_gps_location()
        
        if not self.current_location:
            speak_hausa("Ba na iya samun wurin ku. Sake gwadawa.")
            return None
        
        # Build Google Maps API URL
        origin = f"{self.current_location['latitude']},{self.current_location['longitude']}"
        url = f"https://maps.googleapis.com/maps/api/directions/json"
        
        params = {
            'origin': origin,
            'destination': destination_address,
            'mode': 'walking',
            'language': 'ha',  # Hausa directions
            'key': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if data['status'] == 'OK':
                route = data['routes'][0]['legs'][0]
                steps = route['steps']
                
                # Convert steps to Hausa voice instructions
                hausa_steps = []
                for step in steps:
                    instruction = step['html_instructions']
                    distance = step['distance']['text']
                    
                    # Simplify and translate to Hausa
                    hausa_instruction = self._translate_to_hausa(instruction, distance)
                    hausa_steps.append(hausa_instruction)
                
                self.destination = destination_address
                return hausa_steps
            else:
                speak_hausa("Ba na iya samun hanya. Sake gwadawa.")
                return None
                
        except Exception as e:
            print(f"Navigation Error: {e}")
            speak_hausa("Akwai matsala da intanet.")
            return None
    
    def _translate_to_hausa(self, instruction, distance):
        """
        Simplify English directions to Hausa
        """
        instruction = instruction.lower()
        
        # Simple translations
        if 'turn left' in instruction:
            return f"Koma hagu. Tafi {distance}."
        elif 'turn right' in instruction:
            return f"Koma dama. Tafi {distance}."
        elif 'straight' in instruction or 'continue' in instruction:
            return f"Tafi kai tsaye. Tafi {distance}."
        elif 'destination' in instruction:
            return f"Kun isa wurin ku. Sannu."
        else:
            return f"Tafi {distance}."
    
    def announce_current_location(self):
        """
        Announce current GPS coordinates
        """
        location = self.get_gps_location()
        if location:
            lat = round(location['latitude'], 4)
            lon = round(location['longitude'], 4)
            speak_hausa(f"Wurin ku: Latitude {lat}, Longitude {lon}")
            return location
        return None
    
    def start_navigation(self, destination):
        """
        Start turn-by-turn navigation
        """
        speak_hausa(f"Na shirya hanya zuwa {destination}")
        
        directions = self.get_directions(destination)
        
        if directions:
            speak_hausa(f"Hanya tana da mataki {len(directions)}.")
            
            for i, step in enumerate(directions):
                speak_hausa(f"Mataki {i+1}: {step}")
                time.sleep(5)  # Wait between instructions
            
            speak_hausa("Kun isa wurin ku. Barka da waraka!")
            return True
        
        return False

def get_current_location():
    """
    Main function to get current GPS location
    """
    nav = NavigationSystem()
    return nav.announce_current_location()

def navigate_to(destination):
    """
    Main function to navigate to a destination
    """
    nav = NavigationSystem()
    return nav.start_navigation(destination)

if __name__ == "__main__":
    # Test navigation
    print("=== Testing Navigation ===")
    get_current_location()
    # navigate_to("Babura Market, Jigawa, Nigeria")
