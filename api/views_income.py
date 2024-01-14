from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound, APIException
from .serializers import (CreateIncomeSerializer,
                          IncomeSerializer
                        )
from .models import Income


@api_view(http_method_names=['GET', 'POST'])
@permission_classes([IsAuthenticated])
def income(request: Request) -> Response:

    if request.method == 'GET':
        start_date=request.query_params.get('start_date',None)
        end_date=request.query_params.get('end_date',None)
        incomes = Income.objects.filter(user=request.user)
        if start_date and end_date:
            incomes=incomes.filter(added_at__range=[start_date,end_date])
        serialized_incomes = IncomeSerializer(incomes, many=True)
        return Response(serialized_incomes.data, status=status.HTTP_200_OK)

    if request.method == 'POST':

        data = {**request.data, "user": request.user.pk}

        serialized_income = CreateIncomeSerializer(data=data)

        if serialized_income.is_valid():
            newIncome = serialized_income.save()

            reponse = IncomeSerializer(newIncome, many=False)

            return Response(reponse.data, status=status.HTTP_201_CREATED)
        return Response(serialized_income.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def update_income(request: Request, pk: int) -> Response:

    if request.method == "PUT":
        data = {**request.data, "user": request.user.pk}
        income = Income.objects.filter(user=request.user.pk, pk=pk).first()

        if income:
            serialized_income = CreateIncomeSerializer(income, data=data)

            if serialized_income.is_valid():
                data = serialized_income.save()

                reponse = IncomeSerializer(data, many=False)

                return Response(reponse.data, status=status.HTTP_202_ACCEPTED)
            return Response(serialized_income.errors, status=status.HTTP_424_FAILED_DEPENDENCY)

        raise APIException(
            "Income of this credentials don't exits", code=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        income_existis = Income.objects.filter(
            user=request.user.pk, pk=pk).first()
        if income_existis:
            income_existis.delete()
            return Response({'detail': 'Income removed succesfully'}, status=status.HTTP_204_NO_CONTENT)
        raise NotFound('Counld not find this income',
                       code=status.HTTP_404_NOT_FOUND)
