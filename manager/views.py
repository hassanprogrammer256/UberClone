from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Count, IntegerField, OuterRef, Subquery, Sum, Value
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, redirect, render
from api.models import Location,Trip,Vehicle,CustomerPayment
from accounts.models import DriverProfile,CustomerProfile,CustomUser
from django.views.generic import TemplateView
from .forms import CustomerAdminForm

SIDENAV_MENU = [
                {"to": "admin_index", "icon_class": "bx bx-dashboard", "label": "Dashboard"},
                {"to": "admin_customers", "icon_class": "bx bx-group", "label": "Customers"}
                    ]


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
        'side_nav': SIDENAV_MENU,
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
        ],

        'recent_trip_data' : get_admin_dashboard_recent_data()
       
    }
    return render(request, 'administrator/index.html', context)


class CustomersView(TemplateView):
    temp_name= "administrator/customers.html"

    def get(self,request):
        return self.render_page(request)

    def post(self, request):
        action = request.POST.get('action')
        customer_id = request.POST.get('customer_id')
        customer = None

        if action == 'edit' and customer_id:
            customer = get_object_or_404(
                CustomerProfile.objects.select_related('user'), pk=customer_id
            )

        form = CustomerAdminForm(request.POST, request.FILES, customer=customer)
        if form.is_valid():
            data = form.cleaned_data
            user_model = get_user_model()
            if customer:
                print("customer Available")
                user = customer.user
                user.first_name = data['first_name']
                user.last_name = data['last_name']
                user.phone_number = data['phone_number']
                user.email = data['email']
                user.gender = data['gender']
                if data['image']:
                    user.image = data['image']
                user.save()
                customer.address = data['address']
                customer.save()
                messages.success(request, 'Customer details updated.')
            else:
                print("customer Not Available")
                user = get_user_model().objects.create_user(
                    phone_number=data['phone_number'],
                    email=data['email'],
                    password='1234',
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    gender=data['gender'],
                    role='customer' 
                )
                if data['image']:
                    user.image = data['image']
                    user.save()

                customer = user
                customer.address = data['address']
                customer.save()
                print(customer.address)
                
            return redirect('admin_customers')

        return self.render_page(
            request,
            form=form,
            modal='edit' if action == 'edit' else 'add',
            selected_customer=customer,
        )

    def render_page(self, request, form=None, modal='', selected_customer=None):
        trip_counts = Trip.objects.filter(customer_id=OuterRef('pk')) \
            .values('customer_id').annotate(total=Count('pk')).values('total')
        payment_totals = CustomerPayment.objects.filter(customer_id=OuterRef('pk')) \
            .values('customer_id').annotate(total=Sum('amount')).values('total')

        customers = list(
            CustomerProfile.objects.select_related('user')
            .annotate(
                trip_count=Coalesce(Subquery(trip_counts), Value(0), output_field=IntegerField()),
                amount_spent=Coalesce(Subquery(payment_totals), Value(0), output_field=IntegerField()),
            )
            .order_by('user__first_name', 'user__last_name', 'user__email')
        )
        top_spender = max(customers, key=lambda customer: customer.amount_spent, default=None)
        totals = CustomerPayment.objects.filter(customer__isnull=False).aggregate(amount_spent=Sum('amount'))
        context = {
            'tab': 'Customers',
            'title': 'Easy Rides Admin | Customers',
            'role': request.user.role,
            'side_nav': SIDENAV_MENU,
            'customers': customers,
            'customer_count': len(customers),
            'trip_count': sum(customer.trip_count for customer in customers),
            'amount_spent': totals['amount_spent'] or 0,
            'top_spender': top_spender,
            'customer_form': form or CustomerAdminForm(),
            'active_modal': modal,
            'selected_customer': selected_customer,
        }
        return render(request, self.temp_name, context=context)





def get_admin_dashboard_recent_data():
    admin_dashboard_trip_data = []
    last_5_trips = Trip.objects.all().order_by('-trip_date')[:5]
    for trip in last_5_trips:
        trip_id = trip.id
        driver = trip.driver
        trip_payt = CustomerPayment.objects.get(trip_id=trip.id)
        driver_trips = Trip.objects.filter(driver__id=driver.id).count()
        vehicle = trip.vehicle
        vehicle_name = vehicle.name
        vehicle_plate_no = vehicle.plate_number
        route_from = trip.origin
        route_to = trip.destination
        trip_fare = trip_payt.amount
        payt_mthd = trip_payt.payment_method
        status = trip.status

        admin_dashboard_trip_data.append(
            {"id": trip_id , "driver" : driver ,  "trip_counts" : driver_trips , "vehicle_name" : vehicle_name, "vehicle_plate_number" : vehicle_plate_no, "route_from": route_from, "route_to" : route_to, "trip_fare" :trip_fare ,"payment_method" : payt_mthd, "status": status}
        )
    return admin_dashboard_trip_data






