from django.shortcuts import render


def HomePageView(request):
    template_name = 'index.html'
    return render(request, template_name)