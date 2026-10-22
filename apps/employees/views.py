from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .forms import EmployeeForm
from .models import Employee

# Create your views here.
def add_employee(request):
    template_name = 'employees/add_employee.html'
    context = {}
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            form.save_m2m()
            return redirect('employees:list_employees')
    form = EmployeeForm()
    context['form'] = form
    return render(request, template_name, context)

def list_employees(request):
    template_name = 'employees/list_employees.html'
    employees = Employee.objects.filter()
    context = {
        'employees': employees,
    }
    return render(request, template_name, context)

def edit_employee(request, id_employee):
    template_name = 'employees/add_employee.html'
    context ={}
    employee = get_object_or_404(Employee, id=id_employee)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employees:list_employees')
    form = EmployeeForm(instance=employee)
    context['form'] = form
    return render(request, template_name, context)

def delete_employee(request, id_employee):
    employee = Employee.objects.get(id=id_employee)
    employee.delete()
    return redirect('employees:list_employees')