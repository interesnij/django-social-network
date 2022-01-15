from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_framework import serializers
from rest_framework.response import Response
from users.models import User
from common.utils import get_first_location
from users.model.settings import UserColorSettings
from datetime import date, datetime
from django.utils import timezone
import string
from rest_framework.exceptions import PermissionDenied
import re

absolute_words = [
                "пизда",
                "блядь",
                "мудак",
                "мудил",
                "пидора",
                "дрочит",
                "залупа",
                "хуеть",
                "ебтвою",
                "заебись",
                "нахуйй",
                "похуйй",
                "нахерр",
                "похерр",
                "хуйня",
                "хуетень",
                "хуетаа",
                "хуёв",
                "охуев",
                "охуите",
                "нахуяч",
                "нехуйй",
                "похуйй",
                "нехуёв",
                "охуист",
                "хуйнутьь",
                "ахуячить",
                "тхуярить",
                "хуякнут",
                "дохуяч",
                "хуипан",
                "хуйлор",
                "уебало",
                "еблети",
                "ебатьь",
                "ебану́т",
                "ебальник",
                "ебаната",
                "ебанько",
                "ебанат",
                "выёбыва",
                "аебнуться",
                "поеботина",
                "поебень",
                "уёбищее",
                "заебала",
                "мозгоёб",
                "ебенев",
                "оебучий",
                "аебашить",
                "ебляя",
                "хуясебе",
                "хуйсни",
                "какогохуя",
                "схуяли",
                "хуюверт",
                "хуйнадо",
                "ебаныйв",
                "ебатьмозги",
                "оебучий",
                "аебашить",
                "ебляя",
                "блять",
                "хуй",
                "хер",
                "хули",
                "бля",
                ]

def distance(a, b):
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]

def is_have_bad_words(text):
    _text = text.lower().replace(" ", "")

    d = {'а' : ['а', 'a', '@'],
      'б' : ['б', '6', 'b'],
      'в' : ['в', 'b', 'v'],
      'г' : ['г', 'r', 'g'],
      'д' : ['д', 'd'],
      'е' : ['е', 'e'],
      'ё' : ['ё', 'e'],
      'ж' : ['ж', 'zh', '*'],
      'з' : ['з', '3', 'z'],
      'и' : ['и', 'u', 'i'],
      'й' : ['й', 'u', 'i'],
      'к' : ['к', 'k', 'i{', '|{'],
      'л' : ['л', 'l', 'ji'],
      'м' : ['м', 'm'],
      'н' : ['н', 'h', 'n'],
      'о' : ['о', 'o', '0'],
      'п' : ['п', 'n', 'p'],
      'р' : ['р', 'r', 'p'],
      'с' : ['с', 'c', 's'],
      'т' : ['т', 'm', 't'],
      'у' : ['у', 'y', 'u'],
      'ф' : ['ф', 'f'],
      'х' : ['х', 'x', 'h' , '}{'],
      'ц' : ['ц', 'c', 'u,'],
      'ч' : ['ч', 'ch'],
      'ш' : ['ш', 'sh'],
      'щ' : ['щ', 'sch'],
      'ь' : ['ь', 'b'],
      'ы' : ['ы', 'bi'],
      'ъ' : ['ъ'],
      'э' : ['э', 'e'],
      'ю' : ['ю', 'io'],
      'я' : ['я', 'ya']
    }
    for key, value in d.items():
        for letter in value:
            for phr in _text:
                if letter == phr:
                    _text = _text.replace(phr, key)

    for word in absolute_words:
        for part in range(len(_text)):
            fragment = _text[part: part+len(word)]
            if distance(fragment, word) <= len(word)*0.25:
                bad_text = "Исправьте слово: " + fragment + ", похожее на " + word
                raise PermissionDenied(bad_text)
    return False


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    date_day = serializers.CharField(required=True, write_only=True)
    date_month = serializers.CharField(required=True, write_only=True)
    date_year = serializers.CharField(required=True, write_only=True)
    gender = serializers.CharField(required=True, write_only=True)
    phone = serializers.CharField(required=True, write_only=True)
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
        is_have_bad_words(user.first_name)
        is_have_bad_words(user.last_name)

        user.phone = self.validated_data.get('phone', '')
        self.date_day = self.validated_data.get('date_day', '')
        self.date_month = self.validated_data.get('date_month', '')
        self.date_year = self.validated_data.get('date_year', '')
        user.gender = self.validated_data.get('gender', '')

        birthday = str(self.date_day) + "/" + str(self.date_month) + "/" + str(self.date_year)

        birthday = datetime.strptime(birthday, '%d/%m/%Y')
        if timezone.now() < birthday:
            raise serializers.ValidationError("tttrrrrtttrrr")
        user.birthday = birthday

        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.save()
        try:
            get_first_location(request, user)
        except:
            pass
        return user
