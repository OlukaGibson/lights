# WLED DDP Lighting Project

## Project Structure

This repository contains a Python backend for controlling ESP32/ESP8266 devices running WLED firmware. The communication uses the Distributed Display Protocol (DDP) to send color data to SK6812 LED strips.

## Key Files Created

### Configuration Files (`config/`)
- `devices.json` - WLED device configurations (IP addresses, LED counts, etc.)
- `zones.json` - Zone definitions for controlling different areas  
- `effects.json` - Effect definitions and presets

### Example Scripts (`examples/`)
- `basic_control.py` - Simple color control demonstration
- `effects_demo.py` - Various lighting effects showcase

### Requirements
- `requirements.txt` - Python package dependencies for DDP communication and effects

## Next Steps

To complete the implementation, you'll need to:

1. **Implement DDP Protocol Classes** (`src/ddp/`):
   - Create actual DDP packet structure
   - Implement UDP socket communication
   - Handle packet sequencing and reliability

2. **Develop Effect Classes** (`src/effects/`):
   - Base effect class with common functionality
   - Specific effect implementations (rainbow, fire, etc.)
   - Real-time effect rendering

3. **Add Device Discovery** (`src/discovery/`):
   - Network scanning for WLED devices
   - mDNS/Bonjour service discovery
   - Automatic device configuration

4. **Create Main Controller** (`src/controllers/`):
   - High-level lighting control interface
   - Zone management
   - Effect scheduling and transitions

## WLED Setup

Make sure your ESP devices have:
- WLED firmware installed
- DDP enabled in sync settings (usually port 4048)
- Correct LED count and GPIO pin configured
- Stable WiFi connection

## Ready to Develop

The project structure is now set up with:
- Descriptive README explaining the WLED DDP approach
- Proper requirements file for dependencies
- Configuration templates
- Example scripts to get started
- Clear project organization

You can now begin implementing the actual DDP communication and effect generation code!
