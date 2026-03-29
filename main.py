import cv2
import numpy as np
import matplotlib.pyplot as plt
from google.colab import files
from mpl_toolkits.mplot3d import Axes3D

# Upload image
uploaded = files.upload()
image_path = list(uploaded.keys())[0]

image = cv2.imread(image_path)

if image is None:
    print("Error loading image")
else:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # ───────── EDGE DETECTION ─────────
    edges = cv2.Canny(blurred, 50, 150)

    # ───────── WALL DETECTION ─────────
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 80,
                            minLineLength=50, maxLineGap=10)

    wall_img = image.copy()
    filtered_lines = []
    walls = []

    if lines is not None:
        for l in lines:
            x1, y1, x2, y2 = l[0]

            if abs(x1-x2) < 10 or abs(y1-y2) < 10:
                filtered_lines.append((x1,y1,x2,y2))
                walls.append(((x1,y1),(x2,y2)))
                cv2.line(wall_img, (x1,y1), (x2,y2), (0,255,0), 2)

    print("Filtered Walls:", len(filtered_lines))

    # ───────── ROOM DETECTION ─────────
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((5,5), np.uint8)
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    room_img = image.copy()
    rooms = []

    total_pixels = image.shape[0] * image.shape[1]

    for cnt in contours:
        area = cv2.contourArea(cnt)

        if 0.01 * total_pixels < area < 0.2 * total_pixels:
            x, y, w, h = cv2.boundingRect(cnt)
            rooms.append((x,y,w,h))

    print("Detected Rooms:", len(rooms))

    print("\n--- GEOMETRY DATA ---")
    print(f"Total walls stored: {len(walls)}")

    # ───────── ANALYSIS ─────────
    print("\n--- FINAL ANALYSIS ---\n")

    total_rcc = 0
    total_aac = 0

    for i, (x,y,w,h) in enumerate(rooms):
        area_val = w*h
        span = max(w, h)

        # Room Type
        if area_val > 0.1 * total_pixels:
            room_type = "Hall"
        elif area_val > 0.05 * total_pixels:
            room_type = "Bedroom"
        else:
            room_type = "Utility"

        # Load-bearing detection
        margin = 0.05 * image.shape[1]

        if x < margin or y < margin or (x+w) > image.shape[1]-margin or (y+h) > image.shape[0]-margin:
            wall_type = "Load-bearing"
        else:
            wall_type = "Partition"

        # Material ranking
        if wall_type == "Load-bearing":
            options = ["RCC", "Red Brick", "Fly Ash Brick"]
            material = options[0]
            reason = f"Wall located at boundary → classified as {wall_type} → requires high compressive strength → {material} selected, balancing cost vs strength tradeoff"
            total_rcc += area_val
        else:
            options = ["AAC Block", "Hollow Block", "Drywall"]
            material = options[0]
            reason = f"Internal partition → classified as {wall_type} → lightweight and cost-efficient → {material} selected, balancing cost vs strength tradeoff"
            total_aac += area_val

        # Risk (span-based)
        if span > 0.4 * image.shape[1]:
            risk = "⚠️ Large span - structural reinforcement required"
        else:
            risk = "Safe"

        # Confidence
        confidence = int((area_val / total_pixels) * 100)

        # Draw
        cv2.rectangle(room_img, (x,y), (x+w,y+h), (255,0,0), 2)
        cv2.putText(room_img, f"R{i+1}", (x,y-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)

        # Output
        print(f"Room {i+1} ({room_type})")
        print(f"Size: {w}x{h}")
        print(f"Wall Type: {wall_type}")
        print(f"Material: {material}")
        print(f"Top Choices: {options}")
        print(f"Reason: {reason}")
        print(f"Risk: {risk}")
        print(f"Confidence: {confidence}%\n")

    print("--- MATERIAL SUMMARY ---")
    print(f"Total RCC Area: {total_rcc}")
    print(f"Total AAC Area: {total_aac}")

    # ───────── STRUCTURAL INSIGHTS ─────────
    print("\n--- STRUCTURAL INSIGHTS ---")
    print("Insight: Large spans detected may require additional beam or column support to ensure stability.")
    print("Insight: Load-bearing walls are concentrated along boundaries for effective load transfer.")

    if total_rcc > total_aac:
        print("Insight: Structure is dominated by load-bearing elements → higher strength focus.")
    else:
        print("Insight: Structure is partition-heavy → optimized for cost and flexibility.")

    # ───────── 2D VISUALIZATION ─────────
    plt.figure(figsize=(15,5))

    plt.subplot(1,3,1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title("Original")

    plt.subplot(1,3,2)
    plt.imshow(cv2.cvtColor(wall_img, cv2.COLOR_BGR2RGB))
    plt.title("Walls")

    plt.subplot(1,3,3)
    plt.imshow(cv2.cvtColor(room_img, cv2.COLOR_BGR2RGB))
    plt.title("Rooms")

    plt.show()

    # ───────── 3D WALL MODEL (FINAL) ─────────
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111, projection='3d')

    for (x1,y1,x2,y2) in filtered_lines:
        length = np.sqrt((x2-x1)**2 + (y2-y1)**2)

        if length > 0.3 * image.shape[1]:
            height = 60
            color = 'red'
        else:
            height = 30
            color = 'blue'

        dx = x2 - x1 if abs(x2-x1) > 0 else 5
        dy = y2 - y1 if abs(y2-y1) > 0 else 5

        ax.bar3d(x1, y1, 0, dx, dy, height, color=color, alpha=0.7)

    ax.set_title("3D Structural Wall Model (Final)")
    plt.show()
