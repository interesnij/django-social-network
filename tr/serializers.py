from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_framework import serializers
from rest_framework.response import Response
from users.models import User
from common.utils import get_first_location
from users.model.settings import UserColorSettings
from common.processing.user import create_user_models
from datetime import date, datetime
from django.utils import timezone


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    date_day = serializers.CharField(required=True, write_only=True)
    date_month = serializers.CharField(required=True, write_only=True)
    date_year = serializers.CharField(required=True, write_only=True)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    "A user is already registered with this e-mail address.")
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Пароль 1 и пароль 2 не совпадают")
        return data

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        users_count = User.objects.only("pk").count()

        user.phone = users_count + 156
        self.date_day = self.validated_data.get('date_day', '')
        self.date_month = self.validated_data.get('date_month', '')
        self.date_year = self.validated_data.get('date_year', '')

        self.birtday = str(self.date_day) + "." + str(self.date_month) + "." + str(self.date_year)

        self.birtday = datetime.strptime(self.birthday, '%m/%d/%Y')
        if timezone.now() < self.birtday:
            raise serializers.ValidationError("tttrrrrtttrrr")
        user.birthday = self.birtday

        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.save()
        get_first_location(request, user)
        create_user_models(user)
        return user
