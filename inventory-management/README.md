# Inventory Management System

A comprehensive Flask-based web application for managing inventory across multiple warehouse locations.

## Features

- **Product Management**: Add, edit, and view products with unique IDs
- **Location Management**: Manage warehouse and store locations
- **Movement Tracking**: Record product movements between locations
- **Balance Reports**: View current stock levels across all locations
- **Responsive Design**: Modern Bootstrap-based UI

## Database Schema

### Tables
- **Product**: `product_id` (PK), `name`, `description`
- **Location**: `location_id` (PK), `name`, `description`
- **ProductMovement**: `movement_id` (PK), `timestamp`, `from_location`, `to_location`, `product_id`, `qty`

### Movement Types
- **Stock In**: Leave `from_location` empty, specify `to_location`
- **Stock Out**: Specify `from_location`, leave `to_location` empty
- **Transfer**: Specify both `from_location` and `to_location`

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. (Optional) Load sample data:
```bash
python sample_data.py
```

## Usage

1. **Dashboard**: Overview of all modules with quick access buttons
2. **Products**: Manage your inventory items
3. **Locations**: Set up warehouse and store locations
4. **Movements**: Record all product movements
5. **Balance Report**: View current stock levels in a grid format

## Sample Data

The application includes sample data with:
- 4 products (Laptop, Mouse, Chair, Monitor)
- 4 locations (2 warehouses, 2 stores)
- 26 movements demonstrating various scenarios

## Technology Stack

- **Backend**: Flask, SQLAlchemy
- **Frontend**: Bootstrap 5, Font Awesome
- **Database**: SQLite
- **Python**: 3.7+

## License

This project is open source and available under the MIT License.
