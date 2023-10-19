# Importing OpenCV  
import cv2 
  
  
# Getting the kernel to be used in Top-Hat 
filterSize =(3, 3) 
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,  
                                   filterSize) 
  
# Reading the image named 'input.jpg' 
input_image = cv2.imread("data/image.jpg") 
input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY) 
  
# Applying the Top-Hat operation 
tophat_img = cv2.morphologyEx(input_image,  
                              cv2.MORPH_TOPHAT, 
                              kernel) 
  
cv2.imshow("original", input_image) 
cv2.imshow("tophat", tophat_img) 
cv2.waitKey(20000) 