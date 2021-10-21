from django.conf import settings
from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, related_name="profile", verbose_name="Пользователь", on_delete=models.CASCADE)
    activity = models.TextField(max_length=settings.POST_MAX_LENGTH, blank=True, verbose_name="Деятельность")
    interests = models.TextField(max_length=settings.POST_MAX_LENGTH, blank=True, verbose_name="Интересы")
    favorite_music = models.TextField(max_length=settings.POST_MAX_LENGTH, blank=True, verbose_name="Любимая музыка")
    favorite_films = models.TextField(max_length=settings.POST_MAX_LENGTH, blank=True, verbose_name="Любимые фильмы")
    favorite_books = models.TextField(max_length=settings.POST_MAX_LENGTH, blank=True, verbose_name="Любимые книги")
    favorite_game = models.TextField(max_length=settings.POST_MAX_LENGTH, blank=True, verbose_name="Любимые игры")
    favorite_quotes = models.TextField(max_length=settings.POST_MAX_LENGTH, blank=True, verbose_name="Любимые цитаты")
    about = models.TextField(max_length=settings.POST_MAX_LENGTH, blank=True, verbose_name="О себе")

    posts = models.PositiveIntegerField(default=0, verbose_name="Кол-во постов")
    views_post = models.PositiveIntegerField(default=0, verbose_name="Кол-во просмотров постов")
    friends = models.PositiveIntegerField(default=0, verbose_name="Кол-во друзей")
    follows = models.PositiveIntegerField(default=0, verbose_name="Кол-во подписчиков")
    communities = models.PositiveIntegerField(default=0, verbose_name="Кол-во групп")
    photos = models.PositiveIntegerField(default=0, verbose_name="Кол-во фотографий")
    goods = models.PositiveIntegerField(default=0, verbose_name="Кол-во товаров")
    docs = models.PositiveIntegerField(default=0, verbose_name="Кол-во документов")
    tracks = models.PositiveIntegerField(default=0, verbose_name="Кол-во аудиозаписей")
    videos = models.PositiveIntegerField(default=0, verbose_name="Кол-во видеозаписей")
    articles = models.PositiveIntegerField(default=0, verbose_name="Кол-во статей")
    time = models.DurationField(default=timedelta(), verbose_name="Общее проведенное время")
    height = models.FloatField(default=0, verbose_name="Общая высота в метрах")

    def __str__(self):
        return self.user.last_name

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
        #index_together = [('id', 'user'),]

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)


class UserLocation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user_location", verbose_name="Пользователь", on_delete=models.CASCADE)
    city_ru = models.CharField(max_length=100, blank=True, verbose_name="Город по-русски")
    city_en = models.CharField(max_length=100, blank=True, verbose_name="Город по-английски")
    city_lat = models.FloatField(blank=True, null=True, verbose_name="Ширина города")
    city_lon = models.FloatField(blank=True, null=True, verbose_name="Долгота города")
    region_ru = models.CharField(max_length=100, blank=True, verbose_name="Регион по-русски")
    region_en = models.CharField(max_length=100, blank=True, verbose_name="Регион по-английски")
    country_ru = models.CharField(max_length=100, blank=True, verbose_name="Страна по-русски")
    country_en = models.CharField(max_length=100, blank=True, verbose_name="Страна по-английски")
    phone = models.CharField(max_length=5, blank=True, verbose_name="Начало номера")

    class Meta:
        verbose_name = "Местоположение 1"
        verbose_name_plural = "Местоположения 1"
        index_together = [('id', 'user'),]

    def __str__(self):
        return '{}, {}, {}'.format(self.country_ru, self.region_ru, self.city_ru)


class IPUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user_ip", verbose_name="Пользователь", on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(protocol='both', null=True, blank=True, verbose_name="ip")

    class Meta:
        verbose_name = "ip пользователя"
        verbose_name_plural = "ip пользователей"
        index_together = [('id', 'user'),]

    def __str__(self):
        return '{} - {}'.format(self.user.get_full_name(), self.ip)


class UserProfileFamily(models.Model):
    NO_VALUE = 'NV'
    NOT_MARRIED = 'NM'
    MEET_FRIEND = 'MF'
    ENGADED = 'EN'
    MARRIED = 'MA'
    CIVIL_MARRIAGE = 'CM'
    LOVER = 'LO'
    DIFFICULT = 'DI'
    ACTIVE_SEARCH = 'AS'
    STATUS_MALE = (
        (NO_VALUE, 'Не выбрано'),
        (NOT_MARRIED, 'Не женат'),
        (MEET_FRIEND, 'Есть подруга'),
        (ENGADED, 'Помолвлен'),
        (MARRIED, 'Женат'),
        (CIVIL_MARRIAGE, 'В гражданском браке'),
        (LOVER, 'Влюблён'),
        (DIFFICULT, 'Всё сложно'),
        (ACTIVE_SEARCH, 'В активном поиске'),
    )
    STATUS_FEMALE = (
        (NO_VALUE, 'Не выбрано'),
        (NOT_MARRIED, 'Не замужем'),
        (MEET_FRIEND, 'Есть друг'),
        (ENGADED, 'Помолвлена'),
        (MARRIED, 'Замужем'),
        (CIVIL_MARRIAGE, 'В гражданском браке'),
        (LOVER, 'Влюблёна'),
        (DIFFICULT, 'Всё сложно'),
        (ACTIVE_SEARCH, 'В активном поиске'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE, related_name='user_family', verbose_name="Пользователь")
    male_status = models.CharField(max_length=5, choices=STATUS_MALE, default=NO_VALUE, verbose_name="Статус мужчины")
    female_status = models.CharField(max_length=5, choices=STATUS_FEMALE, default=NO_VALUE, verbose_name="Статус женщины")
    partner = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='user_profile_partner', verbose_name="Муж/Жена")
    mom = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='user_profile_mom', verbose_name="Мама")
    dad = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='user_profile_dad', verbose_name="Папа")
    brother_sister = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='user_profile_bro', verbose_name="Братья, сёстры")
    children = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='user_profile_chilren', verbose_name="Дети")
    grandsons = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='user_profile_grandsons', verbose_name="Внуки")

    class Meta:
        verbose_name = 'Семья пользователя'
        verbose_name_plural = 'Семьи пользователей'

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfileFamily.objects.create(user=instance)

class UserProfileAnketa(models.Model):
    POLITIC=(
        ('Не выбраны','Не выбраны'),
        ('Индиффирентные','Индиффирентные'),
        ('Коммунистические','Коммунистические'),
        ('Социалистические','Социалистические'),
        ('Умеренные','Умеренные'),
        ('Либеральные','Либеральные'),
        ('Консервативные','Консервативные'),
        ('Либералистические','Либералистические'),
        ('Ультраконсервативные','Ультраконсервативные'),
    )
    WORLDVIEW=(
        ('Не выбрано','Не выбрано'),
        ('Иудаизм','Иудаизм'),
        ('Православие','Православие'),
        ('Католицизм','Католицизм'),
        ('Протестантизм','Протестантизм'),
        ('Ислам','Ислам'),
        ('Буддизм','Буддизм'),
        ('Конфуцианство','Конфуцианство'),
        ('Светский гуманизм','Светский гуманизм'),
        ('Пастафарианство','Пастафарианство'),
    )
    MAINTHING_IN_LIFE=(
        ('Не выбрано','Не выбрано'),
        ('Семья и дети','Семья и дети'),
        ('Карьера и деньги','Карьера и деньги'),
        ('Развлечение и отдых','Развлечение и отдых'),
        ('Наука и исследования','Наука и исследования'),
        ('Совершенствование мира','Совершенствование мира'),
        ('Саморазвитие','Саморазвитие'),
        ('Красота и искусство','Красота и искусство'),
        ('Слава и влияние','Слава и влияние'),
    )
    MAINTHING_IN_PEOPLE=(
        ('Не выбрано','Не выбрано'),
        ('Ум и креативность','Ум и креативность'),
        ('Доброта и честность','Доброта и честность'),
        ('Красота и здоровье','Красота и здоровье'),
        ('Власть и богатство','Власть и богатство'),
        ('Смелость и упорство','Смелость и упорство'),
        ('Юмор и жизнелюбие','Юмор и жизнелюбие'),
    )
    ATTITUDE_TO_SMOKING=(
        ('Не выбрано','Не выбрано'),
        ('Резко негативное','Резко негативное'),
        ('Негативное','ДНегативное'),
        ('Компромиссное','Компромиссное'),
        ('Помогу бросить курить','Помогу бросить курить'),
    )
    ATTITUDE_TO_ALCOHOL=(
        ('Не выбрано','Не выбрано'),
        ('Резко негативное','Резко негативное'),
        ('Негативное','ДНегативное'),
        ('Компромиссное','Компромиссное'),
        ('Помогу бросить пить','Помогу бросить пить'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE, related_name='user_profile_anketa', verbose_name="Пользователь")
    political_preferences = models.CharField(max_length=50, blank=True, choices = POLITIC, verbose_name="Полит. предпочтения")
    worldview = models.CharField(max_length=50, blank=True, choices = WORLDVIEW, verbose_name="Мировоззрение")
    mainthing_in_life = models.CharField(max_length=50, blank=True, choices = MAINTHING_IN_LIFE, verbose_name="Главное в жизни")
    mainthing_in_people = models.CharField(max_length=50, blank=True, choices = MAINTHING_IN_PEOPLE, verbose_name="Главное в людях")
    attitude_to_smoking = models.CharField(max_length=50, blank=True, choices = ATTITUDE_TO_SMOKING, verbose_name="Отношение к курению")
    attitude_to_alcohol = models.CharField(max_length=50, blank=True, choices = ATTITUDE_TO_ALCOHOL, verbose_name="Отношение к алкоголю")
    inspiration = models.CharField(max_length=200, verbose_name="Что меня вдохновляет")

    class Meta:
        verbose_name = "Анкета"
        verbose_name_plural = "Анкеты"

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfileAnketa.objects.create(user=instance)


class UserDeleted(models.Model):
    PAGE = 'Pa'
    TIME = 'Ti'
    FREE = 'Fr'
    SAFE = 'Sa'
    CHILD = 'Ch'
    OTHER = 'Ot'
    ANSWER = (
        (PAGE, 'У меня есть другая страница'),
        (TIME, 'Соцсеть отнимает много времени'),
        (FREE, 'Мало свободы самовыражения'),
        (SAFE, 'Соцсеть плохо защищает данные'),
        (CHILD, 'Соцсеть плохо защищает детей'),
        (OTHER, 'Другая причина'),
    )

    user = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    answer = models.CharField(max_length=5, choices=ANSWER, default=OTHER, verbose_name="Причины удаления страницы")
    other = models.CharField(max_length=200, verbose_name="Свой вариант ответа")

    class Meta:
        verbose_name = 'Причина удаления страницы'
        verbose_name_plural = 'Причины удаления страницы'
