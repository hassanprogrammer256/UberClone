from django.shortcuts import render


def manager_dashboard(request):
    return render(request, 'administrator/index.html')