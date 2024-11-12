# Note Taking Journal
#### Video Demo:  https://youtu.be/xDwk_c9P7-Q
#### Description:

# Personal Journal Web App

## Overview

This Personal Journal Web App is a simple web application built with Python and Flask, allowing users to create, edit, and manage journal entries. It also includes basic user authentication, ensuring that each user’s entries are private and secure. The app uses SQLite for data storage, making it lightweight and easy to set up without external database dependencies.

This project demonstrates essential web development concepts, such as user authentication, CRUD operations, and templating with HTML, making it an excellent choice for learning Flask and Python web applications.

## Features

1. **User Registration and Login**: Users can create accounts and log in, ensuring privacy for each user’s journal entries.
2. **CRUD Operations for Entries**: Users can create, edit, view, and delete their journal entries.
3. **SQLite Database**: The app uses an SQLite database to store user information and journal entries.
4. **Simple User Interface**: A minimal HTML and CSS design provides a clean and responsive layout.
5. **Navigation and Flash Messages**: Provides feedback to users for successful actions, errors, and form validations.

## Project Structure

```
journal_app/
├── app.py                 # Main Flask application
├── database.db            # SQLite database file
├── templates/             # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── entry.html
│   └── edit_entry.html
└── static/
    └── styles.css         # CSS file for styling
```

- **app.py**: Contains the Flask app logic, routes, and database interactions.
- **database.db**: SQLite database where user data and entries are stored.
- **templates/**: HTML templates that make up the UI.
- **static/styles.css**: CSS file to style the HTML templates.

## Code Explanation

### app.py

This is the main application file. It imports necessary libraries, initializes the Flask app, and defines routes and helper functions.

#### Key Components:

1. **Database Setup**:
   - `connect_db()`: Connects to the SQLite database.
   - `init_db()`: Creates tables for `users` and `entries` if they do not exist, including columns for user credentials and entry details.
   
2. **User Authentication**:
   - Passwords are hashed using `werkzeug.security` functions for security.
   - User sessions are managed with Flask’s session to track login status.
   - `login_required` is a decorator function that restricts routes to authenticated users only.

3. **Routes**:
   - `/`: Redirects to the login page by default.
   - `/register`: Displays a registration form and handles new user registration, storing hashed passwords securely.
   - `/login`: Manages user login by verifying hashed passwords and setting a session variable.
   - `/logout`: Clears the session and redirects to the login page.
   - `/dashboard`: Displays the user’s journal entries in reverse chronological order.
   - `/entry`: Allows users to create a new journal entry.
   - `/edit/<int:entry_id>`: Allows users to edit an existing entry.
   - `/delete/<int:entry_id>`: Deletes a specified entry belonging to the user.

### Templates

1. **`base.html`**: A base template extended by other templates. It includes navigation and flash messages to notify users of success or error messages.
2. **`register.html`**: A registration form where users can create a new account.
3. **`login.html`**: A login form for users to enter their username and password.
4. **`dashboard.html`**: Displays all entries for the logged-in user, with links to create, edit, or delete entries.
5. **`entry.html`**: A form for creating a new journal entry, including fields for the title and content.
6. **`edit_entry.html`**: Similar to `entry.html`, but used for editing existing entries. The form is pre-filled with the current entry data.

### CSS (styles.css)

This file provides basic styling to enhance readability and usability. It styles elements like buttons, forms, navigation, and lists, making the app more visually appealing.

## Installation and Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ProPlazys1913/journal_app.git
   cd journal_app
   ```

2. **Install Dependencies**:
   Make sure you have Flask installed:
   ```bash
   pip install flask
   ```
4. **Run the Application**:
   Start the app with:
   ```bash
   flask run
   ```
   The app will be accessible at `http://127.0.0.1:5000`.

## Usage

1. **Register**: Start by creating a new user account through the registration form.
2. **Login**: Log in with your registered credentials to access the dashboard.
3. **Dashboard**: After logging in, you’ll be directed to your dashboard where you can:
   - View all your journal entries.
   - Create a new entry by clicking “Create New Entry.”
   - Edit or delete existing entries.
4. **Logout**: Log out from the app using the “Logout” button in the navigation.
