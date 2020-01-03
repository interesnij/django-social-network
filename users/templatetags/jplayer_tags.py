from django import template
register = template.Library()


@register.filter
def render_jplayer(context, player):
    return {'player': player}
