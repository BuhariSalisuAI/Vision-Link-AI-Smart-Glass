# button_controls.py
# Vision-Link AI Smart Glass - Physical Button Controls
# Handles button presses on the glasses frame

import RPi.GPIO as GPIO
import time
import threading
import config
from TTS import speak_hausa

class ButtonController:
    def __init__(self):
        # GPIO pin numbers for buttons (adjust based on your wiring)
        self.BUTTON_PIN = 17  # GPIO 17
        self.LED_PIN = 27     # GPIO 27 for status LED
        
        # Timing for press detection
        self.LONG_PRESS_DURATION = 2.0  # seconds
        self.DOUBLE_PRESS_INTERVAL = 0.5  # seconds
        
        self.last_press_time = 0
        self.press_count = 0
        self.is_running = False
        
        # Setup GPIO
        self._setup_gpio()
        
        # Callback function mapping
        self.actions = {
            'single_press': None,
            'double_press': None,
            'long_press': None,
            'triple_press': None,
        }
    
    def _setup_gpio(self):
        """
        Initialize GPIO pins
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.LED_PIN, GPIO.OUT)
        GPIO.output(self.LED_PIN, GPIO.LOW)
        
        # Add event detection
        GPIO.add_event_detect(
            self.BUTTON_PIN,
            GPIO.FALLING,
            callback=self._button_pressed,
            bouncetime=200
        )
    
    def _button_pressed(self, channel):
        """
        Callback when button is pressed
        """
        current_time = time.time()
        time_since_last = current_time - self.last_press_time
        
        if time_since_last < self.DOUBLE_PRESS_INTERVAL:
            self.press_count += 1
        else:
            self.press_count = 1
        
        self.last_press_time = current_time
        
        # Start timer to detect long press and determine action
        threading.Timer(self.LONG_PRESS_DURATION, self._determine_action).start()
    
    def _determine_action(self):
        """
        Determine what action to take based on press pattern
        """
        current_time = time.time()
        time_since_last = current_time - self.last_press_time
        
        # Wait a bit more for possible additional presses
        if time_since_last < self.DOUBLE_PRESS_INTERVAL and self.press_count < 3:
            return
        
        # Determine action
        action = None
        
        if self.press_count >= 3:
            action = 'triple_press'
        elif self.press_count == 2:
            action = 'double_press'
        else:
            # Check if it was a long press
            press_duration = current_time - self.last_press_time
            if press_duration >= self.LONG_PRESS_DURATION - 0.5:
                action = 'long_press'
            else:
                action = 'single_press'
        
        # Execute action
        self._execute_action(action)
        self.press_count = 0
    
    def _execute_action(self, action):
        """
        Execute the mapped action
        """
        print(f"Button action: {action}")
        
        # Flash LED to confirm
        self._flash_led()
        
        # Get action from config
        action_name = config.BUTTON_ACTIONS.get(action)
        
        if action_name and self.actions.get(action):
            speak_hausa(f"An danna button: {action_name}")
            self.actions[action]()
        else:
            speak_hausa(f"Button {action} ba a saita ba.")
    
    def _flash_led(self, duration=0.2):
        """
        Flash status LED
        """
        GPIO.output(self.LED_PIN, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(self.LED_PIN, GPIO.LOW)
    
    def register_action(self, press_type, callback_function):
        """
        Register a callback function for a button press type
        """
        if press_type in self.actions:
            self.actions[press_type] = callback_function
            print(f"Registered {press_type} action")
    
    def start_listening(self):
        """
        Start listening for button presses
        """
        self.is_running = True
        speak_hausa("Button controls shirya.")
        
        try:
            while self.is_running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """
        Stop listening and cleanup
        """
        self.is_running = False
        GPIO.cleanup()
        speak_hausa("Button controls an daina.")

def setup_buttons(single=None, double=None, long_press=None, triple=None):
    """
    Setup button controller with callbacks
    """
    controller = ButtonController()
    
    if single:
        controller.register_action('single_press', single)
    if double:
        controller.register_action('double_press', double)
    if long_press:
        controller.register_action('long_press', long_press)
    if triple:
        controller.register_action('triple_press', triple)
    
    return controller

if __name__ == "__main__":
    # Test buttons
    print("=== Testing Buttons ===")
    
    def test_single():
        print("Single press detected!")
    
    def test_double():
        print("Double press detected!")
    
    controller = setup_buttons(
        single=test_single,
        double=test_double
    )
    
    print("Press the button to test...")
    controller.start_listening()
