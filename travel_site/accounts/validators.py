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

    def get_help_text(self):
        return (
            "Your password must be at least 10 characters long, and contain both numbers and lowercase letters."
        )