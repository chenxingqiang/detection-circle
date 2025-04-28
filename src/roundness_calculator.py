import numpy as np
import cv2
from scipy.optimize import minimize

class RoundnessCalculator:
    """
    Class for calculating roundness tolerance using various methods.
    """
    
    def min_zone_method(self, points):
        """
        Calculate roundness using minimum zone method.
        
        Args:
            points (numpy.ndarray): Array of points (N, 2).
            
        Returns:
            tuple: Inner circle (center_x, center_y, radius), outer circle (center_x, center_y, radius), and roundness.
        """
        # Initial guess for center using centroid
        initial_center = np.mean(points, axis=0)
        
        # Define objective function to minimize (difference between max and min radius)
        def objective(center):
            center_x, center_y = center
            # Calculate distances from center to all points
            distances = np.sqrt((points[:, 0] - center_x)**2 + (points[:, 1] - center_y)**2)
            # Return the difference between max and min radius
            return np.max(distances) - np.min(distances)
        
        # Minimize the objective function
        result = minimize(objective, initial_center, method='Nelder-Mead')
        optimal_center = result.x
        
        # Calculate distances from optimal center to all points
        distances = np.sqrt((points[:, 0] - optimal_center[0])**2 + (points[:, 1] - optimal_center[1])**2)
        min_radius = np.min(distances)
        max_radius = np.max(distances)
        
        # Calculate roundness (difference between max and min radius)
        roundness = max_radius - min_radius
        
        # Return inner circle, outer circle, and roundness
        inner_circle = (optimal_center[0], optimal_center[1], min_radius)
        outer_circle = (optimal_center[0], optimal_center[1], max_radius)
        
        return inner_circle, outer_circle, roundness
    
    def least_squares_method(self, points):
        """
        Calculate roundness using least squares circle method.
        
        Args:
            points (numpy.ndarray): Array of points (N, 2).
            
        Returns:
            tuple: Center coordinates (x, y), radius, and roundness.
        """
        # Fit a circle using least squares
        A = np.column_stack((2 * points[:, 0], 2 * points[:, 1], np.ones(len(points))))
        b = points[:, 0]**2 + points[:, 1]**2
        
        # Solve the system using least squares
        try:
            solution, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
            center_x, center_y, c = solution
            radius = np.sqrt(c + center_x**2 + center_y**2)
            
            # Calculate distances from center to all points
            distances = np.sqrt((points[:, 0] - center_x)**2 + (points[:, 1] - center_y)**2)
            
            # Calculate roundness (difference between max and min radius)
            roundness = np.max(distances) - np.min(distances)
            
            return (center_x, center_y), radius, roundness
        except np.linalg.LinAlgError:
            # Fallback to OpenCV's minEnclosingCircle if least squares fails
            (center_x, center_y), radius = cv2.minEnclosingCircle(np.array(points, dtype=np.int32))
            
            # Calculate distances from center to all points
            distances = np.sqrt((points[:, 0] - center_x)**2 + (points[:, 1] - center_y)**2)
            
            # Calculate roundness (difference between max and min radius)
            roundness = np.max(distances) - np.min(distances)
            
            return (center_x, center_y), radius, roundness
    
    def min_circumscribed_method(self, points):
        """
        Calculate roundness using minimum circumscribed circle method.
        
        Args:
            points (numpy.ndarray): Array of points (N, 2).
            
        Returns:
            tuple: Center coordinates (x, y), outer radius, inner radius, and roundness.
        """
        # Find the minimum enclosing circle (outer circle)
        points_int = np.array(points, dtype=np.int32)
        (center_x, center_y), outer_radius = cv2.minEnclosingCircle(points_int)
        
        # Calculate distances from center to all points
        distances = np.sqrt((points[:, 0] - center_x)**2 + (points[:, 1] - center_y)**2)
        
        # Find the minimum distance (inner radius)
        inner_radius = np.min(distances)
        
        # Calculate roundness (difference between outer and inner radius)
        roundness = outer_radius - inner_radius
        
        return (center_x, center_y), outer_radius, inner_radius, roundness
    
    def max_inscribed_method(self, points):
        """
        Calculate roundness using maximum inscribed circle method.
        
        Args:
            points (numpy.ndarray): Array of points (N, 2).
            
        Returns:
            tuple: Center coordinates (x, y), inner radius, outer radius, and roundness.
        """
        # Initial guess for center using centroid
        initial_center = np.mean(points, axis=0)
        
        # Define objective function to maximize (inner radius)
        def objective(center):
            center_x, center_y = center
            # Calculate distances from center to all points
            distances = np.sqrt((points[:, 0] - center_x)**2 + (points[:, 1] - center_y)**2)
            # Return the negative of the minimum distance (to maximize)
            return -np.min(distances)
        
        # Minimize the negative of the objective function
        result = minimize(objective, initial_center, method='Nelder-Mead')
        optimal_center = result.x
        
        # Calculate distances from optimal center to all points
        distances = np.sqrt((points[:, 0] - optimal_center[0])**2 + (points[:, 1] - optimal_center[1])**2)
        inner_radius = np.min(distances)
        outer_radius = np.max(distances)
        
        # Calculate roundness (difference between outer and inner radius)
        roundness = outer_radius - inner_radius
        
        return (optimal_center[0], optimal_center[1]), inner_radius, outer_radius, roundness
