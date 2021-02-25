import django.forms as forms
from django.contrib.auth.models import User
from dal import autocomplete

import crispy_forms.bootstrap as bforms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, HTML

from default.models import Article, Mail
from users.models import Transaction
from users.forms import StudentRegisterForm, CoachRegisterForm, BaseRegistration, TableForm


class MailForm(forms.ModelForm):

    class Meta:
        model = Mail
        fields = ['name', 'subject', 'content', 'role']


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['name', 'title', 'subtitle', 'content']
        widgets = {
            'name': forms.TextInput(attrs={"readonly": "readonly"}),
        }


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ['amount', 'comment']


class newCoachForm(forms.Form):
    coach = forms.ModelChoiceField(
        queryset=User.objects.filter(profile__account_type='b'),
        widget=autocomplete.ModelSelect2(url='coach-autocomplete'),
        required=True
    )


class OtherAdminForm(BaseRegistration):
    verifiedAccount = forms.BooleanField(
        required=False, label="A vérifié son addresse mail")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-form-student-register'
        self.helper.form_method = 'post'
        self.fields['password'].required = False
        self.fields['confirm_password'].required = False

        self.helper.layout = Layout(
            Fieldset(
                'Modifier un compte',
                Row(
                    Column('first_name', css_class='form-group col-md-6 mb-0', placeholder="Prénom"),
                    Column('last_name', css_class='form-group col-md-6 mb-0', placeholder="Nom de famille"),
                    css_class='form-row'
                ),
                Row(
                    Column('birthdate', css_class='form-group col-md-6 mb-0'),
                    Column('email', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                'address',
                'phone_number',
                bforms.FieldWithButtons(
                    'secret_key',
                    HTML(
                        '<button type="button" id="buttoncopy" class="btn btn-primary" name="Save" onclick="copyKey()"> \
                            copier\
                        </button>')),
                'verifiedAccount'
            ),
            bforms.FormActions(
                Submit('save', 'Enregistrer les modifications'),
                HTML('<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#SendNotif">\
                        Envoyer une notification\
                    </button>')
            )
        )

    def clean(self):
        super().clean(admin=True)


class StudentAdminForm(StudentRegisterForm, OtherAdminForm):
    coach = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "readonly": "readonly",
                "placeholder": "Aucun coach pour l'instant",
                "class": "coach_readonly"
            }
        ),
        required=False
    )
    balance = forms.FloatField(
        required=False, label="Balance",
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-form-student-register'
        self.helper.form_method = 'post'
        self.helper.include_media = False

        self.helper.layout = Layout(
            Fieldset(
                'Modifier un élève',
                Row(
                    Column('first_name', css_class='form-group col-md-6 mb-0', placeholder="Prénom"),
                    Column('last_name', css_class='form-group col-md-6 mb-0', placeholder="Nom de famille"),
                    css_class='form-row'
                ),
                Row(
                    Column('birthdate', css_class='form-group col-md-6 mb-0'),
                    Column('school_level', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('tutor_firstName', css_class='form-group col-md-6 mb-0'),
                    Column('tutor_name', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('ville', css_class='form-group col-md-4 mb-0'),
                    Column('zip', css_class='form-group col-md-4 mb-0'),
                    Column('address', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('email', css_class='form-group col-md-6 mb-0'),
                    Column('phone_number', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('resp_phone_number1', css_class='form-group col-md-4 mb-0'),
                    Column('resp_phone_number2', css_class='form-group col-md-4 mb-0'),
                    Column('resp_phone_number3', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row'
                ),
                bforms.InlineCheckboxes('courses'),
                Row(
                    Column('comments', css_class='form-group col-md-12 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('wanted_schedule', css_class='form-group col-md-12 mb-0'),
                    css_class='form-row'
                ),
                'NeedsVisit',
                Row(
                    Column('coach', css_class="form-group col-xs-12 col-sm-12 col-md-12 col-lg-8 col-xl-8"),
                    HTML('<div class="col-xs-12 col-sm-12 col-md-6 col-lg-2 col-xl-2 justify-content-center"><button class="btn btn-primary" type="button" onclick="$(\'#chooseCoach\').modal(\'toggle\');">Choisir un nouveau coach</button></div>'),
                    HTML('<div class="col-xs-12 col-sm-12 col-md-6 col-lg-2 col-xl-2 justify-content-center"><button class="btn btn-primary" type="button" onclick="reloadCoach()">Rechercher un nouveau coach</button></div>'),
                ),
                'balance',
                'verifiedAccount'
            ),
            bforms.FormActions(
                Submit('save', 'Enregistrer les modifications', css_class="btn btn-success"),
                HTML('<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#SendNotif">\
                        Envoyer une notification\
                    </button>\
                    <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#UpdateBalance">\
                        <i class="fas fa-plus"></i>\
                        Augmenter la balance\
                    </button>')
            )
        )


class CoachAdminForm(CoachRegisterForm, OtherAdminForm):
    coach_states = [
        ('a', '----'),
        ('b', 'Engagé'),
        ('c', 'Refusé'),
    ]

    nbStudents = forms.IntegerField(
        required=False,
        label="nombre d'étudiants du coach")
    confirmedAccount = forms.ChoiceField(
        choices=coach_states, required=False,
        label="Etat du coach")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-form-coach-register'
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Fieldset(
                'Modifier un coach',
                Row(
                    Column('first_name', css_class='form-group col-md-6 mb-0', placeholder="Prénom"),
                    Column('last_name', css_class='form-group col-md-6 mb-0', placeholder="Nom de famille"),
                    css_class='form-row'
                ),
                Row(
                    Column('birthdate', css_class='form-group col-md-6 mb-0'),
                    Column('nationalRegisterID', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                'address',
                Row(
                    Column('email', css_class='form-group col-md-6 mb-0'),
                    Column('phone_number', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                bforms.InlineCheckboxes('courses'),
                Row(
                    Column('school', css_class='form-group col-md-6 mb-0'),
                    Column('school_level', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                TableForm(
                    'french_level',
                    'dutch_level',
                    'english_level',
                ),
                'IBAN',
                'confirmedAccount',
                bforms.FieldWithButtons(
                    'secret_key',
                    HTML(
                        '<button type="button" id="buttoncopy" class="btn btn-primary" name="Save" onclick="copyKey()"> \
                            copier\
                        </button>')
                ),
                'verifiedAccount'
            ),
            bforms.FormActions(
                Submit('save', 'Enregistrer les modifications'),
                HTML('<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#SendNotif">\
                        Envoyer une notification\
                    </button>')
            )
        )
