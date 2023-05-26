# Food Order Management App
This is a simple Food Order Management application built with FastAPI and MySQL. It provides RESTful endpoints for creating, updating, deleting, and retrieving orders, as well as user authentication using JWT bearer tokens.

# Features
1. User Signup: Users can create an account by providing their email, name, and password.
2. User Login: Existing users can log in using their email and password.
3. Order Creation: Users can create orders by selecting food items, specifying quantities, and confirming the order.
4. Order Listing: Users can view a list of their orders.
5. Order Details: Users can view details of a specific order, including item names, quantities, and an option to delete the order.
6. Order Deletion: Users can delete an order from the order details page.

# Technologies Used
1. FastAPI
2. MySQL

# Getting Started
1. Clone the repository:
```
git clone git@github.com:shobhamrj/food-order-app.git
```
2. Install the Python dependencies:
```
pip install -r requirements.txt
```
3. Update the database configuration in a new .env file:
```
DB_HOST=""
DB_PASS=""
DB_USER=""
DB_DATABASE=""
DB_PORT=""

```
4. Create the database and the tables by running the queries in food_order.sql:

5. Start the FastAPI server:
```
uvicorn app:app --reload
```
6. Open your web browser and navigate to this url to access the application.
```
http://localhost:8000
```
7. FastAPI also generated a Swagger Docs for the API endpoints.

# Directory Structure
main.py: The main FastAPI application file, with route handlers.
config.py: contains a class to populate environment variables
auth.py: Utilities for handling token validations and authentication.
db.py: Database configurations
models.py: models representing FoodItems, User and Order.
food_order.sql: Database querries for generating tables.
requirements.txt: dependencies for this application.
README.md: This README file.

# Improvements
The database configuration, API endpoints, and add frontend to fit the specific requirements can be added.
Popular frontend framework like React can be used for better UI experience and client side functionalities.
