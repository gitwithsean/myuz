from django import template

register = template.Library()

@register.filter
def camel_case(value):
    return "".join(word.capitalize() for word in value.split("_"))

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
