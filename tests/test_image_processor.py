import unittest
import os
import numpy as np
import cv2
import sys

# Add the src directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from image_processor import ImageProcessor

class TestImageProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = ImageProcessor()
        # Create a sample test image path
        self.test_image_path = os.path.join(os.path.dirname(__file__), '..', 'dataset', '0.jpg')
        
    def test_load_image(self):
        """Test that an image can be loaded correctly"""
        image = self.processor.load_image(self.test_image_path)
        self.assertIsNotNone(image)
        self.assertTrue(isinstance(image, np.ndarray))
        self.assertTrue(image.shape[2] == 3)  # Should be a color image with 3 channels
        
    def test_preprocess(self):
        """Test that image preprocessing works correctly"""
        image = self.processor.load_image(self.test_image_path)
        processed_image = self.processor.preprocess(image)
        self.assertIsNotNone(processed_image)
        self.assertTrue(isinstance(processed_image, np.ndarray))
        self.assertTrue(len(processed_image.shape) == 2)  # Should be a grayscale image
        
    def test_detect_edges(self):
        """Test that edge detection works correctly"""
        image = self.processor.load_image(self.test_image_path)
        processed_image = self.processor.preprocess(image)
        edges = self.processor.detect_edges(processed_image)
        self.assertIsNotNone(edges)
        self.assertTrue(isinstance(edges, np.ndarray))
        self.assertTrue(len(edges.shape) == 2)  # Should be a binary image
        
    def test_extract_contours(self):
        """Test that contour extraction works correctly"""
        image = self.processor.load_image(self.test_image_path)
        processed_image = self.processor.preprocess(image)
        edges = self.processor.detect_edges(processed_image)
        contours = self.processor.extract_contours(edges)
        self.assertIsNotNone(contours)
        self.assertTrue(isinstance(contours, list))
        self.assertTrue(len(contours) > 0)  # Should find at least one contour
        
if __name__ == '__main__':
    unittest.main()
