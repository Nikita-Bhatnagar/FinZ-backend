from typing import Optional

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import NotFound
from rest_framework.decorators import (
    api_view, permission_classes, parser_classes)

# from .models import Expenses, Category
from .models import Expenses
from .serializers import (
    ExpenseSerializer, 
    CreateExpenseSerializer, UpdateExpenseSerializer)


@api_view(http_method_names=['GET', 'POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def expenses(request: Request) -> Optional[Response]:
    if request.method == 'GET':
        start_date=request.query_params.get('start_date',None)
        end_date=request.query_params.get('end_date',None)
        
        expenses = Expenses.objects.filter(user=request.user)
        if start_date and end_date:
            expenses = expenses.filter(added_at__range=[start_date, end_date])
        expense_serializer = ExpenseSerializer(
            expenses, many=True)
        return Response(expense_serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        data = request.data.copy()
        data["user"] = request.user.pk
       
        serialized_expense = CreateExpenseSerializer(data=data)

        if serialized_expense.is_valid():
            new_expense = serialized_expense.save()

            response = ExpenseSerializer(new_expense)

            return Response(response.data, status=status.HTTP_201_CREATED)

        return Response(serialized_expense.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upgrade_expense(request: Request, pk: int) -> Optional[Response]:
    user = request.user.pk

    if request.method == "PUT":
        data = request.data.copy()
        data['user'] = user
        expense = Expenses.objects.filter(user=user, pk=pk).first()

        if expense:
            serialized_expense = UpdateExpenseSerializer(expense, data=data)

            if serialized_expense.is_valid():
                updated_expense = serialized_expense.save()

                response = ExpenseSerializer(updated_expense, many=False)

                return Response(response.data, status=status.HTTP_202_ACCEPTED)

            return Response(serialized_expense.errors, status=status.HTTP_424_FAILED_DEPENDENCY)

        raise NotFound(f"ExpenseId: {pk} do not exists")

    if request.method == "DELETE":
        expense: Optional[Expenses] = Expenses.objects.filter(
            user=user, pk=pk).first()
        if expense:
            expense.delete()
            return Response({'data': f'Expense titled {expense.title} do not exits'}, status=status.HTTP_204_NO_CONTENT)
        raise NotFound('Could not remove this expense',
                       code=status.HTTP_404_NOT_FOUND)


