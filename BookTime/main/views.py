from django.views.generic.edit import FormView
from main import forms
#from django.shortcuts import render
from main import models
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import logging
from django.contrib.auth import login,authenticate
from django.contrib import messages
# Create your views here.

logger = logging.getLogger(__name__)
# A CLASS BASED VIEW.
class ContactUsView(FormView):
    template_name = 'contact_form.html'
    form_class = forms.ContactForm
    success_url = '/'

    def form_valid(self,form):
        form.send_mail()
        return super().form_valid(form)

# FUNCTION BASED VIEW FOR ABOVE CODE(JUST FOR REFERENCE)

'''
 def contact_us(request):
     if request.method == 'POST':
         form = forms.ContactForm(request.POST)
         if form.is_valid():
             form.send_mail()
             return HttpResponseRedirect('/')

    else:
        form = forms.ContactForm()
        
    return render(request,'contact_form.html', {'form':form})                  
'''
class ProductListView(ListView):
    template_name = "main/product_list.html"
    paginate_by = 4
    
    def get_queryset(self):
        tag = self.kwargs['tag']
        self.tag = None
        if tag != "all":
            self.tag = get_object_or_404(
                models.ProductTag, slug=tag
            )

        if self.tag:
            products = models.Product.objects.active().filter(
                tags = self.tag
            )
        else:
            products = models.Product.objects.active()
            
        return products.order_by("name")  
      
# FOR FURTHER FUNCTIONALITY        
def add_to_basket(request):
    product = get_object_or_404(
        models.Product, pk=request.GET.get("product_id")
    )
    basket = request.basket
    if not request.basket:
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None
        basket = models.Basket.objects.create(user=user)
        request.session["basket_id"] = basket.id                
        
    basketline,created = models.BasketLine.objects.get_or_create(
        basket=basket, product=product
    )   
    if not created:
        basketline.quantity += 1
        basketline.save()
        
    return HttpResponseRedirect(
        reverse("product", args=(product.slug))
    )    

class SignupView(FormView):
    template_name = "signup.html"
    form_class = forms.UserCreationForm
    
    def get_success_url(self):
        redirect_to = self.request.GET.get("next", "/")
        return redirect_to
    
    def form_valid(self,form):
        response = super().form_valid(form)
        form.save()    
        
        email = form.cleaned_data.get("email")
        raw_password = form.cleaned_data.get("password1")
        logger.info(
            "New Signup for email=%s through SignupView", email
        )
        
        user = authenticate(email=email, password=raw_password)
        login(self.request,user)
        
        form.send_mail()
        
        messages.info(
            self.request, "You signed up Successfully."
        )
        
        return response
     