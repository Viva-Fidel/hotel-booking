from django.core.exceptions import ValidationError

class MyPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 10:
            raise ValidationError(
                ("Password must be at least 10 characters long."),
                code='password_too_short',
            )
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                ("Password must contain at least one digit."),
                code='password_no_digit',
            )
        if not any(char.islower() for char in password):
            raise ValidationError(
                ("Password must contain at least one lowercase letter."),
                code='password_no_lower',
            )
        if not any(char.isupper() for char in password):
            raise ValidationError(
                ("Password must contain at least one uppercase letter."),
                code='password_no_upper',
            )
