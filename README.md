
# 🚀 Quizly Backend API

<div align="center">

[![GitHub stars](https://img.shields.io/github/stars/NicolausFeldtmann/quizly_backend?style=for-the-badge)](https://github.com/NicolausFeldtmann/quizly_backend/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/NicolausFeldtmann/quizly_backend?style=for-the-badge)](https://github.com/NicolausFeldtmann/quizly_backend/network)
[![GitHub issues](https://img.shields.io/github/issues/NicolausFeldtmann/quizly_backend?style=for-the-badge)](https://github.com/NicolausFeldtmann/quizly_backend/issues)
[![GitHub license](https://img.shields.io/github/license/NicolausFeldtmann/quizly_backend?style=for-the-badge)](LICENSE)

**A robust and scalable backend API for the Quizly application, powering user authentication, quiz creation, question management, and score tracking.**

</div>

## 📖 Overview
https://github.com/NicolausFeldtmann/quizly_backend/
The Quizly Backend API serves as the central data and logic hub for the Quizly application. Built with Django and Django REST Framework, it provides a secure and efficient set of RESTful endpoints to manage users, quizzes, questions, answers, and user performance. This backend is designed to be highly extensible and ready for integration with a variety of frontend clients (web, mobile, desktop).

## ✨ Features

-   🎯 **User Authentication & Authorization**: Secure user registration, login, and token-based authentication (likely JWT or Django's built-in token system based on `auth_app`).
-   📝 **Quiz Management**: Create, retrieve, update, and delete quizzes with various categories and difficulty levels.
-   ❓ **Question & Answer Handling**: Define multiple-choice questions, associate them with quizzes, and manage correct answers.
-   📊 **User Score Tracking**: Record and retrieve user scores for completed quizzes.
-   🔗 **RESTful API Interface**: Clean and well-structured API endpoints for seamless frontend integration.
-   🔒 **Secure & Scalable**: Designed with security best practices and built on a robust framework for scalability.

## 🛠️ Tech Stack

**Backend:**
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-A71C0F?style=for-the-badge&logo=django-rest-framework&logoColor=white)](https://www.django-rest-framework.org/)

**Database:**
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/) (Recommended for production)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/index.html) (Default for development)

**Tools:**
[![Pip](https://img.shields.io/badge/pip-2B3B48?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/pip/)
[![Virtualenv](https://img.shields.io/badge/virtualenv-337F39?style=for-the-badge&logo=python&logoColor=white)](https://virtualenv.pypa.io/en/latest/)

## 🚀 Quick Start

Follow these steps to get the Quizly Backend API up and running on your local machine.

### Prerequisites
-   **Python 3.12 or higher: Ensure you have Python 3.12 + installed.
-   **pip**: Python package installer (comes with Python).
-   **virtualenv**: Recommended for managing project dependencies.
-   **PostgreSQL (Optional)**: If you plan to use PostgreSQL, ensure it's installed and running. Otherwise, SQLite will be used by default.

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/NicolausFeldtmann/quizly_backend.git
    cd quizly_backend
    ```

2.  **Create and activate a virtual environment**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Install "ffmpeg"**
    - For Windows
    ```
    Download from https://ffmpeg.org/download.html
    Unzip in "C:\ffmpeg" and add to path.
    ```
    - For MAC
    ```
    Install "Homebrew", if not allready installed: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    Install "ffmpeg": brew install ffmpeg
    ```
    - For Linux
    ```
    sudo apt install ffmpeg
    ```

5.  **Environment setup**
    Create a `.env` file in the project root based on a potential `.env.example` (or common Django settings) to store sensitive configuration.
    ```bash
    cp .env.example .env # If .env.example existed, otherwise create manually
    ```
    Configure your environment variables in `.env`. At a minimum, you'll need:
    ```ini
    GENAI_API_KEY=your_google_gemini_api_key_here (Generate your Gemini API Key at https://ai.google.dev/gemini-api/docs
    SECRET_KEY='your_secret_key_here'
    DEBUG=True for development, False for production
    ```
    If not using PostgreSQL, Django will default to SQLite, and `DATABASE_URL` is not strictly required in `.env` for initial setup.

6.  **Database setup**
    Apply database migrations to set up the schema.
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
    You might also want to create a superuser for accessing the Django admin interface:
    ```bash
    python manage.py createsuperuser
    ```

7.  **Start development server**
    ```bash
    python manage.py runserver
    ```

8.  **Access the API**
    The API will be running at `http://localhost:8000/`. You can access the Django Admin at `http://localhost:8000/admin/`.

## 📁 Project Structure

```
quizly_backend/
├── .gitignore              # Specifies intentionally untracked files to ignore
├── README.md               # Project documentation
├── auth_app/               # Django app for user authentication and authorization
│   ├── migrations/         # Database migration files for auth models
│   ├── admin.py            # Admin interface configuration for auth models
│   ├── apps.py             # App configuration
│   ├── models.py           # Database models for users, tokens, etc.
│   ├── views.py            # API views for authentication endpoints
│   └── urls.py             # URL routing for auth_app API endpoints
├── core/                   # Main project configuration and global settings
│   ├── __init__.py         # Python package marker
│   ├── settings.py         # Main Django settings file
│   ├── urls.py             # Root URL routing for the entire project
│   └── wsgi.py             # WSGI configuration for production deployment
├── manage.py               # Django's command-line utility
├── pyvenv.cfg              # Virtual environment configuration
├── quizzes_app/            # Django app for managing quizzes, questions, and scores
│   ├── migrations/         # Database migration files for quiz models
│   ├── admin.py            # Admin interface configuration for quiz models
│   ├── apps.py             # App configuration
│   ├── models.py           # Database models for quizzes, questions, answers, scores
│   ├── views.py            # API views for quiz and question endpoints
│   └── urls.py             # URL routing for quizzes_app API endpoints
├── requirements.txt        # List of Python dependencies
└── share/                  # (Potentially) Shared utilities, static files, or documentation
```

## ⚙️ Configuration

### Environment Variables
Sensitive information and environment-specific settings should be managed via environment variables, typically loaded from a `.env` file.

| Variable        | Description                                                  | Default      | Required |
|-----------------|--------------------------------------------------------------|--------------|----------|
| `GENAI_API_KEY` | Your Google Gemini API Key. [(ai.google.dev)](https://ai.google.dev/gemini-api/docs)         | `None`       | Yes      |
| `SECRET_KEY`    | A unique, secret key for Django project security.            | `None`       | Yes      |
| `DEBUG`         | Enables/disables debug mode. Set to `False` in production.   | `False`      | Yes      |

### Configuration Files
-   `core/settings.py`: The main Django settings file where you configure installed apps, middleware, database connections, static files, etc.
-   `core/urls.py`: The root URL configuration, which includes URLs from individual apps (`auth_app`, `quizzes_app`).
-   `[app_name]/urls.py`: Individual app-specific URL configurations.

## 🔧 Development

### Available Scripts
| Command                            | Description                                     |
|------------------------------------|-------------------------------------------------|
| `python manage.py runserver`       | Starts the Django development server.           |
| `python manage.py makemigrations`  | Creates new database migrations based on model changes. |
| `python manage.py migrate`         | Applies pending database migrations.            |
| `python manage.py createsuperuser` | Creates an administrative user for the Django admin. |
| `python manage.py shell`           | Opens an interactive Python shell with Django context. |

### Development Workflow
1.  Ensure your virtual environment is activated (`source venv/bin/activate`).
2.  Make changes to your Python code (models, views, serializers).
3.  If you modify database models, run `python manage.py makemigrations` and `python manage.py migrate`.
4.  Restart the development server if you change `settings.py` or new code doesn't reflect immediately.

## 🧪 Testing

The project uses Django's built-in testing framework.

```bash
# Run all tests
python manage.py test

# Run tests for a specific app (e.g., auth_app)
python manage.py test auth_app
```

## 🚀 Deployment

### Production Build
Django projects don't have a "build" step like frontend applications. Deployment typically involves:
1.  Installing dependencies in a production environment.
2.  Configuring `settings.py` for production (e.g., `DEBUG=False`, `ALLOWED_HOSTS`, static file settings).
3.  Running `python manage.py collectstatic` to gather static files.
4.  Running `python manage.py migrate` to ensure the database schema is up to date.

### Deployment Options
-   **WSGI Server**: Use a production-ready WSGI server like Gunicorn or uWSGI.
-   **Web Server**: Use a web server like Nginx or Apache to serve static files and proxy requests to the WSGI server.
-   **Cloud Platforms**: Deploy to platforms like Heroku, AWS Elastic Beanstalk, Google Cloud App Engine, or a custom VPS.

## 📚 API Reference

The Quizly Backend API provides a set of RESTful endpoints. Documentation for these endpoints (e.g., using `drf-yasg` or `Django REST Swagger`) would typically be found here if generated.

### Authentication
-   Users authenticate by sending credentials to a login endpoint (e.g., `/api/auth/login/`) to receive an authentication token.
-   This token must be included in the `Authorization` header (`Bearer <token>` or `Token <token>`) for all protected endpoints.

### Endpoints
**Authentication (`/api/auth/`)**
-   `POST /api/auth/register/`: Register a new user.
-   `POST /api/auth/login/`: Authenticate and receive a token.
-   `POST /api/auth/logout/`: Invalidate the current user's token.
-   `GET /api/auth/user/`: Retrieve the authenticated user's profile.

**Quizzes (`/api/quizzes/`)**
-   `GET /api/quizzes/`: List all available quizzes.
-   `POST /api/quizzes/`: Create a new quiz (requires authentication).
-   `GET /api/quizzes/{id}/`: Retrieve a specific quiz and its questions.
-   `PUT /api/quizzes/{id}/`: Update a quiz (requires authentication).
-   `DELETE /api/quizzes/{id}/`: Delete a quiz (requires authentication).

**Questions (`/api/questions/`)**
-   `GET /api/quizzes/{quiz_id}/questions/`: List questions for a specific quiz.
-   `POST /api/quizzes/{quiz_id}/questions/`: Add a question to a quiz (requires authentication).

**Scores (`/api/scores/`)**
-   `POST /api/quizzes/{quiz_id}/submit-answers/`: Submit answers for a quiz and record the score.
-   `GET /api/users/{user_id}/scores/`: Retrieve scores for a specific user.

*(Note: Actual endpoint paths and methods may vary based on `urls.py` and `views.py` implementations.)*

## 🤝 Contributing

We welcome contributions! If you're interested in improving Quizly Backend, please follow these general guidelines:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and ensure tests pass.
4.  Submit a pull request with a clear description of your changes.

### Development Setup for Contributors
The development setup is the same as the Quick Start guide. Please ensure your code adheres to PEP 8 guidelines.

## 📄 License

This project is licensed under the **[MISSING_LICENSE_INFORMATION]** - see the `LICENSE` file for details (TODO: Add LICENSE file).

## 🙏 Acknowledgments

-   Built with **Python** and the **Django** framework.
-   Leverages **Django REST Framework** for powerful API creation.
-   Powered by the strong community and extensive ecosystem of Python.

## 📞 Support & Contact

-   🐛 Issues: [GitHub Issues](https://github.com/NicolausFeldtmann/quizly_backend/issues)

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with by [NicolausFeldtmann](https://github.com/NicolausFeldtmann)

</div>
