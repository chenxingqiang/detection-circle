import unittest
import os
import numpy as np
import cv2
import sys

# Add the src directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from circle_detector import CircleDetector
from image_processor import ImageProcessor
from contour_processor import ContourProcessor

class TestCircleDetector(unittest.TestCase):
    def setUp(self):
        self.circle_detector = CircleDetector()
        self.image_processor = ImageProcessor()
        self.contour_processor = ContourProcessor()
        # Create a sample test image path
        self.test_image_path = os.path.join(os.path.dirname(__file__), '..', 'dataset', '0.jpg')
        
    def test_detect_circles(self):
        """Test that circle detection works correctly"""
        # Load and process an image to get contours
        image = self.image_processor.load_image(self.test_image_path)
        processed_image = self.image_processor.preprocess(image)
        edges = self.image_processor.detect_edges(processed_image)
        contours = self.image_processor.extract_contours(edges)
        filtered_contours = self.contour_processor.filter_contours(contours)
        
        # Detect circles from contours
        circles = self.circle_detector.detect_circles(filtered_contours)
        
        self.assertIsNotNone(circles)
        self.assertTrue(isinstance(circles, list))
        
    def test_fit_circle(self):
        """Test that circle fitting works correctly"""
        # Create points that lie approximately on a circle
        theta = np.linspace(0, 2*np.pi, 100)
        center_x, center_y, radius = 100, 100, 50
        x = center_x + radius * np.cos(theta)
        y = center_y + radius * np.sin(theta)
        points = np.column_stack((x, y)).astype(np.int32)
        
        # Add some noise
        points += np.random.normal(0, 1, points.shape).astype(np.int32)
        
        # Fit a circle to the points
        center, radius = self.circle_detector.fit_circle(points)
        
        self.assertIsNotNone(center)
        self.assertIsNotNone(radius)
        self.assertTrue(isinstance(center, tuple))
        self.assertTrue(isinstance(radius, float))
        # Check that the fitted circle is close to the original
        self.assertAlmostEqual(center[0], center_x, delta=5)
        self.assertAlmostEqual(center[1], center_y, delta=5)
        self.assertAlmostEqual(radius, 50, delta=5)
        
    def test_is_circle(self):
        """Test that circle validation works correctly"""
        # Create a contour that is approximately a circle
        theta = np.linspace(0, 2*np.pi, 100)
        center_x, center_y, radius = 100, 100, 50
        x = center_x + radius * np.cos(theta)
        y = center_y + radius * np.sin(theta)
        points = np.column_stack((x, y)).astype(np.int32)
        contour = points.reshape(-1, 1, 2)
        
        # Check if it's a circle
        is_circle = self.circle_detector.is_circle(contour)
        
        self.assertTrue(is_circle)
        
        # Create a contour that is not a circle (e.g., a square)
        square = np.array([[[0, 0]], [[100, 0]], [[100, 100]], [[0, 100]]], dtype=np.int32)
        
        # Check if it's a circle
        is_circle = self.circle_detector.is_circle(square)
        
        self.assertFalse(is_circle)
        
if __name__ == '__main__':
    unittest.main()
