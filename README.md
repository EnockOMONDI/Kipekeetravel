# Kipekee Travelmaster

Kipekee Travelmaster is a Django-based web application designed for managing travel bookings, events, and user interactions. It provides a comprehensive platform for users to explore destinations, book tours, and manage events.

## Project Structure

- **tours_travels/**: Main project directory containing settings and configuration files.
  - `settings.py`: Configuration for the Django project.
  - `urls.py`: URL routing for the project.
  - `mail.py`: Email configuration and utilities.
  - `views.py`: General views for the project.

- **dede/**: Core app for managing destinations and tours.
  - `models.py`: Database models for destinations and tours.
  - `views.py`: Views for handling requests related to destinations and tours.
  - `urls.py`: URL patterns for the `dede` app.
  - `admin.py`: Admin interface configuration for the `dede` app.

- **events/**: App for managing events.
  - `models.py`: Database models for events.
  - `views.py`: Views for handling event-related requests.
  - `urls.py`: URL patterns for the `events` app.
  - `forms.py`: Forms for event creation and management.

- **users/**: App for user management and authentication.
  - `models.py`: User-related database models.
  - `views.py`: Views for user authentication and profile management.
  - `urls.py`: URL patterns for the `users` app.
  - `forms.py`: Forms for user registration and login.

- **static/**: Directory for static files like CSS, JavaScript, and images.

- **templates/**: Directory for HTML templates used across the project.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd KipekeeTravelmaster
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the Application**:
   - Open your web browser and go to `http://127.0.0.1:8000/` to access the application.

## Features

- **Destination Management**: Explore and manage travel destinations.
- **Tour Booking**: Book tours and view tour details.
- **Event Management**: Create and manage events.
- **User Authentication**: Register, login, and manage user profiles.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.