# Beat Sync Pictures

This program visualizes images that respond to bass intensity in real time, with parameters you can customize via command-line arguments. Use this to create dynamic, beat-synced visual effects that can be adjusted according to sensitivity, time interval, and outer circle expansion rate.

## Features

- **Beat-Synced Sensitivity**: Adjust the program’s responsiveness to bass amplitude.
- **Image Switching Interval**: Set a timed interval for switching images.
- **Outer Circle Effect**: Control the expansion rate of a ripple effect around the central image.

## Requirements

- Python 3.x
- `argparse` (standard library)
- Additional packages like `pygame` and `numpy` if they're required for the visualizations


```bash
pip install -r requirements.txt
```

## Usage

Run the program with customizable arguments:

```bash
python python beat_video_sync.py [options]
```

### Arguments

| Argument | Short | Type | Default | Description |
| --- | --- | --- | --- | --- |
| `--sensitivity` | `-s` | float | 0.0000001 | Set bass sensitivity for image movement |
| `--interval` | `-i` | int | 250 | Set time interval (in seconds) between image switches |
| `--circle` | `-c` | float | 2   | Set the outer circle expansion rate |

### Examples

1.  **Run with default settings**:
    
```bash
python beat_video_sync.py
```
    
2.  **Adjust bass sensitivity for small speakers**:
    
```bash
python beat_video_sync.py -s 0.0005
```
    
3.  **Switch image every 10 seconds**:
    
```bash
python beat_video_sync.py -s 0.0005 -i 10
```

## License

This project is licensed under the MIT License.