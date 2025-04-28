import cv2
import numpy as np

class ImageProcessor:
    """
    Class for processing images to prepare them for contour detection.
    """
    
    def load_image(self, image_path):
        """
        Load an image from a file path.
        
        Args:
            image_path (str): Path to the image file.
            
        Returns:
            numpy.ndarray: The loaded image.
        """
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Failed to load image from {image_path}")
        return image
    
    def preprocess(self, image):
        """
        Preprocess the image for edge detection.
        
        Args:
            image (numpy.ndarray): The input image.
            
        Returns:
            numpy.ndarray: The preprocessed image.
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        return blurred
    
    def detect_edges(self, image):
        """
        Detect edges in the preprocessed image.
        
        Args:
            image (numpy.ndarray): The preprocessed image.
            
        Returns:
            numpy.ndarray: The edge image.
        """
        # Apply Canny edge detection
        edges = cv2.Canny(image, 50, 150)
        
        # Apply morphological operations to close gaps in the edges
        kernel = np.ones((3, 3), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)
        edges = cv2.erode(edges, kernel, iterations=1)
        
        return edges
    
    def extract_contours(self, edge_image):
        """
        Extract contours from the edge image.
        
        Args:
            edge_image (numpy.ndarray): The edge image.
            
        Returns:
            list: List of contours.
        """
        # Find contours in the edge image
        contours, _ = cv2.findContours(edge_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Ensure we return a list
        return list(contours)
