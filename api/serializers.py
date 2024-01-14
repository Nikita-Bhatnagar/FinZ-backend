from rest_framework import serializers
from .models import Expenses, Income



class IncomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Income
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True},
            'amount': {'required': False}
        }


class CreateIncomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Income
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True},
            'amount': {'required': True}
        }


class ExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expenses
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True}
        }


class CreateExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expenses
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True}
        }

    def validate(self, attrs):

        amount: float = attrs['amount']
        return super().validate(attrs)


class UpdateExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expenses
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True}
        }

    def update(self, instance: Expenses, validated_data):
        return super().update(instance, validated_data)


class EntriesSerializer(serializers.Serializer):
    highest_count = serializers.IntegerField()
    overall_count = serializers.IntegerField()
    previous = serializers.URLField(allow_blank=True)
    next = serializers.URLField(allow_blank=True)
    results = serializers.ListField(allow_empty=True)
