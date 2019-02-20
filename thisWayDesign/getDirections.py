import googlemaps, os, json, sys, django
from datetime import datetime
from .findLandmark import getLandmark

sys.path.append("/CloudAssignment2/thisWay")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thisWay.settings")

def findDirections(startPoint, endPoint):
	gmaps = googlemaps.Client(key="AIzaSyDD4eCOaVp405TbIJZGXA1QMNnGUV9Glro")

	start = startPoint
	finish = endPoint

	now = datetime.now()
	directions = gmaps.directions(start, finish, mode="driving", departure_time=now)
	try:
		directions = directions[0]

		i=1
		route = []
		for leg in directions['legs']:
			startAddress = leg['start_address']
			endAddress = leg['end_address']
			for step in leg['steps']:
				html_instructions = str(step['html_instructions'])
				html_instructions = html_instructions.replace('<b>', '')
				html_instructions = html_instructions.replace('</b>', '')
				html_instructions = html_instructions.replace('</div>', '')
				html_instructions = html_instructions.replace('<div style="font-size:0.9em">', '')
				html_instructions = html_instructions.replace('</div>', '')
				html_instructions = html_instructions.replace('E/', '')
				route.append(html_instructions)
				i = i+1
		return route
	except IndexError:
		error = "Sorry, we are unable to find a terrain permitting path to that landmark."
		return error
