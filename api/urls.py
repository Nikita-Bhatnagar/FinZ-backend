from django.urls import path
from .views import base_information
from .views_income import (update_income, income, 
                           )
from .views_expense import (
    expenses, upgrade_expense)
from .multimodelviews import Entries

urlpatterns = [

    path('info', base_information, name="base_info"),
    path('income', income, name='income'),
    path('income/<int:pk>', update_income, name="income_details"),
    path('expenses', expenses, name="expenses"),
    path('expenses/<int:pk>', upgrade_expense, name="update-expenses"),
    path('entries', Entries.as_view(), name="entries"),

]
