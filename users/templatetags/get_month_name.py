from django import template
register=template.Library()


@register.filter
def get_month_name(value):
    if value == 1:
        return 'январь'
    if value == 2:
        return 'февраль'
    if value == 3:
        return 'март'
    if value == 4:
        return 'апрель'
    if value == 5:
        return 'май'
    if value == 6:
        return 'июнь'
    if value == 7:
        return 'июль'
    if value == 8:
        return 'август'
    if value == 9:
        return 'сентябрь'
    if value == 10:
        return 'октябрь'
    if value == 11:
        return 'ноябрь'
    if value == 12:
        return 'декабрь'
