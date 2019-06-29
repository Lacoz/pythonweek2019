from requests_html import HTMLSession
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--source")
parser.add_argument("--destination")
parser.add_argument("--departure_date")
args = parser.parse_args()


session = HTMLSession()
r = session.get('https://www.studentagency.cz/data/wc/ybus-form/destinations-sk.json')
site_data = r.json()

def get_city_id(city_name, site_data):
    for dest in site_data['destinations']:
        for city in dest['cities']:
            if city_name in city['name']:
                return city['id']


source_id = get_city_id(args.source,site_data)
destination_id = get_city_id(args.destination,site_data)
departure_date = args.departure_date


s_url = "https://brn-ybus-pubapi.sa.cz/restapi/routes/search/simple"


r = session.get(s_url, params = {'locale':'sk',
                        'departureDate':departure_date,
                        'fromLocationId':source_id,
                        'toLocationId':destination_id,
                        'fromLocationType':'CITY',
                        'toLocationType':'CITY',
                        'tarrifs':'REGULAR'})
routes_data = r.json()


output = []
for route in routes_data['routes']:
    output.append({
        'departure_datetime': route['departureTime'],
        'arrival_datetime': route['arrivalTime'],
        'source': args.source,
        'destinations': args.destination,
        'price': route['priceFrom'],
        'type': ''.join(route['vehicleTypes']).lower(),
        'source_id': route['departureStationId'],
        'destination_id': route['arrivalStationId'],
        'free_seats': route['freeSeatsCount'],
        'carrier': 'Student Agency'
    })

print(output)
