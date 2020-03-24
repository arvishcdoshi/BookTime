from django.test import TestCase
from django.urls import reverse
from main import forms
from decimal import Decimal
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