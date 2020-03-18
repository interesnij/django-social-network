from django import template
register=template.Library()


@register.filter
def get_month_name(value):
    if value == 1:
        return 'январь'
    elif value == 2:
        return 'февраль'
    elif value == 3:
        return 'март'
    elif value == 4:
        return 'апрель'
    elif value == 5:
        return 'май'
    elif value == 6:
        return 'июнь'
    elif value == 7:
        return 'июль'
    elif value == 8:
        return 'август'
    elif value == 9:
        return 'сентябрь'
    elif value == 10:
        return 'октябрь'
    elif value == 11:
        return 'ноябрь'
    elif value == 12:
        return 'декабрь'
