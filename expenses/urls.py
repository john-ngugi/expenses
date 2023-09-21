from django.urls import path 
from . import views 
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index , name = 'expenses'),
    path('add-expense',views.addExpense,name='add-expense'),
    path('edit-expense/<int:id>', views.expense_edit, name="expense-edit"),
    path('delete-expense/<int:id>', views.delete_expense, name="expense-delete"),
    path('search-expenses', csrf_exempt(views.search_expenses), name="search-expenses"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)