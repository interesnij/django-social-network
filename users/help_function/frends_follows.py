   def confirm_connection_with_user_with_id(self, user_id):
        check_is_not_fully_connected_with_user_with_id(user=self, user_id=user_id)

        connection = self.update_connection_with_user_with_id(user_id, circles_ids=circles_ids)

        if not self.is_following_user_with_id(user_id):
            self.follow_user_with_id(user_id)

        return connection

def update_connection_with_user_with_id(self, user_id):
    check_is_connected_with_user_with_id(user=self, user_id=user_id)

    connection = self.get_connection_for_user_with_id(user_id)
    connection.save()
    return connection

def disconnect_from_user(self, user):
    return self.disconnect_from_user_with_id(user.pk)

def disconnect_from_user_with_id(self, user_id):
    check_is_connected_with_user_with_id(user=self, user_id=user_id)
    if self.is_fully_connected_with_user_with_id(user_id):
        if self.is_following_user_with_id(user_id):
            self.unfollow_user_with_id(user_id)

    connection = self.connections.get(target_connection__user_id=user_id)
    connection.delete()

    return connection


def follow_user(self, user):
    return self.follow_user_with_id(user.pk)

def follow_user_with_id(self, user_id):
    check_can_follow_user_with_id(user=self, user_id=user_id)

    if self.pk == user_id:
        raise ValidationError(
            _('Вы не можете подписаться сами на себя'),
        )

    follow = Follow.create_follow(user_id=self.pk, followed_user_id=user_id)
    return follow

def unfollow_user(self, user):
    return self.unfollow_user_with_id(user.pk)

def unfollow_user_with_id(self, user_id):
    check_is_following_user_with_id(user=self, user_id=user_id)
    follow = self.follows.get(followed_user_id=user_id)
    follow.delete()

def get_followers(self, max_id=None):
    followers_query = self._make_followers_query()

    if max_id:
        followers_query.add(Q(id__lt=max_id), Q.AND)

    return User.objects.filter(followers_query).distinct()

def get_followings(self, max_id=None):
    followings_query = self._make_followings_query()

    if max_id:
        followings_query.add(Q(id__lt=max_id), Q.AND)

    return User.objects.filter(followings_query).distinct()

def search_followers_with_query(self, query):
    followers_query = Q(follows__followed_user_id=self.pk, is_deleted=False)

    names_query = Q(username__icontains=query)
    names_query.add(Q(profile__name__icontains=query), Q.OR)

    followers_query.add(names_query, Q.AND)

    return User.objects.filter(followers_query).distinct()

def search_followings_with_query(self, query):
    followings_query = Q(followers__user_id=self.pk, is_deleted=False)

    names_query = Q(username__icontains=query)
    names_query.add(Q(profile__name__icontains=query), Q.OR)

    followings_query.add(names_query, Q.AND)

    return User.objects.filter(followings_query).distinct()
