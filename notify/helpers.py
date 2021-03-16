ITEM = "I"
COMMENT, WOMEN_COMMENT, GROUP_COMMENT = 'C', 'WC', 'GC'
REPLY, WOMEN_REPLY, GROUP_REPLY = 'R', 'WR', 'GR'
USER_MENTION, WOMEN_USER_MENTION, GROUP_USER_MENTION = 'PUM', 'WPUM', 'GPUM'
COMMENT_USER_MENTION, WOMEN_COMMENT_USER_MENTION, GROUP_COMMENT_USER_MENTION = 'PCUM', 'WPCUM', 'GPCUM'
LIKE, WOMEN_LIKE, GROUP_LIKE = 'L', 'WL', 'GL'
DISLIKE, WOMEN_DISLIKE, GROUP_DISLIKE = 'D', 'WD', 'GD'
LIKE_REPLY, WOMEN_LIKE_REPLY, GROUP_LIKE_REPLY = 'LR', 'WLR', 'GLR'
DISLIKE_REPLY, WOMEN_DISLIKE_REPLY, GROUP_DISLIKE_REPLY = 'DR', 'WDR', 'GDR'
LIKE_COMMENT, WOMEN_LIKE_COMMENT, GROUP_LIKE_COMMENT =  'LC', 'WLC', 'GLC'
DISLIKE_COMMENT, WOMEN_DISLIKE_COMMENT, GROUP_DISLIKE_COMMENT =  'DC', 'WDC', 'GDC'

REPOST, WOMEN_REPOST, GROUP_REPOST = 'RE', 'WRE', 'GRE'
COMMUNITY_REPOST, GROUP_COMMUNITY_REPOST = 'CR', 'GCR'
LIST_REPOST, WOMEN_LIST_REPOST, GROUP_LIST_REPOST = 'LRE', 'WLRE', 'GLRE'
COMMUNITY_LIST_REPOST, GROUP_COMMUNITY_REPOST = 'CLR', 'GCLR'

UNREAD, READ, DELETED = 'U', 'R', 'P'

VERB = (
    (ITEM, 'разместил'),
    (COMMENT, 'оставил'), (WOMEN_COMMENT, 'оставила'), (GROUP_COMMENT, 'оставили'),
    (REPLY, 'ответил на'), (WOMEN_REPLY, 'ответила на'), (GROUP_REPLY, 'ответили на'),
    (USER_MENTION, 'упомянул Вас в записи'), (WOMEN_USER_MENTION, 'упомянула Вас в записи'), (GROUP_USER_MENTION, 'упомянули Вас в записи'),
    (COMMENT_USER_MENTION, 'упомянул Вас в комментарии к записи'), (WOMEN_COMMENT_USER_MENTION, 'упомянула Вас в комментарии к записи'), (GROUP_COMMENT_USER_MENTION, 'упомянули Вас в комментарии к записи'),
    (LIKE, 'оценил'), (WOMEN_LIKE, 'оценила'), (GROUP_LIKE, 'оценили'),
    (DISLIKE, 'не оценил'), (WOMEN_DISLIKE, 'не оценила'), (GROUP_DISLIKE, 'не оценили'),
    (LIKE_COMMENT, 'оценил'), (WOMEN_LIKE_COMMENT, 'оценила '), (GROUP_LIKE_COMMENT, 'оценили'),
    (DISLIKE_COMMENT, 'не оценил'), (WOMEN_DISLIKE_COMMENT, 'не оценила'), (GROUP_DISLIKE_COMMENT, 'не оценили'),
    (LIKE_REPLY, 'оценил'), (WOMEN_LIKE_REPLY, 'оценила'), (GROUP_LIKE_REPLY, 'оценили'),
    (DISLIKE_REPLY, 'не оценил'), (WOMEN_DISLIKE_REPLY, 'не оценила'), (GROUP_DISLIKE_REPLY, 'не оценили'),

    (REPOST, 'поделился'), (WOMEN_REPOST, 'поделилась'), (GROUP_REPOST, 'поделились'),
    (COMMUNITY_REPOST, 'поделилось'), (GROUP_COMMUNITY_REPOST, 'поделились'),
    (LIST_REPOST, 'поделился'), (WOMEN_REPOST, 'поделилась'), (GROUP_REPOST, 'поделились'),
    (COMMUNITY_LIST_REPOST, 'поделилось'), (GROUP_COMMUNITY_REPOST, 'поделились'),
)

STATUS = ((UNREAD, 'Не прочитано'),(READ, 'Прочитано'),(DELETED, 'Удалено'),)
