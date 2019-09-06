"""Amendment UI helpers."""

import difflib

from django import template
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.db import models


register = template.Library()


@register.simple_tag
def field_diff(aid, amendment, field):
    """Returns the difference between the two values in html."""

    v1 = extract_value(aid, field)
    v2 = extract_value(amendment, field)

    try:
        diff = list(difflib.ndiff(v1, v2))
    except Exception:
        diff = []

    html_diff = [make_html_diff_line(line) for line in diff]
    return mark_safe('<pre>{}</pre>'.format('\n'.join(html_diff)))


def extract_value(obj, field):
    """Get the value for a model field.

    Getting the actual displayable value depends on the field type.
      - CharField: display as if
      - CharField with choices: show the `get_FOO_display` result
      - ForeignKey: show the foreign object `__str__`
      - ManyToMany: show a list of objects' `__str__`
      - ArrayField: show a list of values
      - ArrayField with a `choices` for the `base_field`: show a list of
        get_FOO_display
      - Other fields: display raw value

    Since difflib compares list of strings, we return a list.
    """

    raw_val = getattr(obj, field)
    model_field = obj._meta.get_field(field)

    if isinstance(raw_val, str):
        val = raw_val.splitlines()

    elif isinstance(raw_val, list):
        if hasattr(model_field, 'base_field'):
            choices = model_field.base_field.choices
        else:
            choices = model_field.choices

        if choices:
            data_dict = dict(choices)
            val = [data_dict[c] for c in raw_val]
        else:
            val = raw_val

    elif isinstance(model_field, models.ManyToManyField):
        val = list(raw_val.all())
    else:
        val = ['{}'.format(raw_val)]

    return val


def make_html_diff_line(line):
    """Generates the html for a single line.

    The line is in the format generated by `difflib.Differ`.
    """
    if not line:
        return None

    prefix = line[0]
    content = line[2:].rstrip('\n')
    diff_class = {
        '+': 'add',
        '-': 'rm',
        '?': 'context',
        ' ': 'common',
    }.get(prefix)
    html = format_html(
        '<div class="diff-line {}"><span class="prefix">{} </span>{}</div>',
        diff_class, prefix, content)
    return html
