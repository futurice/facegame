from django import template
from django.conf import settings
from django.template.loader import render_to_string, get_template
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.contrib.sites.models import get_current_site
from django.shortcuts import get_object_or_404
from django.db.models.fields import FieldDoesNotExist

from datetime import datetime
from facegame.nameguessing.views import get_image_for_hash

register = template.Library()

@register.simple_tag()
def imgchoice(index, l):
    return get_image_for_hash(l[index])
