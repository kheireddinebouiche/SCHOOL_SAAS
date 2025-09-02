# SCHOOL_SAAS - Django SaaS Application for Educational Institutions

A multi-tenant SaaS platform built with Django for managing educational institutions, students, courses, and administrative tasks.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Overview

SCHOOL_SAAS is a comprehensive multi-tenant Software as a Service (SaaS) solution designed for educational institutions. The platform allows managing multiple institutions (tenants) from a single codebase, each with their own isolated data, students, courses, staff, and administrative functions.

The system implements a hierarchical structure where:
- **Master tenant** manages all institutions
- **Individual institutions** operate as separate tenants with their own data
- **Users** can belong to specific institutions with role-based access

## Features

### Core Modules
1. **Institution Management**
   - Multi-tenant architecture with Django-Tenants
   - Institution profile and settings
   - Domain management

2. **Student Management**
   - Student profiles with personal information
   - Enrollment and registration tracking
   - Document management
   - Academic records

3. **Course & Formation Management**
   - Course catalog management
   - Specialization programs
   - Curriculum planning
   - Module organization

4. **CRM System**
   - Prospect tracking
   - Visitor management
   - Lead conversion
   - Appointment scheduling
   - Follow-up reminders

5. **Human Resources**
   - Employee management
   - Payroll processing
   - Attendance tracking
   - Performance evaluation

6. **Examination System**
   - Exam scheduling
   - Grade management
   - Result processing

7. **Financial Management**
   - Fee management
   - Payment tracking
   - Financial reporting

8. **Internship Management**
   - Internship placement tracking
   - Company partnerships
   - Progress monitoring

9. **Dashboard & Reporting**
   - Analytics dashboard
   - Custom reports
   - Data visualization

## Technology Stack

- **Backend**: Python 3.x, Django 5.1.4
- **Database**: PostgreSQL with Django-Tenants
- **Frontend**: HTML, CSS, JavaScript (with some table_view.js)
- **Authentication**: Django Auth System
- **Static Files**: Django Static Files Handling
- **Internationalization**: French (fr-fr)

## Project Structure

```
SCHOOL_SAAS/
├── app/                 # Main application with tenant models
├── institut_app/        # Institution-specific application
├── school/              # Django project settings
├── t_crm/               # Customer Relationship Management
├── t_etudiants/         # Student management
├── t_formations/        # Course and formation management
├── t_rh/                # Human resources
├── t_exam/              # Examination system
├── t_tresorerie/        # Financial management
├── t_stage/             # Internship management
├── t_commercial/        # Commercial operations
├── t_config/            # Configuration management
├── t_groupe/            # Group management
├── t_conseil/           # Advisory services
├── t_dashboard/         # Dashboard and analytics
├── static_in_inv/       # Static files
├── profile_images/      # User profile images
├── templates/           # HTML templates
└── manage.py            # Django management script
```

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Virtual environment tool (venv or virtualenv)

### Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SCHOOL_SAAS
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   - Create a PostgreSQL database named `insim`
   - Update database credentials in `school/settings.py` if needed
   - Default credentials:
     - USER: postgres
     - PASSWORD: 1230042690
     - HOST: localhost
     - PORT: 5432

5. **Run migrations**
   ```bash
   python manage.py migrate
   python manage.py migrate --database=your_tenant_name  # For each tenant
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## Configuration

### Database Configuration
Update the `DATABASES` setting in `school/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Tenant Settings
- `TENANT_MODEL`: "app.Institut"
- `TENANT_DOMAIN_MODEL`: "app.Domaine"

### Static and Media Files
- `STATIC_URL`: '/static/'
- `MEDIA_URL`: '/media/'
- `STATIC_ROOT`: Project-level static directory
- `MEDIA_ROOT`: Project-level media directory

## Usage

### Creating a New Institution (Tenant)
1. Access the Django admin panel
2. Create a new Institut entry
3. Add a corresponding Domaine entry
4. Run tenant-specific migrations

### Managing Institutions
- Access institution-specific dashboards
- Manage students, courses, and staff
- Generate reports and analytics

### User Roles
The system supports different user roles with appropriate permissions:
- Super Admin (Master tenant)
- Institution Admin
- Staff members
- Students

## Development

### Code Structure
The application follows Django best practices with a multi-app architecture:
- Each module is separated into its own Django app
- Shared functionality in the main `app` directory
- Tenant-specific functionality in respective `t_*` apps

### Adding New Features
1. Create a new Django app if needed
2. Add models following the existing patterns
3. Register models in admin.py
4. Create views and templates
5. Update URL configurations

### Running Tests
```bash
python manage.py test
```

### Code Quality
- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to models and complex functions
- Keep functions small and focused

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

Please ensure your code follows the existing style and includes appropriate tests.

## License

This project is proprietary and confidential. All rights reserved.

## Contact

For support or inquiries, please contact the development team.