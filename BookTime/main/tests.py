from django.test import TestCase, override_settings
from django.urls import reverse
from main import forms
from decimal import Decimal
from main import models
from io import StringIO
import tempfile
from django.conf import settings
from django.core.management import call_command
from main import models
# Create your tests here.
class TestPage(TestCase):
    def test_home_page_works(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'home.html')
        self.assertContains(response,'BookTime')
        
    def test_about_us_page_works(self):
        response = self.client.get(reverse('about_us'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'about_us.html')
        self.assertContains(response,'BookTime')    
        
    def test_contact_us_page_works(self):
        response = self.client.get(reverse('contact_us'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/contact_form.html')
        self.assertContains(response, 'BookTime')
        self.assertIsInstance(response.context['form'], forms.ContactForm)
    
    def test_add_to_basket_loggedin_works(self):
        user1 = models.User.objects.create_user(
            "user1@a.com", "pw432joij"
        )
        cb = models.Product.objects.create(
            name = "The cathedral and the bazaar",
            slug = "cathedral-bazaar",
            price = Decimal("10.00"),
            
        )
        
        w = models.Product.objects.create(
            name = "MicroSoft Windows Guide",
            slug = "microsoft-windows-guide",
            price = Decimal("12.00"),
        )
        
        self.client.force_login(user1)
        response = self.client.get(reverse("add_to_basket"), {"product_id": cb.id})
        response = self.client.get(reverse("add_to_basket"), {"product_id": cb.id})
        self.assertTrue(models.Basket.objects.filter(user=user1).exists())
        self.assertEquals(models.BasketLine.objects.filter(basket__user=user1).count(),1,)
        
        response = self.client.get(reverse("add_to_basket"),{"product_id": w.id})
        
        self.assertEquals(models.BasketLine.objects.filter(basket__user=user1).count(),2,)
                  
    
        
class TestModel(TestCase):
    def test_active_manager_works(self):
        models.Product.objects.create(
            name='The cathedral and the bazaar',
            price=Decimal("10.00")
        )
        
        models.Product.objects.create(
            name="Pride and Prejudice",
            price=Decimal("2.00")
        )
        
        models.Product.objects.create(
            name="A Tale of Two Cities",
            price=Decimal("2.00"),
            active=False
        )        
        
        self.assertEqual(len(models.Product.objects.active()),2) 
        
        
class TestImport(TestCase):
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    
    def test_import_data(self):
        out = StringIO()
        args = ['main/fixtures/product-sample.csv',
                'main/fixtures/product-sampleimages/']
        
        call_command('import_data', *args, stdout=out)
        
        expected_out = ("Importing Products\n"
                        "Products processed=3 (created=3)\n"
                        "Tags processed=6 (created=6)\n"
                        "Images processed=3\n")
        
        self.assertEqual(out.getvalue(),expected_out)
        self.assertEqual(models.Product.objects.count(),3)
        self.assertEqual(models.ProductTag.objects.count(),6)
        self.assertEqual(models.ProductImage.objects.count(),3)
        
    