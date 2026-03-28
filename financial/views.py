from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'financial/pages/dashboard.html')

def recipe_calc(request):
    if request.method == 'POST':
        return render(request, 'financial/pages/recipe_calc.html')