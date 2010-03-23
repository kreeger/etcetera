"""DateTime form fields that are very flexible in what formats they
accept by using the ``python-dateutil`` parser.

Based on:
    http://www.djangosnippets.org/snippets/268/
But changed to:
    * Subclass the default fields, which means:
        - Standard EMPTY_VALUES handling.
        - Standard localized validation error messages.
    It also means we are still let the parent class try the default
    input formats before falling back to the dateutil parser. You
    can change that by passing anempty ``input_formats`` list to
    ``__init__``.

    * Added support for ``SplitDateTimeWidget``.

    * Support for custom ``parserinfo``, custom ``parse`` arguments.
"""

from __future__ import absolute_import

from datetime import datetime, date
from dateutil import parser
from django.db import models
from django import forms
from django.forms import ValidationError


__all__ = ('DateTimeField', 'DateField',
           'get_formfield_for', 'formfield_callback',)


class DateUtilMixin(object):
    """Helper that implements shared dateutil-related functionality-

    ``parserinfo`` is the parserinfo class that will be used with
    the python-dateutil parser.

    ``parse_kwargs`` are additional arguments that will be passed
    to python-dateutil's ``parse`` function.
    """
    
    def __init__(self, *args, **kwargs):
        self.parserinfo = kwargs.pop('parserinfo', None)
        self.parse_kwargs = kwargs.pop('parse_kwargs', {})
        super(DateUtilMixin, self).__init__(*args, **kwargs)
    
    def parse(self, value):
        # Call dateutil.parser with the configured values.
        kw = self.parse_kwargs.copy()
        if self.parserinfo:
            kw.update({'parserinfo': self.parserinfo})
        return parser.parse(value, **kw)
    

class DateTimeField(DateUtilMixin, forms.DateTimeField):
    """DateTime field that accepts natural-language input.
    """

    def clean(self, value):
        try:
            return super(DateTimeField, self).clean(value)
        except ValidationError, pe:
            # Copied this from parent class.
            if isinstance(value, list):
                # Input comes from a SplitDateTimeWidget, for example.
                # So, it's two components: date and time.
                if len(value) != 2:
                    raise ValidationError(self.error_messages['invalid'])
                value = '%s %s' % tuple(value)

            try:
                return self.parse(value)
            except ValueError:
                raise pe


class DateField(DateUtilMixin, forms.DateField):
    """Date field that accepts natural-language input.
    """

    def clean(self, value):
        try:
            value = super(DateField, self).clean(value)
        except ValidationError, pe:
            try:
                return self.parse(value).date()
            except ValueError:
                raise pe


def get_formfield_for(field, **kwargs):
    """Returns a matching one of our form fields for the model field
    ``field`` (e.g. a DateTime form field for a DateTime model field),
    or ``None``, if we do not have a matching form field.

    This is intended to help you create a form that is using these
    dateutil parser-based form fields. You probably want to use this
    inside your ModelForm's ``formfield_callback`` method. In ``kwargs``
    you may pass arguments specific to our fields, like a ``parserinfo``.

    For simple cases, a full ``formfield_callback`` implementation is
    also provided by us, see below.

    Note that we are passing a custom ``form_class`` argument to the
    model field's formfield() method, rather than creating an instance
    of the form field ourselves. This ensures that Django still takes
    care of initializing the form field with the proper label, required
    status etc, based on the model field; otherwise, we'd have to do that
    ourselves.
    """
    if isinstance(field, models.DateTimeField):
        kwargs.update({'form_class': DateTimeField})
        return field.formfield(**kwargs)
    elif isinstance(field, models.DateField):
        kwargs.update({'form_class': DateField})
        return field.formfield(**kwargs)


def formfield_callback(field, **kwargs):
    """An implementation of a ``ModelForm.formfield_callback``
    implementation that you can use to get these dateutil.parser based
    form field implementations.

        class MyForm(ModelForm):
            formfield_callback = dateutil_fields.formfield_callback
            class Meta:
                model = Foo

    If you need more control, see the ``get_formfield_for`` helper.
    """
    result = get_formfield_for(field, **kwargs)
    if not result:
        result = field.formfield(**kwargs)
    return result