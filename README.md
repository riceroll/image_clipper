# image_clipper
A simple tool to clip bounding boxes from an image, especially used to label the dataset.

## Requirements

- Python-2.7
- matplotlib-1.5.3 
- Numpy
- Pylab

## Quick Start
### Download Data
By default, the tool only process png files in "./data". You can put some png files there or download a sample set(47.1MB) by typing:

```bash
sh download_data.sh
```

### Run
Run the tool by typing:
```bash
python clipper.py
```
Type "0" to process from the first image or type the filename to start from that image.

### Operation
Operations are shown at the bottom-left corner.
