from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key))  # importante: cast a str para coincidir con las claves del dict
