import numpy as np
import cv2
import time
from typing import Dict, List, Tuple, Optional, Callable

def get_led_colors_from_frame(frame, tv_width_cm, tv_height_cm, leds_per_meter):
    """
    Calculate per-LED colors for all edges based on a single frame.

    Args:
        frame (numpy.ndarray): Image frame as numpy array.
        tv_width_cm (float): TV width in centimeters.
        tv_height_cm (float): TV height in centimeters.
        leds_per_meter (int): Number of LEDs per meter.

    Returns:
        dict: Colors for each edge in order: {'top': [...], 'right': [...], 'bottom': [...], 'left': [...]}
    """
    # Calculate LED count per edge
    width_m = tv_width_cm / 100.0
    height_m = tv_height_cm / 100.0

    leds_top_bottom = int(width_m * leds_per_meter)
    leds_left_right = int(height_m * leds_per_meter)

    # Convert BGR to RGB if needed
    if len(frame.shape) == 3 and frame.shape[2] == 3:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Resize for performance
    resized = cv2.resize(frame, (160, 90))
    h, w, _ = resized.shape
    strip_size = 10  # Pixels for edge sampling

    # Helper function to average color
    def avg_color(region):
        avg = np.mean(region, axis=(0, 1))
        return tuple(map(int, avg))

    # Process edges
    colors = {'top': [], 'right': [], 'bottom': [], 'left': []}

    # Top edge
    segment_width = max(1, w // leds_top_bottom)
    top_strip = resized[0:strip_size, :, :]
    for i in range(leds_top_bottom):
        start_x = i * segment_width
        end_x = min((i + 1) * segment_width, w)
        seg = top_strip[:, start_x:end_x, :]
        colors['top'].append(avg_color(seg))

    # Bottom edge
    bottom_strip = resized[h - strip_size:h, :, :]
    for i in range(leds_top_bottom):
        start_x = i * segment_width
        end_x = min((i + 1) * segment_width, w)
        seg = bottom_strip[:, start_x:end_x, :]
        colors['bottom'].append(avg_color(seg))

    # Left edge
    segment_height = max(1, h // leds_left_right)
    left_strip = resized[:, 0:strip_size, :]
    for i in range(leds_left_right):
        start_y = i * segment_height
        end_y = min((i + 1) * segment_height, h)
        seg = left_strip[start_y:end_y, :, :]
        colors['left'].append(avg_color(seg))

    # Right edge
    right_strip = resized[:, w - strip_size:w, :]
    for i in range(leds_left_right):
        start_y = i * segment_height
        end_y = min((i + 1) * segment_height, h)
        seg = right_strip[start_y:end_y, :, :]
        colors['right'].append(avg_color(seg))

    return colors

def get_led_colors(image_path, tv_width_cm, tv_height_cm, leds_per_meter):
    """
    Calculate per-LED colors for all edges based on an image.

    Args:
        image_path (str): Path to image frame.
        tv_width_cm (float): TV width in centimeters.
        tv_height_cm (float): TV height in centimeters.
        leds_per_meter (int): Number of LEDs per meter.

    Returns:
        dict: Colors for each edge in order: {'top': [...], 'right': [...], 'bottom': [...], 'left': [...]}
    """
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not load image from {image_path}")
    
    return get_led_colors_from_frame(image, tv_width_cm, tv_height_cm, leds_per_meter)

def process_video(video_path: str, tv_width_cm: float, tv_height_cm: float, 
                 leds_per_meter: int, color_callback: Callable[[Dict], None],
                 target_fps: Optional[float] = None):
    """
    Process a video file and call callback with LED colors for each frame.

    Args:
        video_path (str): Path to video file.
        tv_width_cm (float): TV width in centimeters.
        tv_height_cm (float): TV height in centimeters.
        leds_per_meter (int): Number of LEDs per meter.
        color_callback (Callable): Function to call with colors dict for each frame.
        target_fps (Optional[float]): Target FPS for playback. If None, uses video's native FPS.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video file {video_path}")

    # Get video properties
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    fps = target_fps if target_fps else original_fps
    frame_delay = 1.0 / fps if fps > 0 else 0.033  # Default to ~30fps

    print(f"Processing video: {video_path}")
    print(f"Original FPS: {original_fps:.2f}, Target FPS: {fps:.2f}")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            start_time = time.time()
            
            # Get LED colors for this frame
            colors = get_led_colors_from_frame(frame, tv_width_cm, tv_height_cm, leds_per_meter)
            
            # Call the callback with colors
            color_callback(colors)
            
            # Maintain target FPS
            elapsed = time.time() - start_time
            sleep_time = max(0, frame_delay - elapsed)
            if sleep_time > 0:
                time.sleep(sleep_time)

    finally:
        cap.release()

def process_live_video(camera_index: int, tv_width_cm: float, tv_height_cm: float,
                      leds_per_meter: int, color_callback: Callable[[Dict], None],
                      target_fps: float = 30.0):
    """
    Process live video from camera and call callback with LED colors for each frame.

    Args:
        camera_index (int): Camera index (usually 0 for default camera).
        tv_width_cm (float): TV width in centimeters.
        tv_height_cm (float): TV height in centimeters.
        leds_per_meter (int): Number of LEDs per meter.
        color_callback (Callable): Function to call with colors dict for each frame.
        target_fps (float): Target FPS for processing.
    """
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        raise ValueError(f"Could not open camera {camera_index}")

    # Set camera properties for better performance
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, target_fps)

    frame_delay = 1.0 / target_fps
    print(f"Starting live video processing from camera {camera_index}")
    print("Press 'q' to quit")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame")
                break

            start_time = time.time()
            
            # Get LED colors for this frame
            colors = get_led_colors_from_frame(frame, tv_width_cm, tv_height_cm, leds_per_meter)
            
            # Call the callback with colors
            color_callback(colors)
            
            # Show preview window (optional)
            cv2.imshow('Live Video - Press q to quit', frame)
            
            # Check for quit key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            # Maintain target FPS
            elapsed = time.time() - start_time
            sleep_time = max(0, frame_delay - elapsed)
            if sleep_time > 0:
                time.sleep(sleep_time)

    finally:
        cap.release()
        cv2.destroyAllWindows()

def process_screen_capture(tv_width_cm: float, tv_height_cm: float,
                          leds_per_meter: int, color_callback: Callable[[Dict], None],
                          target_fps: float = 30.0, monitor_index: int = 0):
    """
    Process screen capture and call callback with LED colors for each frame.
    Note: Requires additional packages like mss or pyautogui for screen capture.

    Args:
        tv_width_cm (float): TV width in centimeters.
        tv_height_cm (float): TV height in centimeters.
        leds_per_meter (int): Number of LEDs per meter.
        color_callback (Callable): Function to call with colors dict for each frame.
        target_fps (float): Target FPS for processing.
        monitor_index (int): Monitor index to capture (0 for primary).
    """
    try:
        import mss
    except ImportError:
        raise ImportError("Screen capture requires 'mss' package. Install with: pip install mss")

    frame_delay = 1.0 / target_fps
    
    with mss.mss() as sct:
        monitors = sct.monitors
        if monitor_index >= len(monitors):
            raise ValueError(f"Monitor index {monitor_index} not available. Available monitors: {len(monitors)-1}")
        
        monitor = monitors[monitor_index + 1]  # monitors[0] is all monitors combined
        print(f"Capturing screen {monitor_index}: {monitor}")
        print("Press Ctrl+C to stop")

        try:
            while True:
                start_time = time.time()
                
                # Capture screenshot
                screenshot = sct.grab(monitor)
                frame = np.array(screenshot)
                
                # Convert BGRA to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
                
                # Get LED colors for this frame
                colors = get_led_colors_from_frame(frame, tv_width_cm, tv_height_cm, leds_per_meter)
                
                # Call the callback with colors
                color_callback(colors)
                
                # Maintain target FPS
                elapsed = time.time() - start_time
                sleep_time = max(0, frame_delay - elapsed)
                if sleep_time > 0:
                    time.sleep(sleep_time)

        except KeyboardInterrupt:
            print("\nScreen capture stopped")