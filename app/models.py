from django.db import models
from django.core import validators


class Item(models.Model):

    host_name = models.CharField(
        verbose_name='HOST NAME',
        max_length=200,
    )
    port = models.IntegerField(
        verbose_name='PORT',
        validators=[validators.MinValueValidator(1)],
    )
    created_at = models.DateTimeField(
        verbose_name='CREATED DATE',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='UPDATED DATE',
        auto_now=True
    )

    # Display settings for administrator site.
    def __str__(self):
        return self.host_name

    class Meta:
        verbose_name = 'mysql'
        verbose_name_plural = 'mysql'
