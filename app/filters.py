from django_filters import filters
from django_filters import FilterSet
from .models import Item


class MyOrderingFilter(filters.OrderingFilter):
    descending_fmt = '%s (DESC)'


class ItemFilter(FilterSet):

    host_name = filters.CharFilter(
        name='host_name', label='HOST NAME', lookup_expr='contains')
    port = filters.CharFilter(
        name='port', label='PORT', lookup_expr='contains')

    order_by = MyOrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('host_name', 'HOST NAME'),
            ('port', 'PORT'),
        ),
        field_labels={
            'host_name': 'HOST NAME',
            'port': 'PORT',
        },
        label='Order'
    )

    class Meta:

        model = Item
        fields = ('host_name', 'port')
