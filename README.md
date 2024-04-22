# User Authentication API

This API provides endpoints for user authentication and password management. It is built using Flask and SQLAlchemy and has a MySQL database backend.

## Base URL

The base URL for all endpoints is: `http://your-app-url/`

## Endpoints

### 1. User Registration

#### Request
` POST /register `

**Request Body**:
- `username` (string, required): The desired username for the new account.
- `email` (string, required): The email address for the new account.
- `password` (string, required): The desired password for the new account.

**Responses**:
- `201 Created`: Registration successful.
- `400 Bad Request`: Missing required fields or username/email already exists.
- `500 Internal Server Error`: An unexpected error occurred on the server.

### 2. User Login

#### Request
` POST /login `

**Request Body**:
- `email` (string, required): The email address for the account.
- `password` (string, required): The password for the account.

**Responses**:
- `200 OK`: Login successful.
- `400 Bad Request`: Missing required fields.
- `401 Unauthorized`: Invalid email or password.
- `500 Internal Server Error`: An unexpected error occurred on the server.

### 3. Forgot Password

#### Request
` POST /forgot-password `

**Request Body**:
- `email` (string, required): The email address associated with the account.

**Responses**:
- `200 OK`: Password reset instructions sent to the provided email.
- `400 Bad Request`: Missing email field.
- `404 Not Found`: No user found with the provided email.
- `500 Internal Server Error`: An unexpected error occurred on the server.

**Note**: This endpoint sends a password reset email with a unique token to the provided email address. The reset token can be used to reset the password by navigating to the appropriate reset password page or endpoint.

### 4. Logout

#### Request
` GET /logout ` 

This endpoint logs out the current user session.

**Responses**:
- `302 Found`: Redirects to the login page after logging out.

## Error Handling

All endpoints return appropriate HTTP status codes and JSON responses with error messages in case of failures or invalid requests.

## Libraries and Dependencies

This API uses the following libraries and dependencies:

- Flask: A lightweight Python web framework.
- SQLAlchemy: A Python SQL toolkit and Object-Relational Mapping (ORM) library.
- PyMySQL: A Pure Python MySQL driver.
- bcrypt: A library for hashing and checking passwords.
- python-dotenv: A library for loading environment variables from a `.env` file.