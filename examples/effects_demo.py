"""
Example demonstrating various lighting effects for WLED devices
"""

import time
import math
import json
from pathlib import Path


class EffectGenerator:
    """Generate various lighting effects"""
    
    @staticmethod
    def rainbow_cycle(position, total_leds, cycle_offset=0):
        """Generate rainbow colors"""
        hue = ((position / total_leds) + cycle_offset) % 1.0
        return EffectGenerator.hsv_to_rgb(hue, 1.0, 1.0)
    
    @staticmethod
    def fire_effect(position, total_leds, heat_map):
        """Generate fire effect colors"""
        # Simplified fire effect
        heat = heat_map.get(position, 0)
        if heat < 85:
            return (heat * 3, 0, 0)
        elif heat < 170:
            return (255, (heat - 85) * 3, 0)
        else:
            return (255, 255, (heat - 170) * 3)
    
    @staticmethod
    def hsv_to_rgb(h, s, v):
        """Convert HSV color to RGB"""
        import colorsys
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return (int(r * 255), int(g * 255), int(b * 255))
    
    @staticmethod
    def breathing_effect(time_ms, color, min_brightness=0.1, max_brightness=1.0):
        """Generate breathing effect"""
        # Sine wave for smooth breathing
        breath_factor = (math.sin(time_ms / 1000.0) + 1) / 2
        brightness = min_brightness + (max_brightness - min_brightness) * breath_factor
        
        return (
            int(color[0] * brightness),
            int(color[1] * brightness), 
            int(color[2] * brightness)
        )


def run_rainbow_demo(clients_and_devices, duration=10):
    """Demonstrate rainbow cycle effect"""
    print("Running Rainbow Effect...")
    
    start_time = time.time()
    cycle_offset = 0
    
    while time.time() - start_time < duration:
        for client, device in clients_and_devices:
            led_count = device['led_count']
            pixel_data = []
            
            for i in range(led_count):
                r, g, b = EffectGenerator.rainbow_cycle(i, led_count, cycle_offset)
                pixel_data.append((r, g, b))
            
            client.send_pixel_data(pixel_data)
        
        cycle_offset += 0.02  # Speed of rainbow movement
        time.sleep(0.05)  # 20 FPS


def run_breathing_demo(clients_and_devices, duration=10):
    """Demonstrate breathing effect"""
    print("Running Breathing Effect...")
    
    start_time = time.time()
    base_color = (255, 100, 50)  # Warm orange
    
    while time.time() - start_time < duration:
        current_time_ms = (time.time() - start_time) * 1000
        r, g, b = EffectGenerator.breathing_effect(current_time_ms, base_color)
        
        for client, device in clients_and_devices:
            client.send_solid_color(r, g, b, device['led_count'])
        
        time.sleep(0.05)  # 20 FPS


def run_fire_demo(clients_and_devices, duration=10):
    """Demonstrate fire effect"""
    print("Running Fire Effect...")
    
    start_time = time.time()
    
    while time.time() - start_time < duration:
        for client, device in clients_and_devices:
            led_count = device['led_count']
            pixel_data = []
            
            # Simple fire simulation
            for i in range(led_count):
                # Create heat based on position (more heat at bottom)
                base_heat = max(0, 255 - (i * 255 // led_count))
                # Add some randomness
                import random
                heat = max(0, min(255, base_heat + random.randint(-50, 50)))
                
                heat_map = {i: heat}
                r, g, b = EffectGenerator.fire_effect(i, led_count, heat_map)
                pixel_data.append((r, g, b))
            
            client.send_pixel_data(pixel_data)
        
        time.sleep(0.1)  # 10 FPS for fire effect


def main():
    """Run effects demonstration"""
    print("WLED DDP Effects Demonstration")
    print("=" * 40)
    
    # Load device configuration
    config_path = Path(__file__).parent.parent / "config" / "devices.json"
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    devices = config['devices']
    
    # Import the DDPClient (placeholder for now)
    import sys
    sys.path.append(str(Path(__file__).parent))
    from basic_control import DDPClient
    
    # Initialize clients
    clients_and_devices = []
    for device in devices:
        client = DDPClient(device['ip'], device['port'])
        clients_and_devices.append((client, device))
        print(f"Connected to: {device['name']} at {device['ip']}")
    
    print("\nStarting effects demonstration...")
    
    # Run different effects
    effects = [
        ("Rainbow Cycle", run_rainbow_demo),
        ("Breathing Effect", run_breathing_demo), 
        ("Fire Effect", run_fire_demo)
    ]
    
    for effect_name, effect_function in effects:
        print(f"\n{effect_name}:")
        print("-" * 20)
        effect_function(clients_and_devices, duration=8)
        
        # Brief pause between effects
        print("Pausing...")
        for client, device in clients_and_devices:
            client.send_solid_color(0, 0, 0, device['led_count'])
        time.sleep(2)
    
    print("\nEffects demonstration complete!")
    
    # Turn off all LEDs
    print("Turning off all LEDs...")
    for client, device in clients_and_devices:
        client.send_solid_color(0, 0, 0, device['led_count'])


if __name__ == "__main__":
    main()
