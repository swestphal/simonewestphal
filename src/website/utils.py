import random
import string

from django.utils.text import slugify


#from django import template


#register = template.Library()


def germanslugify(value):
    replacements = [(u'ä', u'ae'), (u'ö', u'oe'),
                    (u'ü', u'ue'), (u'ß', u'ss'), ]
    for (s, r) in replacements:
        value = value.replace(s, r)
    return slugify(value)


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance 
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = germanslugify(new_slug.lower())
    else:
        if (hasattr(instance, 'title')):
            bezeichnung = instance.title
        else:
            bezeichnung = instance.name
        slug = germanslugify(bezeichnung.lower())

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)

    return slug
