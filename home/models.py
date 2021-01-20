from django.db import models
from django.db.models.signals import pre_save
from home.utils import unique_order_id_generator
# Create your models here.
from django.utils import timezone




class Customer(models.Model):
    fname = models.CharField(max_length=50,blank= False,default='',null=True )
    oname = models.CharField(max_length=50,blank= False,default='',null=True )
    emp_id = models.CharField(max_length=50,blank= False,default='',null=True )
    mob = models.CharField(max_length=15,blank= False,default='',null=True )
    email = models.EmailField(max_length=254,blank= False,default='',null=True )
    image = models.FileField(upload_to='uploads/ids/',blank= False,default='',null=True )
    password = models.CharField(max_length=500,blank= False,default='',null=True )
    order_id=models.CharField(max_length=120,blank= True,null=True )
    reg_date=models.DateField(auto_now_add=True,auto_now=False,blank=True)
    #reg_date = models.DateTimeField(editable=False)

    #def save(self, *args, **kwargs):
        #''' On save, update timestamps '''
        #if not self.id:
            #self.reg_date = timezone.now()
        #self.modified = timezone.now()
        #return super(Customer, self).save(*args, **kwargs)

    def register(self):
        self.save()

    def __str__(self):
        return self.fname

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False


    def doExists(self):
        if Customer.objects.filter(email=self.email):
            return True

        return False

    def validateEmail(self):
        email=self.email
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False


    def validatePhone(self):
            mob = self.mob
            from django.core.exceptions import ValidationError
            try:
                int(mob)
                return True
            except (ValueError, TypeError,ValidationError):
                return False

    @staticmethod
    def get_customer_by_id(ids):
        return Customer.objects.filter(id__in =ids)

def pre_save_create_order_id(sender,instance,*args,**kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)

pre_save.connect(pre_save_create_order_id,sender=Customer)



class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='uploads/products/', default='', null=True)

    def __str__(self):
        return self.name

class Menu(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(
        Category,on_delete=models.CASCADE,default='')
    #description = models.CharField(max_length=200, default='',null=True , blank=True)
    image = models.ImageField(upload_to='uploads/products/',default='',null=True )

    def __str__(self):
        return self.name

    @staticmethod
    def get_menu_by_category(category):
        try:
            return Menu.objects.get(category=category)
        except:
            return False
    @staticmethod
    def get_menu_by_id(ids):
        return Menu.objects.filter(id__in =ids)
