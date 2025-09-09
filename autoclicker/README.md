# Advanced Auto Clicker

A sophisticated auto-clicking application with statistical distribution controls for natural, human-like clicking patterns.

![Distribution Comparison](https://github.com/user-attachments/files/distribution_comparison.png)

## Features

### Core Functionality
- **Configurable Hotkey Toggle**: Set any key to start/stop the auto clicker
- **Statistical Distributions**: Choose between Gaussian (normal) and weighted log-normal distributions
- **Precise Delay Control**: Configure minimum, maximum, target, and deviation values in milliseconds
- **Real-time Preview**: Test and preview delay patterns before clicking
- **Intuitive GUI**: Easy-to-use interface with clear controls and status indicators
- **Graceful Degradation**: Works with optional dependencies, warns about missing features

### Distribution Types

#### Standard Distribution (Gaussian/Normal)
- Classic bell curve distribution centered around the target value
- Symmetric spread controlled by deviation parameter
- Most natural for consistent timing patterns

#### Weighted Distribution (Log-Normal)
- Right-shifted distribution pattern creating more realistic human behavior
- Occasional longer delays mixed with consistent shorter ones
- Better simulation of natural clicking variations

## Configuration Parameters

### Toggle Control
- **Hotkey**: Click "Set Hotkey" and press any key to assign a toggle hotkey (requires pynput)

### Delay Settings (All values in milliseconds)
- **Absolute Delay Min**: The absolute minimum delay between clicks (hard lower bound)
- **Absolute Delay Max**: The absolute maximum delay between clicks (hard upper bound)  
- **Delay Target**: The peak of the distribution curve (most common delay value)
- **Delay Deviation**: Controls the spread of the distribution around the target
- **Weighted Distribution**: Toggle between standard (Gaussian) and weighted (log-normal) distributions

## Installation and Setup

### System Requirements
- **Python 3.7+** 
- **Windows, macOS, or Linux** (Windows recommended for .exe compilation)

### Required Dependencies
```bash
pip install tkinter  # Usually included with Python
```

### Optional Dependencies (for full functionality)
```bash
pip install numpy pyautogui pynput
```

Or install all at once:
```bash
pip install -r requirements.txt
```

### Running from Python Source

1. **Clone or download** this repository
2. **Navigate to the autoclicker directory**:
   ```bash
   cd autoclicker
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the application**:
   ```bash
   python main.py
   ```

### Creating a Windows Executable

See [COMPILE_INSTRUCTIONS.md](COMPILE_INSTRUCTIONS.md) for detailed steps to create a standalone .exe file.

**Quick build**:
```bash
# Windows only
build.bat
```

## Usage Instructions

### Basic Setup

1. **Launch the application** 
   - Run `python main.py` OR
   - Double-click the compiled `AdvancedAutoClicker.exe`

2. **Configure delay parameters**:
   - Set minimum delay (e.g., 20ms) 
   - Set maximum delay (e.g., 200ms)
   - Choose target delay (e.g., 50ms) - the most common value
   - Adjust deviation (e.g., 10ms) to control variation
   - Check "Weighted Distribution" for more realistic human-like patterns

3. **Test your settings**:
   - Click "Test Delay" to see sample delay values
   - Adjust parameters until satisfied with the pattern

### Hotkey Configuration (Optional)

4. **Set a hotkey** (if pynput is installed):
   - Click "Set Hotkey" button
   - Press the desired key in the popup window  
   - The key will now toggle the auto clicker on/off globally

### Operation

5. **Start clicking**:
   - Click "Start Clicking" button OR press your configured hotkey
   - Status changes to "Running" with green text
   - Clicks occur at configured delay intervals

6. **Stop clicking**:
   - Click "Stop Clicking" button OR press your hotkey again OR close the application

## Example Configurations

### Gaming - Fast Clicking
```
Min Delay: 10ms
Max Delay: 30ms  
Target: 20ms
Deviation: 3ms
Weighted: No
```

### Farming/Grinding - Natural Rhythm  
```
Min Delay: 800ms
Max Delay: 2000ms
Target: 1200ms
Deviation: 200ms
Weighted: Yes
```

### Automated Tasks - Consistent Timing
```
Min Delay: 50ms
Max Delay: 100ms
Target: 75ms
Deviation: 10ms
Weighted: No
```

## Safety Features

- **Fail-safe enabled**: Moving mouse to top-left corner stops the program (when pyautogui available)
- **Thread-safe operation**: Clicking runs separately from GUI for smooth operation  
- **Input validation**: Prevents invalid configuration combinations
- **Graceful shutdown**: Properly stops all operations when closing
- **Optional dependencies**: Application works with basic features even if some libraries are missing

## Distribution Analysis

For a configuration with min=20ms, max=80ms, target=50ms, deviation=5ms and 10,000 samples:

**Standard Distribution Results:**
- Mean: ~50ms (as expected)
- Most values clustered around target
- Symmetric spread

**Weighted Distribution Results:**  
- Mean: ~50ms but with right skew
- More natural variation pattern
- Occasional longer delays create realistic human behavior

## Technical Details

### Architecture
- **Main Thread**: GUI and user interaction
- **Background Thread**: Auto-clicking loop  
- **Hotkey Listener**: Global keyboard monitoring (optional)
- **Statistical Engine**: Distribution-based delay generation

### Dependencies Status
The application checks for optional dependencies at startup:

- ✅ **tkinter**: GUI framework (built into Python)
- 🔧 **numpy**: Enhanced statistical distributions (fallback: built-in random)
- 🔧 **pyautogui**: Mouse clicking functionality (fallback: console output)  
- 🔧 **pynput**: Global hotkey detection (fallback: disabled)

### Fallback Behavior
- **No numpy**: Uses Python's built-in `random.gauss()` and approximated log-normal
- **No pyautogui**: Prints simulated clicks to console instead of actual clicking
- **No pynput**: Hotkey functionality disabled, manual button control only

## Troubleshooting

### Common Issues

**Application won't start:**
- Ensure Python 3.7+ is installed
- Install tkinter: `pip install tk` (if not included)

**"Feature Unavailable" warnings:**
- Install missing dependencies: `pip install numpy pyautogui pynput`
- Application will work with limited functionality

**Clicking too fast/slow:**
- Adjust min/max delay values
- Ensure target is within min/max bounds  
- Reduce deviation for more consistent timing

**Hotkey not working:**
- Ensure pynput is installed: `pip install pynput`
- Try setting a different key
- Run as Administrator if needed on Windows

**Antivirus false positives (.exe):**
- Add executable to antivirus whitelist
- This is common with PyInstaller-generated executables

### Performance Notes

- Minimal CPU usage (~1-2%)
- Memory usage typically under 50MB
- Delay generation optimized for performance
- GUI remains responsive during operation

## Customization & Development

The application is designed for easy customization:

### Adding New Distribution Types
Edit the `generate_delay()` method in `main.py` to add new statistical distributions.

### Extending the GUI  
The tkinter interface can be extended with additional controls, statistics displays, or configuration options.

### Adding Features
- Click pattern recordings
- Multiple click locations
- Scheduling/timing controls
- Statistics logging

## Best Practices

### Ethical Usage
- Only use this tool for legitimate automation purposes
- Respect terms of service of applications/games
- Don't use for cheating or unfair advantages
- Consider the impact on other users

### Technical Recommendations
- Test configurations before extended use
- Use realistic delay ranges for your use case
- Monitor system performance during operation
- Keep the application updated

## License & Disclaimer

This project is provided as-is for educational and legitimate automation purposes. Users are responsible for ensuring compliance with applicable terms of service and local laws.

The authors are not responsible for any misuse of this software or any consequences resulting from its use.

## Contributing

Contributions are welcome! Please feel free to submit:
- Bug reports
- Feature requests  
- Pull requests with improvements
- Documentation updates

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Install development dependencies: `pip install -r requirements.txt`
4. Make your changes
5. Test thoroughly
6. Submit a pull request

## Acknowledgments

- Built with Python and tkinter for cross-platform compatibility
- Uses NumPy for robust statistical distributions
- PyAutoGUI provides cross-platform mouse control
- pynput enables global hotkey functionality