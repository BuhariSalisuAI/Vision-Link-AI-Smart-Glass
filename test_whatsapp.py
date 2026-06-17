# test_whatsapp.py
# Vision-Link AI Smart Glass - Test WhatsApp Integration

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.api.whatsapp_webhook import send_whatsapp_message, send_emergency_alert
from app.config import WHATSAPP_SETTINGS

def test_send_message():
    """
    Test sending a WhatsApp message
    """
    print("=== Testing WhatsApp Message ===")
    
    test_number = input("Enter test phone number (with country code, e.g., +234...): ")
    test_message = "Vision-Link AI Test Message: System is working correctly!"
    
    result = send_whatsapp_message(test_number, test_message)
    
    if result:
        print("Message sent successfully!")
    else:
        print("Failed to send message.")

def test_emergency_alert():
    """
    Test emergency alert functionality
    """
    print("\n=== Testing Emergency Alert ===")
    
    # Get location (mock if GPS not available)
    location = {
        'latitude': 12.0000,
        'longitude': 8.0000,
        'address': 'Test Location, Babura, Jigawa'
    }
    
    result = send_emergency_alert(location)
    
    if result:
        print("Emergency alert sent!")
    else:
        print("Failed to send emergency alert.")

def test_webhook():
    """
    Test webhook endpoint
    """
    print("\n=== Testing Webhook ===")
    
    from flask import Flask
    from app.api.whatsapp_webhook import app
    
    print("Starting webhook server for testing...")
    print("Send a WhatsApp message to test the webhook.")
    print("Press Ctrl+C to stop.")
    
    app.run(debug=True, port=5000)

def test_twilio_connection():
    """
    Test Twilio API connection
    """
    print("\n=== Testing Twilio Connection ===")
    
    from twilio.rest import Client
    from app.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
    
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        account = client.api.accounts(TWILIO_ACCOUNT_SID).fetch()
        
        print(f"Twilio account status: {account.status}")
        print("Connection successful!")
        return True
        
    except Exception as e:
        print(f"Twilio connection failed: {e}")
        return False

if __name__ == "__main__":
    print("Vision-Link AI - WhatsApp Tests")
    print("=" * 40)
    
    # First test connection
    if not test_twilio_connection():
        print("Please check your Twilio credentials in config.py")
        sys.exit(1)
    
    print("\n1. Send test message")
    print("2. Send emergency alert")
    print("3. Test webhook server")
    
    choice = input("Enter choice (1-3): ")
    
    if choice == '1':
        test_send_message()
    elif choice == '2':
        test_emergency_alert()
    elif choice == '3':
        test_webhook()
    else:
        print("Invalid choice")
