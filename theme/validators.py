from django.core.exceptions import ValidationError
from datetime import date
from datetime import timedelta


def validate_date_uploaded(value):
    delta = date.today() - timedelta(days=365)
    if not value >= delta <= date.today():
        raise ValidationError('Video is over a year old')
