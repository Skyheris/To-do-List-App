# TODO LIST
#### Video Demo: https://youtu.be/zoRhSgXZXbo
#### PS: Sorry for the bad audio, there has a problem while recording...

The TO-DO App is a robust, full-stack web application designed to help users organize their daily lives with efficiency and security. Developed using the Flask framework and SQLite, the project emphasizes clean architecture, relational database integrity, and a modern, responsive user interface. It moves beyond a simple checklist by providing a personalized environment where multiple users can manage their private data safely.

## Core Functionalities

### 🛡️ Secure User Authentication & Authorization
At the heart of the application is a reliable security layer. Users can register and log in to access their private dashboards.

The system utilizes PBKDF2 password hashing via the Werkzeug library, ensuring that sensitive credentials are never stored in plain text.

Session-based persistence tracks the user_id throughout the navigation, preventing unauthorized access to private routes.

### 🗂️ Relational Data Management (The Multi-User Engine)
- The application is built to scale for multiple users.

- By implementing a One-to-Many relationship, every task is strictly linked to a specific user via a Foreign Key (user_id).

- The database uses SQLite's INTEGER PRIMARY KEY AUTOINCREMENT logic to ensure flawless data tracking and unique identification for every entry.

### ✍️ Dynamic Task Creation & Detailed Planning
- Users are not limited to just a title. The creation flow allows for:

- Descriptive context: Adding optional details to tasks to provide more information.

- Deadline tracking: Integration with datetime-local inputs to set specific time limits, stored in the database as structured timestamps.

### ⚡ High-Performance Dynamic Editing (JavaScript Integration)
- One of the most advanced features of this project is the Single-Modal Editing System.

- Instead of cluttering the HTML with hundreds of hidden pop-ups, the app uses a single Bootstrap Modal.

- A custom Vanilla JavaScript script intercepts clicks, extracts metadata from data-* attributes, and injects the information into the modal on the fly. This keeps the DOM light and the application fast.

### ✅ Intelligent State Toggling
- Managing progress is intuitive. Users can mark tasks as "Completed" or "Pending" with a single click.

- The backend handles these transitions using optimized SQL UPDATE queries.

- The frontend provides instant visual feedback through Bootstrap Badges, using conditional logic to change colors and icons based on the task's boolean state.

### 🗑️ Secure and Cascading Deletion
- Data safety is enforced even during removal.

- The delete functionality requires both the task_id and the session["user_id"] to match, preventing malicious users from deleting tasks via URL manipulation.

- The database schema includes ON DELETE CASCADE policies, ensuring that if a user account is removed, all associated tasks are automatically cleaned up.

### Technical Stack

- Backend: Python 3, Flask, Flask-Session.

- Database: SQLite3 (Relational).

- Frontend: HTML5, CSS3, JavaScript (ES6+).

- Styling: Bootstrap 5 (Grid System, Modals, Cards, Floating Labels).

- Templating: Jinja2 (Inheritance, Filters, and Conditionals).
