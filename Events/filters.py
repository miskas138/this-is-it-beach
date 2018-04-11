import django_filters
from django.forms import forms

from Events.models import *
from django import forms
from .models import SECTION_CHOISES



class PostFilter(django_filters.FilterSet):
    section = django_filters.ChoiceFilter(choices=SECTION_CHOISES, label='Είδος εκδήλωσης')
    title = django_filters.CharFilter(lookup_expr='icontains', label='Τίτλος')
    location__city = django_filters.CharFilter(lookup_expr='icontains', label='Πόλη/περιοχή')
    location__address = django_filters.CharFilter(lookup_expr='icontains', label='Διεύθυνση')
    user__username = django_filters.CharFilter(lookup_expr='icontains', label='Όνομα Διοργανωτή')
    dateTime_gte = django_filters.DateTimeFilter(name='information__dateTime', lookup_expr='gte', label='Ημερομηνία από')
    dateTime_lte = django_filters.DateTimeFilter(name='information__dateTime', lookup_expr='lte', label='Ημερομηνία εώς')
    information__ticket_price = django_filters.NumberFilter(lookup_expr='lte', label='Τιμή εισητηρίου εώς')
    description = django_filters.CharFilter(lookup_expr='icontains', label='Σύντομη περιγραφή')
    content = django_filters.CharFilter(lookup_expr='icontains', label='Περιεχόμενο')
    comments__body = django_filters.CharFilter(lookup_expr='icontains', label='Μηνύματα')

    class Meta:
        model = Event
        fields = {
                  }
