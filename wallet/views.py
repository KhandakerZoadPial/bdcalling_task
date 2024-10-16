from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Wallet, Transaction
import json

@csrf_exempt
def add_funds(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        amount = data.get('amount')
        description = data.get('description', 'Funds added')

        if not user_id or amount is None:
            return JsonResponse({'error': 'User ID and amount are required'}, status=400)

        try:
            user = User.objects.get(id=user_id)
            wallet, created = Wallet.objects.get_or_create(user=user)

            # Update the wallet balance
            wallet.balance += float(amount)
            wallet.save()

            # Log the transaction
            Transaction.objects.create(wallet=wallet, amount=amount, description=description)

            return JsonResponse({'message': 'Funds added successfully', 'new_balance': wallet.balance}, status=201)

        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

@csrf_exempt
def get_wallet_balance(request, user_id):
    if request.method == 'GET':
        try:
            wallet = Wallet.objects.get(user_id=user_id)
            return JsonResponse({'user_id': user_id, 'balance': wallet.balance}, status=200)
        except Wallet.DoesNotExist:
            return JsonResponse({'error': 'Wallet not found'}, status=404)
