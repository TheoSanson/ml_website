from django.forms.formsets import formset_factory
from django.shortcuts import render, redirect
from registration_website.forms import NewSubjectForm, StudentBooles, StudentForm, SubjectAssignmentForm, SubjectForm, SchoolForm
from .models import SCHOOL_TYPE, Subject, SubjectAssignment, Student, School
from django.forms import modelformset_factory, formset_factory
from django.utils.crypto import get_random_string
import string, pickle
import pandas as pd

# Create your views here.
def home(request):
    return

def subject_form(request,id=0):
    if request.method == "GET":
        if id == 0:
            form = SubjectForm()
        else:
            subject = Subject.objects.get(pk=id)
            form = SubjectForm(instance=subject)
        return render(request,"subject/subject_form.html",{'form':form})
    else:
        if id == 0:
            form = SubjectForm(request.POST)
        else:
            subject = Subject.objects.get(pk=id)
            form = SubjectForm(request.POST,instance=subject)
        if form.is_valid():
            form.save()

        return redirect('/registration/subject/list/')

        if id == 0:
            return #redirect('/examination/list/')

def subject_view(request,id=0):
    if id != 0:
        subject = [
            Subject.objects.get(pk=id),
        ]
        context = {
            'subject': subject
        }
        return render(request,"subject/subject_view.html",context)
    return #

def subject_list(request):
    subject_objects = Subject.objects.all
    context = {
        'subject_list': subject_objects
    }
    return render(request, "subject/subject_list.html ", context)

def school_form(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = SchoolForm()
        else:
            school = School.objects.get(pk=id)
            form = SchoolForm(instance=school)
        return render(request,"school/school_form.html",{'form':form})
    else:
        if id == 0:
            form = SchoolForm(request.POST)
        else:
            examination = School.objects.get(pk=id)
            form = SchoolForm(request.POST,instance=examination)
        if form.is_valid():
            form.save()
            
        return redirect('/registration/school/list/')

def school_view(request,id=0):
    if id != 0:
        school = [
            School.objects.get(pk=id),
        ]
        context = {
            'school':school
        }
        return render(request,"school/school_view.html",context)
    return #

def school_list(request):
    school_objects = School.objects.all
    context = {
        'school_list': school_objects
    }
    return render(request, "school/school_list.html", context)

def student_apply(request):
    subjectFormset = formset_factory(SubjectAssignmentForm, extra=4)
    newSubjectFormset = formset_factory(NewSubjectForm)
    if request.method == "GET":
        while True:
            key = get_random_string(6,allowed_chars=string.ascii_uppercase + string.ascii_lowercase + string.digits)
            if not Student.objects.filter(tracking_number__iexact = key).exists():
                break
        initial_data = {'predicted_performance':'Pending', 'tracking_number':key}
        form = StudentForm(initial=initial_data)
        schoolform = SchoolForm()
        formset = subjectFormset()
        newformset = newSubjectFormset(prefix='newformset')
        boole_initial = {'other_school_boole':'false'}
        student_boole_form = StudentBooles(initial=boole_initial)
        context = {
            'form': form,
            'schoolform':schoolform,
            'formset': formset,
            'newformset':newformset,
            'student_boole_form':student_boole_form,
        } 
        return render(request, "applicant/student_form.html ", context)
    else:

        #Get Main Student Form
        form = StudentForm(request.POST)

        #Get BooleForm to check if student has other school and other subjects.
        booleForm = StudentBooles(request.POST)
        
        if form.is_valid():

            #Saves Main Student Form temporarily to edit data.
            tempForm = form.save(commit=False)
            
            if booleForm.is_valid():

                #Code to add new school
                tempBooleForm = booleForm.cleaned_data
                if tempBooleForm['other_school_boole'] == 'true': #IMPORTANT! Other Value in forms.py MUST point to a valid School Object. Form won't validate otherwise.
                    schoolform = SchoolForm(request.POST)
                    if schoolform.is_valid():
                        school = schoolform.save()
                    tempForm.school = School.objects.get(pk=school.id)

                #Code to add new Subjects


            #Final Student Form added to db
            tempForm.save()


            #formset = subjectFormset(request.POST, request.FILES, instance=form)

            #Code fo Subject Assignments
            formset = subjectFormset(request.POST)
            for subjectform in formset:
                tempSubjectform = subjectform.save(commit=False)
                tempSubjectform.student = Student.objects.get(pk=tempForm.id)
                tempSubjectform.save()

            #Code for Machine Learning Model.
            loaded_model = pickle.load(open('finalized_model.sav', 'rb'))
            if loaded_model:
                columns = [
                    'school_category_numerical=1',
                    'school_category_numerical=2',
                    'school_type_numerical=1',
                    'school_type_numerical=2',
                    'school_type_numerical=3',
                    'district=1',
                    'district=2',
                    'track_numerical=1',
                    'track_numerical=2',
                    'track_numerical=3',
                    'strand_numerical=1',
                    'strand_numerical=2',
                    'strand_numerical=3',
                    'strand_numerical=4',
                    'strand_numerical=5',
                    'strand_numerical=6',
                    'strand_numerical=7',
                    'strand_numerical=8',
                    'strand_numerical=9',
                    'strand_numerical=10',
                    'english_number',
                    'english_average',
                    'math_number',
                    'math_average',
                    'science_number',
                    'science_average',
                    'sum_ems',
                    'ems_average_number',
                    'ems_average'
                ]
                df = pd.DataFrame(index=['student'],columns=columns)
                tempStudent = Student.objects.get(pk=tempForm.id)
                tempSchool = School.objects.get(pk=tempStudent.school.id)

                school_category = tempSchool.school_type
                SCHOOL_CATEGORY = [
                    "Public",
                    "Private"
                ]
                for i in range(2):
                    if school_category == SCHOOL_CATEGORY[i]:
                        df['school_category_numerical='+str(i+1)] = 1
                    else:
                        df['school_category_numerical='+str(i+1)] = 0

                school_type = tempSchool.school_category
                SCHOOL_TYPE = [
                    "University",
                    "College",
                    "School",
                    "Other",
                ]
                for i in range(3):
                    if school_type == SCHOOL_TYPE[i]:
                        df['school_type_numerical='+str(i+1)] = 1
                    else:
                        df['school_type_numerical='+str(i+1)] = 0

                school_district = tempSchool.district
                SCHOOL_DISTRICT = [
                    ("District I", "District I"),
                    ("District II","District II"),
                    ("Other","Other"),
                ]
                for i in range(2):
                    if school_district == SCHOOL_DISTRICT[i]:
                        df['district='+str(i+1)] = 1
                    else:
                        df['district='+str(i+1)] = 0

                student_strand = tempStudent.strand

                STRAND = [
                    'ABM', 
                    'STEM',
                    'HUMSS',
                    'GAS',
                    'TVL - Information Communication and Technology',
                    'TVL - Home Economics',
                    'TVL - Other',
                    'TVL - Food Related',
                    'Industrial Arts',
                    'Arts & Design / Sports',
                ]

                for i in range(10):
                    if student_strand == STRAND[i]:
                        df['strand_numerical='+str(i+1)] = 1
                    else:
                        df['strand_numerical='+str(i+1)] = 0

                student_track = ''
                if student_strand == 'ABM' or student_strand == 'STEM' or student_strand == 'HUMSS' or student_strand == 'GAS':
                    student_track = 'Academic'
                elif student_strand == 'Arts & Design / Sport':
                    student_track = 'Sports and Arts'
                else:
                    student_track = 'TVL'
                TRACK = [
                    'Academic',
                    'TVL',
                    'Sports and Arts'
                ]
                for i in range(3):
                    if student_track == TRACK[i]:
                        df['track_numerical='+str(i+1)] = 1
                    else:
                        df['track_numerical='+str(i+1)] = 0

                SUBJECT_TYPE = [
                    "English",
                    "Math",
                    "Science",
                    "Other",
                ]

                all_subjects = Subject.objects.all()
                english_subject_list = []
                math_subject_list = []
                science_subject_list = []

                for tempSubject in all_subjects:
                    if tempSubject.subject_type == 'English':
                        english_subject_list.append(tempSubject.id)
                    elif tempSubject.subject_type == 'Math':
                        math_subject_list.append(tempSubject.id)
                    elif tempSubject.subject_type == 'Science':
                        science_subject_list.append(tempSubject.id)

                student_english_grades = []
                student_math_grades = []
                student_science_grades = []
                master_subject_list = list(SubjectAssignment.objects.filter(student_id__exact = tempForm.id))
                for subject_assignment in master_subject_list:
                    if subject_assignment.subject.id in english_subject_list: #Risky subject.id | I want to try subject_assignment.subject.type == 'English'
                        student_english_grades.append(subject_assignment.value)
                    elif subject_assignment.subject.id in math_subject_list:
                        student_math_grades.append(subject_assignment.value)
                    elif subject_assignment.subject.id in science_subject_list:
                        student_science_grades.append(subject_assignment.value)

                english_total = 0
                for i in range(0, len(student_english_grades)):
                    english_total = english_total + int(student_english_grades[i])
                if len(student_english_grades) != 0:
                    english_average = english_total / len(student_english_grades)
                else:
                    english_average = 0
                    
                math_total = 0
                for i in range(0, len(student_math_grades)):
                    math_total = math_total + int(student_math_grades[i])
                if len(student_math_grades) != 0:
                    math_average = math_total / len(student_math_grades)
                else:
                    math_average = 0

                science_total = 0
                for i in range(0, len(student_science_grades)):
                    science_total = science_total + int(student_science_grades[i])
                if len(student_science_grades) != 0:
                    science_average = science_total / len(student_science_grades)
                else:
                    science_average = 0

                sum_ems = len(student_english_grades) + len(student_math_grades) + len(student_science_grades)
                ems_average_number = sum_ems / 3
                ems_average = (english_average + math_average + science_average) / 3

                df['english_number'] = len(student_english_grades)
                df['english_average'] = english_average
                df['math_number'] = len(student_math_grades)
                df['math_average'] = math_average
                df['science_number'] = len(student_science_grades)
                df['science_average'] = science_average
                df['sum_ems'] = sum_ems
                df['ems_average_number'] = ems_average_number
                df['ems_average'] = ems_average

                X = df
                prediction = loaded_model.predict(X)
                tempStudent.predicted_performance = prediction[0]
                tempStudent.save()

                return render(request, "subject/subject_list.html ")

        schoolform = SchoolForm()
        formset = subjectFormset()
        return render(request, "applicant/student_form.html ", {'form':form, 'schoolform':schoolform,'formset':formset})
