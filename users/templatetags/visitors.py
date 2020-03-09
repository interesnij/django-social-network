from django import template
register=template.Library()


@register.filter
def count_visitor_for_user(user, user_id):
    return user.get_count_visitor_for_user(user_id)

@register.filter
def count_visitor_pluralize(value, arg="дурак,дурака"):
    args = arg.split(",")
    a = value % 10
    b = value % 100

    if (a == 1) and (b != 11):
        return args[0]
    elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
        return args[1]
