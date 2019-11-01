def verify_moderated_object_with_id(self, moderated_object_id):
    moderated_object = ModeratedObject.objects.get(pk=moderated_object_id)
    return self.verify_moderated_object(moderated_object=moderated_object)

def verify_moderated_object(self, moderated_object):
    check_can_verify_moderated_object(user=self, moderated_object=moderated_object)
    moderated_object.verify_with_actor_with_id(actor_id=self.pk)

def unverify_moderated_object_with_id(self, moderated_object_id):
    moderated_object = ModeratedObject.objects.get(pk=moderated_object_id)
    return self.unverify_moderated_object(moderated_object=moderated_object)

def unverify_moderated_object(self, moderated_object):
    check_can_unverify_moderated_object(user=self, moderated_object=moderated_object)
    moderated_object.unverify_with_actor_with_id(actor_id=self.pk)

def approve_moderated_object_with_id(self, moderated_object_id):
    moderated_object = ModeratedObject.objects.get(pk=moderated_object_id)
    return self.approve_moderated_object(moderated_object=moderated_object)

def approve_moderated_object(self, moderated_object):
    check_can_approve_moderated_object(user=self, moderated_object=moderated_object)
    moderated_object.approve_with_actor_with_id(actor_id=self.pk)

def reject_moderated_object_with_id(self, moderated_object_id):
    moderated_object = ModeratedObject.objects.get(pk=moderated_object_id)
    return self.reject_moderated_object(moderated_object=moderated_object)

def reject_moderated_object(self, moderated_object):
    check_can_reject_moderated_object(user=self, moderated_object=moderated_object)
    moderated_object.reject_with_actor_with_id(actor_id=self.pk)

def update_moderated_object_with_id(self, moderated_object_id, description=None,
                                    category_id=None):
    moderated_object = ModeratedObject.objects.get(pk=moderated_object_id)

    return self.update_moderated_object(moderated_object=moderated_object, description=description,
                                        category_id=category_id)

def update_moderated_object(self, moderated_object, description=None,
                                category_id=None):
    check_can_update_moderated_object(user=self, moderated_object=moderated_object)
    moderated_object.update_with_actor_with_id(actor_id=self.pk, description=description,
                                               category_id=category_id)
    return moderated_object


def report_comment_with_id_for_post_with_uuid(self, post_comment_id, post_uuid, category_id, description=None):
    post_comment = PostComment.objects.get(id=post_comment_id)
    post = Post.objects.get(uuid=post_uuid)

    return self.report_comment_for_post(post_comment=post_comment, category_id=category_id, description=description,
                                        post=post)

def report_comment_for_post(self, post_comment, post, category_id, description=None):
    check_can_report_comment_for_post(user=self, post_comment=post_comment, post=post)
    ModerationReport.create_post_comment_moderation_report(post_comment=post_comment,
                                                           category_id=category_id,
                                                           reporter_id=self.pk,
                                                           description=description)
    post_comment.delete_notifications_for_user(user=self)

def report_post_with_uuid(self, post_uuid, category_id, description=None):
    post = Post.objects.get(uuid=post_uuid)
    return self.report_post(post=post, category_id=category_id, description=description)

def report_post(self, post, category_id, description=None):
    check_can_report_post(user=self, post=post)
    ModerationReport.create_post_moderation_report(post=post,
                                                   category_id=category_id,
                                                   reporter_id=self.pk,
                                                   description=description)
    post.delete_notifications_for_user(user=self)

def report_user_with_username(self, username, category_id, description=None):
    user = User.objects.get(username=username)
    return self.report_user(user=user, category_id=category_id, description=description)

def report_user(self, user, category_id, description=None):
    check_can_report_user(user=self, user_to_report=user)
    ModerationReport.create_user_moderation_report(user=user,
                                                   category_id=category_id,
                                                   reporter_id=self.pk,
                                                   description=description)

def report_community_with_name(self, community_name, category_id, description=None):
    community = Community.objects.get(name=community_name)
    return self.report_community(community=community, category_id=category_id, description=description)

def report_community(self, community, category_id, description=None):
    check_can_report_community(user=self, community=community)
    ModerationReport.create_community_moderation_report(community=community,
                                                        category_id=category_id,
                                                        reporter_id=self.pk,
                                                        description=description)


def get_global_moderated_objects(self, types=None, max_id=None, verified=None, statuses=None):
    check_can_get_global_moderated_objects(user=self)
    ModeratedObject = get_moderated_object_model()

    moderated_objects_query = Q()

    if types:
        moderated_objects_query.add(Q(object_type__in=types), Q.AND)

    if max_id:
        moderated_objects_query.add(Q(id__lt=max_id), Q.AND)

    if verified is not None:
        moderated_objects_query.add(Q(verified=verified), Q.AND)

    if statuses is not None:
        moderated_objects_query.add(Q(status__in=statuses), Q.AND)

    return ModeratedObject.objects.filter(moderated_objects_query)

def get_logs_for_moderated_object_with_id(self, moderated_object_id, max_id=None):
    moderated_object = ModeratedObject.objects.get(pk=moderated_object_id)
    return self.get_logs_for_moderated_object(moderated_object=moderated_object, max_id=max_id)

def get_logs_for_moderated_object(self, moderated_object, max_id=None):
    check_can_get_moderated_object(user=self, moderated_object=moderated_object)

    query = Q()

    if max_id:
        query.add(Q(id__lt=max_id), Q.AND)

    return moderated_object.logs.filter(query)

def get_reports_for_moderated_object_with_id(self, moderated_object_id, max_id=None):
    moderated_object = ModeratedObject.objects.get(pk=moderated_object_id)
    return self.get_reports_for_moderated_object(moderated_object=moderated_object, max_id=max_id)

def get_reports_for_moderated_object(self, moderated_object, max_id=None):
    check_can_get_moderated_object(user=self, moderated_object=moderated_object)

    query = Q()

    if max_id:
        query.add(Q(id__lt=max_id), Q.AND)

    return moderated_object.reports.filter(query)

def get_community_moderated_objects(self, community_name, types=None, max_id=None, verified=None, statuses=None):
    check_can_get_community_moderated_objects(user=self, community_name=community_name)

    moderated_objects_query = Q(community__name=community_name)

    if types:
        moderated_objects_query.add(Q(object_type__in=types), Q.AND)

    if verified is not None:
        moderated_objects_query.add(Q(verified=verified), Q.AND)

    if statuses is not None:
        moderated_objects_query.add(Q(status__in=statuses), Q.AND)

    if max_id:
        moderated_objects_query.add(Q(id__lt=max_id), Q.AND)

    return ModeratedObject.objects.filter(moderated_objects_query)

def get_moderation_penalties(self, max_id=None):
    query = Q()
    if max_id:
        query.add(Q(id__lt=max_id), Q.AND)
    return self.moderation_penalties.filter(query)

def count_active_moderation_penalties(self):
    return self.get_moderation_penalties().filter(expiration__gt=timezone.now()).count()

def get_pending_moderated_objects_communities(self, max_id):
    """Retrieves the communities staff of that have pending moderated objects"""
    query = Q(memberships__user_id=self.pk) & (
            Q(memberships__is_moderator=True) | Q(memberships__is_administrator=True))

    query.add(Q(moderated_objects__status=ModeratedObject.STATUS_PENDING), Q.AND)

    if max_id:
        query.add(Q(id__lt=max_id), Q.AND)

    return Community.objects.filter(query).distinct()

def count_pending_communities_moderated_objects(self):

    query = Q(community__memberships__user_id=self.pk) & (
            Q(community__memberships__is_moderator=True) | Q(community__memberships__is_administrator=True))

    query.add(Q(status=ModeratedObject.STATUS_PENDING), Q.AND)

    return ModeratedObject.objects.filter(query).count()


def has_reported_post_comment_with_id(self, post_comment_id):
    return ModerationReport.objects.filter(reporter_id=self.pk,
                                           moderated_object__object_id=post_comment_id,
                                           moderated_object__object_type=ModeratedObject.OBJECT_TYPE_POST_COMMENT
                                           ).exists()

def has_reported_post_with_id(self, item_id):
    return ModerationReport.objects.filter(reporter_id=self.pk,
                                           moderated_object__object_id=item_id,
                                           moderated_object__object_type=ModeratedObject.OBJECT_TYPE_POST
                                           ).exists()

def has_reported_user_with_id(self, user_id):
    return ModerationReport.objects.filter(reporter_id=self.pk,
                                           moderated_object__object_id=user_id,
                                           moderated_object__object_type=ModeratedObject.OBJECT_TYPE_USER
                                           ).exists()

def has_reported_community_with_id(self, community_id):
    return ModerationReport.objects.filter(reporter_id=self.pk,
                                           moderated_object__object_id=community_id,
                                           moderated_object__object_type=ModeratedObject.OBJECT_TYPE_COMMUNITY
                                           ).exists()


def has_reported_moderated_object_with_id(self, moderated_object_id):
    return ModerationReport.objects.filter(reporter_id=self.pk,
                                           moderated_object__object_id=moderated_object_id,
                                           moderated_object__object_type=ModeratedObject.OBJECT_TYPE_MODERATED_OBJECT
                                           ).exists()


def get_longest_moderation_suspension(self):
    return self.moderation_penalties.order_by('expiration')[0:1][0]


def is_suspended(self):
    return self.moderation_penalties.filter(type=ModerationPenalty.TYPE_SUSPENSION,
                                            expiration__gt=timezone.now()).exists()


def count_moderation_penalties_for_moderation_severity(self, moderation_severity):
    return self.moderation_penalties.filter(
        moderated_object__category__severity=moderation_severity).count()
