from django import template

register = template.Library()

@register.filter
def widget_class_name(field):
    return field.field.widget.__class__.__name__

@register.filter
def widget_in_classes(field, class_list):
    widget_class = field.field.widget.__class__.__name__
    return widget_class in class_list.split(',')