from app import app, db, Product, Location, ProductMovement

def view_database():
    with app.app_context():
        print("=" * 50)
        print("INVENTORY DATABASE CONTENTS")
        print("=" * 50)
        
        # View Products
        print("\n📦 PRODUCTS:")
        print("-" * 30)
        products = Product.query.all()
        if products:
            for product in products:
                print(f"ID: {product.product_id}")
                print(f"Name: {product.name}")
                print(f"Description: {product.description or 'No description'}")
                print("-" * 20)
        else:
            print("No products found")
        
        # View Locations
        print("\n🏢 LOCATIONS:")
        print("-" * 30)
        locations = Location.query.all()
        if locations:
            for location in locations:
                print(f"ID: {location.location_id}")
                print(f"Name: {location.name}")
                print(f"Description: {location.description or 'No description'}")
                print("-" * 20)
        else:
            print("No locations found")
        
        # View Movements
        print("\n🔄 MOVEMENTS:")
        print("-" * 30)
        movements = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).limit(10).all()
        if movements:
            print("(Showing last 10 movements)")
            for movement in movements:
                print(f"ID: {movement.movement_id}")
                print(f"Product: {movement.product_id}")
                print(f"From: {movement.from_location or 'N/A'}")
                print(f"To: {movement.to_location or 'N/A'}")
                print(f"Quantity: {movement.qty}")
                print(f"Time: {movement.timestamp}")
                print("-" * 20)
        else:
            print("No movements found")
        
        # View Balance Summary
        print("\n📊 BALANCE SUMMARY:")
        print("-" * 30)
        balance_data = {}
        
        for movement in ProductMovement.query.all():
            product_id = movement.product_id
            qty = movement.qty
            
            if product_id not in balance_data:
                balance_data[product_id] = {}
            
            # Handle incoming movements (to_location)
            if movement.to_location:
                if movement.to_location not in balance_data[product_id]:
                    balance_data[product_id][movement.to_location] = 0
                balance_data[product_id][movement.to_location] += qty
            
            # Handle outgoing movements (from_location)
            if movement.from_location:
                if movement.from_location not in balance_data[product_id]:
                    balance_data[product_id][movement.from_location] = 0
                balance_data[product_id][movement.from_location] -= qty
        
        for product_id, locations_data in balance_data.items():
            print(f"Product: {product_id}")
            for location_id, qty in locations_data.items():
                if qty != 0:
                    print(f"  {location_id}: {qty}")
            print("-" * 15)

if __name__ == '__main__':
    view_database()
