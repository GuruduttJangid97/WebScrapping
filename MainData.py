import json
import csv
import os
from datetime import datetime

file_path = 'data.json'

# Load JSON data from file
with open(file_path, 'r') as file:
    data = json.load(file)

# Function to process data and return a list of dictionaries
def process_data(data):
    rows = []
    for room_type in data.get('roomTypes', []):
        room_name = room_type.get('name', 'N/A')
        max_occupancy = room_type.get('maxOccupantCount', 'N/A')
        
        for offer in room_type.get('offers', []):
            checkin = offer.get('checkIn', 'N/A')
            checkout = offer.get('checkOut', 'N/A')
            rate_name = offer.get('name', 'N/A')
            cancellation_policy = offer.get('cancellationPolicy', {}).get('description', 'N/A')
            price = offer.get('charges', {}).get('total', {}).get('amount', 'N/A')
            currency = offer.get('charges', {}).get('total', {}).get('currency', 'N/A')
            
            # Default date format
            default_datein = "2024-08-17"
            default_dateout = "2024-08-18"
            # Use default dates if checkin or checkout are 'N/A'
            checkin = checkin if checkin != 'N/A' else default_datein
            checkout = checkout if checkout != 'N/A' else default_dateout
            
            # Safely handle promotion
            promotion = offer.get('promotion', {})
            if isinstance(promotion, dict):
                is_top_deal = 'Top Deal' in promotion.get('name', '')
            else:
                is_top_deal = False
            
            rows.append({
                'Room Name': room_name,
                'Max Occupancy': max_occupancy,
                'Rate Name': rate_name,
                'Checkin Date': checkin,
                'Checkout Date': checkout,
                'Cancellation Policy': cancellation_policy,
                'Price': price,
                'Currency': currency,
                'Is Top Deal': is_top_deal
            })
    
    return rows

# Function to sanitize folder names
def sanitize_folder_name(name):
    # Replace invalid characters with underscores
    return name.replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')

# Function to ensure directories exist
def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to export data to CSV in checkin and checkout directories
def export_to_csv(data):
    for entry in data:
        checkin_date = entry.get('Checkin Date', 'unknown')
        checkout_date = entry.get('Checkout Date', 'unknown')

        # Sanitize checkin and checkout dates for folder and file names
        sanitized_checkin_date = sanitize_folder_name(checkin_date)
        sanitized_checkout_date = sanitize_folder_name(checkout_date)
        
        # Create directories based on checkin and checkout dates
        checkin_folder = f"checkin_{sanitized_checkin_date}"
        checkout_folder = f"checkout_{sanitized_checkout_date}"
        ensure_directory(checkin_folder)
        ensure_directory(checkout_folder)
        
        # Define the output CSV file paths
        checkin_file_path = os.path.join(checkin_folder, f"checkin_{sanitized_checkin_date}.csv")
        checkout_file_path = os.path.join(checkout_folder, f"checkout_{sanitized_checkout_date}.csv")

        # Write checkin data to CSV file
        with open(checkin_file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=entry.keys())
            writer.writeheader()
            writer.writerow(entry)

        # Write checkout data to CSV file
        with open(checkout_file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=entry.keys())
            writer.writeheader()
            writer.writerow(entry)

# Main function
def main():
    processed_data = process_data(data)
    export_to_csv(processed_data)


# Entry point of the program
if __name__ == '__main__':
    main()
