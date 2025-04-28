import unittest
import os
import numpy as np
import sys

# Add the src directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from roundness_calculator import RoundnessCalculator

class TestRoundnessCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = RoundnessCalculator()
        
    def test_min_zone_method(self):
        """Test that minimum zone method works correctly"""
        # Create points that lie approximately on a circle with some deviations
        theta = np.linspace(0, 2*np.pi, 100)
        center_x, center_y, radius = 100, 100, 50
        x = center_x + radius * np.cos(theta)
        y = center_y + radius * np.sin(theta)
        points = np.column_stack((x, y))
        
        # Add some controlled deviations to create known roundness error
        # Make some points closer to center and some further away
        deviations = np.zeros(len(points))
        deviations[0:10] = -2  # Points closer to center
        deviations[50:60] = 3  # Points further from center
        
        # Apply deviations along radial direction
        for i in range(len(points)):
            dx = points[i, 0] - center_x
            dy = points[i, 1] - center_y
            dist = np.sqrt(dx**2 + dy**2)
            points[i, 0] += deviations[i] * dx / dist
            points[i, 1] += deviations[i] * dy / dist
        
        # Calculate roundness using minimum zone method
        inner_circle, outer_circle, roundness = self.calculator.min_zone_method(points)
        
        self.assertIsNotNone(inner_circle)
        self.assertIsNotNone(outer_circle)
        self.assertIsNotNone(roundness)
        self.assertTrue(isinstance(inner_circle, tuple))
        self.assertTrue(isinstance(outer_circle, tuple))
        self.assertTrue(isinstance(roundness, float))
        # The roundness should be positive and reflect the deviations we applied
        # Note: The actual value may vary based on the optimization algorithm
        self.assertTrue(roundness > 0)
        self.assertTrue(roundness < 10.0)  # A reasonable upper bound
        
    def test_least_squares_method(self):
        """Test that least squares method works correctly"""
        # Create points that lie approximately on a circle with some deviations
        theta = np.linspace(0, 2*np.pi, 100)
        center_x, center_y, radius = 100, 100, 50
        x = center_x + radius * np.cos(theta)
        y = center_y + radius * np.sin(theta)
        points = np.column_stack((x, y))
        
        # Add some controlled deviations
        deviations = np.zeros(len(points))
        deviations[0:10] = -2
        deviations[50:60] = 3
        
        # Apply deviations along radial direction
        for i in range(len(points)):
            dx = points[i, 0] - center_x
            dy = points[i, 1] - center_y
            dist = np.sqrt(dx**2 + dy**2)
            points[i, 0] += deviations[i] * dx / dist
            points[i, 1] += deviations[i] * dy / dist
        
        # Calculate roundness using least squares method
        center, radius, roundness = self.calculator.least_squares_method(points)
        
        self.assertIsNotNone(center)
        self.assertIsNotNone(radius)
        self.assertIsNotNone(roundness)
        self.assertTrue(isinstance(center, tuple))
        self.assertTrue(isinstance(radius, float))
        self.assertTrue(isinstance(roundness, float))
        # Check that the center is close to the original
        self.assertAlmostEqual(center[0], center_x, delta=1)
        self.assertAlmostEqual(center[1], center_y, delta=1)
        
    def test_min_circumscribed_method(self):
        """Test that minimum circumscribed circle method works correctly"""
        # Create points that lie approximately on a circle
        theta = np.linspace(0, 2*np.pi, 100)
        center_x, center_y, radius = 100, 100, 50
        x = center_x + radius * np.cos(theta)
        y = center_y + radius * np.sin(theta)
        points = np.column_stack((x, y))
        
        # Add some controlled deviations
        deviations = np.zeros(len(points))
        deviations[0:10] = -2
        deviations[50:60] = 3
        
        # Apply deviations along radial direction
        for i in range(len(points)):
            dx = points[i, 0] - center_x
            dy = points[i, 1] - center_y
            dist = np.sqrt(dx**2 + dy**2)
            points[i, 0] += deviations[i] * dx / dist
            points[i, 1] += deviations[i] * dy / dist
        
        # Calculate roundness using minimum circumscribed circle method
        center, radius, inner_radius, roundness = self.calculator.min_circumscribed_method(points)
        
        self.assertIsNotNone(center)
        self.assertIsNotNone(radius)
        self.assertIsNotNone(inner_radius)
        self.assertIsNotNone(roundness)
        self.assertTrue(isinstance(center, tuple))
        self.assertTrue(isinstance(radius, float))
        self.assertTrue(isinstance(inner_radius, float))
        self.assertTrue(isinstance(roundness, float))
        # The roundness should be positive
        self.assertTrue(roundness > 0)
        
    def test_max_inscribed_method(self):
        """Test that maximum inscribed circle method works correctly"""
        # Create points that lie approximately on a circle
        theta = np.linspace(0, 2*np.pi, 100)
        center_x, center_y, radius = 100, 100, 50
        x = center_x + radius * np.cos(theta)
        y = center_y + radius * np.sin(theta)
        points = np.column_stack((x, y))
        
        # Add some controlled deviations
        deviations = np.zeros(len(points))
        deviations[0:10] = -2
        deviations[50:60] = 3
        
        # Apply deviations along radial direction
        for i in range(len(points)):
            dx = points[i, 0] - center_x
            dy = points[i, 1] - center_y
            dist = np.sqrt(dx**2 + dy**2)
            points[i, 0] += deviations[i] * dx / dist
            points[i, 1] += deviations[i] * dy / dist
        
        # Calculate roundness using maximum inscribed circle method
        center, radius, outer_radius, roundness = self.calculator.max_inscribed_method(points)
        
        self.assertIsNotNone(center)
        self.assertIsNotNone(radius)
        self.assertIsNotNone(outer_radius)
        self.assertIsNotNone(roundness)
        self.assertTrue(isinstance(center, tuple))
        self.assertTrue(isinstance(radius, float))
        self.assertTrue(isinstance(outer_radius, float))
        self.assertTrue(isinstance(roundness, float))
        # The roundness should be positive
        self.assertTrue(roundness > 0)
        
if __name__ == '__main__':
    unittest.main()
