import string
from rest_framework.exceptions import PermissionDenied
import re
import urllib.request
import mimetypes

absolute_words = [
                "пизда",
                "блядь",
                "мудак",
                "мудил",
                "пидора",
                "дрочит",
                "залупа",
                "хуеть",
                "ебтвою",
                "заебись",
                "нахуйй",
                "похуйй",
                "нахерр",
                "похерр",
                "хуйня",
                "хуетень",
                "хуетаа",
                "хуёв",
                "охуев",
                "охуите",
                "нахуяч",
                "нехуйй",
                "похуйй",
                "нехуёв",
                "охуист",
                "хуйнутьь",
                "ахуячить",
                "тхуярить",
                "хуякнут",
                "дохуяч",
                "хуипан",
                "хуйлор",
                "уебало",
                "еблети",
                "ебатьь",
                "ебану́т",
                "ебальник",
                "ебаната",
                "ебанько",
                "ебанат",
                "выёбыва",
                "аебнуться",
                "поеботина",
                "поебень",
                "уёбищее",
                "заебала",
                "мозгоёб",
                "ебенев",
                "оебучий",
                "аебашить",
                "ебляя",
                "хуясебе",
                "хуйсни",
                "какогохуя",
                "схуяли",
                "хуюверт",
                "хуйнадо",
                "ебаныйв",
                "ебатьмозги",
                "оебучий",
                "аебашить",
                "ебляя",
                ]

relative_words = [
                    "блять",
                    "хуй",
                    "хер",
                    "хули",
                    "бля",
                ]

zons = [
        '.рф','.ru','.su','.net','.aero','.asia','.biz','.com','.info','.mobi','.name','.net','.org','.pro','.tel',
        '.travel','.xxx','.ad', '.ae', '.af', '.ai',
        '.al', '.am', '.aq', '.as', '.at', '.aw', '.ax', '.az', '.ba', '.be', '.bg', '.bh', '.bi', '.bj', '.bm',
        '.bo', '.bs', '.bt', '.ca', '.cc', '.cd', '.cf', '.cg', '.ch', '.ci', '.cl', '.cm', '.cn', '.co',
        '.cr', '.cu', '.cx', '.cz', '.de', '.dj', '. dk', '.dm', '.do', '.dz', '.ec', '.ee',
        '.es', '.eu', '.fi', '.fo', '.fr', '.ga', '.gd', '.ge', '.gf', '.gg', '.gi', '.gl', '.gm', '.gp', '.gr',
        '.gs', '.gy', ' .hk', '.hm', '.hn', '.hr', '.ht', '.hu', '.ie', '.im', '.in', '.io ', '.ir',
        '.is', '.it', '.je', '.jo', '.jp', '.kg', '.ki', '.kn', '.kr', '.ky', '.kz', '.li', '.lk', '.lt',
        '.lu', '.lv', '.ly', '.ma', '.mc', '.md', '.mg', '.mk', '.mo', '.mp', '.ms', '.mt', '.mu', '.mw',
        '.mx', '.my', ' .na', '.nc', '.nf', '.ng', '.nl', '.no', '.nu', '.nz',
        '.pe', '.ph', '.pk', '.pl', '.pn', '.pr', '.ps', '.pt', '.re', '.ro', '. rs', '.rw', '.sd', '.se', '.sg',
        '.si', '.sk', '.sl', '.sm', '.sn', '.so', '.sr', '.st', '.sz', '.tc', '.td', '.tg', '.tj', '.tk', '.tl',
        '.tm', '.tn', '.to', '.tt', '.tw', '.ua', '.ug', '.uk', '.us', '.vc', '.vg', '.vn', '.vu', '.ws', '.academy',
        '.accountant', '.accountants', '.actor', '.adult', '.africa', '.agency', '.airforce', '.apartments', '.app', '.army',
        '.art', '.associates', '.attorney', '.auction', '.audio', '.auto', '.band', '.bank', '.bar', '.bargains', '.bayern', '.beer',
        '.berlin', '.best', '.bet', '.bid', '.bike', '.bingo', '.bio', '.black', '.blackfriday', '.blog', '.blue', '.boutique',
        '.broker', '.brussels', '.build', '.builders', '.business', '.buzz', '.cab', '.cafe', '.cam', '.camera', '.camp', '.capital',
        '.car', '.cards', '.care', '.career', '.careers', '.cars', '.casa ', '.cash', '.casino', '.cat', '.catering', '.center',
        '.ceo', '.charity', '.chat', '.cheap', '.christmas', '.church', '.city', '.claims', '.cleaning', '.click', '.clinic',
        '.clothing', '.cloud', '.club', '.coach', '.codes', '.coffee', '.college', '.cologne', '.community', '.company', '.computer',
        '.condos', '.construction', '.consulting', '.contractors', '.cooking', '.cool', '.coop', '.country', '.coupons', '.courses',
        '.credit', '.creditcard', '.cricket', '.cruises', '.dance', '.date', '.dating', '.deals', '.degree', '.delivery', '.democrat',
        '.dental', '.dentist', '.desi', '.design', '.diamonds', '.diet', '.digital', '.direct', '.directory', '.discount', '.doctor',
        '.dog', '.domains', '.download', '.earth', '.education', '.email', '.energy', '.engineer', '.engineering', '.enterprises',
        '.equipment', '.estate', '.events', '.exchange', '.expert', '.exposed', '.express', '.fail', '.faith', '.family', '.fans',
        '.farm', '.fashion', '.film', '.finance', '.financial', '.fish', '.fishing', '.fit', '.fitness', '.flights', '.florist',
        '.flowers', '.fm', '.football', '.forex', '.forsale', '.foundation', '.fun', '.fund', '.furniture', '.futbol', '.fyi',
        '.gallery', '.game', '.games', '.garden', '.gent', '.gift', '.gifts', '.gives', '.glass', '.global', '.gmbh', '.gold', '.golf',
        '.graphics', '.gratis', '.green', '.gripe', '.group', '.guide', '.guitars', '.guru', '.haus', '.healthcare', '.help',
        '.hiphop', '.hockey', '.holdings', '.holiday', '.horse', '.hospital', '.host', '.hosting', '.house', '.how', '.immo',
        '.immobilien', '.industries', '.ink', '.institute', '.insure', '.international', '.investments', '.irish', '.jewelry',
        '.jobs', '.juegos', '.kaufen', '.kim', '.kitchen', '.kiwi', '.land', '.lawyer', '.lease', '.legal', '.life', '.lighting',
        '.limited', '.limo', '.link', '.live', '.llc', '.loan', '.loans', '.lol', '.london', '.love', '.ltd', '.luxe', '.luxury',
        '.maison', '.management', '.market', '.marketing', '.mba', '.media', '.memorial', '.men', '.menu', '.miami', '.moda', '.moe',
        '.mom', '.money', '.mortgage', '.moscow', '.movie', '.navy ', '.network', '.news', '.ninja', '.observer', '.one', '.onl',
        '.online', '.ooo', '.page ', '.paris', '.partners', '.parts', '.party', '.pet', '.photo', '.photography', '.photos',
        '.pics', '.pictures', '.pink', '.pizza', '.plumbing', '.plus', '.poker', '.press', '.productions', '.promo',
        '.properties', '.property', '.protection', '.pub', '.qpon', '.racing', '.radio', '.realty',
        '.recipes', '.red', '.rehab', '.reisen', '.rent', '.rentals', '.repair', '.report', '.republican', '.rest', '.restaurant ',
        '.review', '.reviews', '.rich', '.rip', '.rocks', '.rodeo', '.run', '.sale', '.salon', '.sarl', '.school',
        '.schule', '.science', '.security', '.services', '.sex', '.sexy', ' .shiksha', '.shoes', '.shop', '.shopping',
        '.show', '.singles', '.site', '.ski', '.soccer ', '.social', '.software', '.solar', '.solutions', '.soy',
        '.space', '.sport', '.store', '.stream', '.studio', '.study', '.style', '.sucks', '.supplies', '.supply',
        '.support', '.surf', '.surgery', '.systems', '.tatar', '.tattoo', '.tax', '.taxi', '.team', '.tech',
        '.technology', '.tennis', '.theater', '.theatre', '.tickets', '.tienda', '.tips', '.tires', '.tirol', '.today', '.tools',
        '.top', '.tours', '.town', '.toys', '.trade', '.trading', '.training', '.tube', '.tv', '.university', '.uno', '.vacations',
        '.vegas', '.ventures', '.vet', '.viajes', '.video', '.villas', '.vin', '.vip', '.vision', '.vodka', '.vote', '.voting',
        '.voto', '.voyage', '.watch', '.webcam', '.website', '.wedding', '.wien', '.wiki', '.win', '.wine', '.work', '.works',
        '.world', '.wtf', '.xyz', '.yoga', '.zone', '.дети', '.москва', '.онлайн', '.орг', '.рус', '.сайт'
    ]

def distance(a, b):
    "Вычисляет расстояние Левенштейна между a и b."
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]

def is_have_bad_words(text):
    lower_replace_text = text.lower().replace(" ", "")
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    _text = re.sub(CLEANR, '', lower_replace_text)

    d = {'а' : ['а', 'a', '@'],
      'б' : ['б', '6', 'b'],
      'в' : ['в', 'b', 'v'],
      'г' : ['г', 'r', 'g'],
      'д' : ['д', 'd'],
      'е' : ['е', 'e'],
      'ё' : ['ё', 'e'],
      'ж' : ['ж', 'zh', '*'],
      'з' : ['з', '3', 'z'],
      'и' : ['и', 'u', 'i'],
      'й' : ['й', 'u', 'i'],
      'к' : ['к', 'k', 'i{', '|{'],
      'л' : ['л', 'l', 'ji'],
      'м' : ['м', 'm'],
      'н' : ['н', 'h', 'n'],
      'о' : ['о', 'o', '0'],
      'п' : ['п', 'n', 'p'],
      'р' : ['р', 'r', 'p'],
      'с' : ['с', 'c', 's'],
      'т' : ['т', 'm', 't'],
      'у' : ['у', 'y', 'u'],
      'ф' : ['ф', 'f'],
      'х' : ['х', 'x', 'h' , '}{'],
      'ц' : ['ц', 'c', 'u,'],
      'ч' : ['ч', 'ch'],
      'ш' : ['ш', 'sh'],
      'щ' : ['щ', 'sch'],
      'ь' : ['ь', 'b'],
      'ы' : ['ы', 'bi'],
      'ъ' : ['ъ'],
      'э' : ['э', 'e'],
      'ю' : ['ю', 'io'],
      'я' : ['я', 'ya']
    }
    for key, value in d.items():
        for letter in value:
            for phr in _text:
                if letter == phr:
                    _text = _text.replace(phr, key)

    for word in absolute_words:
        for part in range(len(_text)):
            fragment = _text[part: part+len(word)]
            if distance(fragment, word) <= len(word)*0.25:
                bad_text = "Исправьте слово: " + fragment + ", похожее на " + word
                raise PermissionDenied(bad_text)
    return False

def create_mention_and_socket(self, recipient, socket_name):
    from asgiref.sync import async_to_sync
    from channels.layers import get_channel_layer

    channel_layer = get_channel_layer()
    payload = {
        'type': 'receive',
        'key': 'notification',
        'recipient_id': str(recipient.id),
        'name': socket_name,
        'beep': beep_on,
    }
    async_to_sync(channel_layer.group_send)('notification', payload)

def is_html_link(link, strict=True):
    link_type, _ = mimetypes.guess_type(link)
    if link_type is None and strict:
        u = urllib.request.urlopen(link)
        link_type = u.headers["content-type"]
    return link_type

def get_formatted_text(text, is_message=False):
    _words = text.replace("<img src"," |<imgsrc").replace('.png">','.png">| ').replace("\n"," <br> ").replace("<br>"," <br> ").replace("&nbsp;"," ") 
    words = _words.replace("  "," ").split(" ")

    if words:
        _loop, _exlude, this, next, count = [], [], -1, 0, 0
        _loop.append(text)
        for word in words:
            count += 1
            if count == 1:
                indent = ""
            else:
                indent = " "
            if word == "":
                continue
            if "#" in word:
                _loop.append("")
                this += 1
                next += 1

                if word[0] == "#":
                    _p = word.strip(".,:;!_*-+()/@#¤%&)")
                    tag = "#" + _p
                    _loop[next] = _loop[this].replace(indent + tag, indent + '<a class="ajax action"href="/search/?tag=' + _p + '">' + tag + '</a>').replace("#<", "<")
                else:
                    _p = word.strip(".,:;!_*-+()/@#¤%&)")
                    p_2 = _p[_p.find("#") + 1:]
                    tag = "#" + p_2
                    _loop[next] = _loop[this].replace(tag, '<a class="ajax action"href="/search/?tag=' + p_2 + '">' + tag + '</a>')
            if word[0] == "@":
                from common.model.other import CustomLink
                exists = False
                _p = word.strip(".,:;!_*-+()/@#¤%&)").lower()

                if _p[:2] == "id":
                    from users.models import User
                    if User.objects.filter(id=_p[2:]).exists():
                        user = User.objects.get(id=_p[2:])
                        exists, name = True, user.get_full_name()
                elif _p[:6] == "public":
                    from communities.models import Community
                    if Community.objects.filter(id=_p[6:]).exists():
                        community = Community.objects.get(id=_p[6:])
                        exists, name = True, community.name
                elif _p[:4] == "chat":
                    from chat.models import Chat
                    if Chat.objects.filter(id=_p[4:]).exists():
                        chat = Chat.objects.get(id=_p[4:])
                        exists, name = True, chat.name
                elif CustomLink.objects.filter(link=_p).exists():
                    exists = True
                    link = CustomLink.objects.get(link=_p)
                    if link.community:
                        name = link.community.name
                    else:
                        name = link.user.get_full_name()
                if exists:
                    _loop.append("")
                    this += 1
                    next += 1
                    p_2 = "@" + _p
                    _loop[next] = _loop[this].replace(indent + word, indent + '<a class="action ajax show_mention_info pointer"href="/' + _p + '/">' + name + '</a>')

            elif "." in word:
                _p = word.strip(".,:;!_*-+()/@#¤%&)")
                if "." in _p and not ".png" in _p:
                    if _p[0] == "h":
                        p_2 = _p
                    else:
                        p_2 = "//" + _p
                    if "трезвый.рус" in _p:
                        _loop.append("")
                        p_2 = _p.replace("трезвый.рус", "/").replace("http://", "").replace("https://", "")
                        this += 1
                        next += 1
                        _loop[next] = _loop[this].replace(indent + _p, indent + '<a class="ajax action"href="' + p_2 + '">' + _p[:30] + '</a>')
                    else:
                        p_items = _p.split(".")

                        type = is_html_link(_p)
                        if "text/html" in type or "x-msdos-program" in type:
                            p_zone = "." + p_items[-1]
                        else:
                            p_zone = "." + p_items[-2]
                        if "/" in p_zone:
                            p_zone = p_zone.partition('/')[0]
                        for zone in zons:
                            if zone == p_zone:
                                _loop.append("")
                                this += 1
                                next += 1
                                _loop[next] = _loop[this].replace(_p, '<a class="action"rel="nofollow"target="_blank"href="' + p_2 + '">' + _p[:30] + '</a>')
                                break
                    _exlude.append(_p)
        result = _loop[next].replace(" |<imgsrc","<img src").replace('.png">| ','.png">').replace(" <br> ","<br>")
        return result

def get_text_processing(text, is_message=False):
    is_have_bad_words(text)
    return get_formatted_text(text, is_message=False)
