from django.views import View
from users.models import User
from django.http import HttpResponse


class UserBanCreate(View):
    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        request.user.block_user_with_pk(self.user.pk)
        return HttpResponse('Пользователь заблокирован')


class UserUnbanCreate(View):
    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        request.user.unblock_user_with_pk(self.user.pk)
        return HttpResponse('Пользователь разблокирован')


class UserColorChange(View):

    def get(self,request,*args,**kwargs):
        from users.model.settings import UserColorSettings

        try:
            model = UserColorSettings.objects.get(user=request.user)
        except:
            model = UserColorSettings.objects.create(user=request.user)
        color = self.kwargs["color"]
        if model.color == color:
            return HttpResponse('Этот цвет уже выбран')
        else:
            model.color = color
            model.save(update_fields=['color'])
            return HttpResponse('Цвет выбран')


class UserItemView(View):
    def get(self,request,*args,**kwargs):
        from stst.models import ItemNumbers

        pk = self.kwargs["pk"]
        try:
            obj = ItemNumbers.objects.get(user=request.user.pk, item=pk)
            return HttpResponse('')
        except:
            obj = ItemNumbers.objects.create(user=request.user.pk, item=pk)
            return HttpResponse('')


class PhoneVerify(View):
    def get(self,request,*args,**kwargs):
        from common.model.other import PhoneCodes
        from users.models import User

        code = self.kwargs["code"]
        _phone = self.kwargs["phone"]
        try:
            phone = request.user.get_last_location().phone + _phone
            obj = PhoneCodes.objects.get(code=code, phone=phone)
            user = User.objects.get(pk=request.user.pk)
            user.is_phone_verified=True
            user.phone=obj.phone
            user.save()
            obj.delete()
            return HttpResponse('')
        except:
            return HttpResponse('Возникла проблема в получении Вашего номера')


class PhoneSend(View):
    def get(self,request,*args,**kwargs):
        import json, requests
        from common.model.other import PhoneCodes
        from users.models import User

        if request.user.is_phone_verified:
            return HttpResponse("")
        else:
            _phone = self.kwargs["phone"]
            if len(_phone) > 8:
                phone = request.user.get_last_location().phone + _phone
                response = requests.get(url="https://api.ucaller.ru/v1.0/initCall?service_id=12203&key=GhfrKn0XKAmA1oVnyEzOnMI5uBnFN4ck&phone=" + phone)
                data = response.json()
                PhoneCodes.objects.create(phone=phone, code=data['code'])
                return HttpResponse("")
            else:
                data = {text:'Введите, пожалуйста, корректное количество цифр Вашего телефона'}
                return HttpResponse(data)
