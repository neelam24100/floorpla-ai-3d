FloorScan — Autonomous Structural Intelligence System

🚀 Overview

FloorScan is an AI-assisted system that converts a 2D floor plan into a structured engineering analysis pipeline.

It performs:

- Floor plan parsing (walls + rooms)
- Geometry abstraction
- 3D structural modeling
- Material selection using engineering tradeoffs
- Explainable reasoning for decisions

---

🧠 Pipeline (5 Stages)

1️⃣ Floor Plan Parsing

- Edge detection (Canny)
- Wall detection (Hough Transform)
- Room detection (Contours)

2️⃣ Geometry Reconstruction

- Walls treated as structural edges
- Boundary + span logic for classification

3️⃣ 3D Model Generation

- Wall-based extrusion
- Load-bearing vs partition visualization

4️⃣ Material Analysis

- Weighted scoring:
  - Strength
  - Cost
  - Durability
- Outputs ranked material options

5️⃣ Explainability

- Each decision includes:
  - Reason
  - Structural logic
  - Risk insights

---

⚙️ Tech Stack

- Python
- OpenCV
- NumPy
- Matplotlib

---

📂 Project Structure

├── main.py              # Main pipeline code
├── input/              # Input images
├── output/             # Generated outputs
├── README.md

---

▶️ How to Run

1. Clone the repository

git clone https://github.com/YOUR_USERNAME/floorscan.git
cd floorscan

2. Install dependencies

pip install opencv-python numpy matplotlib

3. Add your floor plan

- Place image inside "input/"
- Update path in "main.py"

4. Run the project

python main.py

---

📊 Output

- Detected walls and rooms (2D)
- 3D structural visualization
- Material recommendations
- Engineering explanations

---

🧠 Key Features

- Real-world scaling (pixel → meter)
- Load-bearing detection
- Span-based risk analysis
- Multi-material ranking
- Explainable AI decisions

---

⚠️ Limitations

- Assumes orthogonal floor plans
- No door/window detection (future work)
- Geometry graph is simplified

---

🏁 Future Improvements

- Full graph-based geometry reconstruction
- Door/window detection
- Web-based interactive 3D visualization

---

👥 Team

- Your Team Name

---

🏆 Hackathon Submission

Technovate 7.0 — Prompt Coding
PS2: Autonomous Structural Intelligence System

---

💡 Final Note

This system focuses on engineering reasoning + explainability, not just image processing. 
