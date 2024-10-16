from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import bcrypt
import json
from django.utils.dateparse import parse_datetime


from .models import *

# Authentication
@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        # using bcrypt for hashing password
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        if User.objects.filter(username=username).count() == 0:
            user = User.objects.create(username=username, password=hashed_pw.decode('utf-8'))
            return JsonResponse({'message': 'User registered successfully'}, status=201)
        else:
            return JsonResponse({'message': 'Username exists!'}, status=400)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = User.objects.filter(username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            refresh = RefreshToken.for_user(user)
            return JsonResponse({'access': str(refresh.access_token), 'refresh': str(refresh)}, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)




# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def protected_view(request):
#     print('helo')
#     return JsonResponse({"message": "You are authenticated"}, status=200)

# Train Related code
@csrf_exempt
def train(request, train_id=None):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        schedule = data.get('schedule')  # Expecting ISO format date-time

        if not name or not schedule:
            return JsonResponse({'error': 'Name and schedule are required'}, status=400)

        train = Train.objects.create(name=name, schedule=schedule)
        return JsonResponse({'message': 'Train created successfully', 'train_id': train.id}, status=201)
    
    elif request.method == 'GET':
        # Retrieve a specific train or all trains
        if train_id:
            try:
                train = Train.objects.get(id=train_id)
                return JsonResponse({
                    'id': train.id,
                    'name': train.name,
                    'schedule': train.schedule.isoformat(),  # Returning in ISO format
                }, status=200)
            except Train.DoesNotExist:
                return JsonResponse({'error': 'Train not found'}, status=404)
        else:
            # Get all trains
            trains = Train.objects.all().values('id', 'name', 'schedule')
            return JsonResponse(list(trains), safe=False)

    elif request.method == 'PUT' and train_id:
        # Update an existing train
        try:
            train = Train.objects.get(id=train_id)
            data = json.loads(request.body)

            name = data.get('name', train.name)
            schedule_str = data.get('schedule', train.schedule.isoformat())

            schedule = parse_datetime(schedule_str)
            if schedule is None:
                return JsonResponse({'error': 'Invalid schedule format.'}, status=400)

            train.name = name
            train.schedule = schedule
            train.save()
            return JsonResponse({'message': 'Train updated successfully'}, status=200)

        except Train.DoesNotExist:
            return JsonResponse({'error': 'Train not found'}, status=404)

    elif request.method == 'DELETE' and train_id:
        # Delete a train
        try:
            train = Train.objects.get(id=train_id)
            train.delete()
            return JsonResponse({'message': 'Train deleted successfully'}, status=204)
        except Train.DoesNotExist:
            return JsonResponse({'error': 'Train not found'}, status=404)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def create_train_stop(request, train_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        station_id = data.get('station_id')
        stop_time = data.get('stop_time')

        if not station_id or not stop_time:
            return JsonResponse({'error': 'Station ID and stop time are required'}, status=400)

        try:
            train = Train.objects.get(id=train_id)
            station = Station.objects.get(id=station_id)
            train_stop = TrainStop.objects.create(train=train, station=station, stop_time=parse_datetime(stop_time))
            return JsonResponse({'message': 'Train stop created successfully', 'stop_id': train_stop.id}, status=201)

        except Train.DoesNotExist:
            return JsonResponse({'error': 'Train not found'}, status=404)
        except Station.DoesNotExist:
            return JsonResponse({'error': 'Station not found'}, status=404)
    elif request.method == 'GET':
        # Retrieve a specific train stop or all stops for the train
        if stop_id:
            try:
                train_stop = TrainStop.objects.get(id=stop_id)
                return JsonResponse({
                    'train_id': train_stop.train.id,
                    'station_name': train_stop.station.name,
                    'stop_time': train_stop.stop_time,
                }, status=200)
            except TrainStop.DoesNotExist:
                return JsonResponse({'error': 'Train stop not found'}, status=404)
        else:
            # Get all stops for the specified train
            stops = TrainStop.objects.filter(train=train_id).values('id', 'station__name', 'stop_time')
            return JsonResponse(list(stops), safe=False)

    elif request.method == 'PUT' and stop_id:
        # Update an existing train stop
        data = json.loads(request.body)

        try:
            train_stop = TrainStop.objects.get(id=stop_id)

            station_id = data.get('station_id')
            stop_time = data.get('stop_time')

            if station_id:
                station = Station.objects.get(id=station_id)
                train_stop.station = station

            if stop_time:
                stop_time_dt = parse_datetime(stop_time)
                if stop_time_dt is None:
                    return JsonResponse({'error': 'Invalid stop time format.'}, status=400)
                train_stop.stop_time = stop_time_dt

            train_stop.save()
            return JsonResponse({'message': 'Train stop updated successfully'}, status=200)

        except TrainStop.DoesNotExist:
            return JsonResponse({'error': 'Train stop not found'}, status=404)
        except Station.DoesNotExist:
            return JsonResponse({'error': 'Station not found'}, status=404)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'DELETE' and stop_id:
        # Delete a train stop
        try:
            train_stop = TrainStop.objects.get(id=stop_id)
            train_stop.delete()
            return JsonResponse({'message': 'Train stop deleted successfully'}, status=204)
        except TrainStop.DoesNotExist:
            return JsonResponse({'error': 'Train stop not found'}, status=404)


def get_train_with_stops(request, train_id):
    try:
        train = Train.objects.get(id=train_id)
        stops = train.stops.all().values('station__name', 'stop_time')
        return JsonResponse({'id': train.id, 'name': train.name, 'schedule': train.schedule, 'stops': list(stops)})
    except Train.DoesNotExist:
        return JsonResponse({'error': 'Train not found'}, status=404)
