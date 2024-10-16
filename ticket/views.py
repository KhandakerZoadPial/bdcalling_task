from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

# models import
from .models import Ticket 
from train.models import Train, TrainStop
from wallet.models import Wallet, Transaction

from django.utils.dateparse import parse_datetime
import json

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

@permission_classes([IsAuthenticated])
@csrf_exempt
def purchase_ticket(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        train_id = data.get('train_id')
        stop_ids = data.get('stop_ids')  # List of stop IDs selected for the journey

        if not user_id or not train_id or not stop_ids:
            return JsonResponse({'error': 'User ID, Train ID, and stop IDs are required'}, status=400)

        try:
            user = User.objects.get(id=user_id)
            train = Train.objects.get(id=train_id)
            wallet = Wallet.objects.get(user=user)

            # Retrieve the selected train stops
            stops = TrainStop.objects.filter(id__in=stop_ids, train=train)
            if not stops.exists():
                return JsonResponse({'error': 'Invalid route selected'}, status=400)

            # Calculate the fare based on stops
            fare = calculate_fare(stops)

            # Check if the user has enough funds
            if wallet.balance < fare:
                return JsonResponse({'error': 'Insufficient funds'}, status=400)

            # Deduct the fare from the wallet
            wallet.balance = float(wallet.balance) - fare
            wallet.save()

            # Create the ticket
            ticket = Ticket.objects.create(user=user, train=train, fare=fare)
            ticket.stops.set(stops)  # Associate the selected stops with the ticket

            # Log the transaction
            Transaction.objects.create(wallet=wallet, amount=-fare, description=f'Ticket purchase for {train.name}')

            return JsonResponse({'message': 'Ticket purchased successfully', 'ticket_id': ticket.id}, status=201)

        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Train.DoesNotExist:
            return JsonResponse({'error': 'Train not found'}, status=404)
        except Wallet.DoesNotExist:
            return JsonResponse({'error': 'User did not connected a wallet'}, status=404)

def calculate_fare(stops):
    # Assuming that we charge 10.00 taka per stop
    fare_per_stop = 10.00
    return len(stops) * fare_per_stop
