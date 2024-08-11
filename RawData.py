from bs4 import BeautifulSoup
import requests
import json
import time
import os
import csv


url = 'https://www.qantas.com/hotels/properties/18482?adults=2&checkIn=2024-08-25&checkOut=2024-08-26&children=0&infants=0&location=London%2C%20England%2C%20United%20Kingdom&page=1&payWith=cash'  

response = requests.get(url) 

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

script_tag = soup.find("script", id="__NEXT_DATA__")

data = json.loads(script_tag.string)

propertyData = data['props']['pageProps']['initialState']['property']['property']
propertyName = propertyData['description']
CheckOut = propertyData['checkOutBefore']
CheckIn = propertyData['checkInAfter']
roomInformation = propertyData['roomInformation']
Facilities = propertyData['propertyFacilities']
policyDescription = propertyData['policyDescription']
Rating = propertyData['rating']
RoomType = propertyData['description']
CheckInInstruction = propertyData['checkInInstructions']
RoomType1 = propertyData['roomTypes']
RegionName = propertyData['regionFullName']
TimeZone = propertyData['timeZone']
Popularity = propertyData['popularity']
MandatoryFee = propertyData['mandatoryFeesDescription']
CustomerRating = propertyData['customerRatings']
RatingType = propertyData['ratingType']


# Extracting variables
propertyData = data['props']['pageProps']['initialState']['property']
description = propertyData
checkOut = propertyData
checkIn = propertyData
roomInformation = propertyData
facilities = propertyData
policyDescription = propertyData
rating = propertyData
checkInInstructions = propertyData
roomTypes = ', '.join(propertyData)
regionName = propertyData
timeZone = propertyData
popularity = propertyData
mandatoryFee = propertyData
customerRating = propertyData
ratingType = propertyData

# Creating a list of dictionaries to be written to CSV
csv_data = [{
    'Description': description,
    'CheckOut': checkOut,
    'CheckIn': checkIn,
    'RoomInformation': roomInformation,
    'Facilities': facilities,
    'PolicyDescription': policyDescription,
    'Rating': rating,
    'CheckInInstructions': checkInInstructions,
    'RoomTypes': roomTypes,
    'RegionName': regionName,
    'TimeZone': timeZone,
    'Popularity': popularity,
    'MandatoryFee': mandatoryFee,
    'CustomerRating': customerRating,
    'RatingType': ratingType
}]

# File path
file_path = 'RAW_property_data.csv'

# Writing data to CSV
with open(file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=csv_data[0].keys())
    writer.writeheader()
    writer.writerows(csv_data)

print(f"Data has been written to {file_path}")
