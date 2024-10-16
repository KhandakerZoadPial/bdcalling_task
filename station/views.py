from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# model import
from .models import Station

# Create your views here.

# @permission_classes([IsAuthenticated])
@csrf_exempt
def create_station(request):
    if request.method == 'POST':
        # if needed we can check here if the authenticated user is admin or not
        data = json.loads(request.body)
        name = data.get('name')
        location = data.get('location')
        
        if not name or not location:
            return JsonResponse({'error': 'Name and location are required'}, status=400)

        station = Station.objects.create(name=name, location=location)
        return JsonResponse({'message': 'Station created successfully', 'station': {'name': station.name, 'location': station.location}}, status=201)


def get_stations(request):
    stations = Station.objects.all().values('id', 'name', 'location')
    stations_list = list(stations)
    return JsonResponse(stations_list, safe=False)


@csrf_exempt
def station_details(request, station_id):
    try:
        station = Station.objects.get(id=station_id)
    except Station.DoesNotExist:
        return JsonResponse({'error': 'Station not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse({'name': station.name, 'location': station.location})

    if request.method == 'PUT':
        data = json.loads(request.body)
        station.name = data.get('name', station.name)
        station.location = data.get('location', station.location)
        station.save()
        return JsonResponse({'message': 'Station updated successfully'})

    if request.method == 'DELETE':
        station.delete()
        return JsonResponse({'message': 'Station deleted successfully'}, status=204)
