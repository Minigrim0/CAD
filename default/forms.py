from django import forms


class contactForm(forms.Form):
    sujet = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)
    envoyeur = forms.EmailField(label=u"Votre adresse mail")
