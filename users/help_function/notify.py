def has_notification_with_id(self, notification_id):
    return self.notifications.filter(pk=notification_id).exists()

def has_follow_notifications_enabled(self):
    return self.notifications_settings.follow_notifications

def has_post_comment_mention_notifications_enabled(self):
    return self.notifications_settings.post_comment_user_mention_notifications

def has_post_mention_notifications_enabled(self):
    return self.notifications_settings.post_user_mention_notifications

def has_reaction_notifications_enabled_for_post_with_id(self, item_id):
    return self.notifications_settings.post_reaction_notifications and not self.has_muted_post_with_id(
        item_id=item_id)

def has_reaction_notifications_enabled_for_post_comment(self, post_comment):
    return self.notifications_settings.post_comment_reaction_notifications and not self.has_muted_post_with_id(
        item_id=post_comment.item_id) and not self.has_muted_post_comment_with_id(
        post_comment_id=post_comment.id)

def has_comment_notifications_enabled_for_post_with_id(self, item_id):
    return self.notifications_settings.post_comment_notifications and not self.has_muted_post_with_id(
        item_id=item_id)

def has_reply_notifications_enabled_for_post_comment(self, post_comment):
    return self.notifications_settings.post_comment_reply_notifications and not self.has_muted_post_with_id(
        item_id=post_comment.item_id) and not self.has_muted_post_comment_with_id(
        post_comment_id=post_comment.id)

def has_connection_request_notifications_enabled(self):
    return self.notifications_settings.connection_request_notifications

def has_community_invite_notifications_enabled(self):
    return self.notifications_settings.community_invite_notifications

def has_connection_confirmed_notifications_enabled(self):
    return self.notifications_settings.connection_confirmed_notifications
