from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.forms.widgets import MultiWidget, RadioSelect, TextInput
from .models import SCHOOL_CATEGORY, SCHOOL_TYPE, School, Subject, SubjectAssignment, Venue, Student

SUBJECT_TYPE = [
    ("English","English"),
    ("Math","Math"),
    ("Science","Science"),
    ("Other","Other"),
]

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
        widgets = {
            'subject_name': forms.TextInput(attrs={'class': 'form-control mt-1 mb-3'}),
            'subject_type': forms.Select(attrs={'class': 'form-control mt-1 mb-3'},choices=SUBJECT_TYPE),
        }

class ReligionWidget(MultiWidget):
    def __init__(self,attrs={}):
        RELIGIONS = (
            ('Roman Catholicism','Roman Catholicism'),
            ('Islam','Islam'), 
            ('Protestantism','Protestantism'), 
            ('Others','Others (Please Specify)')
        )

        _widgets = (
            RadioSelect(attrs={'class': 'mt-1 mb-1 unstyled', 'required':True},choices=RELIGIONS),
            TextInput(attrs=attrs)
        )

        super().__init__(_widgets,attrs)

    def decompress(self, value):
        if value:
            return value
        return ['', '']

class ReligionMultiValueField(forms.MultiValueField):
    widget = ReligionWidget()
    def __init__(self, **kwargs):
        fields = (
            forms.CharField(
                max_length=30,
                required = True
            ),
            forms.CharField(
                max_length=30,
                required = False
            )
        )
    
        super().__init__(fields=fields,required = False,require_all_fields=True, **kwargs)

    def compress(self,value):
        if 'Others' in value:
            del value[0]
        else:
            del value[1]
        return "|".join(value)

class EthnicityWidget(MultiWidget):
    def __init__(self,attrs={}):
        ETHNICITIES = (
                    ('None','I am not part of any cultural/ethnic group'),
                    ('Badjao','Badjao'), 
                    ('Kalibugan','Kalibugan'), 
                    ('Maranaw','Maranaw'), 
                    ('Subanen','Subanen'), 
                    ('Yakan','Yakan'), 
                    ('Bagobo','Bagobo'), 
                    ('Maguindanao','Maguindanao'), 
                    ('Samal','Samal'), 
                    ('Tausug','Tausug'), 
                    ('Others','Others (Please Specify)'), 
        )

        _widgets = (
            RadioSelect(attrs={'class': 'mt-1 mb-1 unstyled', 'required':True},choices=ETHNICITIES),
            TextInput(attrs=attrs)
        )

        super().__init__(_widgets,attrs)

    def decompress(self, value):
        if value:
            return value
        return ['', '']

class EthnicityMultiValueField(forms.MultiValueField):
    widget = EthnicityWidget()
    def __init__(self, **kwargs):
        fields = (
            forms.CharField(
                max_length=30,
                required = True
            ),
            forms.CharField(
                max_length=30,
                required = False
            )
        )
    
        super().__init__(fields=fields, required=False, **kwargs)

    def compress(self,value):
        if 'Others' in value:
            del value[0]
        else:
            del value[1]
        return "|".join(value)
class StudentForm(forms.ModelForm):

    religion = ReligionMultiValueField() #Assigns custom multivaluefield to religion formfield
    religion.widget.widgets[0].attrs['required'] = True #Ensures that radiobutton choices must be selected
    religion.label = "<strong>Religious Affiliation*</strong>"
    ethnicity = EthnicityMultiValueField()
    ethnicity.label = "<strong>Which Cultural/Ethnic Group are you a part of?*</strong>"
    ethnicity.widget.widgets[0].attrs['required'] = True

    class Meta:
        model = Student
        fields = '__all__'

        GENDER = (
            ('','---------'), 
            ('Male','Male'), 
            ('Female','Female')
        )

        STRAND = (
            ('','---------'), 
            ('ABM','ABM'), 
            ('STEM','STEM'),
            ('HUMSS','HUMSS'),
            ('GAS','GAS'),
            ('TVL - Information Communication and Technology','TVL - Information Communication and Technology'),
            ('TVL - Home Economics','TVL - Home Economics'),
            ('TVL - Other','TVL - Other'),
            ('TVL - Food Related','TVL - Food Related'),
            ('Industrial Arts','Industrial Arts'),
            ('Arts & Design / Sports','Arts & Design / Sports'),
        )

        widgets = {
            'firstname': forms.TextInput(attrs={'class': 'form-control mt-1 mb-3'}),
            'middlename': forms.TextInput(attrs={'class': 'form-control mt-1 mb-3'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control mt-1 mb-3'}),
            'gender': forms.Select(attrs={'class': 'form-control mt-1 mb-3'},choices=GENDER),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control mt-1 mb-3', 'type': 'date'}),
            'contactno': forms.TextInput(attrs={'class': 'form-control mt-1 mb-3'}),
            'school': forms.Select(attrs={'class':'form-control mt-1 mb-3'}),
            'strand': forms.Select(attrs={'class': 'form-control mt-1 mb-3'},choices=STRAND),
            'home_address': forms.TextInput(attrs={'class': 'form-control mt-1 mb-3'}), #New Data Starts Here
            'combined_parent_income': forms.Select(attrs={'class':'form-control mt-1 mb-3'}),
            'applicant_type': forms.Select(attrs={'class':'form-control mt-1 mb-3'}),
            'times_taken': forms.NumberInput(attrs={'class': 'form-control mt-1 mb-3'}),
            'last_time': forms.DateInput(attrs={'class': 'form-control mt-1 mb-3', 'type': 'date'}),
            'applicant_type': forms.Select(attrs={'class': 'form-control mt-1 mb-3'}),
            'last_course': forms.TextInput(attrs={'class': 'form-control mt-1 mb-3'}),
            'target_campus': forms.Select(attrs={'class': 'form-control mt-1 mb-3'}),
            'first_course': forms.TextInput(attrs={'class': 'form-control mt-1 mb-3'}), #Collect All Courses to make Dropdown
            'second_course': forms.TextInput(attrs={'class': 'form-control mt-1 mb-3'}), #Collect All Courses to make Dropdown
            'graduation_date': forms.DateInput(attrs={'class': 'form-control mt-1 mb-3', 'type': 'date'}),
        }

        labels = {
            'firstname':'<strong>Firstname</strong>',
            'middlename':'<strong>Middlename</strong>',
            'lastname':'<strong>Lastname</strong>',
            'date_of_birth':'<strong>Date of Birth</strong>',
            'gender':'<strong>Gender</strong>',
            'contactno':'<strong>Contact No.</strong>',
            'home_address':'<strong>Home Address</strong>',
            'times_taken':'<strong>How many times have you taken the CET?</strong>',
            'last_time':'If taken before, when was the last time you took the CET?',
            'combined_parent_income':'<strong>What is the combined income of your parents or guardian?</strong>',
            'school':'<strong>What is the the school you are graduated/graduating from?</strong>',
            'strand':'<strong>Senior High School Strand</strong>',
            'applicant_type':'<strong>Applicant Type</strong>',
            'last_course':'(If applicable) What was the last course you were enrolled in?',
            'graduation_date':'<strong>When did you graduate? (Graduation Date if Graduating?)</strong>',
            'target_campus':'<strong>Which Campus do you intend to enroll in?</strong>',
            'first_course':'<strong>Course to take up: 1st Choice</strong>',
            'second_course':'<strong>2nd Choice</strong>',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        school = self.fields['school']                                    
        school.choices = list(school.choices)
        school.choices.append(tuple(('1', 'Other (Specify)'))) #IMPORTANT! Validation will FAIL when choosing "other" in the school field, unless the number points to a valid object id in the db

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = '__all__'
        widgets = {
            'school_name': forms.TextInput(attrs={'class': 'form-control mt-1 mb-3'}),
            'school_type': forms.Select(attrs={'class':'form-control mt-1 mb-3'}),
            'school_category': forms.Select(attrs={'class':'form-control mt-1 mb-3'}),
            'district': forms.Select(attrs={'class':'form-control mt-1 mb-3'}),
            'school_address': forms.TextInput(attrs={'class': 'form-control mt-1 mb-3'}),
        }
        labels = {
            'district':'School district',
        }

        

class SubjectAssignmentForm(forms.ModelForm):
    class Meta:
        model = SubjectAssignment
        exclude = ('student',)
        widgets = {
            'subject': forms.Select(attrs={'class':'form-control mt-1 mb-2'}),
            'value': forms.NumberInput(attrs={'class':'form-control mt-1 mb-2'}),
        }

class NewSubjectForm(forms.Form):
    value = forms.FloatField()
    subject_name = forms.CharField(max_length=100)
    subject_type = forms.CharField(max_length=30,widget=forms.Select(choices=SUBJECT_TYPE))

class StudentBooles(forms.Form):
    other_school_boole = forms.CharField(max_length=10)
    other_subject_boole = forms.CharField(max_length=10)

class SearchStatusForm(forms.Form):
    tracking_number = forms.CharField(max_length=6)