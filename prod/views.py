from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from .models import Category, Product, Staff, Sale
from .forms import CategoryForm, ProductForm, StaffForm, SaleForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

def home(request):
    form = SaleForm()
    if request.method=='POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()

    return render(request, 'stf/home.html',{'form':form})

def add_product(request):
    form = ProductForm()
    if request.method=='POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'stf/add_p.html',{'form':form})        

def add_category(request):
    form = CategoryForm()
    if request.method=='POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'stf/add_cat.html',{'form':form})        


def add_sale(request):
    form = SaleForm()
    if request.method=='POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('home')
    return render(request, 'stf/add_sale.html',{'form':form})  
def add_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_staff')  # Redirect to the same page after successful submission
    else:
        form = StaffForm()

    return render(request, 'stf/add_staff.html', {'form': form})
def add_staff(request):
    form = StaffForm()
    
    if request.method=='POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('home')
    return render(request, 'stf/add_staff.html',{'form':form})   
 
 
def list_user(request):
    staff_members = User.objects.all()
    return render(request, 'stf/list_user.html', {'staff_members': staff_members})    
def list_staff(request):
    staff_members = Staff.objects.all()
    return render(request, 'stf/staff_list.html', {'staff_members': staff_members})    
from django.db.models import Count
from .models import Staff, Attendance

def staff_detail(request, staff_id):
    staff = Staff.objects.get(pk=staff_id)
    sales = Sale.objects.filter(staff=staff)
    # Calculate absent days for each day in the current month
    today = timezone.now()
    first_day_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_day_of_month = (first_day_of_month.replace(month=first_day_of_month.month % 12 + 1) - timezone.timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=999999)

    total_absent_days = Attendance.objects.filter(
        staff=staff,
        check_in_time__gte=first_day_of_month,
        check_out_time__lte=last_day_of_month
    ).exclude(check_in_time__isnull=False, check_out_time__isnull=False).values('check_in_time__date').distinct().count()
    total_attendance_days = Attendance.objects.filter(
        staff=staff,
        check_in_time__gte=first_day_of_month,
        check_out_time__lte=last_day_of_month,
        check_in_time__isnull=False,
        check_out_time__isnull=False
    ).values('check_in_time__date').distinct().count()
    return render(request, 'stf/staff_detail.html', {'total_attendance_days':total_attendance_days,'staff': staff, 'total_absent_days': total_absent_days, 'sales':sales})



import matplotlib.pyplot as plt
from io import BytesIO
import base64
from .models import Sale

def plot_cumulative_sales(request):
    all_sales = Sale.objects.all().order_by('sale_date')

    # Extracting sales data for plotting
    sale_dates = [sale.sale_date for sale in all_sales]
    cumulative_quantities_sold = [sum(sale.quantity_sold for sale in all_sales if sale.sale_date <= date) for date in sale_dates]

    # Plotting the cumulative sales data
    plt.figure(figsize=(10, 6))
    plt.plot(sale_dates, cumulative_quantities_sold, marker='o')
    plt.title('Cumulative Sales Over Time')
    plt.xlabel('Sale Date')
    plt.ylabel('Cumulative Quantity Sold')

    # Saving the plot to a BytesIO object
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()

    # Embedding the plot in the HTML template
    img_str = base64.b64encode(img_buffer.read()).decode('utf-8')
    img_src = f'data:image/png;base64,{img_str}'

    context = {
        'img_src': img_src,
    }

    return render(request, 'stf/plot.html', context)
def list_sales(request):
    sales = Sale.objects.all()
    return render(request, 'stf/list_sale.html',{'sales':sales})


from .models import  Attendance

def mark_check_in(request, staff_id):
    staff = Staff.objects.get(pk=staff_id)

    # Check if there's an existing attendance record for today
    today_attendance = Attendance.objects.filter(staff=staff, check_in_time__date=timezone.now().date()).first()

    if today_attendance:
        return HttpResponse("Check-in already marked for today.")

    # Create a new attendance record for today and mark check-in time
    Attendance.objects.create(staff=staff, check_in_time=timezone.now())
    return HttpResponse(f"Check-in marked for {staff.first_name} {staff.last_name}.")

def mark_check_out(request, staff_id):
    staff = Staff.objects.get(pk=staff_id)

    # Retrieve the latest attendance record for today
    today_attendance = Attendance.objects.filter(staff=staff, check_in_time__date=timezone.now().date()).last()

    if not today_attendance or today_attendance.check_out_time:
        return HttpResponse("No valid check-in or check-out record found.")

    # Mark check-out time
    today_attendance.mark_check_out()
    return HttpResponse(f"Check-out marked for {staff.first_name} {staff.last_name}.")

def view_attendance(request):
    # Retrieve all staff members and their attendance records for today
    staff_members = Staff.objects.all()
    today_attendance = [
        {'staff': staff, 'attendance': Attendance.objects.filter(staff=staff, check_in_time__date=timezone.now().date()).last()}
        for staff in staff_members
    ]

    return render(request, 'stf/view_attendance.html', {'today_attendance': today_attendance})





def mark_user_attendance(request):
    # Assuming you're using Django's built-in User model
    user = request.user

    # Check if there's an existing attendance record for today
    today_attendance = Attendance.objects.filter(staff__user=user, check_in_time__date=timezone.now().date()).first()

    if today_attendance:
        return HttpResponse("Check-in already marked for today.")

    # Create a new attendance record for today and mark check-in time
    staff = get_object_or_404(Staff, user=user)
    Attendance.objects.create(staff=staff, check_in_time=timezone.now())

    return HttpResponse(f"Check-in marked for {user.username}.")





