from django.core.exceptions import ValidationError
from django.core.validators import validate_email


def validate_registration_passwords(data):
    password = data['password'].strip()
    repeat_password = data['confirm_password']

    if not password:
        raise ValidationError("Password missing")
    if password != repeat_password:
        raise ValidationError("Passwords do not match")
    if len(password) < 8:
        raise ValidationError("Password too short")
