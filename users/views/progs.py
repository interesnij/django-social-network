from django.views import View
from users.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse


class UserBanCreate(View):
    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        request.user.block_user_with_pk(self.user.pk)
        return HttpResponse('Пользователь заблокирован')


class GetUserGender(View):
    def get(self,request,*args,**kwargs):
        if request.user.gender:
            return HttpResponse()
        else:
            import pandas as pd

            dfru = pd.read_csv('http://трезвый.рус/static/scripts/csv/FNru.csv', encoding='utf8')
            dfen = pd.read_csv('http://трезвый.рус/static/scripts/csv/FNen.csv', encoding='utf8')

            rumalenames = set(dfru[dfru['Gender'] == 'male']['GivenName'])
            rumalesurnames = set(dfru[dfru['Gender'] == 'male']['Surname'])

            rufemalenames = set(dfru[dfru['Gender'] == 'female']['GivenName'])
            rufemalesurnames = set(dfru[dfru['Gender'] == 'female']['Surname'])

            enmalenames = set(dfen[dfen['Gender'] == 'male']['GivenName'])
            enmalesurnames = set(dfen[dfen['Gender'] == 'male']['Surname'])

            enfemalenames = set(dfen[dfen['Gender'] == 'female']['GivenName'])
            enfemalesurnames = set(dfen[dfen['Gender'] == 'female']['Surname'])

            name = request.user.first_name
            surname = request.user.last_name

            if name in rumalenames and surname in rumalesurnames:
                request.user.gender = "Man"
            elif name in rufemalenames and surname in rufemalesurnames:
                request.user.gender = "Fem"
            elif name in enmalenames and surname in enmalesurnames:
                request.user.gender = "Man"
            elif name in enfemalenames and surname in enfemalesurnames:
                request.user.gender = "Fem"
            else:
                request.user.gender = "Man"
            request.user.save(update_fields=['gender'])
            return HttpResponse()


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


class UserPostView(View):
    def get(self,request,*args,**kwargs):
        from stst.models import PostNumbers
        if request.user.is_authenticated:
            pk = self.kwargs["pk"]
            try:
                obj = PostNumbers.objects.get(user=request.user.pk, post=pk)
                return HttpResponse('')
            except:
                obj = PostNumbers.objects.create(user=request.user.pk, post=pk)
                return HttpResponse('')
        else:
            return HttpResponse('')


class PhoneVerify(View):
    def get(self,request,*args,**kwargs):
        from common.model.other import PhoneCodes
        from users.models import User

        code = self.kwargs["code"]
        _phone = self.kwargs["phone"]
        phone = request.user.get_last_location().phone + _phone
        try:
            obj = PhoneCodes.objects.get(code=code, phone=phone)
        except:
            obj = None
        if obj:
            user = User.objects.get(pk=request.user.pk)
            user.perm = User.STANDART
            user.phone = obj.phone
            user.save()
            obj.delete()
            data = 'ok'
            response = render(request,'generic/response/phone.html',{'response_text':data})
            return response
        else:
            data = 'Код подтверждения неверный. Проверьте, пожалуйста, номер, с которого мы Вам звонили. Последние 4 цифры этого номера и есть код подтверждения, который нужно ввести с поле "Последние 4 цифры". Если не можете найти номер, нажмите на кнопку "Перезвонить повторно".'
            response = render(request,'generic/response/phone.html',{'response_text':data})
            return response


class PhoneSend(View):
    def get(self,request,*args,**kwargs):
        import json, requests
        from common.model.other import PhoneCodes
        from users.models import User

        text = ""
        if not request.user.is_no_phone_verified():
            return HttpResponse("")
        else:
            _phone = self.kwargs["phone"]
            if len(_phone) > 8:
                phone = request.user.get_last_location().phone + _phone
                try:
                    user = User.objects.get(phone=phone)
                    data = 'Пользователь с таким номером уже зарегистрирован. Используйте другой номер или напишите в службу поддержки, если этот номер Вы не использовали ранее.'
                    response = render(request,'generic/response/phone.html',{'response_text':data})
                    return response
                except:
                    response = requests.get(url="https://api.ucaller.ru/v1.0/initCall?service_id=12203&key=GhfrKn0XKAmA1oVnyEzOnMI5uBnFN4ck&phone=" + phone)
                    data = response.json()
                    PhoneCodes.objects.create(phone=phone, code=data['code'])
                    data = 'Мы Вам звоним. Последние 4 цифры нашего номера - код подтверждения, который нужно ввести в поле "Последние 4 цифры" и нажать "Подтвердить"'
                    response = render(request,'generic/response/code_send.html',{'response_text':data})
                    return response
            else:
                data = 'Введите, пожалуйста, корректное количество цифр Вашего телефона'
                response = render(request,'generic/response/phone.html',{'response_text':data})
                return response
