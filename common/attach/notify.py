
def get_notify(user, notify):
    attach = notify.attach
    if attach[:3] == "pos":
        from common.items.post import get_post
        if notify.verb == "ITE":
            "ght"
        else:
            if notify.is_have_user_set():
                first_notify = notify.get_first_user_set()
                '<p><a href="' + first_notify.creator.get_link() + '" class="ajax">' + first_notify.creator.get_full_name() + '</a> '\
                + first_notify.get_verb_display() + str(notify.count_user_set()) + '</p>' + get_post(user, attach[3:])
            elif notify.is_have_object_set():
                first_notify = notify.get_first_object_set()
                '<p><a href="' + first_notify.creator.get_link() + '" class="ajax" style="font-weight: bold;">'+ \
                first_notify.creator.get_full_name() + '</a> и ещё ' + str(notify.count_object_set()) + first_notify.get_verb_display()\
                 + 'запись</p>' + get_post(user, attach[3:])
            else:
                get_post(user, attach[3:])
