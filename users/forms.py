import django.forms as forms
from django.contrib.auth.models import User

import crispy_forms.bootstrap as bforms
from crispy_forms.utils import render_field
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, Field

from cad.settings import CRISPY_TEMPLATE_PACK
from users.models import FollowElement


class TableForm(Field):
    """Renders several choice fields as a table of radio buttons"""

    def render(
        self,
        form,
        form_style,
        context,
        template_pack: str = CRISPY_TEMPLATE_PACK,
        extra_context=None,
        **kwargs
    ) -> str:
        """Generates the html string of the table

        Returns:
            str: A rendered table form
        """
        return """<table class="table" id="gridLang">
                <thead>
                    <tr><th scope="col" class="col-md-2">/</th>{}</tr>
                </thead>
                <tbody>{}</tbody>
            </table>
            """.format(
            "".join(
                '<th scope="col" class="col-md-2">{}</th>'.format(choice)
                for _, choice in form[self.fields[0]].field.choices
            ),
            "".join(
                render_field(
                    self.fields[x],
                    form,
                    form_style,
                    context,
                    template="table_form.html",
                    template_pack=template_pack,
                    **kwargs
                )
                for x in range(len(self.fields))
            ),
        )


class BaseRegistration(forms.Form):
    """The base registration form"""

    first_name = forms.CharField(max_length=30, required=True, label="Prénom")
    last_name = forms.CharField(max_length=150, required=True, label="Nom")
    password = forms.CharField(
        min_length=8,
        max_length=150,
        required=True,
        widget=forms.PasswordInput,
        label="Mot de passe",
    )
    confirm_password = forms.CharField(
        min_length=8,
        max_length=150,
        required=True,
        widget=forms.PasswordInput,
        label="Confirmez le mot de passe",
    )
    birthdate = forms.CharField(max_length=25, required=True, label="Date de naissance")
    email = forms.EmailField(required=True, label="Adresse mail")
    address = forms.CharField(required=True, label="Rue et numéro")
    phone_number = forms.CharField(
        required=True, max_length=25, label="numéro de téléphone"
    )

    def clean(self, admin=False, *args, **kwargs):  # skipcq PYL-W0221
        """Cleans the data from the form, adding errors where the data is not correct

        Args:
            admin (bool, optional): Whether to force the data saving or not. Defaults to False.
        """
        cleaned_data = super().clean(*args, **kwargs)
        if admin:
            return
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        username = "{}_{}".format(last_name, first_name)

        if password != confirm_password:
            # If passwords are different
            msg = "Les mots de passe ne sont pas identiques!"
            self.add_error("password", msg)

        if User.objects.filter(username=username).count() > 0:
            msg = "Un compte avec les mêmes noms et prénoms existe déjà!"
            self.add_error("first_name", msg)


class StudentRegisterForm(BaseRegistration):
    """The student registration form"""

    levels = [
        ("a", "Primaire"),
        ("b", "1ère humanité"),
        ("c", "2ème humanité"),
        ("d", "3ème humanité"),
        ("e", "4ème humanité"),
        ("f", "5ème humanité"),
        ("g", "6ème humanité"),
    ]

    courses_choices = [
        ("a", "Maths"),
        ("b", "Physique"),
        ("c", "Français"),
        ("d", "Chimie"),
    ]

    school_level = forms.ChoiceField(
        required=True, choices=levels, label="Niveau Scolaire"
    )

    tutor_name = forms.CharField(
        required=True, max_length=50, label="Nom d'une personne responsable"
    )
    tutor_firstName = forms.CharField(
        required=True, max_length=50, label="Prénom d'une personne responsable"
    )
    comments = forms.CharField(required=False, label="Remarques éventuelles")
    wanted_schedule = forms.CharField(
        required=True, widget=forms.Textarea, label="Horaire"
    )
    zip = forms.CharField(max_length=4, required=True, label="Code Postal")
    ville = forms.CharField(max_length=50, required=True, label="Ville")
    NeedsVisit = forms.BooleanField(
        required=False, label="Désire une visite pédagogique ?"
    )
    courses = forms.MultipleChoiceField(
        choices=courses_choices, required=True, label="Cours désirés"
    )
    phone_number = forms.CharField(
        required=False, max_length=25, label="numéro de téléphone de l'étudiant"
    )
    resp_phone_number1 = forms.CharField(
        required=True, label="numéro de téléphone d'un responsable 1", max_length=25
    )
    resp_phone_number2 = forms.CharField(
        required=False, label="numéro de téléphone d'un responsable 2", max_length=25
    )
    resp_phone_number3 = forms.CharField(
        required=False, label="numéro de téléphone d'un responsable 3", max_length=25
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id-form-student-register"
        self.helper.form_method = "post"

        self.helper.layout = Layout(
            Fieldset(
                """Devenez élève! <br/>
                <small>
                    Les champs suivis d\'une astérisque (<span style="color:red">*</span>) sont obligatoires
                </small>""",
                Row(
                    Column("first_name", css_class="form-group col-md-6 mb-0"),
                    Column("last_name", css_class="form-group col-md-6 mb-0"),
                    css_class="form-row",
                ),
                Row(
                    Column("password", css_class="form-group col-md-6 mb-0"),
                    Column("confirm_password", css_class="form-group col-md-6 mb-0"),
                    css_class="form-row",
                ),
                Row(
                    Column("birthdate", css_class="form-group col-md-6 mb-0"),
                    Column("school_level", css_class="form-group col-md-6 mb-0"),
                    css_class="form-row",
                ),
                Row(
                    Column("tutor_firstName", css_class="form-group col-md-6 mb-0"),
                    Column("tutor_name", css_class="form-group col-md-6 mb-0"),
                    css_class="form-row",
                ),
                Row(
                    Column("ville", css_class="form-group col-md-4 mb-0"),
                    Column("zip", css_class="form-group col-md-4 mb-0"),
                    Column("address", css_class="form-group col-md-4 mb-0"),
                    css_class="form-row",
                ),
                Row(
                    Column("email", css_class="form-group col-md-6 mb-0"),
                    Column("phone_number", css_class="form-group col-md-6 mb-0"),
                    css_class="form-row",
                ),
                Row(
                    Column("resp_phone_number1", css_class="form-group col-md-4 mb-0"),
                    Column("resp_phone_number2", css_class="form-group col-md-4 mb-0"),
                    Column("resp_phone_number3", css_class="form-group col-md-4 mb-0"),
                    css_class="form-row",
                ),
                bforms.InlineCheckboxes("courses"),
                Row(
                    Column("comments", css_class="form-group col-md-12 mb-0"),
                    css_class="form-row",
                ),
                Row(
                    Column("wanted_schedule", css_class="form-group col-md-12 mb-0"),
                    css_class="form-row",
                ),
                "NeedsVisit",
            ),
            Submit("submit", "S'inscrire"),
        )


class CoachRegisterForm(BaseRegistration):
    """The coach registration form"""

    levels = [
        ("h", "Primaire"),
        ("i", "Humanité"),
        ("j", "Les deux"),
    ]

    lang_levels = [
        ("a", "Langue maternelle"),
        ("b", "Très bon"),
        ("c", "Bon"),
        ("d", "Notions de base"),
        ("e", "Aucun"),
    ]

    courses_choices = [
        ("a", "Maths"),
        ("b", "Physique"),
        ("c", "Français"),
        ("d", "Chimie"),
    ]

    school_level = forms.ChoiceField(
        required=True, choices=levels, label="Niveau Scolaire"
    )
    school = forms.CharField(required=True, max_length=50, label="Ecole")
    IBAN = forms.CharField(required=True, max_length=50, label="numéro de compte IBAN")
    french_level = forms.ChoiceField(
        choices=lang_levels, required=True, label="Niveau de français"
    )
    dutch_level = forms.ChoiceField(
        choices=lang_levels, required=True, label="Niveau de néerlandais"
    )
    english_level = forms.ChoiceField(
        choices=lang_levels, required=True, label="Niveau d'anglais"
    )
    nationalRegisterID = forms.CharField(
        required=True, max_length=50, label="numéro de registre national"
    )
    courses = forms.MultipleChoiceField(
        choices=courses_choices, required=True, label="Vous souhaitez donner cours en"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id-form-coach-register"
        self.helper.form_method = "post"

        self.helper.layout = Layout(
            Fieldset(
                "Devenez coach!",
                Row(
                    Column("first_name", css_class="form-group col-md-6 mb-0"),
                    Column("last_name", css_class="form-group col-md-6 mb-0"),
                    css_class="form-row",
                ),
                Row(
                    Column("password", css_class="form-group col-md-6 mb-0"),
                    Column("confirm_password", css_class="form-group col-md-6 mb-0"),
                    css_class="form-row",
                ),
                Row(
                    Column("birthdate", css_class="form-group col-md-6 mb-0"),
                    Column("nationalRegisterID", css_class="form-group col-md-6 mb-0"),
                    css_class="form-row",
                ),
                "address",
                Row(
                    Column("email", css_class="form-group col-md-6 mb-0"),
                    Column("phone_number", css_class="form-group col-md-6 mb-0"),
                    css_class="form-row",
                ),
                bforms.InlineCheckboxes("courses"),
                Row(
                    Column("school", css_class="form-group col-md-6 mb-0"),
                    Column("school_level", css_class="form-group col-md-6 mb-0"),
                    css_class="form-row",
                ),
                TableForm(
                    "french_level",
                    "dutch_level",
                    "english_level",
                ),
                "IBAN",
            ),
            Submit("submit", "S'inscrire"),
        )


class StudentReadOnlyForm(StudentRegisterForm):
    """The student readonly form"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id-form-student-readonly"
        for key, _ in self.fields.items():
            self.fields[key].widget.attrs.update({"readonly": "readonly"})

        self.helper.layout = Layout(
            Fieldset(
                "Mon compte",
                Row(
                    Column("first_name", css_class="form-group col-md-6 mb-0"),
                    Column("last_name", css_class="form-group col-md-6 mb-0"),
                    css_class="form-row",
                ),
                Row(
                    Column("birthdate", css_class="form-group col-md-6 mb-0"),
                    Column("school_level", css_class="form-group col-md-6 mb-0"),
                    css_class="form-row",
                ),
                Row(
                    Column("tutor_firstName", css_class="form-group col-md-6 mb-0"),
                    Column("tutor_name", css_class="form-group col-md-6 mb-0"),
                    css_class="form-row",
                ),
                Row(
                    Column("ville", css_class="form-group col-md-4 mb-0"),
                    Column("zip", css_class="form-group col-md-4 mb-0"),
                    Column("address", css_class="form-group col-md-4 mb-0"),
                    css_class="form-row",
                ),
                Row(
                    Column("email", css_class="form-group col-md-6 mb-0"),
                    Column("phone_number", css_class="form-group col-md-6 mb-0"),
                    css_class="form-row",
                ),
                bforms.InlineCheckboxes("courses"),
                Row(
                    Column("comments", css_class="form-group col-md-12 mb-0"),
                    css_class="form-row",
                ),
                Row(
                    Column("wanted_schedule", css_class="form-group col-md-12 mb-0"),
                    css_class="form-row",
                ),
                "NeedsVisit",
            ),
        )

    def clean(self, *args, **kwargs):  # skipcq PYL-W0221
        """Cleans the data from the form"""
        super().clean(admin=True, *args, **kwargs)


class CoachReadOnlyForm(CoachRegisterForm):
    """The coach readonly form"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id-form-coach-readonly"
        self.helper.form_method = "post"
        for key, _ in self.fields.items():
            self.fields[key].widget.attrs.update({"readonly": "readonly"})

        self.helper.layout = Layout(
            Fieldset(
                "Mon compte",
                Row(
                    Column(
                        "first_name", css_class="form-group col-md-6 mb-0 read-only"
                    ),
                    Column("last_name", css_class="form-group col-md-6 mb-0 read-only"),
                    css_class="form-row",
                ),
                Row(
                    Column("birthdate", css_class="form-group col-md-6 mb-0"),
                    Column("nationalRegisterID", css_class="form-group col-md-6 mb-0"),
                    css_class="form-row",
                ),
                "address",
                Row(
                    Column("email", css_class="form-group col-md-6 mb-0"),
                    Column("phone_number", css_class="form-group col-md-6 mb-0"),
                    css_class="form-row",
                ),
                bforms.InlineCheckboxes("courses"),
                Row(
                    Column("school", css_class="form-group col-md-6 mb-0"),
                    Column("school_level", css_class="form-group col-md-6 mb-0"),
                    css_class="form-row",
                ),
                TableForm(
                    "french_level",
                    "dutch_level",
                    "english_level",
                ),
                "IBAN",
            )
        )

    def clean(self, *args, **kwargs):  # skipcq PYL-W0221
        """Cleans the data from the form"""
        super().clean(admin=True, *args, **kwargs)


class BaseReadOnly(BaseRegistration):
    """The base readonly form"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id-form-coach-readonly"
        self.helper.form_method = "post"
        for key, _ in self.fields.items():
            self.fields[key].widget.attrs.update({"readonly": "readonly"})

        self.helper.layout = Layout(
            Fieldset(
                "Mon compte",
                Row(
                    Column(
                        "first_name", css_class="form-group col-md-6 mb-0 read-only"
                    ),
                    Column("last_name", css_class="form-group col-md-6 mb-0 read-only"),
                    css_class="form-row",
                ),
                Row(
                    Column("birthdate", css_class="form-group col-md-6 mb-0"),
                    Column("email", css_class="form-group col-md-6 mb-0"),
                    css_class="form-row",
                ),
                Row(
                    Column("address", css_class="form-group col-md-6 mb-0"),
                    Column("phone_number", css_class="form-group col-md-6 mb-0"),
                    css_class="form-row",
                ),
            ),
        )

    def clean(self, *args, **kwargs):  # skipcq PYL-W0221
        """Cleans the data from the form"""
        super().clean(admin=True, *args, **kwargs)


class addFollowElementForm(forms.ModelForm):
    """The follow element form"""

    class Meta:
        """The meta class of the follow element form"""

        model = FollowElement
        exclude = ("approved", "coach", "student")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id-add-follow-elem"
        self.helper.form_method = "post"

        self.helper.layout = Layout(
            Fieldset(
                "Ajouter un cours",
                Row(
                    Column("date", css_class="form-group col-md-4 mb-0"),
                    Column(
                        "startHour",
                        placeholder="Heure de début",
                        css_class="form-group col-md-4 mb-0",
                    ),
                    Column("endHour", css_class="form-group col-md-4 mb-0"),
                    css_class="form-row",
                ),
                Row(
                    Column("comments", css_class="form-group col-md-12 mb-2"),
                    css_class="form-row",
                ),
            ),
            Submit("submit", "Ajouter le cours"),
        )
