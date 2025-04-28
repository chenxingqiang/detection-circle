import cv2
import numpy as np

class ContourProcessor:
    """
    Class for processing and filtering contours.
    """
    
    def filter_contours(self, contours, min_area=100, min_perimeter=100):
        """
        Filter contours based on shape properties.
        
        Args:
            contours (list): List of contours.
            min_area (float): Minimum contour area.
            min_perimeter (float): Minimum contour perimeter.
            
        Returns:
            list: Filtered list of contours.
        """
        filtered_contours = []
        
        for contour in contours:
            # Calculate contour area and perimeter
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            
            # Filter based on area and perimeter
            if area > min_area and perimeter > min_perimeter:
                # Calculate circularity (4*pi*area/perimeter^2)
                # A perfect circle has circularity = 1
                circularity = 4 * np.pi * area / (perimeter * perimeter)
                
                # Filter based on circularity
                if circularity > 0.7:  # Threshold for circular shapes
                    filtered_contours.append(contour)
        
        return filtered_contours
    
    def single_line_processing(self, contour):
        """
        Convert contour to single-line representation.
        
        Args:
            contour (numpy.ndarray): Input contour.
            
        Returns:
            numpy.ndarray: Single-line contour.
        """
        # Approximate the contour to reduce the number of points
        epsilon = 0.005 * cv2.arcLength(contour, True)
        approx_contour = self.approximate_contour(contour, epsilon)
        
        # Convert to single line (remove nested structure)
        single_line = approx_contour.reshape(-1, 2)
        
        return single_line
    
    def approximate_contour(self, contour, epsilon):
        """
        Approximate a contour using the Douglas-Peucker algorithm.
        
        Args:
            contour (numpy.ndarray): Input contour.
            epsilon (float): Maximum distance from contour to approximated contour.
            
        Returns:
            numpy.ndarray: Approximated contour.
        """
        approx_contour = cv2.approxPolyDP(contour, epsilon, True)
        return approx_contour
