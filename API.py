import requests
import json
import datetime as d
import pandas as pd

class color:
	"""
	"""
	PURPLE = '\033[95m'
	CYAN = '\033[96m'
	DARKCYAN = '\033[36m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	END = '\033[0m'

def location( address , filename_to_save="location.json"):
	"""
	"""

	url = "https://maps.googleapis.com/maps/api/geocode/json?"
	key = "AIzaSyBxKro3LSRlznGG61C6SPUVtrGPvdK9YCg"
	inputs = {"address":address, "key":key}

	result = requests.get(url, params=inputs)
	data = result.json()

	lat = data["results"][0]["geometry"]["location"]["lat"]
	lng = data["results"][0]["geometry"]["location"]["lng"]

	return [lat,lng]

def duration( start_string , end_string ):
	"""
	"""

	start = d.datetime.strptime(start_string,'%B %d').strftime('2017-%m-%d')
	end = d.datetime.strptime(end_string,'%B %d').strftime('2017-%m-%d')

	date_list = pd.date_range(start, end).tolist()

	return date_list 

def weather( latitude, longitude, time ):
	"""
	"""

	url = "https://api.darksky.net/forecast"
	key = "242ce562c19357ab55f05b7d5a622aea"
	string = url + "/" + key + "/" + str(latitude) + "," + str(longitude) + "," + str(time) + "?exclude=currently,minutely,flags"
	
	result = requests.get(string)
	data = result.json()

	# save this json data to file
	f = open( "w"+time[:10]+".json", "w" )
	string_data = json.dumps( data, indent=4 )
	f.write(string_data)
	f.close()

	# print("\nfile ", "w"+time[:10]+".json", " written.")

	pass 

def parse_json( filename ):
	"""
	"""

	f = open( filename, "r" )
	string_data = f.read()
	data = json.loads( string_data )

	max_temp = data["daily"]["data"][0]["apparentTemperatureMax"]
	min_temp = data["daily"]["data"][0]["apparentTemperatureMin"]
	summary = data["hourly"]["summary"]

	return [max_temp, min_temp, summary]

def packing_list( weather_list , date_list ):
	"""
		weather_list is a list of lists
		date_list is a list of dates
	"""
	pack_dict = {}

	# ESSENTIALS! 
	pack_dict["Headlamp:"] = 1
	pack_dict["Plate:"] = 1
	pack_dict["Utensil:"] = 1
	pack_dict["Sleeping Pad: "] = 1

	# DURATION DEPENDENT!
	if len(date_list) == 1:
		pairs = 1
	elif len(date_list) > 1 and len(date_list) < 4:
		pairs = 2
	else:
		pairs = 3

	pack_dict["Shirts:"] = pairs
	pack_dict["Pants:"] = pairs
	pack_dict["Underwear:"] = pairs
	pack_dict["Socks:"] = pairs

	# TEMPATURE DEPENDENT!
	max_vals = []
	for i in range(len(weather_list)):
		max_vals.append(weather_list[i][0])

	abs_max = min(max_vals)

	if abs_max > 80:
		pack_dict["Water Bottle (Liters):"] = (pairs * 2) - ((pairs * 2) % 4)
	else:
		pack_dict["Water Bottle (Liters):"] = pairs

	
	min_vals = []
	for i in range(len(weather_list)):
		min_vals.append(weather_list[i][1])

	abs_min = min(min_vals)

	if round(abs_min,-1) < abs_min:
		bag_rating = round(abs_min,-1)
	else:
		bag_rating = round(abs_min,-1) - 10
	
	if bag_rating < 50:
		pack_dict["Sleeping Bag (" + str(bag_rating) + " degree):"] = 1
	else:
		pack_dict["Light Sleeping Bag:"] = 1

	if abs_min < 80 and abs_min > 60:
		pack_dict["Light Jacket:"] = 1
	elif abs_min< 60 and abs_min > 40:
		pack_dict["Medium Jacket:"] = 1
	elif abs_min < 40:
		pack_dict["Heavy Jacket:"] = 1

	for item in sorted(pack_dict):
		print(item, pack_dict[item])

	pass

def main():
	"""
	"""

	address = input(color.BOLD + "\nWhere would you like to go? " + color.END)
	start = input(color.BOLD + "\nWhen is your start date? (ex: April 17) " + color.END)
	end = input(color.BOLD + "\nWhen is your end date? (ex: April 24) " + color.END)

	loc = location(address)
	date_list = duration(start,end)

	print(color.BOLD + "\n--" + address + " weather: " + start + " to " + end + color.END + " --\n" )
	weather_list = []
	for date in date_list:

		date = str(date)
		day = date[:10]
		time = date[11:]
		date = day + "T" + time
		weather(loc[0],loc[1],date)
		data_points = parse_json("w"+day+".json")
		weather_list.append(data_points)
		print(color.BOLD + d.datetime.strptime(day, '%Y-%m-%d').strftime('%A') + color.END)
		print("The high is " + str(data_points[0]))
		print("The low is " + str(data_points[1]))
		print("Overall: " + str(data_points[2]) + "\n")

	print(print(color.BOLD + "-- Packing List --" + color.END))
	packing_list(weather_list,date_list)
	pass

main()
