import random
import sys
import time
import requests


user_agents = ['Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0',
               'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
               'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0']


# takes server list outputs locations (each only once) the servers are in.
def get_unique_locations(list_of_servers):
    unique_locations = []
    resolved_locations = []
    locations_count = 0

    for aServer in list_of_servers:
        latLongDic = {"lat": aServer["location"]["lat"], "long": aServer["location"]["long"]}
        if latLongDic not in unique_locations:
            unique_locations.append(latLongDic)
    # print(unique_locations)
    for eachLocation in unique_locations:
        user_agent = {'User-Agent': user_agents[locations_count % 6],
                      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
        geo_address_list = get_locations(eachLocation, user_agent)
        time.sleep(random.randrange(1, 5, 1) * 0.1)
        # geo_address_list = get_location_name(latitude=latitude, longitude=longitude)
        resolved_locations.append(geo_address_list)
        locations_count += 1
    # print("resolved_locations", resolved_locations)
    return resolved_locations


def get_locations(location_dic, req_headers):
    latitude = location_dic["lat"]
    longitude = location_dic["long"]

    url = 'https://nominatim.openstreetmap.org/reverse?format=jsonv2'
    params = "&lat={lat}&lon={lon}".format(
        lat=latitude,
        lon=longitude
    )
    final_url = url + params
    # print("req_headers", req_headers)
    r = requests.get(final_url, headers=req_headers)
    geo_address_list = []
    name_list = []
    try:
        response = r.json()
        results = response['address']
        # print(results)
    except IndexError:
        print("IndexError: Looks like you have reached Google maps API's daily \
request limit. No location data for you :( you could restart your router to get a new IP.")
        sys.exit()

    geo_address_list.append(location_dic)

    for key in results:
        # print(results["city"])
        if key == "country_code":
            geo_address_list.insert(0, results["country"])
        if key == "village":
            name_list.append(results["village"])
        if key == "city":
            name_list.append(results["city"])
        if key == "suburb":
            name_list.append(results["suburb"])
        if key == "region":
            name_list.append(results["region"])
        if key == "state":
            name_list.append(results["state"])
        if key == "state_district":
            name_list.append(results["state_district"])
    geo_address_list.insert(2, name_list)
    print(geo_address_list)
    return geo_address_list


def get_location_name(location_dic):
    latitude = location_dic["lat"]
    longitude = location_dic["long"]
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = "latlng={lat},{lon}&sensor={sen}".format(
        lat=latitude,
        lon=longitude,
        sen='false'
    )
    final_url = url + "?" + params
    r = requests.get(final_url)
    geo_address_list = []
    name_list = []
    try:
        response = r.json()
        results = response['results'][0]['address_components']
        # print(results)
    except IndexError:
        print("IndexError: Looks like you have reached Google maps API's daily \
request limit. No location data for you :( you could restart your router to get a new IP.")
        sys.exit()
    country = None
    geo_address_list.append(location_dic)
    for c in results:
        if "administrative_area_level_2" in c['types']:
            city_name1 = c['short_name']
            name_list.append(city_name1.lower())
        if "locality" in c['types']:
            city_name2 = c['long_name']
            name_list.append(city_name2.lower())
        if "administrative_area_level_1" in c['types']:
            area_name = c['long_name']
            name_list.append(area_name.lower())
        if "administrative_area_level_1" in c['types']:
            area_name_short = c['short_name']
            name_list.append(area_name_short.lower())
        if "country" in c['types']:
            country = c['short_name']
            geo_address_list.insert(0, country.lower().split(" "))
    geo_address_list.insert(2, name_list)
    # print(geo_address_list)
    return geo_address_list
