from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from .models import Customer
# Create your views here.
#def reg(request):
           

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
        image = request.FILES['image']

        value = {'fname': fname,'oname': oname,'emp_id':emp_id,'mob': mob, 'email': email,'image':image}

        customer = Customer(fname=fname,oname=oname,emp_id=emp_id, mob=mob, email=email,image=image)

        err_msg = self.validateCustomer(customer)

        # saving
        if not err_msg:
            customer.register()
            return HttpResponse("Sucess")

        else:
            data = {'error': err_msg, 'values': value}
            return render(request, "regform.html", data)

    def validateCustomer(self, customer):
        err_msg = None
        if (not customer.fname):
            err_msg = "Your Name Required!"
        elif (not customer.oname):
            err_msg = "Organizaton Name Required!"
        elif (not customer.emp_id):
            err_msg = "Employ-id Required!"
        elif (not customer.mob):
            err_msg = "Mobile No. required"
        elif not customer.validatePhone():
            err_msg = "Enter valid Mobile no."
        elif len(customer.mob) < 10:
            err_msg = "Mobile No. must have 10 digits"
        elif not customer.validateEmail():
            err_msg = 'Enter valid email'
        elif not customer.image:
            err_msg = "please upload id image"
        elif customer.doExists():
            err_msg = 'Email Address Already registered..'
        return err_msg