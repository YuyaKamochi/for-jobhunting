from django.db import models

# Create your models here.

class ShopList(models.Model):
    postcode = models.CharField(
        verbose_name='postcode',
        max_length=10,
        blank=True,
        null=True,
    )

    address = models.CharField(
        verbose_name='address',
        max_length=150,
        blank=True,
        null=True,
    )

    prefecture = models.CharField(
        verbose_name='prefecture',
        max_length=5,
        blank=True,
        null=True,
    )

    name = models.CharField(
        verbose_name='shopname',
        max_length=150,
        blank=True,
        null=True,
    )

    latitude = models.FloatField(
        verbose_name='latitude',
        blank=True,
        null=True,
    )

    longitude = models.FloatField(
        verbose_name='longitude',
        blank=True,
        null=True,
    )

    drivethrough = models.BooleanField(
        verbose_name='drivethrough',
        blank=True,
        null=True
    )

    businesshour = models.CharField(
        verbose_name='businesshour',
        max_length=500,
        blank=True,
        null=True
    )

    closed = models.BooleanField(
        verbose_name='closed',
        blank=True,
        null=True,
    )

    yuya = models.BooleanField(
        verbose_name='yuya',
        blank=True,
        null=True,
    )

    non = models.BooleanField(
        verbose_name='non',
        blank=True,
        null=True,
    )

    monday = models.CharField(
        verbose_name='monday',
        max_length=50,
        blank=True,
        null=True,
    )

    tuesday = models.CharField(
        verbose_name='tuesday',
        max_length=50,
        blank=True,
        null=True,
    )

    wednesday = models.CharField(
        verbose_name='wednesday',
        max_length=50,
        blank=True,
        null=True,
    )

    thursday = models.CharField(
        verbose_name='thursday',
        max_length=50,
        blank=True,
        null=True,
    )

    friday = models.CharField(
        verbose_name='friday',
        max_length=50,
        blank=True,
        null=True,
    )

    saturday = models.CharField(
        verbose_name='saturday',
        max_length=50,
        blank=True,
        null=True,
    )

    sunday = models.CharField(
        verbose_name='sunday',
        max_length=50,
        blank=True,
        null=True,
    )

    holiday = models.CharField(
        verbose_name='holiday',
        max_length=50,
        blank=True,
        null=True,
    )

    add_day = models.CharField(
        verbose_name = 'add_day',
        max_length = 30,
        blank = True,
        null = True,
    )
    
    yuya_last_visit = models.CharField(
        verbose_name = 'yuya_last_visit',
        max_length = 300,
        blank = True,
        null = True,
    )
    
    yuya_frequency_of_visit = models.IntegerField(
        verbose_name = 'yuya_frequency_of_visit',
        blank = True,
        null = True,
    )
    
    non_last_visit = models.CharField(
        verbose_name = 'non_last_visit',
        max_length = 300,
        blank = True,
        null = True,
    )
    
    non_frequency_of_visit = models.IntegerField(
        verbose_name = 'non_frequency_of_visit',
        blank = True,
        null = True,
    )

    def __str__(self):
        return self.name