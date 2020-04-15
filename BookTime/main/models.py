from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager
)

from django.core.validators import MinValueValidator
# Create your models here.
'''
class Destination(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField()
    price = models.IntegerField()
    offer = models.BooleanField(default=False)
'''
    
# ActiveManager class is created to add extra methods that return
# filtered QuerySets, we have an 'active' field in the Product model,
# we add a manager with a filter on that
class ActiveManager(models.Manager):
    def active(self):
        return self.filter(active=True)


# While loading data using natural keys, Django cannot use
# the natural_key() method, because model loading happens 
# through managers, not models themselves.
# To be able to load tags back in, we need to create a Manager
# for that model and implement the get_by_natural_key() method.

class ProductTagManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)

class ProductTag(models.Model):
    
    #products = models.ManyToManyField(Product, blank=True)
    objects = ProductTagManager()
    
    name = models.CharField(max_length=32)
    slug = models.SlugField(max_length=48)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    def natural_key(self):
        return(self.slug,)
 



class Product(models.Model):
    
    def __str__(self):
        return self.name
    
    tags = models.ManyToManyField(ProductTag,blank=True)
   # products = models.ManyToManyField(Product, blank=True)       
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    slug = models.SlugField(max_length=48)
    active = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    date_updated = models.DateTimeField(auto_now=True)
    objects = ActiveManager() #connecting ActiveManager to model by overriding an attribute called by convention objects


# class ProductTag(models.Model):
    
#     #products = models.ManyToManyField(Product, blank=True)
#     name = models.CharField(max_length=32)
#     slug = models.SlugField(max_length=48)
#     description = models.TextField(blank=True)
#     active = models.BooleanField(default=True)
    
#     def __str__(self):
#         return self.name
    
#     def natural_key(self):
#         return(self.slug,)
    
    



'''
As for any product catalog, having an image for every product is a must.In our case, we 
want the possibility to have any number of images per product. To accomplish this,
the information about the image needs to be in a seperate table that we can link back to
the Product model via a foreign key relationship
'''
class ProductImage(models.Model):
    
     
    
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product-images")
    thumbnail = models.ImageField(upload_to="product-thumbnails",null=True)
    objects = ActiveManager()
# ForeignKey is a field that stores the Primary key of the linked Product model.
# Install Pillow(for image functioning) pip3 install pillow  

'''
The last model that we are going to introduce is the concept of tag as a generalization
of categories: one product may have one or more tags, and one tag may contain one or 
products
'''  


# "ManyToManyField" automatically creates a linking between two tables, in this case 
# ProductTag and Products. This linking allows us to create relationships where any tags
# can be associated to any products and vice-versa.





class UserManager(BaseUserManager):
    use_in_migrations= True
    
    def _create_user(self,email,password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_user(self,email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff",False)
        extra_fields.setdefault("is_superuser",False)
        return self._create_user(email,password, **extra_fields)
    
    def create_superuser(self,email,password, **extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_superuser=True.")    

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        
        return self._create_user(email,password,**extra_fields)
    
class User(AbstractUser):
    username = None
    email = models.EmailField('email address',unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()        


class Address(models.Model):
    SUPPORTED_COUNTRIES = (
        ("uk","United Kingdom"),
        ("us","United States of America"),
        ("ind","India"),
        ("fra","France"),
        ("rus","Russia"),
        ("isr","Israel"),
    )
    
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    name = models.CharField(max_length=60)
    address1 = models.CharField("Address line 1",max_length=60)
    address2 = models.CharField("Address line 2",max_length=60,blank=True)
    zip_code = models.CharField("ZIP / Postal code",max_length=12)
    city = models.CharField(max_length=60)
    country = models.CharField(max_length=3,choices=SUPPORTED_COUNTRIES)
    objects = ActiveManager()
    def __str__(self):
        return ", ".join(
            [
                self.name,
                self.address1,
                self.address2,
                self.zip_code,
                self.city,
                self.country,
            ]
            
        )

    
        
class Basket(models.Model):
    OPEN = 10
    SUBMITTED = 20
    STATUSES = ((OPEN,"Open"), (SUBMITTED,"Submitted"))
    
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True)
    status = models.IntegerField(choices=STATUSES,default=OPEN)
    objects = ActiveManager()
   
    
    # def is_empty(self):       
    #     return self.basketline_set.all().count() == 0
         
    # def count(self):
    #     return sum(i.quantity for i in self.basketline_set.all())

        
class BasketLine(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    