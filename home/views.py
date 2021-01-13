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
        customer = Customer(fname=fname,oname=oname,emp_id=emp_id, mob=mob, email=email,image=image)
        customer.register()
        return HttpResponse("Sucess")
       