from django import forms

class import_list_form(forms.Form):
    CHOICES = [('yuya', 'yuya'), ('non', 'non')]
    user = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    visited_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'accept': 'text/html'}))

from .models import ShopList

class ToDatabeseForm(forms.Form):
    id = forms.CharField(
        label='number',
        max_length=4,
    )

    postcode = forms.CharField(
        label='postcode',
        max_length=10,
    )

    address = forms.CharField(
        label='address',
        max_length=150,
    )

    prefecture = forms.CharField(
        label='prefecture',
        max_length=5,
    )

    name = forms.CharField(
        label='shopname',
        max_length=150,
    )

    latitude = forms.FloatField(
        label='latitude',
    )

    longitude = forms.FloatField(
        label='longitude',
    )

    drivethrough = forms.BooleanField(
        label='drivethrough',
    )

    businesshour = forms.CharField(
        label='businesshour',
        max_length=500,
    )

    closed = forms.BooleanField(
        label='closed',
    )

    yuya = forms.BooleanField(
        label='yuya',
        initial=True,
    )

    non = forms.BooleanField(
        label='non',
    )

    monday = forms.CharField(
        label='monday',
        max_length=50,
    )

    tuesday = forms.CharField(
        label='tuesday',
        max_length=50,
    )

    wednesday = forms.CharField(
        label='wednesday',
        max_length=50,
    )

    thursday = forms.CharField(
        label='thursday',
        max_length=50,
    )

    friday = forms.CharField(
        label='friday',
        max_length=50,
    )

    saturday = forms.CharField(
        label='saturday',
        max_length=50,
    )

    sunday = forms.CharField(
        label='sunday',
        max_length=50,
    )

    holiday = forms.CharField(
        label='holiday',
        max_length=50,
    )

    add_day = forms.CharField(
        label = 'add_day',
        max_length = 30,
    )
