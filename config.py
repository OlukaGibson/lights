"""
Configuration settings for LED Control System
"""

# TV/Display Configuration
TV_WIDTH_CM = 55.0
TV_HEIGHT_CM = 31.0
LEDS_PER_METER = 60

# Network Configuration
UDP_HOST = "0.0.0.0"
UDP_PORT = 4048  # Standard DDP port

# Processing Configuration
DEFAULT_FPS = 30
MAX_FPS = 60
FRAME_RESIZE_WIDTH = 160
FRAME_RESIZE_HEIGHT = 90
EDGE_STRIP_SIZE = 10

# LED Strip Configuration
LED_ORDER = ['top', 'right', 'bottom', 'left']
REVERSE_EDGES = ['bottom', 'left']

# Debug Configuration
DEBUG_MODE = True
PRINT_COLOR_SUMMARY = True
SHOW_PREVIEW_WINDOW = True