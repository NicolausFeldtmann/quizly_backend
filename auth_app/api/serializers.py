from rest_framework import serializers
from django.contrib.auth.models import User

class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for validate and convert given user data to create user account."""
    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirmed_password"]
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'email': {
                'required': True
            }
        }

    def validate_confirmed_password(self, value):
        """Function to check if conformed password and password match."""
        password = self.initial_data.get('password')
        if password and value and password != value:
            raise serializers.ValidationError('Password do not match')
        return value

    def validate_email(self, value):
        """Function to validate if given email adress is vacant."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists.')
        return value

    def save(self):
        """Function to set password and save validated username, email and password."""
        pw = self.validated_data['password']

        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(pw)
        account.save()
        return account