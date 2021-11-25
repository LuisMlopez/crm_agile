from rest_framework import viewsets

from customers.serializers import CustomerSerializer
from customers.models import Customer


class CustomerViewSet(viewsets.ModelViewSet):
    """
        A ViewSet for viewing, creating and editing customers
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
