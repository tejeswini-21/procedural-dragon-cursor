# procedural-dragon-cursor
# 🐉 Procedural Skeleton Dragon Cursor

An interactive, real-time visual project built in Python using **Pygame**. The program hides the default system cursor canvas restrictions and generates a skeletal, multi-jointed reptile/dragon structure that organically chases your mouse cursor pointer around the screen.

The layout features dynamic movement loops calculated using basic **Inverse Kinematics** and vector geometry formulas.

## 🚀 Visual Features
- **Dynamic Spine Chain:** A 32-joint central backbone that trailing-interpolates behind the mouse.
- **Perpendicular Rib Sweep:** A rib cage structure that automatically shifts and bends backwards dynamically during turns.
- **Multi-Jointed Leg Rigs:** Front and rear limb anchors that bend realistically at the elbows and ankles based on movement speed.
- **Minimalist Aesthetic:** A sleek white wireframe skeleton rendered over a pure cinematic black canvas.

## 🛠️ How to Run Locally

### 1. Prerequisites
Make sure you have Python installed on your system. You will also need the `pygame` library.

### 2. Installation
Open your terminal or PyCharm terminal and install the required package:
```bash
pip install pygame
```

### 3. Execution
Download or copy the code from `main.py` into your environment, save it, and run the file:
```bash
python main.py
```

Move your cursor inside the window to interact with the skeleton physics!

## 📜 Code Architecture Notes
This project was built to explore intermediate Python applications outside standard command-line tools. It maps real-time user inputs (`pygame.mouse.get_pos`) into relative matrix point lines using distance constraints (`math.hypot`) and trigonometry angles (`math.atan2`).
