"""
Basic example of controlling WLED devices via DDP
"""

import time
import json
from pathlib import Path

# This is a placeholder structure - you'll implement the actual DDP classes
class DDPClient:
    """Simple DDP client for sending color data to WLED devices"""
    
    def __init__(self, host, port=4048):
        self.host = host
        self.port = port
        
    def send_solid_color(self, r, g, b, led_count):
        """Send solid color to all LEDs"""
        print(f"Sending RGB({r}, {g}, {b}) to {self.host}:{self.port} for {led_count} LEDs")
        # TODO: Implement actual DDP packet transmission
        
    def send_pixel_data(self, pixel_data):
        """Send raw pixel data"""
        print(f"Sending {len(pixel_data)} pixels to {self.host}:{self.port}")
        # TODO: Implement actual DDP packet transmission


def load_device_config():
    """Load device configuration"""
    config_path = Path(__file__).parent.parent / "config" / "devices.json"
    with open(config_path, 'r') as f:
        return json.load(f)


def main():
    """Basic control example"""
    print("WLED DDP Basic Control Example")
    print("=" * 40)
    
    # Load configuration
    config = load_device_config()
    devices = config['devices']
    
    # Initialize DDP clients for each device
    clients = []
    for device in devices:
        client = DDPClient(device['ip'], device['port'])
        clients.append((client, device))
        print(f"Connected to: {device['name']} at {device['ip']}")
    
    print("\nRunning color sequence...")
    
    # Example color sequence
    colors = [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green  
        (0, 0, 255),    # Blue
        (255, 255, 0),  # Yellow
        (255, 0, 255),  # Magenta
        (0, 255, 255),  # Cyan
        (255, 255, 255) # White
    ]
    
    for r, g, b in colors:
        print(f"Setting color: RGB({r}, {g}, {b})")
        
        # Send color to all devices
        for client, device in clients:
            client.send_solid_color(r, g, b, device['led_count'])
            
        time.sleep(2)  # Wait 2 seconds between colors
    
    print("\nTurning off all LEDs...")
    for client, device in clients:
        client.send_solid_color(0, 0, 0, device['led_count'])
    
    print("Example complete!")


if __name__ == "__main__":
    main()
