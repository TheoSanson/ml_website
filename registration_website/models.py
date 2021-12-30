from django.db import models
from django.db.models.fields.related import ForeignKey

# Create your models here.

class Venue(models.Model):
    room_code = models.CharField(max_length=10,default='')
    college_code = models.CharField(max_length=10,default='')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['room_code', 'college_code'], name='Room x College Constraint')
        ]

class Examination(models.Model):
    exam_date = models.DateField()
    exam_time = models.TimeField()
    max_examinees = models.IntegerField()
    time_set = models.DateTimeField(auto_now=True)

class ExaminationVenueAssignment(models.Model):
    examination = models.ForeignKey(Examination,on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue,on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['examination', 'venue'], name='room_college constraint')
        ]

#REVERSED THE NAMES OF SCHOOL CATEGORY AND TYPE 

SCHOOL_TYPE = [
    ("Public", "Public"),
    ("Private","Private")
]

SCHOOL_CATEGORY = [
    ("High School", "High School"),
    ("College","College"),
    ("University","University"),
    ("Other","Other"),
]

SCHOOL_DISTRICT = [
    ("District I", "District I"),
    ("District II","District II"),
    ("Other","Other"),
]

class School(models.Model):
    school_name = models.CharField(max_length=50)
    school_type = models.CharField(max_length=20, choices=SCHOOL_TYPE)
    school_category = models.CharField(max_length=40, choices=SCHOOL_CATEGORY)
    district = models.CharField(max_length=40, choices=SCHOOL_DISTRICT)
    school_address = models.CharField(max_length=100,default='') #Increased Size

    class Meta:
            ordering = ["school_name"]

    def __str__(self):
        return self.school_name

TYPE = [
            ('','---------'), 
            ('Senior High School Graduating Student','Senior High School Graduating Student'),
            ('Senior High School Graduate','Senior High School Graduate'),
            ('College Student','College Student')
        ]

CAMPUS = [
            ('','---------'), 
            ('Main Campus','Main Campus'),
            ('ESU Alicia','ESU Alicia'),
            ('ESU Aurora','ESU Aurora'),
            ('ESU Curuan','ESU Curuan'),
            ('ESU Imelda','ESU Imelda'),
            ('ESU Ipil','ESU Ipil'),
            ('ESU Malangas','ESU Malangas'),
            ('ESU Molave','ESU Molave'),
            ('ESU Pagadian','ESU Pagadian'),
            ('ESU Siay','ESU Siay'),
            ('ESU Tungawan','ESU Tungawan')
        ]

INCOME_RANGE = [
            ('','---------'), 
            ('< ₱11,000','< ₱11,000'),
            ('₱11,000 - ₱22,000','₱11,000 - ₱22,000'),
            ('₱22,000 - ₱44,000','₱22,000 - ₱44,000'),
            ('₱44,000 - ₱77,000','₱44,000 - ₱77,000'),
            ('₱77,000 - ₱132,000','₱77,000 - ₱132,000'),
            ('₱132,000 - ₱220,000','₱132,000 - ₱220,000'),
            ('> ₱220,000','> ₱220,000')
]        

class Student(models.Model):
    firstname = models.CharField(max_length=30,default='')
    middlename = models.CharField(max_length=20,default='')
    lastname = models.CharField(max_length=20,default='')
    gender = models.CharField(max_length=7,default='') #Dropdown Selection
    date_of_birth = models.DateField()
    contactno = models.CharField(max_length=11,default='')
    school = models.ForeignKey(School,on_delete=models.RESTRICT)
    strand = models.CharField(max_length=50,default='')

    #New BioData Fields
    home_address = models.CharField(max_length=100,default='')
    applicant_type = models.CharField(max_length=50,default='',choices=TYPE)
    ethnicity = models.CharField(max_length=40,default='') #Checkbox Selection, specify if other
    religion = models.CharField(max_length=40,default='') #Checkbox Selection, specify if other
    combined_parent_income = models.CharField(max_length=30,default='',choices=INCOME_RANGE) #ADD CHOICES


    #CET Information
    times_taken = models.CharField(max_length=20,default='')
    last_time = models.DateField(null=True,blank=True)
    last_course = models.CharField(max_length=40, default='', blank=True) #Dropdown? Selection

    #College Student Fields
    target_campus = models.CharField(max_length=40,default='', choices=CAMPUS) #Selection, if ESU specify
    first_course = models.CharField(max_length=40,default='') #Dropdown Selection?
    second_course = models.CharField(max_length=40,default='') #Dropdown Selection?
    graduation_date = models.DateField()

    #examination = models.ForeignKey(ExaminationVenueAssignment,on_delete=models.RESTRICT)
    date_registered = models.DateTimeField(auto_now=True)

    tracking_number = models.CharField(max_length=6,unique=True,default='')
    predicted_performance = models.CharField(max_length=20,default='') #Target Label

    def __str__(self):
        return self.lastname + ', ' + self.firstname

class Subject(models.Model):
    subject_name = models.CharField(max_length=100)
    subject_type = models.CharField(max_length=30)

    class Meta:
            ordering = ["subject_name"]

    def __str__(self):
        return self.subject_name


class SubjectAssignment(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    value = models.FloatField()
