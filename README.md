# Flask Base

## Introduction 🚀

Flask Base is a web server application built using the Flask framework. It is designed to efficiently manage data for companies, employees, and users stored in a MySQL database. 
The application offers a RESTful API that allows users to perform crud operations for companies, employees, and users. Additionally, 
Flask Base provides robust user authentication and management features, ensuring secure access to resources. 
It also offers valuable statistical insights related to employees and companies, enabling better decision-making and performance evaluation. 
The entire application is containerized using Docker, simplifying deployment and scalability while maintaining flexibility and efficiency in managing company and employee data.

## Features 🧐

**Data Management (CRUD Operations):** Easily perform crud operations for companies, employees, and users using a user-friendly RESTful API.

**Authentication and User Management:** Secure user authentication with role-based access control (RBAC) ensures efficient user management, empowering administrators.

**Statistical Insights:** Access comprehensive statistics encompassing employee performance, departmental efficiency, and salary distribution for informed, data-driven decision-making.

**Dockerized Deployment:** Docker containerization simplifies deployment and scalability across diverse environments.

## Requirements 🛠️

- **Python 3.11:** Ensure you have Python 3.11 or a compatible version installed on your system.

- **Python Libraries:** Install the required Python libraries using the provided Pipfile.lock file. You can use `pipenv` to install the dependencies.

## ⚙️ Configuration

### Environment Variables

1. Create a `.env` file in the project root directory.

2. Set the following environment variables in the `.env` file:

   ```plaintext
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=your_email_password
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=465
   MAIL_USE_SSL=True
   MAIL_USE_TLS=False
   REGISTER_TOKEN_LIFESPAN=60000
   
   JWT_COOKIE_SECURE=True
   JWT_TOKEN_LOCATION=["cookies"]
   JWT_SECRET_KEY=super-secret
   JWT_ACCESS_TOKEN_EXPIRES=600
   JWT_REFRESH_TOKEN_EXPIRES=7200
   JWT_COOKIE_CSRF_PROTECT=False
   
   COMPANY_CONSTRAINTS=your_company_constraints
   EMPLOYEE_CONSTRAINTS=your_employee_constraints
   USER_CONSTRAINTS=your_user_constraints
   ```

## 🚀 Running
To run this application locally, follow these steps:

1. **Prerequisites**:
   - Make sure you have Docker and Docker Compose installed on your system. If not, you can download and install them from the official Docker website: [Docker Installation](https://www.docker.com/get-started).
2. **Clone the Repository**:
   ```shell
   git clone <repository_name>
   ```
3. **Navigate to the Project's Root Directory**:
   ```shell
   cd <project_root_directory>
   ```
4. **Configure Environment Variables**:
   - Create a `.env` file in the project's root directory and configure the necessary environment variables. You can use the provided `.env.example` file as a template.
5. **Build and Start Docker Containers**:
   - Run the following command to build and start the Docker containers for the application:
     ```shell
     docker-compose up -d --build
     ```
6. **Apply Database Migrations**:
   - After the containers are up and running, apply the database migrations using Alembic. Replace `a7` with the actual name of your Flask container:
     ```shell
     docker exec -it <flask_container_name> alembic upgrade head
     ```
7. **Access the Application**:
   - Your application should now be accessible at [http://localhost:8000](http://localhost:8000). You can explore the API endpoints and use the Postman collection for testing and interacting with the application.


## 📖 Documentation

### Postman Collection

To facilitate quick testing and integration, a Postman collection is included in the project. It contains pre-configured requests for various API actions, allowing users to easily test the application.

### Codebase Comments

The codebase is well-commented, providing insights into the project's architecture, function descriptions, and class explanations. These comments make it easier for developers to navigate and understand the source code.

### Development Environment Setup

The README file provides instructions on setting up the development environment, including dependencies, Docker containerization, and environment variables.
Ten fragment zawiera opis dokumentacji w formacie Markdown.
