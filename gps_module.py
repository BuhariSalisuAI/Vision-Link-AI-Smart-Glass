# gps_module.py
# Vision-Link AI Smart Glass - GPS Hardware Module
# Reads location from GPS module

import serial
import time
import config

class GPSModule:
    def __init__(self):
        self.port = config.GPS_SETTINGS['port']
        self.baudrate = config.GPS_SETTINGS['baudrate']
        self.timeout = config.GPS_SETTINGS['timeout']
        self.serial_conn = None
        
    def connect(self):
        """
        Connect to GPS module
        """
        try:
            self.serial_conn = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            print(f"GPS connected on {self.port}")
            return True
        except Exception as e:
            print(f"GPS connection error: {e}")
            return False
    
    def read_raw_data(self):
        """
        Read raw NMEA data from GPS
        Returns: str (NMEA sentence)
        """
        if self.serial_conn is None:
            return None
            
        try:
            line = self.serial_conn.readline().decode('ascii', errors='replace').strip()
            return line
        except Exception as e:
            print(f"Error reading GPS: {e}")
            return None
    
    def parse_gps_data(self, nmea_line):
        """
        Parse NMEA sentence to get coordinates
        Returns: dict with lat, lon, altitude, time
        """
        if not nmea_line or not nmea_line.startswith('$'):
            return None
        
        parts = nmea_line.split(',')
        
        if parts[0] == '$GPGGA' and len(parts) > 9:
            # GPGGA format
            time_str = parts[1]
            lat = self._convert_coordinate(parts[2], parts[3])
            lon = self._convert_coordinate(parts[4], parts[5])
            altitude = parts[9] if parts[9] else '0'
            
            return {
                'latitude': lat,
                'longitude': lon,
                'altitude': float(altitude) if altitude else 0,
                'time': time_str
            }
        
        elif parts[0] == '$GPRMC' and len(parts) > 8:
            # GPRMC format
            time_str = parts[1]
            lat = self._convert_coordinate(parts[3], parts[4])
            lon = self._convert_coordinate(parts[5], parts[6])
            
            return {
                'latitude': lat,
                'longitude': lon,
                'time': time_str
            }
        
        return None
    
    def _convert_coordinate(self, value, direction):
        """
        Convert NMEA coordinate to decimal degrees
        """
        if not value or not direction:
            return 0.0
        
        try:
            # Determine degrees length based on direction
            if direction in ['N', 'S']:
                degrees = float(value[:2])
                minutes = float(value[2:])
            else:
                degrees = float(value[:3])
                minutes = float(value[3:])
            
            decimal = degrees + (minutes / 60.0)
            
            if direction in ['S', 'W']:
                decimal = -decimal
            
            return round(decimal, 6)
            
        except:
            return 0.0
    
    def get_location(self, max_attempts=10):
        """
        Get current GPS location
        Tries multiple times to get a valid fix
        """
        if not self.serial_conn:
            if not self.connect():
                return None
        
        for _ in range(max_attempts):
            nmea = self.read_raw_data()
            location = self.parse_gps_data(nmea)
            
            if location and location['latitude'] != 0.0:
                return location
            
            time.sleep(0.5)
        
        print("Could not get GPS fix")
        return None
    
    def disconnect(self):
        """
        Close GPS connection
        """
        if self.serial_conn:
            self.serial_conn.close()
            self.serial_conn = None
            print("GPS disconnected")

def get_current_gps_location():
    """
    Main function to get GPS location
    """
    gps = GPSModule()
    location = gps.get_location()
    gps.disconnect()
    return location

if __name__ == "__main__":
    # Test GPS
    print("=== Testing GPS ===")
    loc = get_current_gps_location()
    if loc:
        print(f"Location: {loc}")
    else:
        print("No GPS signal available")
