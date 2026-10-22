from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import render
from api.models import Location


def manager_dashboard(request):
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
        'active_accounts': sum(role_counts.values()),
        'customer_accounts': role_counts.get('customer', 0),
        'driver_accounts': role_counts.get('driver', 0),
        'admin_accounts': role_counts.get('admin', 0),
        'location_count': Location.objects.count(),
        'role_chart_data': {
            'labels': ['Customers', 'Drivers', 'Admins'],
            'values': [
                role_counts.get('customer', 0),
                role_counts.get('driver', 0),
                role_counts.get('admin', 0),
            ],
        },
        'location_chart_data': location_points,
    }
    return render(request, 'administrator/index.html', context)