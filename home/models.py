from django.db import models

# Create your models here.

class Customer(models.Model):
    fname =models.CharField(max_length=50)
    oname =models.CharField(max_length=50)
    emp_id =models.CharField(max_length=50)
    mob = models.CharField(max_length=15)
    email = models.EmailField(max_length=254)
    image = models.FileField(upload_to='uploads/ids/',blank= False,default='',null=True )
    
    

    def register(self):
        self.save()

    
