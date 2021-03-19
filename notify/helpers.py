ITEM, SUGGEST_ITEM = "ITE", "SIT"
COMMENT, WOMEN_COMMENT, GROUP_COMMENT = 'COM', 'WCOM', 'GCOM'
REPLY, WOMEN_REPLY, GROUP_REPLY = 'REP', 'WREP', 'GREP'

LIKE, WOMEN_LIKE, GROUP_LIKE = 'LIK', 'WLIK', 'GLIK'
DISLIKE, WOMEN_DISLIKE, GROUP_DISLIKE = 'DIS', 'WDIS', 'GDIS'
LIKE_COMMENT, WOMEN_LIKE_COMMENT, GROUP_LIKE_COMMENT =  'LCO', 'WLCO', 'GLCO'
DISLIKE_COMMENT, WOMEN_DISLIKE_COMMENT, GROUP_DISLIKE_COMMENT =  'DCO', 'WDCO', 'GDCO'
LIKE_REPLY, WOMEN_LIKE_REPLY, GROUP_LIKE_REPLY = 'LRE', 'WLRE', 'GLRE'
DISLIKE_REPLY, WOMEN_DISLIKE_REPLY, GROUP_DISLIKE_REPLY = 'DRE', 'WDRE', 'GDRE'
SURVEY_VOTE, WOMEN_SURVEY_VOTE, GROUP_SURVEY_VOTE = 'SVO', 'WSVO', 'GSVO'

USER_MENTION, WOMEN_USER_MENTION, GROUP_USER_MENTION = 'PUM', 'WPUM', 'GPUM'
COMMENT_USER_MENTION, WOMEN_COMMENT_USER_MENTION, GROUP_COMMENT_USER_MENTION = 'PCUM', 'WPCUM', 'GPCUM'

REPOST, WOMEN_REPOST, GROUP_REPOST = 'RE', 'WRE', 'GRE'
COMMUNITY_REPOST, GROUP_COMMUNITY_REPOST = 'CR', 'GCR'
LIST_REPOST, WOMEN_LIST_REPOST, GROUP_LIST_REPOST = 'LRE', 'WLRE', 'GLRE'
COMMUNITY_LIST_REPOST, GROUP_COMMUNITY_REPOST = 'CLR', 'GCLR'

#'подал заявку в' друзья 'подал заявку в' сообщество - универсальное
CONNECTION_REQUEST, WOMEN_CONNECTION_REQUEST, GROUP_CONNECTION_REQUEST = 'CRE', 'WCRE', 'GCRE'
#'принят в' друзья 'принят в' сообщество - универсальное
CONNECTION_CONFIRMED, WOMEN_CONNECTION_CONFIRMED, GROUP_CONNECTION_CONFIRMED = 'CCO', 'WCCO', 'GCCO'
#'рекомендует' друзей 'рекомендует' сообщество - универсальное
INVITE, WOMEN_INVITE, GROUP_INVITE = 'INV', 'WINV', 'GINV'
COMMUNITY_JOIN, WOMEN_COMMUNITY_JOIN, GROUP_COMMUNITY_JOIN = 'CJO', 'WCJO', 'GCJO'

REGISTER, WOMEN_REGISTER, GROUP_REGISTER = 'REG', 'WREG', 'GREG'

UNREAD, READ, DELETED = 'U', 'R', 'D'

VERB = (
    (ITEM, ' разместил'),
    (COMMENT, ' оставил'), (WOMEN_COMMENT, ' оставила'), (GROUP_COMMENT, ' оставили'),
    (REPLY, ' ответил на'), (WOMEN_REPLY, ' ответила на'), (GROUP_REPLY, ' ответили на'),

    (USER_MENTION, ' упомянул Вас в записи'), (WOMEN_USER_MENTION, ' упомянула Вас в записи'), (GROUP_USER_MENTION, ' упомянули Вас в записи'),
    (COMMENT_USER_MENTION, ' упомянул Вас в комментарии к записи'), (WOMEN_COMMENT_USER_MENTION, ' упомянула Вас в комментарии к записи'), (GROUP_COMMENT_USER_MENTION, ' упомянули Вас в комментарии к записи'),

    (LIKE, ' оценил'), (WOMEN_LIKE, ' оценила'), (GROUP_LIKE, ' оценили'),
    (DISLIKE, ' не оценил'), (WOMEN_DISLIKE, ' не оценила'), (GROUP_DISLIKE, ' не оценили'),
    (LIKE_COMMENT, ' оценил'), (WOMEN_LIKE_COMMENT, ' оценила '), (GROUP_LIKE_COMMENT, ' оценили'),
    (DISLIKE_COMMENT, ' не оценил'), (WOMEN_DISLIKE_COMMENT, ' не оценила'), (GROUP_DISLIKE_COMMENT, ' не оценили'),
    (LIKE_REPLY, ' оценил'), (WOMEN_LIKE_REPLY, ' оценила'), (GROUP_LIKE_REPLY, ' оценили'),
    (DISLIKE_REPLY, ' не оценил'), (WOMEN_DISLIKE_REPLY, ' не оценила'), (GROUP_DISLIKE_REPLY, ' не оценили'),
    (SURVEY_VOTE, ' участвовал в опросе'), (WOMEN_SURVEY_VOTE, ' участвовала в опросе'), (GROUP_SURVEY_VOTE, ' участвовали в опросе'),

    (REPOST, ' поделился'), (WOMEN_REPOST, ' поделилась'), (GROUP_REPOST, ' поделились'),
    (COMMUNITY_REPOST, ' поделилось'), (GROUP_COMMUNITY_REPOST, ' поделились'),
    (LIST_REPOST, ' поделился'), (WOMEN_REPOST, ' поделилась'), (GROUP_REPOST, ' поделились'),
    (COMMUNITY_LIST_REPOST, ' поделилось'), (GROUP_COMMUNITY_REPOST, ' поделились'),

    (CONNECTION_REQUEST, ' подал заявку в'), (WOMEN_CONNECTION_REQUEST, ' подала заявку в'), (GROUP_CONNECTION_REQUEST, ' подали заявку в'),
    (CONNECTION_CONFIRMED, ' принят в'), (WOMEN_CONNECTION_CONFIRMED, ' принята'), (GROUP_CONNECTION_CONFIRMED, ' приняты'),
    (INVITE, ' рекомендует'), (WOMEN_INVITE, ' рекомендует'), (GROUP_INVITE, ' рекомендуют'),
    (COMMUNITY_JOIN, ' принят'), (WOMEN_COMMUNITY_JOIN, ' принята'), (GROUP_COMMUNITY_JOIN, ' приняты'),

    (REGISTER, ' зарегистрировался'), (WOMEN_REGISTER, ' зарегистрировалась'), (GROUP_REGISTER, ' зарегистрировались'),
)

STATUS = ((UNREAD, 'Не прочитано'),(READ, 'Прочитано'),(DELETED, 'Удалено'),)
