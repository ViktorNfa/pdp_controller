# PDP Controller - Xbox One Joystick Tools

A small collection of Python scripts to **discover**, **calibrate**, **visualize**, and now **vibrate** an Xbox/PDP controller using [pygame](https://www.pygame.org/) and **python-evdev**.

---

## Files

- **`discover_inputs.py`**  
    Displays all controller inputs (buttons, axes, hats) in real time.  
    ```bash
    python discover_inputs.py
    ```

- **`calibrate_joy.py`**
    Prompts you to click each button on xbox_controller.png to capture coordinates. Prints a dictionary you can copy into your visualizer script.
    ```bash
    python calibrate_joy.py
    ```

- **`joystick.py`**
    Main visualizer:
    - Highlights pressed buttons (using your calibrated coordinates).
    - Draws stick positions.
    ```bash
    python joystick.py
    ```

- **`haptic.py`**
    Uses python-evdev to send three distinct rumble effects to the controller:
    - Strong rumble
    - Weak rumble
    - Sine wave effect
    
    Important: Set the correct EVENT_DEVICE_PATH near the top of the script (e.g., /dev/input/event7). To find which event node your gamepad uses, check:
    ```bash
    cat /proc/bus/input/devices
    ```
    Then look for a block describing your controller (like “Generic X-Box pad”) with lines:
    ```bash
    H: Handlers=event7 js0
    ```
    Indicating the device is on event7 (adjust if yours differs). Run:
    ```bash
    python haptic.py
    ```

- **`inputs.txt`**
    Example file for storing your discovered input indices.

- **`xbox_controller.png`**
    Reference image used by the calibration and visualizer scripts.

## Requirements
- Python 3.x
- `pip install pygame`
- `pip install evdev` (for haptic.py script)

## Usage
1. **Discover Input Indices**
    Run `discover_inputs.py` to see which buttons/axes map to which indices.
2. **Calibrate Button Positions**
    Run `calibrate_joy.py` to map exact button coordinates on the PNG.
3. **Visualize**
    Update `joystick.py` with your mappings and run it to see real-time highlights.
3. **Rumble with `haptic.py`**
    - Edit the `EVENT_DEVICE_PATH` if necessary (e.g. `/dev/input/event7`).
    - Run `haptic.py` to send strong, weak, or sine wave rumble to your controller.
    - Ensure you have write access to `/dev/input/eventX` (e.g., run as root or adjust permissions).

## License
Distributed under the terms of the [LICENSE](LICENSE) file.