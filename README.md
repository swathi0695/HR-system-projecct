# HR System - Django REST Application

This Django REST application serves as an HR system, providing APIs for managing employee data.

## Installation

To set up and run this application locally, follow these steps:

### Prerequisites

- Python 3.x installed
- Virtual environment (optional but recommended)

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/swathi0695/HR-system-project.git
    ```

2. Navigate to the project directory:

    ```bash
    cd HR-system-project
    ```

3. Create a `.env` file in the root directory and define your variables:
   ```bash
   
    # db_creds
    DB_HOST='localhost'
    DB_NAME='hr_data'
    DB_TABLE='employees'
    DB_USER=your_user_name
    DB_PASSWORD=your_password
    DB_PORT='5432'

    # pyspark_creds
    SPARK_APP_NAME='HRSystem'
    SPARK_JDBC_DRIVER_JAR=jdbc_jar_path
    SPARK_FORMAT='jdbc'
    SPARK_JDBC_URL='jdbc:postgresql://localhost:5432/hr_data'
    SPARK_DRIVER='org.postgresql.Driver'
    HADOOP_HOME=path_to_hadoop_home
   ```

5. (Optional) Create a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For Unix/Linux
    # or
    venv\Scripts\activate  # For Windows
    ```

6. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## How to Run

After installation, run the application using the following steps:

1. Apply migrations:

    ```bash
    python manage.py migrate
    ```

2. Start the development server:

    ```bash
    python manage.py runserver
    ```

The application will be available at `http://127.0.0.1:8000/`.

## Additional Notes

- Customize settings (database, environment variables, etc.) as needed in `settings.py`.
- Ensure you have appropriate permissions and setup for database connections (if applicable).
