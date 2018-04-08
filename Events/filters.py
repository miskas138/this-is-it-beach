import django_filters
from Events.models import *


class PostFilter(django_filters.FilterSet):
    class Meta:
        model = Event
        fields = {'section': ['icontains'],
                  'title': ['icontains', ],
                  'user__username': ['icontains', ],
                  'information__dateTime': ['lte', 'gte'],
                  'location__city': ['icontains'],
                  'location__address': ['icontains'],
                  'information__ticket_price': ['lte'],
                  'content': ['icontains'],
                  'comments__body': ['icontains'],
                  }