import cv2
import numpy as np

class CircleDetector:
    """
    Class for detecting circles from contours.
    """
    
    def detect_circles(self, contours):
        """
        Detect circles from contours.
        
        Args:
            contours (list): List of contours.
            
        Returns:
            list: List of detected circles, each represented as (center_x, center_y, radius).
        """
        circles = []
        
        for contour in contours:
            if self.is_circle(contour):
                # Fit a circle to the contour
                center, radius = self.fit_circle(contour.reshape(-1, 2))
                circles.append((center[0], center[1], radius))
        
        return circles
    
    def fit_circle(self, points):
        """
        Fit a circle to a set of points using least squares method.
        
        Args:
            points (numpy.ndarray): Array of points (N, 2).
            
        Returns:
            tuple: Center coordinates (x, y) and radius.
        """
        # Convert points to float for better precision
        points = np.array(points, dtype=np.float64)
        
        # Calculate mean of x and y coordinates
        mean_x = np.mean(points[:, 0])
        mean_y = np.mean(points[:, 1])
        
        # Shift coordinates to origin
        shifted_x = points[:, 0] - mean_x
        shifted_y = points[:, 1] - mean_y
        
        # Calculate the coefficients of the circle equation
        # (x - a)^2 + (y - b)^2 = r^2
        # x^2 + y^2 - 2ax - 2by + a^2 + b^2 - r^2 = 0
        # x^2 + y^2 - 2ax - 2by + c = 0, where c = a^2 + b^2 - r^2
        
        # Formulate as a linear system
        A = np.column_stack((shifted_x, shifted_y, np.ones_like(shifted_x)))
        b = -(shifted_x**2 + shifted_y**2)
        
        # Solve the system using least squares
        try:
            solution, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
            a, b, c = solution
            
            # Calculate center and radius
            center_x = mean_x - a
            center_y = mean_y - b
            radius = np.sqrt(a**2 + b**2 - c)
            
            return (center_x, center_y), radius
        except np.linalg.LinAlgError:
            # Fallback to OpenCV's minEnclosingCircle if least squares fails
            (center_x, center_y), radius = cv2.minEnclosingCircle(np.array(points, dtype=np.int32))
            return (center_x, center_y), radius
    
    def is_circle(self, contour, circularity_threshold=0.8):
        """
        Check if a contour is approximately a circle.
        
        Args:
            contour (numpy.ndarray): Input contour.
            circularity_threshold (float): Threshold for circularity (0 to 1).
            
        Returns:
            bool: True if the contour is a circle, False otherwise.
        """
        # Calculate area and perimeter
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        
        # Calculate circularity (4*pi*area/perimeter^2)
        # A perfect circle has circularity = 1
        if perimeter == 0:
            return False
        
        circularity = 4 * np.pi * area / (perimeter * perimeter)
        
        # Check if circularity is above threshold
        return circularity > circularity_threshold
