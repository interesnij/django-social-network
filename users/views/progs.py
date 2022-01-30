from django.views import View
from users.models import User
from django.http import HttpResponse
from django.http import Http404
from common.templates import render_for_platform, get_detect_platform_template


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
        from common.utils import get_item_with_comments

        type = request.POST.get('item')
        form_post, item = CommentForm(request.POST), get_item_with_comments(type)

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
        from common.utils import get_comment

        type = request.POST.get('comment')
        form_post, parent = CommentForm(request.POST), get_comment(type)
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
        from common.utils import get_comment

        type = request.GET.get('type')
        comment = get_comment(type)
        if not request.is_ajax() and comment.get_item().list.is_user_can_see_comment(request.user.pk):
            raise Http404
        return comment.send_like(request.user, None)

class CommentDislikeCreate(View):
    def get(self, request, **kwargs):
        from common.utils import get_comment

        type = request.GET.get('type')
        comment = get_comment(type)
        if not request.is_ajax() and comment.get_item().list.is_user_can_see_comment(request.user.pk):
            raise Http404
        return comment.send_dislike(request.user, None)


class ItemLikeCreate(View):
    def get(self, request, **kwargs):
        from common.utils import get_item_with_comments

        type = request.GET.get('type')
        item = get_item_with_comments(type)
        if not request.is_ajax() and item.list.is_user_can_see_el(request.user.pk):
            raise Http404
        return item.send_like(request.user, None)

class ItemDislikeCreate(View):
    def get(self, request, **kwargs):
        from common.utils import get_item_with_comments

        type = request.GET.get('type')
        item = get_item_with_comments(type)
        if not request.is_ajax() and item.list.is_user_can_see_el(request.user.pk):
            raise Http404
        return item.send_dislike(request.user, None)


from django.views.generic.base import TemplateView
class CommentEdit(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_my_template
        from common.utils import get_comment

        self.template_name = get_my_template("generic/items/comment/comment_edit.html", request.user, request.META['HTTP_USER_AGENT'])
        self.type = request.GET.get('type')
        self.comment = get_comment(self.type)
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
        from common.utils import get_comment

        type = request.POST.get('type')
        comment = get_comment(type)
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
        from common.utils import get_comment

        type = request.GET.get('type')
        comment = get_comment(type)
        list = comment.get_item().list

        if request.is_ajax() and list.is_user_can_create_comment(request.user.pk) \
        and (list.creator.pk == request.user.pk or comment.commenter.pk == request.user.pk):
            comment.delete_item()
            return HttpResponse()
        raise Http404

class CommentRecover(View):
    def get(self,request,*args,**kwargs):
        from common.utils import get_comment

        type = request.GET.get('type')
        comment = get_comment(type)
        list = comment.get_item().list

        if request.is_ajax() and list.is_user_can_create_comment(request.user.pk) \
        and (list.creator.pk == request.user.pk or comment.commenter.pk == request.user.pk):
            comment.restore_item()
            return HttpResponse()
        raise Http404

class ListDelete(View):
    def get(self,request,*args,**kwargs):
        from common.utils import get_list_of_type

        list = get_list_of_type(request.GET.get('type'))
        if request.is_ajax():
            if list.community and not request.user.pk in list.community.get_administrators_ids():
                return HttpResponse()
            elif not request.user.pk == list.creator.pk:
                return HttpResponse()
            list.delete_item()
        return HttpResponse()

class ListRecover(View):
    def get(self,request,*args,**kwargs):
        from common.utils import get_list_of_type

        list = get_list_of_type(request.GET.get('type'))
        if request.is_ajax():
            if list.community and not request.user.pk in list.community.get_administrators_ids():
                return HttpResponse()
            elif not request.user.pk == list.creator.pk:
                return HttpResponse()
            list.restore_item()
        return HttpResponse()

class RepostCreate(TemplateView):
    template_name, community = None, None

    def get(self,request,*args,**kwargs):
        from common.utils import get_item_of_type
        from common.check.user import check_user_can_get_list
        from common.check.community import check_can_get_lists

        self.type = request.GET.get('type')
        self.item = get_item_of_type(self.type)

        if self.type[0] == "l":
            self.can_copy_item = self.item.is_user_can_copy_el(request.user.pk)
        elif not self.type[0] == "l":
            self.can_copy_item = self.item.list.is_user_can_copy_el(request.user.pk)
        self.template_name = get_detect_platform_template("generic/repost/repost.html", request.user, request.META['HTTP_USER_AGENT'])
        if self.item.community:
            check_can_get_lists(request.user, self.item.community)
        elif self.item.creator.pk != request.user.pk:
            check_user_can_get_list(request.user, self.item.creator)
        return super(RepostCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from posts.forms import PostForm

        context = super(RepostCreate,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.item
        context["can_copy_item"] = self.can_copy_item
        context["community"] = self.item.community
        context["type"] = self.type
        return context

    def post(self, request, *args, **kwargs):
        from common.check.user import check_user_can_get_list
        from common.check.community import check_can_get_lists
        from posts.forms import PostForm
        from django.http import HttpResponse, HttpResponseBadRequest
        from posts.models import PostsList, Post

        type = request.POST.get('type')
        if type[0] == "l":
            if type[:3] == "lpo":
                item, t, i = PostsList.objects.get(pk=type[3:]), "POL", "post"
            elif type[:3] == "lph":
                from gallery.models import PhotoList
                item, t, i =  PhotoList.objects.get(pk=type[3:]), "PHL", "photo"
            elif type[:3] == "lgo":
                from goods.models import GoodList
                item, t, i =  GoodList.objects.get(pk=type[3:]), "GOL", "good"
            elif type[:3] == "lvi":
                from video.models import VideoList
                item, t, i =  VideoList.objects.get(pk=type[3:]), "VIL", "video"
            elif type[:3] == "ldo":
                from docs.models import DocsList
                item, t, i =  DocsList.objects.get(pk=type[3:]), "DOL", "doc"
            elif type[:3] == "lmu":
                from music.models import MusicList
                item, t, i =  MusicList.objects.get(pk=type[3:]), "MUL", "music"
            elif type[:3] == "lsu":
                from survey.models import SurveyList
                item, t, i =  SurveyList.objects.get(pk=type[3:]), "SUL", "survey"
        else:
            if type[:3] == "pos":
                item, t, i =  Post.objects.get(pk=type[3:]), "POS", "post"
            elif type[:3] == "pho":
                from gallery.models import Photo
                item, t, i =  Photo.objects.get(pk=type[3:]), "PHO", "photo"
            elif type[:3] == "goo":
                from goods.models import Good
                item, t, i =  Good.objects.get(pk=type[3:]), "GOO", "good"
            elif type[:3] == "vid":
                from video.models import Video
                item, t, i =  Video.objects.get(pk=type[3:]), "VID", "video"
            elif type[:3] == "doc":
                from docs.models import Doc
                item, t, i =  Doc.objects.get(pk=type[3:]), "DOC", "doc"
            elif type[:3] == "mus":
                from music.models import Music
                item, t, i =  Music.objects.get(pk=type[3:]), "MUS", "music"
            elif type[:3] == "sur":
                from survey.models import Survey
                item, t, i =  Survey.objects.get(pk=type[3:]), "SUR", "survey"

        form_post, attach, lists, chat_items, count, creator = PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), request.POST.getlist('chat_items'), 0, request.user
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            if type[:3] == "pos":
                parent = item
            else:
                parent = Post.create_parent_post(creator=item.creator, community=item.community, attach=type)
            if lists:
                if item.community:
                    from common.notify.notify import community_notify, community_wall
                    check_can_get_lists(request.user, item.community)

                    for list_pk in lists:
                        post_list = PostsList.objects.get(pk=list_pk)
                        if post_list.community:
                            post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, community=post_list.community)
                            community_notify(creator, parent.community, post_list.community.pk, parent.pk, t, "create_" + i + "_notify", "CRE")
                            community_wall(creator, parent.community, post_list.community.pk, parent.pk, t, "create_" + i + "_wall", "CRE")
                        else:
                            post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, community=None)
                            community_notify(creator, parent.community, None, parent.pk, t, "create_" + i + "_notify", "RE")
                            community_wall(creator, parent.community, None, parent.pk, t, "create_" + i + "_wall", "RE")
                        count += 1
                else:
                    from common.notify.notify import user_notify, user_wall
                    if item.creator.pk != request.user.pk:
                        check_user_can_get_list(request.user, item.creator)

                    for list_pk in lists:
                        post_list = PostsList.objects.get(pk=list_pk)
                        if post_list.community:
                            post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, community=post_list.community)
                            user_notify(creator, post_list.community.pk, parent.pk, t, "create_" + i + "_notify", "CRE")
                            user_wall(creator, post_list.community.pk, parent.pk, t, "create_" + i + "_wall", "CRE")
                        else:
                            post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, community=None)
                            user_notify(creator,None, parent.pk, t, "create_" + i + "_notify", "RE")
                            user_wall(creator, None, parent.pk, t, "create_" + i + "_wall", "RE")
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


class ClaimCreate(TemplateView):
    template_name, community = None, None

    def get(self,request,*args,**kwargs):
        from common.utils import get_item_of_type, get_comment
        from common.check.user import check_user_can_get_list
        from common.check.community import check_can_get_lists

        self._type = request.GET.get('type')
        self._subtype = request.GET.get('subtype')

        if self._subtype and self._subtype == "comment":
            self.item = get_comment(self._type)
            if self.item.get_item().community:
                check_can_get_lists(request.user, self.item.get_item().community)
            else:
                check_user_can_get_list(request.user, self.item.get_item().creator)
        elif "use" in self._type:
            from users.models import User
            self.item = User.objects.get(pk=self._type[3:])
            check_user_can_get_list(request.user, self.item)
        elif "com" in self._type:
            from communities.models import Community
            self.item = Community.objects.get(pk=self._type[3:])
            check_can_get_lists(request.user, self.item)
        else:
            self.item = get_item_of_type(self._type)
            if self.item.community:
                self.community = self.item.community
                check_can_get_lists(request.user, self.community)

            elif self.item.creator.pk != request.user.pk:
                check_user_can_get_list(request.user, self.item.creator)
        self.template_name = get_detect_platform_template("generic/report.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(ClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from managers.forms import ReportForm

        context = super(ClaimCreate,self).get_context_data(**kwargs)
        context["form"] = ReportForm()
        context["object"] = self.item
        context["community"] = self.community
        context["type"] = self._type
        context["subtype"] = self._subtype
        return context

    def post(self, request, *args, **kwargs):
        from common.check.user import check_user_can_get_list
        from common.check.community import check_can_get_lists
        from django.http import HttpResponse, HttpResponseBadRequest
        from managers.forms import ReportForm
        from managers.models import Moderated, ModerationReport

        _type = request.POST.get('_type')
        _subtype = request.POST.get('_subtype')

        if _type[0] == "l":
            if _type[:3] == "lpo":
                from posts.models import PostsList
                item, t = PostsList.objects.get(pk=_type[3:]), "POL"
            elif _type[:3] == "lph":
                from gallery.models import PhotoList
                item, t =  PhotoList.objects.get(pk=_type[3:]), "PHL"
            elif _type[:3] == "lgo":
                from goods.models import GoodList
                item, t =  GoodList.objects.get(pk=_type[3:]), "GOL"
            elif _type[:3] == "lvi":
                from video.models import VideoList
                item, t =  VideoList.objects.get(pk=_type[3:]), "VIL"
            elif _type[:3] == "ldo":
                from docs.models import DocsList
                item, t =  DocsList.objects.get(pk=_type[3:]), "DOL"
            elif _type[:3] == "lmu":
                from music.models import MusicList
                item, t =  MusicList.objects.get(pk=_type[3:]), "MUL"
            elif _type[:3] == "lsu":
                from survey.models import SurveyList
                item, t =  SurveyList.objects.get(pk=_type[3:]), "SUL"
            elif _type[:3] == "lfo":
                from survey.models import SurveyList
                item, t =  SurveyList.objects.get(pk=_type[3:]), "FOL"
            elif _type[:3] == "lar":
                from survey.models import SurveyList
                item, t =  SurveyList.objects.get(pk=_type[3:]), "ARL"
            elif _type[:3] == "lwi":
                from survey.models import SurveyList
                item, t =  SurveyList.objects.get(pk=_type[3:]), "WIL"

        elif _subtype and _subtype == "comment":
            if _type[:3] == "pos":
                from posts.models import PostComment
                item, t = PostComment.objects.get(pk=_type[3:]), "CPO"
            elif _type[:3] == "pho":
                from gallery.models import PhotoComment
                item, t =  PhotoComment.objects.get(pk=_type[3:]), "CPH"
            elif _type[:3] == "goo":
                from goods.models import GoodComment
                item, t =  GoodComment.objects.get(pk=_type[3:]), "CGO"
            elif _type[:3] == "vid":
                from video.models import VideoComment
                item, t =  VideoComment.objects.get(pk=_type[3:]), "CVI"
            elif _type[:3] == "wik":
                from video.models import VideoComment
                item, t =  VideoComment.objects.get(pk=_type[3:]), "CWI"
            elif _type[:3] == "CwC":
                from video.models import VideoComment
                item, t =  VideoComment.objects.get(pk=_type[3:]), "CwC"

        elif _subtype and _subtype == "planner":
            if _type[:3] == "WrS":
                from posts.models import PostComment
                item, t = PostComment.objects.get(pk=_type[3:]), "WrS"
            elif type[:3] == "BoA":
                from gallery.models import PhotoComment
                item, t =  PhotoComment.objects.get(pk=_type[3:]), "BoA"
            elif _type[:3] == "CoL":
                from goods.models import GoodComment
                item, t =  GoodComment.objects.get(pk=_type[3:]), "CoL"
            elif _type[:3] == "CaR":
                from video.models import VideoComment
                item, t =  VideoComment.objects.get(pk=_type[3:]), "CaR"

        else:
            if _type[:3] == "pos":
                item, t =  Post.objects.get(pk=_type[3:]), "POS"
            elif _type[:3] == "pho":
                from gallery.models import Photo
                item, t =  Photo.objects.get(pk=_type[3:]), "PHO"
            elif _type[:3] == "goo":
                from goods.models import Good
                item, t =  Good.objects.get(pk=_type[3:]), "GOO"
            elif _type[:3] == "vid":
                from video.models import Video
                item, t =  Video.objects.get(pk=_type[3:]), "VID"
            elif _type[:3] == "doc":
                from docs.models import Doc
                item, t =  Doc.objects.get(pk=_type[3:]), "DOC"
            elif _type[:3] == "mus":
                from music.models import Music
                item, t =  Music.objects.get(pk=_type[3:]), "MUS"
            elif _type[:3] == "sur":
                from survey.models import Survey
                item, t =  Survey.objects.get(pk=_type[3:]), "SUR"
            elif _type[:3] == "mes":
                from chat.models import Message
                item, t =  Message.objects.get(pk=_type[3:]), "CHA"

            elif _type[:3] == "use":
                from users.models import User
                item, t =  User.objects.get(pk=_type[3:]), "USE"
            elif _type[:3] == "com":
                from communities.models import Community
                item, t =  Community.objects.get(pk=_type[3:]), "COM"
            elif _type[:3] == "sit":
                from music.models import Music
                item, t=  Music.objects.get(pk=_type[3:]), "SIT"
            elif type[:3] == "mai":
                from survey.models import Survey
                item, t =  Survey.objects.get(pk=_type[3:]), "MAI"
            elif _type[:3] == "for":
                from survey.models import Survey
                item, t =  Survey.objects.get(pk=_type[3:]), "FOR"

        form_post = ReportForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type=t, object_id=item.pk, description=post.description, type=post.type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class ListCreate(TemplateView):
    template_name, community = None, None

    def get(self,request,*args,**kwargs):
        from common.utils import get_list_of_type
        from common.check.community import check_can_get_lists

        self.type = request.GET.get('type')
        if self.type[:3] == "lpo":
            have_comments = True
            self.text = "Создание списка записей"
        elif self.type[:3] == "lph":
            have_comments = True
            self.text = "Создание фотоальбома"
        elif self.type[:3] == "lgo":
            have_comments = True
            self.text = "Создание подборки товаров"
        elif self.type[:3] == "lvi":
            have_comments = True
            self.text = "Создание видеоальбома"
        elif self.type[:3] == "ldo":
            have_comments = False
            self.text = "Создание списка документов"
        elif self.type[:3] == "lmu":
            have_comments = False
            self.text = "Создание плейлиста"
        elif self.type[:3] == "lsu":
            have_comments = False
            self.text = "Создание списка опросов"

        community_id = request.GET.get('community_id')
        if community_id:
            from communities.models import Community
            self.community = Community.objects.get(pk=community_id)
            if not request.user.pk in self.community.get_administrators_ids():
                return HttpResponseBadRequest()

        if have_comments:
            self.template_name = get_detect_platform_template("generic/form/add_list_with_comment.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_detect_platform_template("generic/form/add_list_not_comment.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(ListCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ListCreate,self).get_context_data(**kwargs)
        context["community"] = self.community
        context["type"] = self.type
        context["text"] = self.text
        return context

    def post(self, request, *args, **kwargs):
        from common.check.community import check_can_get_lists
        from django.http import HttpResponse, HttpResponseBadRequest

        community_id = request.POST.get('community_id')
        if community_id:
            from communities.models import Community
            community = Community.objects.get(pk=community_id)
            if not request.user.pk in community.get_administrators_ids():
                return HttpResponseBadRequest()
        else:
            community = None

        type = request.POST.get('type')
        if type[:3] == "lpo":
            have_comments = True
            self.text = "Создание списка записей"
        elif type[:3] == "lph":
            have_comments = True
        elif type[:3] == "lgo":
            have_comments = True
        elif type[:3] == "lvi":
            have_comments = True
        elif type[:3] == "ldo":
            have_comments = False
        elif type[:3] == "lmu":
            have_comments = False
        elif type[:3] == "lsu":
            have_comments = False

        if have_comments:
            from posts.forms import PostListForm
            form = PostListForm(request.POST)
        else:
            from docs.forms import DocListForm
            form = DocListForm(request.POST)

        if request.is_ajax() and form.is_valid():
            from common.templates import render_for_platform

            list = form.save(commit=False)
            if type[:3] == "lpo":
                from posts.models import PostsList
                new_list = PostsList.create_list(
                    creator=request.user,
                    name=list.name,
                    description=list.description,
                    community=community,
                    can_see_el=list.can_see_el,
                    can_see_el_users=request.POST.getlist("can_see_el_users"),
                    can_see_comment=list.can_see_comment,
                    can_see_comment_users=request.POST.getlist("can_see_comment_users"),
                    create_el=list.create_el,
                    create_el_users=request.POST.getlist("create_el_users"),
                    create_comment=list.create_comment,
                    create_comment_users=request.POST.getlist("create_comment_users"),
                    copy_el=list.copy_el,
                    copy_el_users=request.POST.getlist("create_copy_el"),
                )
                if community:
                    return render_for_platform(request, 'communities/lenta/admin_list.html',{'list': new_list})
                else:
                    return render_for_platform(request, 'users/lenta/my_list.html',{'list': new_list})
            elif type[:3] == "lph":
                from gallery.models import PhotoList
                new_list = PhotoList.create_list(
                    creator=request.user,
                    name=list.name,
                    description=list.description,
                    community=community,
                    can_see_el=list.can_see_el,
                    can_see_el_users=request.POST.getlist("can_see_el_users"),
                    can_see_comment=list.can_see_comment,
                    can_see_comment_users=request.POST.getlist("can_see_comment_users"),
                    create_el=list.create_el,
                    create_el_users=request.POST.getlist("create_el_users"),
                    create_comment=list.create_comment,
                    create_comment_users=request.POST.getlist("create_comment_users"),
                    copy_el=list.copy_el,
                    copy_el_users=request.POST.getlist("create_copy_el"),
                )
                if community:
                    return render_for_platform(request, 'communities/photos/list/new_list.html',{'list': new_list})
                else:
                    return render_for_platform(request, 'users/photos/list/new_list.html',{'list': new_list})
            elif type[:3] == "lgo":
                from goods.models import GoodList
                new_list = GoodList.create_list(
                    creator=request.user,
                    name=list.name,
                    description=list.description,
                    community=community,
                    can_see_el=list.can_see_el,
                    can_see_el_users=request.POST.getlist("can_see_el_users"),
                    can_see_comment=list.can_see_comment,
                    can_see_comment_users=request.POST.getlist("can_see_comment_users"),
                    create_el=list.create_el,
                    create_el_users=request.POST.getlist("create_el_users"),
                    create_comment=list.create_comment,
                    create_comment_users=request.POST.getlist("create_comment_users"),
                    copy_el=list.copy_el,
                    copy_el_users=request.POST.getlist("create_copy_el"),
                )
                if community:
                    return render_for_platform(request, 'communities/goods/list/admin_list.html',{'list': new_list})
                else:
                    return render_for_platform(request, 'users/goods/list/my_list.html',{'list': new_list})
            elif type[:3] == "lvi":
                from video.models import VideoList
                new_list = VideoList.create_list(
                    creator=request.user,
                    name=list.name,
                    description=list.description,
                    community=community,
                    can_see_el=list.can_see_el,
                    can_see_el_users=request.POST.getlist("can_see_el_users"),
                    can_see_comment=list.can_see_comment,
                    can_see_comment_users=request.POST.getlist("can_see_comment_users"),
                    create_el=list.create_el,
                    create_el_users=request.POST.getlist("create_el_users"),
                    create_comment=list.create_comment,
                    create_comment_users=request.POST.getlist("create_comment_users"),
                    copy_el=list.copy_el,
                    copy_el_users=request.POST.getlist("create_copy_el"),
                )
                if community:
                    return render_for_platform(request, 'communities/video/list/new_list.html',{'list': new_list})
                else:
                    return render_for_platform(request, 'users/video/list/new_list.html',{'list': new_list})
            elif type[:3] == "ldo":
                from docs.models import DocsList
                new_list = DocsList.create_list(
                    creator=request.user,
                    name=list.name,
                    description=list.description,
                    community=community,
                    can_see_el=list.can_see_el,
                    can_see_el_users=request.POST.getlist("can_see_el_users"),
                    create_el=list.create_el,
                    create_el_users=request.POST.getlist("create_el_users"),
                    copy_el=list.copy_el,
                    copy_el_users=request.POST.getlist("create_copy_el"),
                )
                if community:
                    return render_for_platform(request, 'communities/docs/list/new_list.html',{'list': new_list})
                else:
                    return render_for_platform(request, 'users/docs/list/new_list.html',{'list': new_list})
            elif type[:3] == "lmu":
                from music.models import MusicList
                new_list = MusicList.create_list(
                    creator=request.user,
                    name=list.name,
                    description=list.description,
                    community=community,
                    can_see_el=list.can_see_el,
                    can_see_el_users=request.POST.getlist("can_see_el_users"),
                    create_el=list.create_el,
                    create_el_users=request.POST.getlist("create_el_users"),
                    copy_el=list.copy_el,
                    copy_el_users=request.POST.getlist("create_copy_el"),
                )
                if community:
                    return render_for_platform(request, 'communities/music/list/new_list.html',{'list': new_list})
                else:
                    return render_for_platform(request, 'users/music/list/new_list.html',{'list': new_list})
            elif type[:3] == "lsu":
                from survey.models import SurveyList
                new_list = SurveyList.create_list(
                    creator=request.user,
                    name=list.name,
                    description=list.description,
                    community=community,
                    can_see_el=list.can_see_el,
                    can_see_el_users=request.POST.getlist("can_see_el_users"),
                    create_el=list.create_el,
                    create_el_users=request.POST.getlist("create_el_users"),
                    copy_el=list.copy_el,
                    copy_el_users=request.POST.getlist("create_copy_el"),
                )
                if community:
                    return render_for_platform(request, 'communities/survey/list/new_list.html',{'list': new_list})
                else:
                    return render_for_platform(request, 'users/survey/list/new_list.html',{'list': new_list})

            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class ListEdit(TemplateView):
    template_name, community = None, None

    def get(self,request,*args,**kwargs):
        from common.utils import get_list_of_type
        from common.check.community import check_can_get_lists

        self.type = request.GET.get('type')
        if self.type[:3] == "lpo":
            from posts.models import PostsList
            self.list = PostsList.objects.get(pk=self.type[3:])
            have_comments = True
            self.text = "Изменение списка записей"
        elif self.type[:3] == "lph":
            from gallery.models import PhotoList
            self.list = PhotoList.objects.get(pk=self.type[3:])
            have_comments = True
            self.text = "Изменение фотоальбома"
        elif self.type[:3] == "lgo":
            from goods.models import GoodList
            self.list = GoodList.objects.get(pk=self.type[3:])
            have_comments = True
            self.text = "Изменение подборки товаров"
        elif self.type[:3] == "lvi":
            from video.models import VideoList
            self.list = VideoList.objects.get(pk=self.type[3:])
            have_comments = True
            self.text = "Изменение видеоальбома"
        elif self.type[:3] == "ldo":
            from docs.models import DocsList
            self.list = DocsList.objects.get(pk=self.type[3:])
            have_comments = False
            self.text = "Изменение списка документов"
        elif self.type[:3] == "lmu":
            from music.models import MusicList
            self.list = MusicList.objects.get(pk=self.type[3:])
            have_comments = False
            self.text = "Изменение плейлиста"
        elif self.type[:3] == "lsu":
            from survey.models import SurveyList
            self.list = SurveyList.objects.get(pk=self.type[3:])
            have_comments = False
            self.text = "Изменение списка опросов"

        community_id = request.GET.get('community_id')
        if community_id:
            from communities.models import Community
            self.community = Community.objects.get(pk=community_id)
            if not request.user.pk in self.community.get_administrators_ids():
                return HttpResponseBadRequest()

        if have_comments:
            self.template_name = get_detect_platform_template("generic/form/edit_list_with_comment.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_detect_platform_template("generic/form/edit_list_not_comment.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(ListEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ListEdit,self).get_context_data(**kwargs)
        context["community"] = self.community
        context["type"] = self.type
        context["text"] = self.text
        context["list"] = self.list
        return context

    def post(self, request, *args, **kwargs):
        from common.check.community import check_can_get_lists
        from django.http import HttpResponse, HttpResponseBadRequest

        community_id = request.POST.get('community_id')
        if community_id:
            from communities.models import Community
            community = Community.objects.get(pk=community_id)
            if not request.user.pk in community.get_administrators_ids():
                return HttpResponseBadRequest()

        type = request.POST.get('type')
        if type[:3] == "lpo":
            from posts.models import PostsList
            _list = PostsList.objects.get(pk=type[3:])
            have_comments = True
        elif type[:3] == "lph":
            from gallery.models import PhotoList
            _list = PhotoList.objects.get(pk=type[3:])
            have_comments = True
        elif type[:3] == "lgo":
            from goods.models import GoodList
            _list = GoodList.objects.get(pk=type[3:])
            have_comments = True
        elif type[:3] == "lvi":
            from video.models import VideoList
            _list = VideoList.objects.get(pk=type[3:])
            have_comments = True
        elif type[:3] == "ldo":
            from docs.models import DocsList
            _list = DocsList.objects.get(pk=type[3:])
            have_comments = False
        elif type[:3] == "lmu":
            from music.models import MusicList
            _list = MusicList.objects.get(pk=type[3:])
            have_comments = False
        elif type[:3] == "lsu":
            from survey.models import SurveyList
            _list = SurveyList.objects.get(pk=type[3:])
            have_comments = False

        if _list.creator.pk != request.user.pk:
            return HttpResponseBadRequest()
        elif have_comments:
            from posts.forms import PostListForm
            form = PostListForm(request.POST)
        else:
            from docs.forms import DocListForm
            form = DocListForm(request.POST)

        if request.is_ajax() and form.is_valid():
            list = form.save(commit=False)
            if type[:3] == "lpo":
                new_list = _list.edit_list(
                    name=list.name,
                    description=list.description,
                    can_see_el=list.can_see_el,
                    can_see_el_users=request.POST.getlist("can_see_el_users"),
                    can_see_comment=list.can_see_comment,
                    can_see_comment_users=request.POST.getlist("can_see_comment_users"),
                    create_el=list.create_el,
                    create_el_users=request.POST.getlist("create_el_users"),
                    create_comment=list.create_comment,
                    create_comment_users=request.POST.getlist("create_comment_users"),
                    copy_el=list.copy_el,
                    copy_el_users=request.POST.getlist("create_copy_el"),
                )
            elif type[:3] == "lph":
                new_list = _list.edit_list(
                    name=list.name,
                    description=list.description,
                    can_see_el=list.can_see_el,
                    can_see_el_users=request.POST.getlist("can_see_el_users"),
                    can_see_comment=list.can_see_comment,
                    can_see_comment_users=request.POST.getlist("can_see_comment_users"),
                    create_el=list.create_el,
                    create_el_users=request.POST.getlist("create_el_users"),
                    create_comment=list.create_comment,
                    create_comment_users=request.POST.getlist("create_comment_users"),
                    copy_el=list.copy_el,
                    copy_el_users=request.POST.getlist("create_copy_el"),
                )
            elif type[:3] == "lgo":
                new_list = _list.edit_list(
                    name=list.name,
                    description=list.description,
                    can_see_el=list.can_see_el,
                    can_see_el_users=request.POST.getlist("can_see_el_users"),
                    can_see_comment=list.can_see_comment,
                    can_see_comment_users=request.POST.getlist("can_see_comment_users"),
                    create_el=list.create_el,
                    create_el_users=request.POST.getlist("create_el_users"),
                    create_comment=list.create_comment,
                    create_comment_users=request.POST.getlist("create_comment_users"),
                    copy_el=list.copy_el,
                    copy_el_users=request.POST.getlist("create_copy_el"),
                )
            elif type[:3] == "lvi":
                new_list = _list.edit_list(
                    name=list.name,
                    description=list.description,
                    can_see_el=list.can_see_el,
                    can_see_el_users=request.POST.getlist("can_see_el_users"),
                    can_see_comment=list.can_see_comment,
                    can_see_comment_users=request.POST.getlist("can_see_comment_users"),
                    create_el=list.create_el,
                    create_el_users=request.POST.getlist("create_el_users"),
                    create_comment=list.create_comment,
                    create_comment_users=request.POST.getlist("create_comment_users"),
                    copy_el=list.copy_el,
                    copy_el_users=request.POST.getlist("create_copy_el"),
                )
            elif type[:3] == "ldo":
                new_list = _list.edit_list(
                    name=list.name,
                    description=list.description,
                    can_see_el=list.can_see_el,
                    can_see_el_users=request.POST.getlist("can_see_el_users"),
                    create_el=list.create_el,
                    create_el_users=request.POST.getlist("create_el_users"),
                    copy_el=list.copy_el,
                    copy_el_users=request.POST.getlist("create_copy_el"),
                )
            elif type[:3] == "lmu":
                new_list = list.edit_list(
                    name=_list.name,
                    description=list.description,
                    can_see_el=list.can_see_el,
                    can_see_el_users=request.POST.getlist("can_see_el_users"),
                    create_el=list.create_el,
                    create_el_users=request.POST.getlist("create_el_users"),
                    copy_el=list.copy_el,
                    copy_el_users=request.POST.getlist("create_copy_el"),
                )
            elif type[:3] == "lsu":
                new_list = _list.edit_list(
                    name=list.name,
                    description=list.description,
                    can_see_el=list.can_see_el,
                    can_see_el_users=request.POST.getlist("can_see_el_users"),
                    create_el=list.create_el,
                    create_el_users=request.POST.getlist("create_el_users"),
                    copy_el=list.copy_el,
                    copy_el_users=request.POST.getlist("create_copy_el"),
                )

            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class ChangeListPosition(View):
    def get(self,request,*args,**kwargs):
        import json

        user, community = User.objects.get(pk=self.kwargs["pk"]), None
        type = request.GET.get('type')
        community_id = request.GET.get('community_id')
        if community_id:
            from communities.models import Community
            community = Community.objects.get(pk=community_id)
            if not request.user.pk in community.get_administrators_ids():
                return HttpResponseBadRequestResponse()
        else:
            if not user.pk == request.user.pk:
                return HttpResponseBadRequestResponse()

        if type == "lpo":
            from posts.models import PostsList
            PostsList.change_position(json.loads(request.body), community, user.pk)
            return HttpResponse(json.loads(request.body))
        elif type == "lph":
            from gallery.models import PhotoList
            PhotoList.change_position(json.loads(request.body), community, user.pk)
        elif type == "lgo":
            from goods.models import GoodList
            GoodList.change_position(json.loads(request.body), community, user.pk)
        elif type == "lvi":
            from video.models import VideoList
            VideoList.change_position(json.loads(request.body), community, user.pk)
        elif type == "ldo":
            from docs.models import DocsList
            _DocsList.change_position(json.loads(request.body), community, user.pk)
        elif type == "lmu":
            from music.models import MusicList
            _MusicList.change_position(json.loads(request.body), community, user.pk)
        elif type == "lsu":
            from survey.models import SurveyList
            SurveyList.change_position(json.loads(request.body), community, user.pk)
        return HttpResponse()
