from django.views import View
from users.models import User
from django.http import HttpResponse
from django.http import Http404
from common.templates import render_for_platform


class UserBanCreate(View):
    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax():
            request.user.block_user_with_pk(self.user.pk)
            return HttpResponse()

class UserUnbanCreate(View):
    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax():
            request.user.unblock_user_with_pk(self.user.pk)
            return HttpResponse()
        else:
            raise Http404

class UserColorChange(View):
    def get(self,request,*args,**kwargs):
        from users.model.settings import UserColorSettings

        if not request.is_ajax():
            raise Http404
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


class PhoneVerify(View):
    def get(self,request,*args,**kwargs):
        from common.model.other import PhoneCodes

        if not request.is_ajax():
            raise Http404
        code = self.kwargs["code"]
        phone = self.kwargs["phone"]
        if PhoneCodes.objects.filter(phone=phone, code=code).exists():
            obj = PhoneCodes.objects.get(phone=phone, code=code)
        else:
            obj = None
        if obj:
            obj.delete()
            data = 'ok'
            response = render_for_platform(request,'generic/response/phone.html',{'response_text':data})
            return response
        else:
            data = 'Код подтверждения неверный. Проверьте, пожалуйста, номер, с которого мы Вам звонили. Последние 4 цифры этого номера и есть код подтверждения, который нужно ввести с поле "Последние 4 цифры". Если не можете найти номер, нажмите на кнопку "Перезвонить повторно".'
            response = render_for_platform(request,'generic/response/phone.html',{'response_text':data})
            return response


class PhoneSend(View):
    def get(self,request,*args,**kwargs):
        import json, requests
        from common.model.other import PhoneCodes

        if not request.is_ajax() and request.user.is_authenticated:
            raise Http404
        else:
            phone = self.kwargs["phone"]
            if len(phone) > 8:
                try:
                    user = User.objects.get(phone=phone)
                    data = 'Пользователь с таким номером уже зарегистрирован. Используйте другой номер или напишите в службу поддержки, если этот номер Вы не использовали ранее.'
                    response = render_for_platform(request,'generic/response/phone.html',{'response_text':data})
                    return response
                except:
                    response = requests.get(url="https://api.ucaller.ru/v1.0/initCall?service_id=12203&key=GhfrKn0XKAmA1oVnyEzOnMI5uBnFN4ck&phone=" + phone)
                    data = response.json()
                    PhoneCodes.objects.create(phone=phone, code=data['code'])
                    data = 'Мы Вам звоним. Последние 4 цифры нашего номера - код подтверждения, который нужно ввести в поле "Последние 4 цифры" и нажать "Подтвердить"'
                    response = render_for_platform(request,'generic/response/code_send.html',{'response_text':data})
                    return response
            else:
                data = 'Введите, пожалуйста, корректное количество цифр Вашего телефона'
                response = render_for_platform(request,'generic/response/phone.html',{'response_text':data})
                return response


class CommentUserCreate(View):
    def post(self,request,*args,**kwargs):
        from posts.forms import CommentForm
        from common.processing_2 import get_text_processing

        type = request.POST.get('item')

        form_post, item = CommentForm(request.POST), request.user.get_item(type)

        if request.is_ajax() and item.list.is_user_can_create_comment(request.user.pk) and form_post.is_valid() and item.comments_enabled:
            comment = form_post.save(commit=False)

            if request.POST.get('text') or request.POST.get('attach_items') or request.POST.get('sticker'):
                from common.templates import render_for_platform

                prefix = type[:3]
                if item.community:
                    target = "c_" + prefix + "_"
                else:
                    target = "u_" + prefix + "_"

                new_comment = item.create_comment(commenter=request.user, parent=None, attach=request.POST.getlist('attach_items'), text=comment.text, sticker=request.POST.get('sticker'))
                return render_for_platform(request, 'generic/items/comment/parent.html', {'comment': new_comment, 'target': target, 'prefix': prefix})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class ReplyUserCreate(View):
    def post(self,request,*args,**kwargs):
        from posts.forms import CommentForm

        type = request.POST.get('comment')

        form_post, parent = CommentForm(request.POST), request.user.get_comment(type)
        item = parent.get_item()

        if request.is_ajax() and item.list.is_user_can_create_comment(request.user.pk) and form_post.is_valid() and item.comments_enabled:
            comment=form_post.save(commit=False)
            if request.POST.get('text') or request.POST.get('attach_items') or request.POST.get('sticker'):
                from common.templates import render_for_platform
                prefix = type[:3]
                if item.community:
                    target = "c_" + prefix + "_"
                else:
                    target = "u_" + prefix + "_"

                new_comment = item.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parent=parent, text=comment.text, sticker=request.POST.get('sticker'))
            else:
                return HttpResponseBadRequest()
            return render_for_platform(request, 'generic/items/comment/reply.html',{'reply': new_comment, 'comment': parent, 'target': target, 'prefix': prefix})
        else:
            return HttpResponseBadRequest()

class CommentLikeCreate(View):
    def get(self, request, **kwargs):
        type = request.GET.get('type')
        comment = request.user.get_comment(type)
        if not request.is_ajax():
            raise Http404
        return comment.send_like(request.user, None)

class CommentDislikeCreate(View):
    def get(self, request, **kwargs):
        type = request.GET.get('type')
        comment = request.user.get_comment(type)
        if not request.is_ajax():
            raise Http404
        return comment.send_dislike(request.user, None)
