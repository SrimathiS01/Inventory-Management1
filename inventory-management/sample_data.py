import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Product, Location, ProductMovement
from datetime import datetime, timedelta
import random

def create_sample_data():
    with app.app_context():
        # Clear existing data
        ProductMovement.query.delete()
        Product.query.delete()
        Location.query.delete()
        
        # Create Products
        products = [
            Product(product_id='PROD001', name='Laptop Computer', description='High-performance business laptop'),
            Product(product_id='PROD002', name='Wireless Mouse', description='Ergonomic wireless mouse'),
            Product(product_id='PROD003', name='Office Chair', description='Comfortable ergonomic office chair'),
            Product(product_id='PROD004', name='Monitor 24"', description='24-inch LED monitor')
        ]
        
        for product in products:
            db.session.add(product)
        
        # Create Locations
        locations = [
            Location(location_id='WH001', name='Main Warehouse', description='Primary storage facility'),
            Location(location_id='WH002', name='Secondary Warehouse', description='Overflow storage facility'),
            Location(location_id='STORE001', name='Retail Store A', description='Downtown retail location'),
            Location(location_id='STORE002', name='Retail Store B', description='Mall retail location')
        ]
        
        for location in locations:
            db.session.add(location)
        
        db.session.commit()
        
        # Create 20+ Product Movements
        movements = []
        movement_counter = 1
        
        # Initial stock in movements
        initial_movements = [
            ('MOV001', None, 'WH001', 'PROD001', 50),
            ('MOV002', None, 'WH001', 'PROD002', 100),
            ('MOV003', None, 'WH001', 'PROD003', 25),
            ('MOV004', None, 'WH001', 'PROD004', 30),
            ('MOV005', None, 'WH002', 'PROD001', 30),
            ('MOV006', None, 'WH002', 'PROD002', 75),
        ]
        
        base_time = datetime.now() - timedelta(days=30)
        
        for i, (mov_id, from_loc, to_loc, prod_id, qty) in enumerate(initial_movements):
            movement = ProductMovement(
                movement_id=mov_id,
                timestamp=base_time + timedelta(hours=i),
                from_location=from_loc,
                to_location=to_loc,
                product_id=prod_id,
                qty=qty
            )
            movements.append(movement)
            movement_counter += 1
        
        # Transfer movements between warehouses and stores
        transfer_movements = [
            ('MOV007', 'WH001', 'STORE001', 'PROD001', 10),
            ('MOV008', 'WH001', 'STORE001', 'PROD002', 20),
            ('MOV009', 'WH001', 'STORE001', 'PROD003', 5),
            ('MOV010', 'WH001', 'STORE002', 'PROD001', 8),
            ('MOV011', 'WH001', 'STORE002', 'PROD002', 15),
            ('MOV012', 'WH001', 'STORE002', 'PROD004', 10),
            ('MOV013', 'WH002', 'STORE001', 'PROD001', 5),
            ('MOV014', 'WH002', 'STORE001', 'PROD002', 10),
            ('MOV015', 'WH002', 'STORE002', 'PROD001', 7),
            ('MOV016', 'WH002', 'STORE002', 'PROD002', 12),
        ]
        
        for i, (mov_id, from_loc, to_loc, prod_id, qty) in enumerate(transfer_movements):
            movement = ProductMovement(
                movement_id=mov_id,
                timestamp=base_time + timedelta(days=1, hours=i),
                from_location=from_loc,
                to_location=to_loc,
                product_id=prod_id,
                qty=qty
            )
            movements.append(movement)
            movement_counter += 1
        
        # Stock out movements (sales)
        stock_out_movements = [
            ('MOV017', 'STORE001', None, 'PROD001', 3),
            ('MOV018', 'STORE001', None, 'PROD002', 8),
            ('MOV019', 'STORE001', None, 'PROD003', 2),
            ('MOV020', 'STORE002', None, 'PROD001', 5),
            ('MOV021', 'STORE002', None, 'PROD002', 6),
            ('MOV022', 'STORE002', None, 'PROD004', 4),
        ]
        
        for i, (mov_id, from_loc, to_loc, prod_id, qty) in enumerate(stock_out_movements):
            movement = ProductMovement(
                movement_id=mov_id,
                timestamp=base_time + timedelta(days=2, hours=i),
                from_location=from_loc,
                to_location=to_loc,
                product_id=prod_id,
                qty=qty
            )
            movements.append(movement)
            movement_counter += 1
        
        # Additional restocking and transfers
        additional_movements = [
            ('MOV023', None, 'WH001', 'PROD003', 15),  # Restock chairs
            ('MOV024', None, 'WH002', 'PROD004', 20),  # Restock monitors
            ('MOV025', 'WH001', 'WH002', 'PROD001', 10),  # Transfer laptops
            ('MOV026', 'WH002', 'WH001', 'PROD002', 25),  # Transfer mice
        ]
        
        for i, (mov_id, from_loc, to_loc, prod_id, qty) in enumerate(additional_movements):
            movement = ProductMovement(
                movement_id=mov_id,
                timestamp=base_time + timedelta(days=3, hours=i),
                from_location=from_loc,
                to_location=to_loc,
                product_id=prod_id,
                qty=qty
            )
            movements.append(movement)
        
        # Add all movements to database
        for movement in movements:
            db.session.add(movement)
        
        db.session.commit()
        
        print(f"Sample data created successfully!")
        print(f"- {len(products)} products")
        print(f"- {len(locations)} locations")
        print(f"- {len(movements)} movements")

if __name__ == '__main__':
    create_sample_data()
