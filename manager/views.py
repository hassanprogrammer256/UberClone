from django.contrib.auth import get_user_model
from django.contrib import messages
from datetime import date

from django.db.models import Count, IntegerField, OuterRef, Subquery, Sum, Value
from django.db.models.functions import Coalesce, TruncMonth
from django.shortcuts import get_object_or_404, redirect, render
from api.models import CustomerPayment, Location, TRIP_STATUSES, Trip, Vehicle
from accounts.models import CustomerProfile, DriverProfile
from django.views.generic import TemplateView
from .forms import CustomerAdminForm, CustomerPaymentAdminForm, DriverAdminForm, TripAdminForm

SIDENAV_MENU = [
                {"to": "admin_index", "icon_class": "bx bx-dashboard", "label": "Dashboard"},
                {"to": "admin_customers", "icon_class": "bx bx-group", "label": "Customers"},
                {"to": "admin_drivers", "icon_class": "bx bx-steering-wheel", "label": "Drivers"},
                {"to": "admin_trips", "icon_class": "bx bx-car", "label": "Trips"},
                {"to": "admin_earnings", "icon_class": "bx bx-wallet", "label": "Earnings"},
                    ]


def get_reporting_months(month_count=6):
    today = date.today()
    current_month = date(today.year, today.month, 1)
    months = []
    for offset in range(month_count - 1, -1, -1):
        month_index = current_month.year * 12 + current_month.month - 1 - offset
        year, month = divmod(month_index, 12)
        months.append(date(year, month + 1, 1))

    next_month_index = current_month.year * 12 + current_month.month
    next_year, next_month = divmod(next_month_index, 12)
    return months, date(next_year, next_month + 1, 1)


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

        if action == 'delete' and customer_id:
            customer = get_object_or_404(CustomerProfile.objects.select_related('user'), pk=customer_id)
            customer.user.delete()
            messages.success(request, 'Customer and linked trip records deleted.')
            return redirect('admin_customers')

        if action == 'edit' and customer_id:
            customer = get_object_or_404(
                CustomerProfile.objects.select_related('user'), pk=customer_id
            )

        form = CustomerAdminForm(request.POST, request.FILES, customer=customer)
        if form.is_valid():
            data = form.cleaned_data
            if customer:
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

                customer = CustomerProfile.objects.create(
                          user=user, 
                           address= data['address']
                              )
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


class DriversView(TemplateView):
    def get(self, request):
        return self.render_page(request)

    def post(self, request):
        action = request.POST.get('action')
        driver_id = request.POST.get('driver_id')
        driver = None

        if action == 'delete' and driver_id:
            driver = get_object_or_404(DriverProfile.objects.select_related('user'), pk=driver_id)
            driver.user.delete()
            messages.success(request, 'Driver, linked vehicles, and trip records deleted.')
            return redirect('admin_drivers')

        if action == 'edit' and driver_id:
            driver = get_object_or_404(DriverProfile.objects.select_related('user'), pk=driver_id)

        form = DriverAdminForm(request.POST, request.FILES, driver=driver)
        if form.is_valid():
            data = form.cleaned_data
            if driver:
                user = driver.user
                user.first_name = data['first_name']
                user.last_name = data['last_name']
                user.phone_number = data['phone_number']
                user.email = data['email']
                user.gender = data['gender']
                if data['image']:
                    user.image = data['image']
                user.save()
                driver.date_of_birth = data['date_of_birth']
                driver.address = data['address']
                driver.save()
                messages.success(request, 'Driver details updated.')
            else:
                user = get_user_model().objects.create_user(
                    phone_number=data['phone_number'],
                    email=data['email'],
                    password=None,
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    gender=data['gender'],
                    role='driver',
                )
                if data['image']:
                    user.image = data['image']
                    user.save()
                DriverProfile.objects.create(
                    user=user,
                    date_of_birth=data['date_of_birth'],
                    address=data['address'],
                )
                messages.success(request, 'Driver added.')
            return redirect('admin_drivers')

        return self.render_page(
            request,
            form=form,
            active_modal=True,
            active_action=action if action == 'edit' else 'add',
            selected_driver=driver,
        )

    def render_page(self, request, form=None, active_modal=False, active_action='add', selected_driver=None):
        trip_counts = Trip.objects.filter(driver_id=OuterRef('pk')) \
            .values('driver_id').annotate(total=Count('pk')).values('total')
        drivers = list(
            DriverProfile.objects.select_related('user')
            .annotate(
                trip_count=Coalesce(Subquery(trip_counts), Value(0), output_field=IntegerField())
            )
            .order_by('user__first_name', 'user__last_name', 'user__email')
        )
        context = {
            'tab': 'Drivers',
            'title': 'Easy Rides Admin | Drivers',
            'role': request.user.role,
            'side_nav': SIDENAV_MENU,
            'drivers': drivers,
            'driver_count': len(drivers),
            'trip_count': sum(driver.trip_count for driver in drivers),
            'top_driver': max(drivers, key=lambda driver: driver.trip_count, default=None),
            'driver_form': form or DriverAdminForm(),
            'active_modal': active_modal,
            'active_action': active_action,
            'selected_driver': selected_driver,
        }
        return render(request, 'administrator/drivers.html', context)


class TripsView(TemplateView):
    def post(self, request):
        action = request.POST.get('action')
        trip_id = request.POST.get('trip_id')
        if action == 'delete' and trip_id:
            trip = get_object_or_404(Trip, pk=trip_id)
            trip.delete()
            messages.success(request, 'Trip deleted. Its payment history remains unlinked.')
            return redirect('admin_trips')

        trip = get_object_or_404(Trip, pk=trip_id) if action == 'edit' and trip_id else None
        if trip:
            form = TripAdminForm(request.POST, instance=trip)
            if form.is_valid():
                form.save()
                messages.success(request, 'Trip details updated.')
                return redirect('admin_trips')
            return self.render_page(request, form=form, active_modal=True)
        return redirect('admin_trips')

    def get(self, request):
        return self.render_page(request)

    def render_page(self, request, form=None, active_modal=False):
        fare = CustomerPayment.objects.filter(trip_id=OuterRef('pk')) \
            .order_by('-payment_date', '-payment_time').values('amount')[:1]
        payment_method = CustomerPayment.objects.filter(trip_id=OuterRef('pk')) \
            .order_by('-payment_date', '-payment_time').values('payment_method')[:1]
        trips = Trip.objects.select_related(
            'customer__user', 'driver__user', 'vehicle', 'origin', 'destination'
        ).annotate(
            fare=Subquery(fare),
            payment_method_value=Subquery(payment_method),
        ).order_by('-trip_date', '-requested_at')

        month_starts, next_month = get_reporting_months()
        monthly_totals = Trip.objects.filter(
            trip_date__gte=month_starts[0], trip_date__lt=next_month
        ).annotate(month=TruncMonth('trip_date')).values('month').annotate(total=Count('pk'))
        totals_by_month = {row['month'].strftime('%Y-%m'): row['total'] for row in monthly_totals}
        status_totals = {
            row['status']: row['total']
            for row in Trip.objects.values('status').annotate(total=Count('pk'))
        }
        context = {
            'tab': 'Trips',
            'title': 'Easy Rides Admin | Trips',
            'role': request.user.role,
            'side_nav': SIDENAV_MENU,
            'trips': trips,
            'trip_count': trips.count(),
            'completed_count': status_totals.get('completed', 0),
            'in_progress_count': status_totals.get('in_progress', 0),
            'cancelled_count': status_totals.get('cancelled', 0),
            'trip_month_labels': [month.strftime('%b') for month in month_starts],
            'trip_month_values': [totals_by_month.get(month.strftime('%Y-%m'), 0) for month in month_starts],
            'trip_status_labels': [label for _, label in TRIP_STATUSES],
            'trip_status_values': [status_totals.get(value, 0) for value, _ in TRIP_STATUSES],
            'trip_form': form or TripAdminForm(),
            'active_modal': active_modal,
        }
        return render(request, 'administrator/trips.html', context)


class EarningsView(TemplateView):
    def post(self, request):
        action = request.POST.get('action')
        payment_id = request.POST.get('payment_id')
        if action == 'delete' and payment_id:
            payment = get_object_or_404(CustomerPayment, pk=payment_id)
            payment.delete()
            messages.success(request, 'Payment permanently deleted from financial history.')
            return redirect('admin_earnings')

        payment = get_object_or_404(CustomerPayment, pk=payment_id) if action == 'edit' and payment_id else None
        if payment:
            form = CustomerPaymentAdminForm(request.POST, instance=payment)
            if form.is_valid():
                form.save()
                messages.success(request, 'Payment details updated.')
                return redirect('admin_earnings')
            return self.render_page(request, form=form, active_modal=True)
        return redirect('admin_earnings')

    def get(self, request):
        return self.render_page(request)

    def render_page(self, request, form=None, active_modal=False):
        payments = CustomerPayment.objects.select_related('customer__user', 'trip') \
            .order_by('-payment_date', '-payment_time')
        totals = payments.aggregate(total=Sum('amount'), count=Count('pk'))
        month_starts, next_month = get_reporting_months()
        monthly_totals = CustomerPayment.objects.filter(
            payment_date__gte=month_starts[0], payment_date__lt=next_month
        ).annotate(month=TruncMonth('payment_date')).values('month').annotate(total=Sum('amount'))
        totals_by_month = {row['month'].strftime('%Y-%m'): row['total'] or 0 for row in monthly_totals}
        choices = CustomerPayment._meta.get_field('payment_method').choices
        method_totals = {
            row['payment_method']: row['total'] or 0
            for row in CustomerPayment.objects.values('payment_method').annotate(total=Sum('amount'))
        }
        total_revenue = totals['total'] or 0
        transaction_count = totals['count'] or 0
        context = {
            'tab': 'Earnings',
            'title': 'Easy Rides Admin | Earnings',
            'role': request.user.role,
            'side_nav': SIDENAV_MENU,
            'payments': payments,
            'total_revenue': total_revenue,
            'transaction_count': transaction_count,
            'average_payment': total_revenue / transaction_count if transaction_count else 0,
            'earnings_month_labels': [month.strftime('%b') for month in month_starts],
            'earnings_month_values': [totals_by_month.get(month.strftime('%Y-%m'), 0) for month in month_starts],
            'payment_method_labels': [label for _, label in choices],
            'payment_method_values': [method_totals.get(value, 0) for value, _ in choices],
            'payment_form': form or CustomerPaymentAdminForm(),
            'active_modal': active_modal,
        }
        return render(request, 'administrator/earnings.html', context)





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






