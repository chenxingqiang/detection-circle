# Circle Detection and Roundness Calculation

This project implements algorithms to detect circles in product images and calculate their roundness tolerance.

## Project Structure
```
detection-circle/
├── dataset/            # Contains input images
├── src/                # Source code
│   ├── image_processor.py
│   ├── contour_processor.py
│   ├── circle_detector.py
│   ├── roundness_calculator.py
│   ├── visualizer.py
│   └── main.py
├── tests/              # Test cases
│   ├── test_image_processor.py
│   ├── test_contour_processor.py
│   ├── test_circle_detector.py
│   └── test_roundness_calculator.py
├── requirements.txt    # Dependencies
└── README.md           # Project documentation
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python src/main.py --image_path dataset/image.jpg --method min_zone
```

Available methods for roundness calculation:
- `min_zone`: Minimum Zone Method
- `least_squares`: Least Squares Circle Method
- `min_circumscribed`: Minimum Circumscribed Circle Method
- `max_inscribed`: Maximum Inscribed Circle Method

## Features

1. Extract product contours from images
2. Implement contour single-line processing
3. Implement geometric description of the single-line contours
4. Calculate roundness tolerance using various methods
