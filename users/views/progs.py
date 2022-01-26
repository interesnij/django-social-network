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
        return HttpResponseBadRequest()

class CommentLikeCreate(View):
    def get(self, request, **kwargs):
        type = request.GET.get('type')
        comment = request.user.get_comment(type)
        if not request.is_ajax() and comment.get_item().list.is_user_can_see_comment(request.user.pk):
            raise Http404
        return comment.send_like(request.user, None)

class CommentDislikeCreate(View):
    def get(self, request, **kwargs):
        type = request.GET.get('type')
        comment = request.user.get_comment(type)
        if not request.is_ajax() and comment.get_item().list.is_user_can_see_comment(request.user.pk):
            raise Http404
        return comment.send_dislike(request.user, None)


class ItemLikeCreate(View):
    def get(self, request, **kwargs):
        type = request.GET.get('type')
        item = request.user.get_item(type)
        if not request.is_ajax() and item.list.is_user_can_see_el(request.user.pk):
            raise Http404
        return item.send_like(request.user, None)

class ItemDislikeCreate(View):
    def get(self, request, **kwargs):
        type = request.GET.get('type')
        item = request.user.get_item(type)
        if not request.is_ajax() and item.list.is_user_can_see_el(request.user.pk):
            raise Http404
        return item.send_dislike(request.user, None)


from django.views.generic.base import TemplateView
class CommentEdit(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_my_template

        self.template_name = get_my_template("generic/items/comment/comment_edit.html", request.user, request.META['HTTP_USER_AGENT'])
        self.type = request.GET.get('type')
        self.comment = request.user.get_comment(self.type)
        return super(CommentEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from posts.forms import CommentForm

        context = super(CommentEdit,self).get_context_data(**kwargs)
        context["comment"] = self.comment
        context["form_post"] = CommentForm(instance=self.comment)
        context["type"] = self.type
        return context

    def post(self,request,*args,**kwargs):
        from posts.forms import CommentForm

        type = request.POST.get('type')
        comment = request.user.get_comment(type)
        form = CommentForm(request.POST,instance=comment)
        list = comment.get_item().list

        if request.is_ajax() and form.is_valid() and list.is_user_can_create_comment(request.user.pk) \
        and (list.creator.pk == request.user.pk or comment.commenter.pk == request.user.pk):
            from common.templates import render_for_platform
            from common.processing_2 import get_text_processing

            _comment = form.save(commit=False)
            attach = request.POST.getlist("attach_items")

            if not _comment.text and not attach:
                from rest_framework.exceptions import ValidationError
                raise ValidationError("Нет текста или прикрепленных элементов")

            _attach = str(attach)
            _attach = _attach.replace("'", "").replace("[", "").replace("]", "").replace(" ", "")
            comment.attach = _attach
            comment.text = get_text_processing(_comment.text)
            comment.type = "EDI"
            comment.save()

            if comment.parent:
                return render_for_platform(request, 'generic/items/comment/reply.html',{'reply': comment, 'prefix': type[:3]})
            else:
                return render_for_platform(request, 'generic/items/comment/parent.html',{'comment': comment, 'prefix': type[:3]})
        else:
            return HttpResponseBadRequest()


class CommentDelete(View):
    def get(self,request,*args,**kwargs):
        type = request.GET.get('type')
        comment = request.user.get_comment(type)
        list = comment.get_item().list

        if request.is_ajax() and list.is_user_can_create_comment(request.user.pk) \
        and (list.creator.pk == request.user.pk or comment.commenter.pk == request.user.pk):
            comment.delete_item()
            return HttpResponse()
        raise Http404

class CommentRecover(View):
    def get(self,request,*args,**kwargs):
        type = request.GET.get('type')
        comment = request.user.get_comment(type)
        list = comment.get_item().list

        if request.is_ajax() and list.is_user_can_create_comment(request.user.pk) \
        and (list.creator.pk == request.user.pk or comment.commenter.pk == request.user.pk):
            comment.restore_item()
            return HttpResponse()
        raise Http404


class RepostCreate(TemplateView):
    template_name, community = None, None

    def get(self,request,*args,**kwargs):
        from common.utils import get_item_of_type
        from common.check.user import check_user_can_get_list
        from common.check.community import check_can_get_lists
        from posts.forms import PostForm

        self.type = request.GET.get('type')
        self.item = get_item_of_type(self.type)

        self.can_copy_item = self.item.list.is_user_can_copy_el(request.user.pk)
        self.template_name = get_detect_platform_template("generic/repost/repost.html", request.user, request.META['HTTP_USER_AGENT'])
        if self.item.community:
            check_can_get_lists(request.user, self.item.community)
        elif self.item.creator.pk != request.user.pk:
            check_user_can_get_list(request.user, self.item.creator)
        return super(RepostCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(RepostCreate,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.item
        context["can_copy_item"] = self.can_copy_item
        context["community"] = self.item.community
        context["type"] = self.item.community
        return context

    def post(self, request, *args, **kwargs):
        from common.check.user import check_user_can_get_list
        from common.check.community import check_can_get_lists
        from posts.forms import PostForm
        from django.http import HttpResponse, HttpResponseBadRequest
        from communities.models import Community

        type = request.POST.get('type')
        item, form_post, attach, lists, chat_items, count, creator = get_item_of_type(type), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), request.POST.getlist('chat_items'), 0, request.user
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            if not item.is_post:
                parent = Post.create_parent_post(creator=doc.creator, community=item.community, attach=type)
            else:
                parent = item
            if lists:
                if item.community:
                    from common.notify.notify import community_notify, community_wall
                    check_can_get_lists(request.user, item.community)

                    for list_pk in lists:
                        post_list = PostsList.objects.get(pk=list_pk)
                        if post_list.community:
                            post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, community=post_list.community)
                            community_notify(creator, parent.community, post_list.community.pk, parent.pk, "DOC", "create_c_doc_notify", "CRE")
                            community_wall(creator, parent.community, post_list.community.pk, parent.pk, "DOC", "create_c_doc_wall", "CRE")
                        else:
                            post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, community=None)
                            community_notify(creator, parent.community, None, parent.pk, "DOC", "create_c_doc_notify", "RE")
                            community_wall(creator, parent.community, None, parent.pk, "DOC", "create_c_doc_wall", "RE")
                        count += 1
                else:
                    from common.notify.notify import user_notify, user_wall
                    if item.creator.pk != request.user.pk:
                        check_user_can_get_list(request.user, item.creator)
                        
                    for list_pk in lists:
                        post_list = PostsList.objects.get(pk=list_pk)
                        if post_list.community:
                            post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, community=post_list.community)
                            user_notify(creator, post_list.community.pk, parent.pk, "DOC", "create_u_doc_notify", "CRE")
                            user_wall(creator, post_list.community.pk, parent.pk, "DOC", "create_u_doc_wall", "CRE")
                        else:
                            post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, community=None)
                            user_notify(creator,None, parent.pk, "DOC", "create_u_doc_notify", "RE")
                            user_wall(creator, None, parent.pk, "DOC", "create_u_doc_wall", "RE")
                            count += 1
                creator.plus_posts(count)

            elif chat_items:
                if item.community:
                    check_can_get_lists(request.user, item.community)
                elif item.creator.pk != request.user.pk:
                    check_user_can_get_list(request.user, item.creator)

                from common.processing.post import repost_message_send
                repost_message_send(item, type, item.community, request)

            item.repost += count
            item.save(update_fields=["repost"])

            return HttpResponse()
        else:
            return HttpResponseBadRequest()
