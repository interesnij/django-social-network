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


class UserItemView(View):
    def get(self,request,*args,**kwargs):
        from common.model.other import PhoneCodes
        from users.models import User
        from django.shortcuts import redirect

        code = self.kwargs["code"]
        phone = self.kwargs["phone"] 
        try:
            obj = PhoneCodes.objects.get(code=code, phone=phone)
            user = User.objects.get(phone=obj.phone)
            user.is_phone_verified=True
            user.save(update_fields=['is_phone_verified'])
            obj.delete()
            return redirect('users', pk=user.pk)
        except:
            return HttpResponse('Возникла проблема в получении Вашего номера')
