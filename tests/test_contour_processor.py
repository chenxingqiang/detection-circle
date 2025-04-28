import unittest
import os
import numpy as np
import cv2
import sys

# Add the src directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from contour_processor import ContourProcessor
from image_processor import ImageProcessor

class TestContourProcessor(unittest.TestCase):
    def setUp(self):
        self.contour_processor = ContourProcessor()
        self.image_processor = ImageProcessor()
        # Create a sample test image path
        self.test_image_path = os.path.join(os.path.dirname(__file__), '..', 'dataset', '0.jpg')
        
    def test_filter_contours(self):
        """Test that contour filtering works correctly"""
        # Load and process an image to get contours
        image = self.image_processor.load_image(self.test_image_path)
        processed_image = self.image_processor.preprocess(image)
        edges = self.image_processor.detect_edges(processed_image)
        contours = self.image_processor.extract_contours(edges)
        
        # Filter the contours
        filtered_contours = self.contour_processor.filter_contours(contours)
        
        self.assertIsNotNone(filtered_contours)
        self.assertTrue(isinstance(filtered_contours, list))
        # The filtered list should not be longer than the original list
        self.assertTrue(len(filtered_contours) <= len(contours))
        
    def test_single_line_processing(self):
        """Test that contour single-line processing works correctly"""
        # Create a simple contour for testing
        contour = np.array([[[0, 0]], [[1, 0]], [[2, 0]], [[2, 1]], [[2, 2]], [[1, 2]], [[0, 2]], [[0, 1]]], dtype=np.int32)
        
        # Process the contour
        single_line_contour = self.contour_processor.single_line_processing(contour)
        
        self.assertIsNotNone(single_line_contour)
        self.assertTrue(isinstance(single_line_contour, np.ndarray))
        # The single-line contour should have the same number of points or fewer
        self.assertTrue(len(single_line_contour) <= len(contour))
        
    def test_approximate_contour(self):
        """Test that contour approximation works correctly"""
        # Create a simple contour for testing
        contour = np.array([[[0, 0]], [[1, 0]], [[2, 0]], [[2, 1]], [[2, 2]], [[1, 2]], [[0, 2]], [[0, 1]]], dtype=np.int32)
        
        # Approximate the contour
        epsilon = 0.01 * cv2.arcLength(contour, True)
        approx_contour = self.contour_processor.approximate_contour(contour, epsilon)
        
        self.assertIsNotNone(approx_contour)
        self.assertTrue(isinstance(approx_contour, np.ndarray))
        # The approximated contour should have fewer points than the original
        self.assertTrue(len(approx_contour) <= len(contour))
        
if __name__ == '__main__':
    unittest.main()
