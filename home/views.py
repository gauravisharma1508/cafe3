from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import HttpResponse
from django.views import View
from .models import Customer
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.
#def reg(request):
           



class Preview(View):
    def get(self,request,value=None):
        #fname = value.fname
        #oname = value.oname
        #emp_id = value.emp_id
        #mob = value.mob
        email = value.email
        #password=value.password
        #image = value.image

        #email = request.session.get('email')
        customer = Customer.get_customer_by_email(email)
        #cust = Customer.objects.filter(email=email)
        return render(request, 'preview.html',customer)#{'fname': fname,'oname': oname,'emp_id':emp_id,'mob': mob, 'email': email,'image':image,'password':password})

    def post(self,request):
        #postData = request.POST
        #fname = postData.get('fname')
        #oname = postData.get('oname')
        #emp_id = postData.get('emp_id')
        #mob = postData.get('mob')
        #email = postData.get('email')
        #password=postData.get('password')
        ##email = request.session['e']
        ##email=val()
        #image = request.FILES.get('image')

        #customer = Customer(fname=fname, oname=oname, emp_id=emp_id, mob=mob, email=email, image=image,password=password)
        #customer.register()
        return HttpResponse("Success")

class Register(View):
    def get(self,request,val=None):
        email=val.email
        password=val.password
        return render(request, 'regform.html',{'email': email, 'password': password})

    def post(self,request):
        postData = request.POST
        fname = postData.get('fname')
        oname = postData.get('oname')
        emp_id = postData.get('emp_id')
        mob = postData.get('mob')
        email = postData.get('email')
        password=postData.get('password')
        #email = request.session['e']
        #email=val()
        image = request.FILES.get('image')





        value = {'fname': fname,'oname': oname,'emp_id':emp_id,'mob': mob, 'email': email,'image':image,'password':password}

        customer = Customer(fname=fname,oname=oname,emp_id=emp_id, mob=mob, email=email,image=image,password=password)

        err_msg = self.validateCustomer(customer)

        # saving
        if not err_msg:
            customer.password = make_password(customer.password)
            customer.register()
            #request.session['customer'] = customer.id
            #cust = Customer.objects.filter(email=email)
            #request.session['email'] = customer.email
            #return HttpResponse("Success")
            return render(request, "preview.html",value) #{'value':value,'cust':cust})

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
        #elif not customer.image:
            #err_msg = "please upload id image"
        elif customer.doExists():
            err_msg = 'Email Address Already registered..'
        return err_msg

class Signin(View):
    def get(self,request):
        Signin.return_url = request.GET.get('return_url')
        return render(request, 'signin.html')




    def post(self, request):

        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        err_msg = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                request.session['email'] = customer.email
                if Signin.return_url:
                    return HttpResponseRedirect(Signin.return_url)
                else:
                    Signin.return_url = None
                    return HttpResponse("Success")
            else:
                err_msg = 'Email or Password invalid'
        else:
            err_msg = 'Email or Password invalid'
        return render(request, 'signin.html', {'error': err_msg})

class Signup(View):
    def get(self,request):
        return render(request, 'signup.html')

    def post(self,request):
        postData = request.POST
        email = postData.get('email')
        password = postData.get('password')
        val={'email': email, 'password': password}
        return render(request,'regform.html',val)

