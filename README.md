
# Chat Application Backend

This is the backend for a chat application built using Django and WebSockets. The frontend for this application is developed in Next.js and is hosted in a separate repository.

## Features

- Real-time chat functionality using WebSockets
- User authentication
- Message storage and retrieval
- Support for multiple chat rooms

## Technologies Used

- **Django**: A high-level Python web framework
- **Django Channels**: To handle WebSocket connections
- **Django REST Framework**: For creating a RESTful API
- **PostgreSQL**: Database for storing user and chat data

## Installation

### Prerequisites

- Python 3.8 or higher
- Django 3.2 or higher
- PostgreSQL
- pip

### Clone the Repository

```bash
git clone https://github.com/kappalasaimohith/CHAT_APP_BACKEND
cd CHAT_APP_BACKEND
```

### Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Setup the Database

1. Create a PostgreSQL database for the chat application.
2. Update the database settings in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<your-database-name>',
        'USER': '<your-database-user>',
        'PASSWORD': '<your-database-password>',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```

### Run Migrations

```bash
python manage.py migrate
```

### Create a Superuser

```bash
python manage.py createsuperuser
```

### Run the Development Server

```bash
python manage.py runserver
```

## WebSocket Configuration

Ensure that your `routing.py` is properly configured to handle WebSocket connections. 

```python
# Example configuration
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from your_app.consumers import ChatConsumer

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [
                path("ws/chat/<str:room_name>/", ChatConsumer.as_asgi()),
            ]
        )
    ),
})
```

## Frontend

The frontend of this application is built using Next.js and is located in a separate repository. Ensure to connect to this backend service by updating the API endpoints accordingly.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Django Documentation
- Django Channels Documentation
- Next.js Documentation
```
