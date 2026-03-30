from django.shortcuts import render
from financial.utils import calculate_recipe
# ===================================================================
# View Django
# ===================================================================

def recipe_calc(request):
    context = {
        'results': {},
        'form_data': {}
    }

    if request.method == 'POST':
        results = calculate_recipe(request.POST)
        context['results'] = results
        context['form_data'] = dict(request.POST)  # para repopular o formulário

    return render(request, 'financial/pages/recipe_calc.html', context)

def dashboard(request):
    return render(request, 'financial/pages/dashboard.html')
