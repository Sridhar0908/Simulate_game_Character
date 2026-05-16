# 🎮 Simulate Game Character - 3D AI Generator

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com)
[![Hunyuan3D-2](https://img.shields.io/badge/Hunyuan3D-2.0-orange.svg)](https://github.com/Tencent/Hunyuan3D-2)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **AI-Powered Text-to-3D Game Character Generator** using Tencent's Hunyuan3D-2.0 and Stable Diffusion. Create game-ready 3D characters from simple text descriptions.

---

## ✨ Features

- 🎮 **Game Character Generation** - Create characters for RPG, FPS, fantasy games
- 🖼️ **Interactive 3D Preview** - Rotate, zoom, pan with Three.js viewer
- ⬇️ **Download GLB** - Export to Blender, Unity, Unreal Engine
- 👤 **User System** - Sign up, login, save your generations
- 🎨 **High Quality** - Background removal, mesh cleanup, no artifacts
- 💻 **GPU Accelerated** - CUDA support for fast generation
- 🆓 **100% Free** - No API credits needed

---

## 🚀 Demo

| Feature | Preview |
|---------|---------|
| Generate Page | ![Generate](generate.png) |
| 3D Preview | ![Preview](screenshots/preview.png) |
| Home page | ![Home](screenshots/home.png) |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Flask, Flask-Login, Flask-SQLAlchemy |
| **3D Generation** | Hunyuan3D-2.0, Stable Diffusion v1.5 |
| **3D Viewer** | Three.js, GLTFLoader |
| **Database** | SQLite |
| **AI/ML** | PyTorch, Transformers, Diffusers |
| **Mesh Processing** | Trimesh, Rembg |

---

## 📦 Installation

### Prerequisites

- Python 3.10+
- NVIDIA GPU with 6GB+ VRAM (recommended)
- CUDA 12.1+ drivers
- [Hugging Face](https://huggingface.co) account + API token

### Step 1: Clone Repository

```bash
git clone https://github.com/Sridhar0908/Simulate_game_Character.git
cd Simulate_game_Character
