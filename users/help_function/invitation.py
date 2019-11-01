def create_invite(self, nickname):
    check_can_create_invite(user=self, nickname=nickname)
    invite = UserInvite.create_invite(nickname=nickname, invited_by=self)
    self.invite_count = F('invite_count') - 1
    self.save()
    return invite

def update_invite(self, invite_id, nickname):
    check_can_update_invite(user=self, invite_id=invite_id)
    invite = UserInvite.objects.get(id=invite_id)
    invite.nickname = nickname
    invite.save()
    return invite

def get_user_invites(self, status_pending=None):
    invites_query = Q(invited_by=self)

    if status_pending is not None:
        invites_query.add(Q(created_user__isnull=status_pending), Q.AND)

    return UserInvite.objects.filter(invites_query)

def search_user_invites(self, query, status_pending=None):
    invites_query = Q(invited_by=self, nickname__icontains=query)

    if status_pending is not None:
        invites_query.add(Q(created_user__isnull=status_pending), Q.AND)

    return UserInvite.objects.filter(invites_query)

def delete_user_invite_with_id(self, invite_id):
    check_can_delete_invite_with_id(user=self, invite_id=invite_id)
    invite = UserInvite.objects.get(id=invite_id)
    self.invite_count = F('invite_count') + 1
    self.save()
    invite.delete()

def send_invite_to_invite_id_with_email(self, invite_id, email):
    check_can_send_email_invite_to_invite_id(user=self, invite_id=invite_id, email=email)
    invite = UserInvite.objects.get(id=invite_id)
    invite.email = email
    invite.send_invite_email()
