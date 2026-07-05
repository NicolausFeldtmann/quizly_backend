# quizly_backend

> A Python-based backend for managing quizzes, authentication, and machine learning components.

![GitHub stars](https://img.shields.io/github/stars/NicolausFeldtmann/quizly_backend?style=for-the-badge&logo=github) ![GitHub forks](https://img.shields.io/github/forks/NicolausFeldtmann/quizly_backend?style=for-the-badge&logo=github) ![GitHub issues](https://img.shields.io/github/issues/NicolausFeldtmann/quizly_backend?style=for-the-badge&logo=github) ![Last commit](https://img.shields.io/github/last-commit/NicolausFeldtmann/quizly_backend?style=for-the-badge&logo=github) ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## 📑 Table of Contents

- [Description](#description)
- [Key Features](#key-features)
- [Use Cases](#use-cases)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Key Dependencies](#key-dependencies)
- [Project Structure](#project-structure)
- [Development Setup](#development-setup)
- [Contributors](#contributors)
- [Contributing](#contributing)

## 📝 Description

quizly_backend is a Python-based server application designed to manage quiz delivery and user sessions. The system organizes its business logic into distinct application modules, separating identity management from quiz administration to maintain a clean and extensible codebase. It provides a structured foundation for developers looking to serve educational content with backend support for complex user flows.

## ✨ Key Features

- **🔐 Dedicated User Authentication** — Manages user access control, registration, and session states securely through the auth_app module.
- **📝 Modular Quiz Administration** — Handles quiz structures, questions, and submission processing within the specialized quizzes_app codebase.
- **⚙️ Django Management Interface** — Uses the standard manage.py entry point to run development servers, manage database schemas, and execute administrative commands.
- **🧠 Computational Evaluation Support** — Integrates PyTorch, TensorFlow, and NumPy to support analytical grading and machine learning model evaluations on quiz data.

## 🎯 Use Cases

- Serving as a backend API for web-based e-learning portals that require structured user authentication and exam management.
- Powering intelligent tutoring systems that process complex student answers using pre-trained machine learning models.

## 🛠️ Tech Stack

- 🐍 **Python**

**Notable libraries:** NumPy, PyTorch/TensorFlow

## ⚡ Quick Start

> The project is tested with Python 3.12.x. Using a different Python version can lead to dependency resolution errors such as the Triton or Python-version mismatch you saw.

```bash
# 1. Clone the repository
git clone https://github.com/NicolausFeldtmann/quizly_backend.git

# 2. Create and activate a virtual environment with Python 3.12
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel

# 3. Install PyTorch first, matching your hardware
# CPU-only (recommended for most local setups):
pip install torch==2.12.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
# CUDA 13 (GPU):
#   pip install --index-url https://download.pytorch.org/whl/cu13 torch==2.12.1

# 4. Install the remaining Python dependencies
pip install -r requirements.txt

# 5. Apply database migrations and start the project
python manage.py migrate
python manage.py runserver
```

## 📦 Key Dependencies

```
annotated-types: 0.7.0
anyio: 4.14.0
asgiref: 3.11.1
certifi: 2026.6.17
cffi: 2.0.0
charset-normalizer: 3.4.7
cryptography: 49.0.0
distro: 1.9.0
Django: 6.0.6
django-cors-headers: 4.9.0
djangorestframework: 3.17.1
djangorestframework_simplejwt: 5.5.1
```

## 📁 Project Structure

```
.
├── auth_app
│   ├── __init__.py
│   ├── admin.py
│   ├── api
│   │   ├── authentications.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── core
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── pyvenv.cfg
├── quizzes_app
│   ├── __init__.py
│   ├── admin.py
│   ├── api
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── utils.py
│   └── views.py
├── requirements.txt
└── share
    ├── bash-completion
    │   └── completions
    │       └── yt-dlp
    ├── doc
    │   └── yt_dlp
    │       └── README.txt
    ├── fish
    │   └── vendor_completions.d
    │       └── yt-dlp.fish
    ├── man
    │   └── man1
    │       ├── isympy.1
    │       └── yt-dlp.1
    └── zsh
        └── site-functions
            └── _yt-dlp
```

## 🛠️ Development Setup

### Python
1. Install Python 3.12.x.
2. Create a virtual environment.
3. Activate the environment.
4. Install PyTorch first.
5. Install the remaining requirements.
6. Start the project.

- Windows:
```powershell
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip setuptools wheel
pip install torch==2.12.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

- Unix/MacOS:
```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install torch==2.12.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 👥 Contributors

Thanks to everyone who has contributed to this project:

<p align="left">
<a href="https://github.com/NicolausFeldtmann" title="NicolausFeldtmann"><img src="https://avatars.githubusercontent.com/u/175417512?v=4&s=64" width="64" height="64" alt="NicolausFeldtmann" style="border-radius:50%" /></a>
</p>

[See the full list of contributors →](https://github.com/NicolausFeldtmann/quizly_backend/graphs/contributors)

## 👥 Contributing

Contributions are welcome! Here's the standard flow:

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/NicolausFeldtmann/quizly_backend.git`
3. **Branch**: `git checkout -b feature/your-feature`
4. **Commit**: `git commit -m 'feat: add some feature'`
5. **Push**: `git push origin feature/your-feature`
6. **Open** a pull request

Please follow the existing code style and include tests for new behavior where applicable.

---
