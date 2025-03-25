# Seeker-Provider Matching Application

## Overview

The Seeker-Provider Matching Application is a Django REST Framework-based platform that facilitates seamless connections between service seekers and service providers across various categories.

### Key Features

- User Registration (Seekers and Providers)
- Service Category Management
- Intelligent Service Matching
- Match Request Handling
- Flexible Service Availability Options

## Project Structure

```
seeker_provider_project/
│
├── manage.py
├── seeker_provider/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── users/
│   ├── models.py
│   ├── views.py
│   └── serializers.py
│
├── services/
│   ├── models.py
│   ├── views.py
│   └── serializers.py
│
└── matching/
    ├── models.py
    ├── views.py
    └── services.py
```

## Prerequisites

- Python 3.9+
- Django 4.2+
- Django Rest Framework

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/seeker-provider-matching.git
cd seeker-provider-matching
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Setup Database
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create Superuser
```bash
python manage.py createsuperuser
```

6. Run Development Server
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `/api-auth/login/` - User Login
- `/api-auth/logout/` - User Logout

### Users
- `GET/POST /api/users/` - List/Create Users
- `GET/PUT/PATCH /api/users/{id}/` - Retrieve/Update User

### Services
- `GET/POST /api/service-categories/` - List/Create Service Categories
- `GET/POST /api/services/` - List/Create Services

### Matching
- `POST /api/match-requests/find_matches/` - Find Matching Services
- `GET/POST /api/match-requests/` - List/Create Match Requests

## User Types

1. **Service Seeker**
   - Search for services
   - Create match requests
   - View available services

2. **Service Provider**
   - Create service listings
   - Manage service categories
   - Respond to match requests

## Matching Algorithm

The application uses a basic matching algorithm considering:
- Service Category
- Price Range
- Availability Type
- Location Proximity

### Match Score Calculation
- Base score: 50 points
- Location match: +25 points
- Future iterations will include more sophisticated scoring

## Configuration

Key configuration files:
- `seeker_provider/settings.py` - Project settings
- `seeker_provider/urls.py` - URL routing

## Environment Variables

Recommended environment variables:
- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode setting
- `ALLOWED_HOSTS` - Permitted hosts

## Authentication

- Session-based authentication
- Permissions based on user type
- Restricted API access

## Future Roadmap

- Implement comprehensive review system
- Advanced matching algorithms
- Real-time notifications
- Enhanced location-based matching

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Charliemagne C. Malicay - charliemalicay@gmail.com

Project Link: [https://github.com/charliemalicay/seeker-provider-matching](https://github.com/yourusername/seeker-provider-matching)
