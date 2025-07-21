import os
import sys
from controllers.ledcontrol import (
    get_led_colors, 
    process_video, 
    process_live_video, 
    process_screen_capture
)

# Configuration
TV_WIDTH_CM = 55.0  # Adjust to your TV width
TV_HEIGHT_CM = 31.0  # Adjust to your TV height
LEDS_PER_METER = 60  # Adjust to your LED strip density

def print_colors(colors):
    """
    Callback function to handle LED colors.
    Replace this with your actual LED control code.
    """
    print(f"\nLED Colors - Top: {len(colors['top'])}, Right: {len(colors['right'])}, "
          f"Bottom: {len(colors['bottom'])}, Left: {len(colors['left'])}")
    
    # Print all LEDs for each edge
    print("\n--- TOP LEDs ---")
    for i, color in enumerate(colors['top']):
        print(f"LED {i:2d}: RGB{color}")
    
    print("\n--- RIGHT LEDs ---")
    for i, color in enumerate(colors['right']):
        print(f"LED {i:2d}: RGB{color}")
    
    print("\n--- BOTTOM LEDs ---")
    for i, color in enumerate(colors['bottom']):
        print(f"LED {i:2d}: RGB{color}")
    
    print("\n--- LEFT LEDs ---")
    for i, color in enumerate(colors['left']):
        print(f"LED {i:2d}: RGB{color}")
    
    print("=" * 50)

def process_image(image_path):
    """Process a single image."""
    print(f"Processing image: {image_path}")
    try:
        colors = get_led_colors(image_path, TV_WIDTH_CM, TV_HEIGHT_CM, LEDS_PER_METER)
        print_colors(colors)
    except Exception as e:
        print(f"Error processing image: {e}")

def process_video_file(video_path, target_fps=None):
    """Process a video file."""
    print(f"Processing video: {video_path}")
    try:
        process_video(video_path, TV_WIDTH_CM, TV_HEIGHT_CM, LEDS_PER_METER, 
                     print_colors, target_fps)
    except Exception as e:
        print(f"Error processing video: {e}")

def process_camera(camera_index=0, target_fps=30):
    """Process live camera feed."""
    print(f"Processing camera {camera_index}")
    try:
        process_live_video(camera_index, TV_WIDTH_CM, TV_HEIGHT_CM, LEDS_PER_METER,
                          print_colors, target_fps)
    except Exception as e:
        print(f"Error processing camera: {e}")

def process_screen(monitor_index=0, target_fps=30):
    """Process screen capture."""
    print(f"Processing screen capture from monitor {monitor_index}")
    try:
        process_screen_capture(TV_WIDTH_CM, TV_HEIGHT_CM, LEDS_PER_METER,
                              print_colors, target_fps, monitor_index)
    except Exception as e:
        print(f"Error processing screen: {e}")

def main():
    """Main function with interactive menu."""
    while True:
        print("\n" + "="*50)
        print("LED Control System")
        print("="*50)
        print("1. Process Image")
        print("2. Process Video File")
        print("3. Process Live Camera")
        print("4. Process Screen Capture")
        print("5. Exit")
        print("-"*50)
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            image_path = input("Enter image path: ").strip()
            if os.path.exists(image_path):
                process_image(image_path)
            else:
                print("Image file not found!")
                
        elif choice == '2':
            video_path = input("Enter video path: ").strip()
            fps_input = input("Enter target FPS (press Enter for original): ").strip()
            target_fps = float(fps_input) if fps_input else None
            
            if os.path.exists(video_path):
                process_video_file(video_path, target_fps)
            else:
                print("Video file not found!")
                
        elif choice == '3':
            camera_input = input("Enter camera index (0 for default): ").strip()
            camera_index = int(camera_input) if camera_input else 0
            fps_input = input("Enter target FPS (30): ").strip()
            target_fps = float(fps_input) if fps_input else 30.0
            
            process_camera(camera_index, target_fps)
            
        elif choice == '4':
            monitor_input = input("Enter monitor index (0 for primary): ").strip()
            monitor_index = int(monitor_input) if monitor_input else 0
            fps_input = input("Enter target FPS (30): ").strip()
            target_fps = float(fps_input) if fps_input else 30.0
            
            process_screen(monitor_index, target_fps)
            
        elif choice == '5':
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()