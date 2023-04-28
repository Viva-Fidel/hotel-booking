from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str

class EmailTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, email, timestamp):
        return (force_str(email) + force_str(timestamp))

email_token_generator = EmailTokenGenerator()
