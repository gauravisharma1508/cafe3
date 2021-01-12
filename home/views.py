from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import Customer
# Create your views here.
#def reg(request):

 #   return render(request,'regform.html')

def preview(request):

    return render(
        request,
        'preview.html',
        #{'categories': categories, 'products': products}
    )


class Register(View):
    def get(self,request):
        return render(request, 'regform.html')

    def post(self,request):
        postData = request.POST
        fname = postData.get('fname')
        oname = postData.get('oname')
        emp_id = postData.get('emp_id')
        mob = postData.get('mob')
        email = postData.get('email')
        
        # validation
        value = {'fname': fname,'oname': oname,'emp_id': emp_id, 'mob': mob, 'email': email}
        customer = Customer(fname=fname,oname=oname,emp_id=emp_id, mob=mob, email=email)
        err_msg = self.validateCustomer(customer)

        # saving
        if not err_msg:
            
            customer.register()
            return HttpResponse("Register Sucessfull")
        else:
            data = {'error': err_msg, 'values': value}
            return render(request, "regform.html", data)

    def validateCustomer(self,customer):
        err_msg = None
        if (not customer.fname):
            err_msg = "Name Required!"
        elif (not customer.oname):
            err_msg = "Organization Name. required"
        elif (not customer.emp_id):
            err_msg = "Employee Id. required"
        elif (not customer.mob):
            err_msg = "Phone No. required"
        elif not customer.validatePhone():
            err_msg = "Enter valid Phone no."
        elif len(customer.mob) < 10:
            err_msg = "Phone No. must have 10 digits"
        elif not customer.validateEmail():
            err_msg = 'Enter valid email'
        elif customer.doExists():
            err_msg = 'Email Address Already registered..'
        return err_msg