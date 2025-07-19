"# WLED DDP Ambient Lighting Controller

A Python-based control system for managing ambient lighting using ESP32/ESP8266 devices running WLED firmware. This system communicates with WLED devices using the **Distributed Display Protocol (DDP)** to send color data to SK6812 (NeoPixel) LED strips.

## Overview

This project provides a Python backend that can send color data and effects to multiple WLED-enabled ESP devices over your local network. The ESP devices control SK6812 LED strips to create ambient lighting effects.

### What is DDP?

The Distributed Display Protocol (DDP) is a simple network protocol designed for controlling addressable LED strips. WLED firmware supports DDP, allowing external applications to send pixel data directly to the LEDs in real-time.

## Features

- **DDP Communication**: Direct communication with WLED devices using Distributed Display Protocol
- **Multi-Device Support**: Control multiple ESP devices simultaneously 
- **Real-time Color Control**: Send RGB color data to individual LEDs or entire strips
- **Effect Generation**: Create custom lighting effects and animations in Python
- **WLED Integration**: Full compatibility with WLED firmware features
- **Network Discovery**: Automatic discovery of WLED devices on the network
- **Zone Management**: Control different zones/segments of your lighting setup
- **Performance Optimized**: Efficient packet transmission for smooth animations

## Hardware Requirements

### ESP Device Setup
- **ESP32** or **ESP8266** microcontroller
- **SK6812** LED strips (RGBW NeoPixels) or **WS2812B** (RGB NeoPixels)
- **WLED firmware** installed on the ESP device
- Stable WiFi connection
- Adequate 5V power supply for LED strips

### Recommended Hardware
- ESP32 (preferred for better performance and memory)
- SK6812 RGBW LED strips for better color accuracy
- Level shifter for reliable data transmission (3.3V to 5V)
- Capacitors for power supply filtering

## WLED Firmware Setup

1. **Install WLED**: Flash WLED firmware to your ESP32/ESP8266
   - Download from: https://github.com/Aircoookie/WLED
   - Use WLED installer or flash manually

2. **Configure WLED**:
   - Connect to WLED AP and configure WiFi
   - Set LED count and GPIO pin in WLED settings
   - Enable DDP in WLED settings (Sync → Network)
   - Note the device IP address

3. **DDP Configuration**:
   - DDP typically runs on port 4048
   - Enable "Receive DDP" in WLED sync settings
   - Set timeout values as needed

## Software Architecture

```
├── src/
│   ├── ddp/                 # DDP protocol implementation
│   │   ├── client.py        # DDP client for sending data
│   │   └── packet.py        # DDP packet structure
│   ├── effects/             # Lighting effects and animations
│   │   ├── base.py          # Base effect class
│   │   ├── solid.py         # Solid color effects
│   │   ├── rainbow.py       # Rainbow effects
│   │   └── custom.py        # Custom effect implementations
│   ├── discovery/           # WLED device discovery
│   │   └── wled_scanner.py  # Network scanning for WLED devices
│   ├── controllers/         # Main control logic
│   │   ├── lighting_controller.py  # Primary lighting controller
│   │   └── zone_controller.py      # Zone-based control
│   └── utils/               # Utility functions
│       ├── color.py         # Color manipulation utilities
│       └── config.py        # Configuration management
├── config/                  # Configuration files
│   ├── devices.json         # WLED device configurations
│   ├── zones.json          # Zone definitions
│   └── effects.json        # Effect presets
├── examples/               # Usage examples
│   ├── basic_control.py    # Simple color control
│   ├── effects_demo.py     # Effect demonstrations
│   └── multi_zone.py       # Multi-zone control
└── tests/                  # Unit tests
```

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure WLED Devices
Create `config/devices.json`:
```json
{
  "devices": [
    {
      "name": "Living Room Strip",
      "ip": "192.168.1.100",
      "port": 4048,
      "led_count": 60,
      "start_index": 0
    },
    {
      "name": "Bedroom Strip", 
      "ip": "192.168.1.101",
      "port": 4048,
      "led_count": 30,
      "start_index": 60
    }
  ]
}
```

### 3. Basic Usage
```python
from src.controllers.lighting_controller import LightingController

# Initialize controller
controller = LightingController()

# Set solid color (red)
controller.set_solid_color(255, 0, 0)

# Start rainbow effect
controller.start_effect("rainbow", speed=50)

# Control specific zones
controller.set_zone_color("living_room", 0, 255, 0)
```

### 4. Run Examples
```bash
python examples/basic_control.py
python examples/effects_demo.py
```

## DDP Protocol Details

DDP packets contain:
- Header with protocol information
- LED data (RGB/RGBW values)
- Sequence numbers for reliability
- Device/zone targeting information

The protocol supports:
- Up to 1440 LEDs per packet
- Multiple data types (RGB, RGBW)
- Push and pull modes
- Sequence tracking

## Configuration

### Device Configuration (`config/devices.json`)
```json
{
  "devices": [
    {
      "name": "Device Name",
      "ip": "192.168.1.100", 
      "port": 4048,
      "led_count": 60,
      "led_type": "SK6812",
      "start_index": 0,
      "reverse": false
    }
  ]
}
```

### Zone Configuration (`config/zones.json`)
```json
{
  "zones": {
    "living_room": {
      "devices": ["192.168.1.100"],
      "start_led": 0,
      "led_count": 30
    },
    "kitchen": {
      "devices": ["192.168.1.100"],
      "start_led": 30,
      "led_count": 30
    }
  }
}
```

## Available Effects

- **Solid Colors**: Single color across all LEDs
- **Rainbow**: Cycling rainbow effect
- **Color Wipe**: Progressive color filling
- **Theater Chase**: Moving dot patterns
- **Fire**: Flickering fire simulation
- **Twinkle**: Random sparkle effects
- **Breathe**: Smooth brightness pulsing
- **Custom**: User-defined effects

## Network Discovery

Automatically discover WLED devices on your network:
```python
from src.discovery.wled_scanner import WLEDScanner

scanner = WLEDScanner()
devices = scanner.discover_devices()
print(f"Found {len(devices)} WLED devices")
```

## Performance Considerations

- **Frame Rate**: Typical 30-60 FPS for smooth animations
- **Packet Size**: Optimize for your network and LED count
- **Network Bandwidth**: Consider bandwidth for multiple devices
- **Power Management**: Ensure adequate power supply for all LEDs

## Integration Examples

### Home Assistant
```python
# MQTT integration for Home Assistant
from src.controllers.lighting_controller import LightingController

controller = LightingController()
# Publish state to MQTT for Home Assistant integration
```

### Scheduling
```python
import schedule
import time

def morning_routine():
    controller.set_solid_color(255, 200, 100)  # Warm white
    
def evening_routine():
    controller.start_effect("fire", speed=30)

schedule.every().day.at("07:00").do(morning_routine)
schedule.every().day.at("19:00").do(evening_routine)
```

## Troubleshooting

### Common Issues
1. **Device Not Found**: Check IP address and network connectivity
2. **Slow Response**: Verify network bandwidth and packet size
3. **Color Issues**: Check LED type configuration (RGB vs RGBW)
4. **Effect Stuttering**: Reduce frame rate or optimize effect code

### WLED Configuration
- Ensure DDP is enabled in WLED sync settings
- Check port configuration (default: 4048)
- Verify LED count matches configuration
- Check power supply adequacy

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-effect`)
3. Implement your changes
4. Add tests for new functionality
5. Submit a pull request

## Resources

- **WLED Project**: https://github.com/Aircoookie/WLED
- **DDP Specification**: https://github.com/Aircoookie/WLED/wiki/DDP
- **SK6812 Datasheet**: LED strip specifications
- **ESP32/ESP8266 Documentation**: Microcontroller resources

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: Project-specific problems
- WLED Discord: WLED firmware questions
- ESP32 Forums: Hardware-related questions" 
