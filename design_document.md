# Circle Detection and Roundness Calculation - Design Document

## Project Overview
This project aims to detect circles in product images and calculate their roundness tolerance. Roundness is a measure of how closely a cross-section of a workpiece approximates a perfect circle. The difference between the maximum and minimum radii is the roundness error.

## Requirements
1. Extract product contours from images
2. Implement contour single-line processing
3. Implement geometric description of the single-line contours
4. Calculate roundness tolerance of key circles

## Technical Approach

### 1. Image Processing Pipeline
1. **Image Loading**: Load images from the dataset
2. **Preprocessing**: 
   - Convert to grayscale
   - Apply Gaussian blur to reduce noise
   - Apply thresholding/edge detection to highlight edges
3. **Contour Detection**: Extract contours from the processed image
4. **Contour Filtering**: Filter contours based on shape properties to identify potential circles
5. **Single-line Processing**: Convert contours to single-line representation
6. **Circle Fitting**: Fit circles to the filtered contours
7. **Roundness Calculation**: Calculate roundness tolerance using one of the four methods described in the requirements

### 2. Roundness Calculation Methods
As specified in the requirements, we will implement all four methods for roundness error evaluation:
1. **Minimum Zone Method**: Find two concentric circles with minimum radial difference that contain all points
2. **Least Squares Circle Method**: Find a circle that minimizes the sum of squares of distances from points to the circle
3. **Minimum Circumscribed Circle Method**: For external circles, find the smallest circle that contains all points
4. **Maximum Inscribed Circle Method**: For internal circles, find the largest circle that is contained by all points

### 3. Visualization
- Display original image with detected contours
- Highlight the detected circles
- Visualize the roundness calculation (inner and outer concentric circles)
- Display numerical results (roundness tolerance value)

## Component Design

### 1. ImageProcessor Class
Responsible for loading and preprocessing images:
- `load_image(path)`: Load image from file
- `preprocess(image)`: Apply preprocessing steps
- `detect_edges(image)`: Apply edge detection
- `extract_contours(image)`: Extract contours from processed image

### 2. ContourProcessor Class
Responsible for processing and filtering contours:
- `filter_contours(contours)`: Filter contours based on shape properties
- `single_line_processing(contour)`: Convert contour to single-line representation

### 3. CircleDetector Class
Responsible for detecting circles and calculating properties:
- `detect_circles(contours)`: Detect circles from contours
- `fit_circle(points)`: Fit a circle to a set of points

### 4. RoundnessCalculator Class
Responsible for calculating roundness tolerance:
- `min_zone_method(points)`: Calculate roundness using minimum zone method
- `least_squares_method(points)`: Calculate roundness using least squares method
- `min_circumscribed_method(points)`: Calculate roundness using minimum circumscribed circle method
- `max_inscribed_method(points)`: Calculate roundness using maximum inscribed circle method

### 5. Visualizer Class
Responsible for visualization:
- `display_image(image)`: Display an image
- `draw_contours(image, contours)`: Draw contours on an image
- `draw_circles(image, circles)`: Draw circles on an image
- `visualize_roundness(image, inner_circle, outer_circle)`: Visualize roundness calculation

## Data Flow
1. Load image → ImageProcessor
2. Preprocess image → ImageProcessor
3. Extract contours → ImageProcessor
4. Filter contours → ContourProcessor
5. Single-line processing → ContourProcessor
6. Detect circles → CircleDetector
7. Calculate roundness → RoundnessCalculator
8. Visualize results → Visualizer

## Test Plan
1. Unit tests for each component
2. Integration tests for the complete pipeline
3. Validation tests using sample images with known roundness values
