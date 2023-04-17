from django import template

register = template.Library()

@register.filter
def camel_case(value):
    return spaceless("".join(word.capitalize() for word in value.split("_")))

@register.filter
def spaceless(value):
    return value.replace(' ', '')

@register.filter
def lowercase(value):
    return value.lower()

@register.filter
def underscore_before_camelhumps(value):
    # Iterate through all characters in the string
    new_value = ''
    for i in range(len(value)):
        # If the current character is uppercase, add an underscore before it
        if value[i].isupper() and i != 0:
            new_value += '_' + value[i]
        else:
            new_value += value[i]
    return new_value

@register.filter
def camelhunps_lowercase_underscore(value):
    return underscore_before_camelhumps(value).lower()
                     
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
