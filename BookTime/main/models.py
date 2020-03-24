from django.db import models

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


class Product(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    slug = models.SlugField(max_length=48)
    active = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    date_updated = models.DateTimeField(auto_now=True)
    objects = ActiveManager() #connecting ActiveManager to model by overriding an attribute called by convention objects
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

# ForeignKey is a field that stores the Primary key of the linked Product model.
# Install Pillow(for image functioning) pip3 install pillow  

'''
The last model that we are going to introduce is the concept of tag as a generalization
of categories: one product may have one or more tags, and one tag may contain one or 
products
'''  

class ProductTag(models.Model):
    products = models.ManyToManyField(Product, blank=True)
    name = models.CharField(max_length=32)
    slug = models.SlugField(max_length=48)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

# "ManyToManyField" automatically creates a linking between two tables, in this case 
# ProductTag and Products. This linking allows us to create relationships where any tags
# can be associated to any products and vice-versa.











