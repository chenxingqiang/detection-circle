import os
import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt
from image_processor import ImageProcessor
from contour_processor import ContourProcessor
from circle_detector import CircleDetector
from roundness_calculator import RoundnessCalculator
from visualizer import Visualizer

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Circle Detection and Roundness Calculation')
    parser.add_argument('--image_path', type=str, required=True, help='Path to the input image')
    parser.add_argument('--method', type=str, default='min_zone', 
                        choices=['min_zone', 'least_squares', 'min_circumscribed', 'max_inscribed'],
                        help='Method for roundness calculation')
    parser.add_argument('--output_dir', type=str, default='output', help='Directory to save output images')
    parser.add_argument('--show', action='store_true', help='Show visualization')
    return parser.parse_args()

def process_image(image_path, method='min_zone', output_dir='output', show=False):
    """
    Process an image to detect circles and calculate roundness.
    
    Args:
        image_path (str): Path to the input image.
        method (str): Method for roundness calculation.
        output_dir (str): Directory to save output images.
        show (bool): Whether to show visualization.
        
    Returns:
        dict: Results including circles and roundness.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize components
    image_processor = ImageProcessor()
    contour_processor = ContourProcessor()
    circle_detector = CircleDetector()
    roundness_calculator = RoundnessCalculator()
    visualizer = Visualizer()
    
    # Load and process image
    image = image_processor.load_image(image_path)
    processed_image = image_processor.preprocess(image)
    edges = image_processor.detect_edges(processed_image)
    contours = image_processor.extract_contours(edges)
    
    # Filter contours and detect circles
    filtered_contours = contour_processor.filter_contours(contours)
    circles = circle_detector.detect_circles(filtered_contours)
    
    # Draw contours and circles
    contour_image = visualizer.draw_contours(image.copy(), filtered_contours)
    circle_image = visualizer.draw_circles(contour_image, circles)
    
    # Save intermediate results
    visualizer.save_image(edges, os.path.join(output_dir, 'edges.jpg'))
    visualizer.save_image(contour_image, os.path.join(output_dir, 'contours.jpg'))
    visualizer.save_image(circle_image, os.path.join(output_dir, 'circles.jpg'))
    
    # Process each detected circle
    results = []
    for i, circle in enumerate(circles):
        center_x, center_y, radius = circle
        
        # Extract points from the contour that corresponds to this circle
        # Find the contour that is closest to the circle
        best_contour = None
        min_distance = float('inf')
        
        for contour in filtered_contours:
            contour_center = np.mean(contour, axis=0)[0]
            distance = np.sqrt((contour_center[0] - center_x)**2 + (contour_center[1] - center_y)**2)
            if distance < min_distance:
                min_distance = distance
                best_contour = contour
        
        if best_contour is None:
            continue
        
        # Convert contour to single-line representation
        points = contour_processor.single_line_processing(best_contour)
        
        # Calculate roundness using the specified method
        if method == 'min_zone':
            inner_circle, outer_circle, roundness = roundness_calculator.min_zone_method(points)
            method_name = "Minimum Zone Method"
        elif method == 'least_squares':
            center, radius, roundness = roundness_calculator.least_squares_method(points)
            inner_circle = (center[0], center[1], radius - roundness/2)
            outer_circle = (center[0], center[1], radius + roundness/2)
            method_name = "Least Squares Method"
        elif method == 'min_circumscribed':
            center, outer_radius, inner_radius, roundness = roundness_calculator.min_circumscribed_method(points)
            inner_circle = (center[0], center[1], inner_radius)
            outer_circle = (center[0], center[1], outer_radius)
            method_name = "Minimum Circumscribed Circle Method"
        elif method == 'max_inscribed':
            center, inner_radius, outer_radius, roundness = roundness_calculator.max_inscribed_method(points)
            inner_circle = (center[0], center[1], inner_radius)
            outer_circle = (center[0], center[1], outer_radius)
            method_name = "Maximum Inscribed Circle Method"
        
        # Visualize roundness
        result_image = visualizer.visualize_roundness(image.copy(), inner_circle, outer_circle, method_name)
        
        # Save result
        result_filename = os.path.join(output_dir, f'result_{i}_{method}.jpg')
        visualizer.save_image(result_image, result_filename)
        
        # Show result if requested
        if show:
            visualizer.display_image(result_image, f"Circle {i} - {method_name}")
        
        # Store result
        results.append({
            'circle_index': i,
            'center': (center_x, center_y),
            'radius': radius,
            'inner_circle': inner_circle,
            'outer_circle': outer_circle,
            'roundness': roundness,
            'method': method,
            'result_image_path': result_filename
        })
    
    return results

def process_all_images(dataset_dir, method='min_zone', output_dir='output', show=False):
    """
    Process all images in a dataset directory.
    
    Args:
        dataset_dir (str): Path to the dataset directory.
        method (str): Method for roundness calculation.
        output_dir (str): Directory to save output images.
        show (bool): Whether to show visualization.
        
    Returns:
        dict: Results for all images.
    """
    # Get all image files in the dataset directory
    image_files = [f for f in os.listdir(dataset_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    all_results = {}
    
    for image_file in image_files:
        image_path = os.path.join(dataset_dir, image_file)
        image_output_dir = os.path.join(output_dir, os.path.splitext(image_file)[0])
        
        print(f"Processing image: {image_file}")
        
        try:
            results = process_image(image_path, method, image_output_dir, show)
            all_results[image_file] = results
            
            # Print results
            for result in results:
                print(f"  Circle {result['circle_index']}: Roundness = {result['roundness']:.2f} pixels")
        except Exception as e:
            print(f"Error processing {image_file}: {str(e)}")
    
    return all_results

def main():
    """Main function."""
    args = parse_args()
    
    if os.path.isdir(args.image_path):
        # Process all images in the directory
        all_results = process_all_images(args.image_path, args.method, args.output_dir, args.show)
    else:
        # Process a single image
        results = process_image(args.image_path, args.method, args.output_dir, args.show)
        all_results = {os.path.basename(args.image_path): results}
    
    print("Processing complete.")

if __name__ == '__main__':
    main()
