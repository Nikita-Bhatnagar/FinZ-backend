from django.contrib import admin
from .models import Income, Expenses

@admin.register(Expenses)
class ExpenseAdmin(admin.ModelAdmin):
    # form = ExpenseForm
    list_display = ("title", "user", "amount", "added_at")
    ordering = ("-added_at",)
    list_filter = ('user',)
    search_fields = ('user__username',)


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'amount', 'added_at')
    ordering = ('-added_at',)
    list_filter = ('user',)
    search_fields = ('user__username',)

