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
            pass
        except:
            obj = ItemNumbers.objects.create(user=request.user.pk, item=pk)
            pass
