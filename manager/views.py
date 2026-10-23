from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import render
from api.models import Location


def dashboard(request):
    user_model = get_user_model()
    role_counts = {
        item['role']: item['total']
        for item in user_model.objects.filter(is_active=True)
        .values('role')
        .annotate(total=Count('id'))
    }
    location_rows = Location.objects.values('name', 'lat', 'long')
    location_points = []

    for location in location_rows:
        try:
            latitude = float(location['lat'])
            longitude = float(location['long'])
        except (TypeError, ValueError):
            continue

        location_points.append({
            'name': location['name'],
            'lat': latitude,
            'long': longitude,
        })

    context = {
        'tab':      'Dashboard',
        'title':    "Easy Rides Admin",
        'role': request.user.role,
        'side_nav': [
                        {"to": " ", "icon_class": "bx bx-dashboard", "label": "Dashboard"}
                    ],
        'overview': [
                        { "label" : 'Customers', "value" : role_counts.get('customer', 0)},
                        {"label" : 'drivers', "value" : role_counts.get('driver', 0)},
                        {"label" : 'locations', "value" : Location.objects.count()}
                    ],
       
        'charts':   [
                    {'type': 'role_chart_data', 'labels': ['Customers', 'Drivers'],'values': [
                                    role_counts.get('customer', 0),
                                    role_counts.get('driver', 0)
                                ]},
                    {'type': 'location_data', 'values': location_points}
        ]

       
    }
    return render(request, 'administrator/index.html', context)