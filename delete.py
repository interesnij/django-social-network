# -*- coding: utf-8 -*-
from locale import *
import csv,sys,os

project_dir = '../tr/tr/'

sys.path.append(project_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django, json, requests

django.setup()

from django.conf import settings
from docs.models import DocList
from music.models import SoundList, Music
from video.models import VideoList
from docs.models import Doc
from chat.models import Message
from gallery.models import PhotoList
from chat.models import Message
from communities.models import Community
from communities.model.settings import CommunityPrivate
import re


text = "Соцсеть трезвый.рус! boroda.fm, https://street.company строится уже 24 месяцев. Сейчас она в состоянии почти завершенном. Проводятся последние работы, достраиваются нужные разделы (остается режим супер-управленцев, рекламная площадка)./."

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

words = text.split(" ")
if words:
    _loop, _exlude, this, next = [], [], -1, 0
    _loop.append(text)
    for word in words:
        if "." in word:
            print (". есть")

            #if word[-1] in ".,:;!_*-+()/#¤%&)":
            #    _p = word[:-1]
            #else:
            if "трезвый.рус" in word:
                a = ""
                _loop.append(a)
                this += 1
                next += 1
                _loop[next] = _loop[this].replace(word, '<a onclick="return stop_load_fullscreen(this);" class="ajax underline" href="' + word + '">' + word + '</a>')
                print ("трезвый.рус есть")
            else:
                for zone in zons:
                    if zone in word:
                        a = ""
                        _loop.append(a)
                        this += 1
                        next += 1
                        _loop[next] = _loop[this].replace(word, '<a onclick="return stop_load_fullscreen(this);" class="underline" target="_blank" href="' + word + '">' + word + '</a>')
                        print ("зона: ", zone)
                        break
        _exlude.append(word)
        ppp = _loop[next]
    print (ppp)
