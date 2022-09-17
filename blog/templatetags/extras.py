from django import template
register = template.Library()

# Template Tag for the Fetching the reply with its parent comment in Django html
@register.filter(name='get_val')
def get_val(dict,key):
    return dict.get(key)

