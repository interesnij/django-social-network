from django import template
import pymorphy2
register=template.Library()


@register.filter
def user_in(objects, user):
    if user.is_authenticated:
        return objects.filter(user=user).exists()
    return False

@register.filter
def rupluralize(value, arg="дурак,дурака,дураков"):
    args = arg.split(",")
    number = abs(int(value))
    a = number % 10
    b = number % 100

    if (a == 1) and (b != 11):
        return args[0]
    elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
        return args[1]
    else:
        return args[2]


@register.filter
def gent(value):
    morph = pymorphy2.MorphAnalyzer()
    word1 = morph.parse(value)[0]
    word2 = morph.parse(value)[0]
    v1 = word1.inflect({'gent'})
    v2 = word2.inflect({'gent'})
    result = v1.word + v2.word
    return result
