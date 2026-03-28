from django.urls import path 
from financial.views import dashboard, recipe_calc

urlpatterns = [
    path('dashboard/', dashboard),
    path('calculadora-receita/', recipe_calc),
]
