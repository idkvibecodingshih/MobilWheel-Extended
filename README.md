# 🚗 MobilWheel-Extended

MobilWheel-Extended is a Python-based system that transforms a smartphone into a steering wheel and control device for PC games.

It allows real-time input streaming from a mobile device (gyro, buttons, etc.) and maps it to a virtual controller on the PC, creating a low-cost and flexible driving setup.

---

## 🧠 Overview

The system works as a bridge between:

📱 Mobile device → 🖥️ Python server → 🎮 Virtual controller (Xbox via ViGEm)

It supports real-time communication, input mapping, and optional web-based control interfaces.

---

## ⚙️ Features

- 📡 Real-time data streaming (TCP / UDP)
- 🎮 Virtual Xbox controller emulation (ViGEmBus)
- 📱 Mobile input support (gyro, steering, buttons)
- 🧠 Custom input mapping system
- 🌐 Optional web dashboard (HTTP / WebSocket)
- ⚡ Low latency communication
- 🧩 Modular backend architecture

---

## 🏗️ Architecture


Mobile Device
↓
(Network: TCP / UDP)
↓
Python Server (MobilWheel)
↓
Input Mapping System
↓
Virtual Controller (ViGEm - Xbox)
↓
Game (Forza, BeamNG, etc.)


---

## 🔧 Technologies Used

- Python
- Socket (TCP / UDP)
- ViGEmBus (Virtual Gamepad Emulation)
- vgamepad
- WebSocket / HTTP server (optional)
- PyQt (optional UI)
- HTML frontend (optional)

---

## 🚀 How It Works

1. The mobile device sends input data (steering, buttons, etc.)
2. The Python server receives and processes the data
3. Inputs are mapped to a virtual Xbox controller
4. The game reads the controller as a real device

---

## 📦 Installation

### 1. Install dependencies

```bash
pip install vgamepad
