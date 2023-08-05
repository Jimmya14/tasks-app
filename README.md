
Note : The os being used is Windows
# Getting Started
This project is a Flask application that performs CRUD (Create, Read, Update, Delete) operations on a PostgreSQL database for a Tasks resource using REST APIs. The application provides HTTP endpoints to interact with the Task resource, allowing users to manage tasks efficiently.

To Test the REST APIs locally, do the following

## Requirements :
1. You should have python installed
2. you should have PostgreSQL installed


# Clone the repository:
```bash
git clone https://github.com/Jimmya14/tasks-app.git
```

# Navigate to the project directory:
```bash
cd <repository>
```

# Procedure
Step-1: Creating virtual enviroment
  ```bash
    python -m venv myenv
    myenv\Scripts\activate
  ```

Step-2: Installing libraries
  ```bash
    pip install -r requirements.txt
  ```

Step-3: Setup the .env file
  ```bash
    copy .env.example .env
  ```
  And replace all the envs with your corresponding ones


Step-4: Run
```bash
  > set FLASK_APP=app.py
  > set FLASK_ENV=development
  > flask run
```
You will also find attachment a Postman Collection and Environment
