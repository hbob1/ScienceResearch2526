import cv2
import numpy as np

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera not found")
        return

    ret, frame = cap.read()
    if not ret:
        print("Could not read from camera")
        return

    roi = cv2.selectROI("Select ROI", frame, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow("Select ROI")

    x, y, w, h = roi
    print(f"Selected ROI: x={x}, y={y}, w={w}, h={h}")

    counter = 0
    stripe_detected = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        roi_frame = frame[y:y+h, x:x+w]
        gray = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY_INV)

        black_pixels = cv2.countNonZero(thresh)

        if black_pixels > 1000:
            if not stripe_detected:
                counter += 1
                stripe_detected = True
                print(f"Turn count: {counter}")
        else:
            stripe_detected = False
            #print(str(black_pixels))

        cv2.imshow("ROI", roi_frame)
        cv2.imshow("Threshold", thresh)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
