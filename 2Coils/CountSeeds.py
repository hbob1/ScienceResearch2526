import cv2
import numpy as np

def count_seeds(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not load image")
        return

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)

    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    kernel = np.ones((3, 3), np.uint8)
    clean = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    contours, _ = cv2.findContours(clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    seed_count = len(contours)
    print(f"Number of seeds: {seed_count}")

    output = image.copy()
    cv2.drawContours(output, contours, -1, (0, 255, 0), 2)
    cv2.namedWindow("Detected Seeds", cv2.WINDOW_NORMAL)
    cv2.imshow("Detected Seeds", output)
    cv2.resizeWindow("Detected Seeds", 800, 600)
    cv2.namedWindow("Original", cv2.WINDOW_NORMAL)
    cv2.imshow("Original", image)
    cv2.resizeWindow("Original", 800, 600)
    cv2.namedWindow("Threshold", cv2.WINDOW_NORMAL)
    cv2.imshow("Threshold", clean)
    cv2.resizeWindow("Threshold", 800, 600)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return seed_count

count_seeds("C:/Users/marik\Documents/000/2025/ScienceResearch_2025_26/Images/SeedImages1/IMG_2003.JPG")  # replace with your image file
