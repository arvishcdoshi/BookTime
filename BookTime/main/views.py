from django.views.generic.edit import FormView
from main import forms
#from django.shortcuts import render

# Create your views here.

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


