from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from .models import Ticket

def expire_tickets():
    now = timezone.now()
    print('ran')
    # Update tickets purchased more than 24 hours ago
    Ticket.objects.filter(purchased_at__lt=now - timezone.timedelta(hours=24), is_expired=False).update(is_expired=True)

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Run the expire_tickets function every hour
    scheduler.add_job(expire_tickets, 'interval', minutes=1)  
    scheduler.start()
