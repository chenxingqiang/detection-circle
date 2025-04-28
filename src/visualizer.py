import cv2
import numpy as np
import matplotlib.pyplot as plt

class Visualizer:
    """
    Class for visualizing images, contours, and circles.
    """
    
    def display_image(self, image, title="Image"):
        """
        Display an image using matplotlib.
        
        Args:
            image (numpy.ndarray): The image to display.
            title (str): Title for the image.
        """
        # Convert BGR to RGB for matplotlib
        if len(image.shape) == 3 and image.shape[2] == 3:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            image_rgb = image
            
        plt.figure(figsize=(10, 8))
        plt.imshow(image_rgb, cmap='gray' if len(image.shape) == 2 else None)
        plt.title(title)
        plt.axis('off')
        plt.tight_layout()
        plt.show()
    
    def draw_contours(self, image, contours, color=(0, 255, 0), thickness=2):
        """
        Draw contours on an image.
        
        Args:
            image (numpy.ndarray): The image to draw on.
            contours (list): List of contours.
            color (tuple): BGR color for contours.
            thickness (int): Line thickness.
            
        Returns:
            numpy.ndarray: Image with contours drawn.
        """
        # Create a copy of the image to avoid modifying the original
        result = image.copy()
        
        # Draw all contours
        cv2.drawContours(result, contours, -1, color, thickness)
        
        return result
    
    def draw_circles(self, image, circles, color=(0, 0, 255), thickness=2):
        """
        Draw circles on an image.
        
        Args:
            image (numpy.ndarray): The image to draw on.
            circles (list): List of circles, each represented as (center_x, center_y, radius).
            color (tuple): BGR color for circles.
            thickness (int): Line thickness.
            
        Returns:
            numpy.ndarray: Image with circles drawn.
        """
        # Create a copy of the image to avoid modifying the original
        result = image.copy()
        
        # Draw all circles
        for circle in circles:
            center_x, center_y, radius = circle
            center = (int(center_x), int(center_y))
            radius = int(radius)
            
            # Draw the circle
            cv2.circle(result, center, radius, color, thickness)
            
            # Draw the center
            cv2.circle(result, center, 5, color, -1)
        
        return result
    
    def visualize_roundness(self, image, inner_circle, outer_circle, method_name=""):
        """
        Visualize roundness calculation by drawing inner and outer circles.
        
        Args:
            image (numpy.ndarray): The image to draw on.
            inner_circle (tuple): Inner circle (center_x, center_y, radius).
            outer_circle (tuple): Outer circle (center_x, center_y, radius).
            method_name (str): Name of the roundness calculation method.
            
        Returns:
            numpy.ndarray: Image with roundness visualization.
        """
        # Create a copy of the image to avoid modifying the original
        result = image.copy()
        
        # Draw inner circle
        center_x, center_y, radius = inner_circle
        center = (int(center_x), int(center_y))
        radius = int(radius)
        cv2.circle(result, center, radius, (0, 255, 0), 2)
        
        # Draw outer circle
        center_x, center_y, radius = outer_circle
        center = (int(center_x), int(center_y))
        radius = int(radius)
        cv2.circle(result, center, radius, (0, 0, 255), 2)
        
        # Draw center
        cv2.circle(result, center, 5, (255, 0, 0), -1)
        
        # Calculate roundness
        roundness = outer_circle[2] - inner_circle[2]
        
        # Add text with roundness value
        text = f"{method_name} Roundness: {roundness:.2f} pixels"
        cv2.putText(result, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        return result
    
    def save_image(self, image, filename):
        """
        Save an image to a file.
        
        Args:
            image (numpy.ndarray): The image to save.
            filename (str): Path to save the image.
        """
        cv2.imwrite(filename, image)
