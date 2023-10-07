from celery import shared_task
from datetime import datetime

@shared_task(bind=True)
def test_func(self):
    # operations
    for i in range(10):
        print(i)
    return "Done"


@shared_task(bind=True)
def test_date(self, date_val):
    # operations
    print("Date got", date_val.strftime('%d-%m-%Y %H:%M:%S'))
    print("Actual datetime", datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    print("Operation eneded")