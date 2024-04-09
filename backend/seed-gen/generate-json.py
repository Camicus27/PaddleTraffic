import json
import re
from datetime import datetime
""" Tranform pickle-head-*.json ->
{
    location: {
        name: string
        latitude: number
        longitude: number
        court_count: number
        courts_occupied: number
        number_waiting: number
        estimated_wait_time: number
        calculated_time: string
        city_state_country: string
    }
}
"""

def stripCityState(address):
    # This pattern is looking for the city, state, and country parts of the address.
    # It assumes that the state is two capital letters and the country, if present, follows after a comma.
    pattern = re.compile(r"([A-Za-z\s]+),\s*([A-Z]{2}),?\s*([A-Z]*)")
    match = pattern.search(address)
    if match:
        city = match.group(1).strip()
        state = match.group(2)
        country = 'USA'  # Default to USA if no country is specified
        if match.group(3):
            country = match.group(3)
        return f"{city}, {state}, {country}"
    else:
        return ""

def transformPickleHeads(picklehead_court):
    location = {
        'picklehead-id': picklehead_court['id'],
        'name': picklehead_court['title'],
        'latitude': picklehead_court['geometry']['coordinates'][1],
        'longitude': picklehead_court['geometry']['coordinates'][0],
        'court_count': picklehead_court['total_courts'],
        'courts_occupied': 0,
        'number_waiting': 0,
        'estimated_wait_time': 0,
        'calculated_time': datetime.now().timestamp(),
        'city_state_country': stripCityState(picklehead_court['address'])
    }
    return location
    

def transformAllPickleHeads(filename):
    locations = []
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        courts = data['courts']
        for court in courts:
            if court.get('total_courts', None) and court['total_courts'] > 0:
                locations.append(transformPickleHeads(court))
    return locations

def main():
    close_locations = transformAllPickleHeads('pickle-head-close.json')
    far_locations = transformAllPickleHeads('pickle-head-far.json')

    locations_dict = {}
    for location in close_locations + far_locations:
        if location['picklehead-id'] not in locations_dict:
            locations_dict[location['picklehead-id']] = location

    combined_locations = list(locations_dict.values())

    with open('pickle-data.json', 'w', encoding='utf-8') as file:
        json.dump({'locations': combined_locations}, file)
            
if __name__ == "__main__":
    main()

    