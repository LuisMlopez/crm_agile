from rest_framework import viewsets

from customers.serializers import CustomerSerializer
from customers.models import Customer


class CustomerViewSet(viewsets.ModelViewSet):
    """
        A ViewSet for viewing, creating and editing customers

        list:

        >
        > **Description**
        >
        > Allow list all customers
        >

        create:

        >
        > **Description**
        >
        > Allow create a customer.
        >

        read:

        >
        > **Description**
        >
        > Read a customer information using the user ID.
        >

        update:

        >
        > **Description**
        >
        > Update a customer. The name and surname fields are always required. 
        > Use the partial_update method to update a customer without sendig required fields.
        >

        partial_update:

        >
        > **Description**
        >
        > Allow update a customer information without sendig the required fields.
        >

        delete:

        >
        > **Description**
        >
        > Allow remove a customer.
        >
        
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_serializer_context(self):
        context = super(CustomerViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context
