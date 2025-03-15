# PDP Controller - Xbox One joystick tools

A small collection of Python scripts to **discover**, **calibrate**, and **visualize** inputs from an Xbox/PDP controller using [pygame](https://www.pygame.org/).

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

- **`inputs.txt`**
    Example file for storing your discovered input indices.

- **`xbox_controller.png`**
    Reference image used by the calibration and visualizer scripts.

## Requirements
- Python 3.x
- `pip install pygame`

## Usage
1. **Discover Input Indices**
    Run `discover_inputs.py` to see which buttons/axes map to which indices.
2. **Calibrate Button Positions**
    Run `calibrate_joy.py` to map exact button coordinates on the PNG.
3. **Visualize**
    Update `joystick.py` with your mappings and run it to see real-time highlights.

## License
Distributed under the terms of the [LICENSE](LICENSE) file.