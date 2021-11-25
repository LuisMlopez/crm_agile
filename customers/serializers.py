from rest_framework import serializers

from customers.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id', 'name', 'surname', 'photo', 'birthday', 'email', 'phone',
            'created_by', 'updated_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'updated_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        current_user = self.context.get('request').user
        validated_data.update({'created_by': current_user, 'updated_by': current_user})
        return super(CustomerSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        current_user = self.context.get('request').user
        instance.updated_by = current_user
        return super(CustomerSerializer, self).update(instance, validated_data)
