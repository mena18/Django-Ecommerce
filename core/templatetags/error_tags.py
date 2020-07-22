from django import template

register = template.Library()

@register.filter
def err_tag(tag):
    m={'error':'danger','info':'info','success':"success","warning":"warning"}
    return m[tag];
