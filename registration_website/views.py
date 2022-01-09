from django.forms.formsets import formset_factory
from django.shortcuts import render, redirect
from numpy import object_
from registration_website.forms import CollegeForm, ExaminationForm, ExaminationVenueAssignmentForm, NewSubjectForm, SearchStatusForm, SignUpForm, StudentBooles, StudentForm, SubjectAssignmentForm, SubjectForm, SchoolForm, VenueBooleForm, VenueForm
from .models import SCHOOL_TYPE, College, Examination, ExaminationVenueAssignment, Subject, SubjectAssignment, Student, School, Venue
from django.forms import modelformset_factory, formset_factory, inlineformset_factory
from django.utils.crypto import get_random_string
import string, pickle
import pandas as pd
#import datetime
from datetime import datetime, timedelta, date

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User

# Create your views here.
def home(request):
    return render(request,'home.html')

@login_required
def user_form(request):
    if not request.user.is_superuser:
            return redirect('permission_redirect')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            my_group = Group.objects.get(name='TEC_User') 
            my_group.user_set.add(user)
            return redirect('home')
    else:
        form = SignUpForm()
        
    return render(request, 'user/user_form.html', {'form': form})

@login_required
def user_list(request):
    if not request.user.is_superuser:
            return redirect('permission_redirect')
    users = User.objects.filter(groups__name='TEC_User')
    context = {
        'users':users
    }
    return render(request, 'user/user_list.html', context)

@login_required
def user_view(request,id=0):
    if not request.user.is_superuser:
            return redirect('permission_redirect')
    user = User.objects.get(pk=id)
    context = {
        'user':user
    }
    return render(request, 'user/user_list.html', context)

@login_required
def user_edit(request):
    user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        form = SignUpForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            #my_group = Group.objects.get(name='TEC_User') 
            #my_group.user_set.add(user)
            return redirect('home')
    else:
        form = SignUpForm(instance=user)

    return render(request, 'user/user_form.html', {'form': form})

@login_required
def user_admin_edit(request,id=0):
    if not request.user.is_superuser:
            return redirect('permission_redirect')
    user = User.objects.get(pk=id)
    if request.method == 'POST':
        form = SignUpForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            #update_session_auth_hash(request, user)
            #username = form.cleaned_data.get('username')
            #raw_password = form.cleaned_data.get('password1')
            #user = authenticate(username=username, password=raw_password)
            #my_group = Group.objects.get(name='TEC_User') 
            #my_group.user_set.add(user)
            return redirect('home')
    else:
        form = SignUpForm(instance=user)

    return render(request, 'user/user_form.html', {'form': form})

def user_permission_redirect(request):
    return render(request, 'permission_warning.html')

@login_required
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

@login_required
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

@login_required
def subject_list(request):
    subject_objects = Subject.objects.all
    context = {
        'subject_list': subject_objects
    }
    return render(request, "subject/subject_list.html ", context)

@login_required
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

@login_required
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

@login_required
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
        formset = subjectFormset(prefix='subject_formset')
        newformset = newSubjectFormset(prefix='newsubject_formset')
        boole_initial = {'other_school_boole':'false', 'other_subject_boole':'false'}
        student_boole_form = StudentBooles(initial=boole_initial)
        context = {
            'form': form,
            'schoolform':schoolform,
            'formset': formset,
            'newformset':newformset,
            'student_boole_form':student_boole_form,
        } 
        return render(request, "applicant/student_form.html", context)

    else:
        #Get Main Student Form
        form = StudentForm(request.POST)

        #Get BooleForm to check if student has other school and other subjects.
        booleForm = StudentBooles(request.POST)
        
        if form.is_valid():

            #Saves Main Student Form temporarily to edit data.
            tempForm = form.save(commit=False)

            tempBooleForm = {}
            if booleForm.is_valid():

                #Code to add new school
                tempBooleForm = booleForm.cleaned_data
                #IMPORTANT! Other Value in forms.py MUST point to a valid School Object. Form won't validate otherwise.
                if tempBooleForm['other_school_boole'] == 'true': 
                    schoolform = SchoolForm(request.POST)
                    if schoolform.is_valid():
                        school = schoolform.save()
                    tempForm.school = School.objects.get(pk=school.id)

            #Assign Student to Exam
            examinations = Examination.objects.filter(exam_date__gt = date.today())
            print('PRE EXAM LOOP')
            for exam in examinations:
                print('EXAM')
                ExamVenues = exam.examination_venues.all()
                for exam_venue in ExamVenues:
                    print('EXAM VENUE')
                    if exam_venue.current_examinees < exam_venue.max_examinees:
                        tempForm.examination_assignment = exam_venue
                        exam_venue.current_examinees = exam_venue.current_examinees + 1
                        exam_venue.save()
                        break
                else:
                    continue
                break

            #Final Student Form added to db
            tempForm.save()

            #Code to add new Subjects
            if tempBooleForm['other_subject_boole'] == 'true':
                newformset = newSubjectFormset(request.POST, request.FILES, prefix='newsubject_formset')
                for newSubjectform in newformset:
                    if newSubjectform.is_valid():
                        tempNewSubjectform = newSubjectform.cleaned_data
                        newSubject = SubjectForm(tempNewSubjectform)
                        tempNewSubject = newSubject.save()
                        tempNewSubjectform['subject'] = tempNewSubject.id
                        tempNewSubjectform['student'] = tempForm.id
                        newSubjectAssignment = SubjectAssignmentForm(tempNewSubjectform)
                        if newSubjectAssignment.is_valid():
                            tempNewSubjectAssignment = newSubjectAssignment.save(commit=False)
                            tempNewSubjectAssignment.student = Student.objects.get(pk=tempForm.id)
                            tempNewSubjectAssignment.save()

            #formset = subjectFormset(request.POST, request.FILES, instance=form)

            #Code fo Subject Assignments
            formset = subjectFormset(request.POST, request.FILES, prefix='subject_formset')
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

                return redirect('/registration/view/'+tempStudent.tracking_number)
                

        schoolform = SchoolForm()
        formset = subjectFormset()
        return render(request, "applicant/student_form.html", {'form':form, 'schoolform':schoolform,'formset':formset})

def student_search(request):
    if request.method == 'GET':
        form = SearchStatusForm()
        return render(request,"applicant/student_search.html",{'form':form})
    else:
        form = SearchStatusForm(request.POST)
        if form.is_valid():
            key = request.POST['tracking_number']
            return redirect('/registration/view/'+key)

def student_view(request, key=0):
    if key != 0:
        student = [
            Student.objects.get(tracking_number = key)
            #Student.objects.filter(tracking_number__iexact = key).first(),
        ]
        exam_assignment = ExaminationVenueAssignment.objects.get(pk=student[0].examination_assignment.id)
        exam_venue = [
           student[0].examination_assignment.venue
        ]
        examination = [
            exam_assignment.examination
        ]
        context = {
            'student':student,
            'examination':examination,
            'exam_venue':exam_venue
        }
        return render(request,"applicant/student_view.html",context)
    return #

@login_required
def student_list(request):
    student = Student.objects.all()
    context = {
        'student_list':student,
    }
    return render(request,"applicant/student_list.html",context)

@login_required
def student_admin_view(request, id=0):
    student = Student.objects.get(pk=id)
    grades = student.grades.all()
    context = {
        'student':student,
        'grades':grades
    }
    return render(request,"applicant/student_admin_view.html",context)

@login_required
def examination_form(request):
    
    if request.method == 'GET':
        form = ExaminationForm()
        #venues = Venue.objects.filter().values()
        venue_objects =  Venue.objects.all()
        venues = venue_objects.values()
        venue_ids = [a_dict['id'] for a_dict in venues]
        id_dicts = []
        for id in venue_ids:
            id_dicts.append({'venue':id})
        temp_formset = formset_factory(ExaminationVenueAssignmentForm,extra=0)
        venue_formset = temp_formset(initial=id_dicts,prefix='venue_formset')

        temp2_formset = formset_factory(VenueBooleForm, extra=0)
        boole_initial = []
        for i in range(len(id_dicts)):
            boole_initial.append({'venue_boole':'false'})
        venueBoole_formset = temp2_formset(initial=boole_initial,prefix='venueBoole_formset')
        
        row_ids = []
        for i in range(len(id_dicts)):
            row_ids.append(i)

        formsets = zip(venue_formset, venueBoole_formset, venue_objects, row_ids)
        return render(request,"examination/examination_form.html",{'form':form, 'formsets':formsets, 'ext_venue_formset':venue_formset,'ext_venueBoole_formset':venueBoole_formset})
    
    else:
        temp_formset = formset_factory(ExaminationVenueAssignmentForm)
        temp2_formset = formset_factory(VenueBooleForm)
        form = ExaminationForm(request.POST)
        if form.is_valid(): #Checks for Sched Conflicts
            duration = 4 # No. of Hrs. per Exam
            set_date = form.cleaned_data.get('exam_date')
            set_time = form.cleaned_data.get('exam_time') #
            set_temp_datetime_delta = datetime.combine(date.today(),set_time) + timedelta(hours = duration)
            set_end = set_temp_datetime_delta.time() #
            #set_test_center = form.cleaned_data.get('test_center_code')
            #set_room = form.cleaned_data.get('room_id')
            all_upcoming_examination_same_room = Examination.objects.filter(exam_date__exact = set_date)
            for exam in all_upcoming_examination_same_room:
                old_start = exam.exam_time
                old_temp_datetime_delta = datetime.combine(date.today(),old_start) + timedelta(hours = duration)
                old_end = old_temp_datetime_delta.time()
                if (set_time >= old_start and set_time < old_end) or (set_end >= old_start and set_end < old_end):

                    venue_objects =  Venue.objects.all()
                    venues = venue_objects.values()
                    venue_ids = [a_dict['id'] for a_dict in venues]
                    id_dicts = []
                    for id in venue_ids:
                        id_dicts.append({'venue':id})
                    temp_formset = formset_factory(ExaminationVenueAssignmentForm,extra=0)
                    venue_formset = temp_formset(initial=id_dicts,prefix='venue_formset')
                    temp2_formset = formset_factory(VenueBooleForm, extra=0)
                    boole_initial = []
                    for i in range(len(id_dicts)):
                        boole_initial.append({'venue_boole':'false'})
                    venueBoole_formset = temp2_formset(initial=boole_initial,prefix='venueBoole_formset')
                    row_ids = []
                    for i in range(len(id_dicts)):
                        row_ids.append(i)
                    formsets = zip(venue_formset, venueBoole_formset, venue_objects, row_ids)

                    return render(request,"examination/examination_form.html",{'form':form, 'exam':exam, 'formsets':formsets, 'ext_venue_formset':venue_formset,'ext_venueBoole_formset':venueBoole_formset})

            examination = form.save()
        venue_formset = temp_formset(request.POST, request.FILES, prefix='venue_formset')
        venue_boole_formset = temp2_formset(request.POST, request.FILES, prefix='venueBoole_formset')
        for booleFormset, formset in zip(venue_boole_formset, venue_formset):
            if booleFormset.is_valid():
                tempBooleForm = booleFormset.cleaned_data
                print(tempBooleForm)
                if tempBooleForm['venue_boole'] == 'true':
                    print('hello world!')
                    if formset.is_valid():
                        formset = formset.save(commit=False)
                        formset.examination = Examination.objects.get(pk=examination.id)
                        formset.max_examinees = examination.max_examinees
                        formset.save()

        return redirect('/registration/exam/list/')

@login_required
def examination_edit(request,id = 0):

    if request.method == 'GET':
        if id != 0:
            exam = Examination.objects.get(pk=id)
            initial = {
                'max_examinees':exam.max_examinees
            }
            form = ExaminationForm(instance=exam, initial=initial)
            exam_venues = ExaminationVenueAssignment.objects.select_related().filter(examination = exam.id)

            object_id_list = exam_venues.values_list('venue_id', flat=True)
            #object_id_list = object_id_list.values_list('id',flat=True)
            venue_objects =  Venue.objects.filter().exclude(id__in = object_id_list)
            venues = venue_objects.values()
            venue_ids = [a_dict['id'] for a_dict in venues]
            id_dicts = []
            for id in venue_ids:
                id_dicts.append({'venue':id})
            temp_formset = formset_factory(ExaminationVenueAssignmentForm,extra=0)
            venue_formset = temp_formset(initial=id_dicts,prefix='venue_formset')
            temp2_formset = formset_factory(VenueBooleForm, extra=0)
            boole_initial = []
            for i in range(len(id_dicts)):
                boole_initial.append({'venue_boole':'false'})
            venueBoole_formset = temp2_formset(initial=boole_initial,prefix='venueBoole_formset')
            row_ids = []
            for i in range(len(id_dicts)):
                row_ids.append(i)
            formsets = zip(venue_formset, venueBoole_formset, venue_objects, row_ids)

            return render(request,"examination/examination_form.html",{'form':form, 'venues':exam_venues, 'formsets':formsets, 'ext_venue_formset':venue_formset,'ext_venueBoole_formset':venueBoole_formset})

    else:
        temp_formset = formset_factory(ExaminationVenueAssignmentForm)
        temp2_formset = formset_factory(VenueBooleForm)
        old_exam = Examination.objects.get(pk=id)
        form = ExaminationForm(request.POST, instance=old_exam)
        if form.is_valid(): #Checks for Sched Conflicts
            duration = 4 # No. of Hrs. per Exam
            set_date = form.cleaned_data.get('exam_date')
            set_time = form.cleaned_data.get('exam_time') #
            set_temp_datetime_delta = datetime.combine(date.today(),set_time) + timedelta(hours = duration)
            set_end = set_temp_datetime_delta.time() #
            #set_test_center = form.cleaned_data.get('test_center_code')
            #set_room = form.cleaned_data.get('room_id')
            all_upcoming_examination_same_room = Examination.objects.filter(exam_date__exact = set_date).exclude(id__iexact = id)
            for exam in all_upcoming_examination_same_room:
                old_start = exam.exam_time
                old_temp_datetime_delta = datetime.combine(date.today(),old_start) + timedelta(hours = duration)
                old_end = old_temp_datetime_delta.time()
                if (set_time >= old_start and set_time < old_end) or (set_end >= old_start and set_end < old_end):

                    venue_objects =  Venue.objects.all()
                    venues = venue_objects.values()
                    venue_ids = [a_dict['id'] for a_dict in venues]
                    id_dicts = []
                    for id in venue_ids:
                        id_dicts.append({'venue':id})
                    temp_formset = formset_factory(ExaminationVenueAssignmentForm,extra=0)
                    venue_formset = temp_formset(initial=id_dicts,prefix='venue_formset')
                    temp2_formset = formset_factory(VenueBooleForm, extra=0)
                    boole_initial = []
                    for i in range(len(id_dicts)):
                        boole_initial.append({'venue_boole':'false'})
                    venueBoole_formset = temp2_formset(initial=boole_initial,prefix='venueBoole_formset')
                    row_ids = []
                    for i in range(len(id_dicts)):
                        row_ids.append(i)
                    formsets = zip(venue_formset, venueBoole_formset, venue_objects, row_ids)

                    return render(request,"examination/examination_form.html",{'form':form, 'exam':exam, 'formsets':formsets, 'ext_venue_formset':venue_formset,'ext_venueBoole_formset':venueBoole_formset})

            examination = form.save()

            venue_formset = temp_formset(request.POST, request.FILES, prefix='venue_formset')
            venue_boole_formset = temp2_formset(request.POST, request.FILES, prefix='venueBoole_formset')

            for booleFormset, formset in zip(venue_boole_formset, venue_formset):
                if booleFormset.is_valid():
                    print('VALID!')
                    tempBooleForm = booleFormset.cleaned_data
                    if tempBooleForm['venue_boole'] == 'true':
                        if formset.is_valid():
                            formset = formset.save(commit=False)
                            formset.examination = Examination.objects.get(pk=examination.id)
                            formset.max_examinees = examination.max_examinees
                            formset.save()

    return redirect('/registration/exam/list/')

@login_required
def examination_list(request):
    exam_objects = Examination.objects.all()
    context = {
        'exam_list': exam_objects
    }
    return render(request, "examination/examination_list.html", context)

@login_required
def examination_view(request,id=0):
    exam = Examination.objects.get(pk=id)
    venues = exam.examination_venues.all()
    students = []
    for venue in venues:
        students.append(venue.student_examinations.all())
    venues_students = zip(venues,students)
    context = {
        'exam':exam,
        'venues_students':venues_students
    }
    return render(request,"examination/examination_view.html",context)

@login_required
def college_venue_form(request,id=0):
    venue_formset = inlineformset_factory(College, Venue, fields=('room_code',), extra=1)
    if request.method == 'GET':
        if id == 0:
            form = CollegeForm()
            formset = venue_formset(prefix='venue_new')
            context = {
                'form':form,
                'new_formset':formset,
            }
        else:
            college = College.objects.get(pk=id)
            form = CollegeForm(instance=college)
            new_formset = venue_formset(prefix='venue_new')
            venue_formset = inlineformset_factory(College, Venue, fields=('room_code',), extra=0)
            formset = venue_formset(prefix='venue',instance=college)
            context = {
                'form':form,
                'formset':formset,
                'new_formset':new_formset
            }

        return render(request, "college/college_form.html", context)

    else:
        if id == 0:
            form = CollegeForm(request.POST)
            formset = venue_formset(request.POST, request.FILES, prefix='venue_new')
            if form.is_valid():
                college = form.save()
                for venue in formset:
                    if venue.is_valid():
                        venue_data = venue.cleaned_data
                        venue_data['college_code'] = college
                        venue_form = VenueForm(venue_data)
                        if venue_form.is_valid():
                            venue_form.save()

        else:
            college = College.objects.get(pk=id)
            form = CollegeForm(request.POST,instance=college)
            old_formset = venue_formset(request.POST, request.FILES, prefix='venue', instance=college)
            new_formset = venue_formset(request.POST, request.FILES, prefix='venue_new')
            if form.is_valid():
                print('POST COLLEGE ISVALID')
                college = form.save()
                print('PRE FS ISVALID')
                if old_formset.is_valid():
                    old_formset.save()
                
                for venue in new_formset:
                    if venue.is_valid():
                        venue_data = venue.cleaned_data
                        venue_data['college_code'] = college
                        venue_form = VenueForm(venue_data)
                        if venue_form.is_valid():
                            venue_form.save()
            return redirect('/registration/college/list/')
    return redirect('/registration/college/list/')

@login_required
def college_list(request):
    college_objects = College.objects.all
    context = {
        'college_list': college_objects
    }
    return render(request, "college/college_list.html", context)

@login_required
def college_view(request,id=0):
    if id != 0:
        college = College.objects.get(pk=id)
        venues = college.venues.all()
        context = {
            'college':college,
            'venues':venues,
        }
        return render(request, "college/college_view.html", context)
    return

@login_required
def student_print(request,id=0):
    student = Student.objects.get(pk=id)
    grades = student.grades.all()
    context = {
        'student':student,
        'grades':grades
    }
    return render(request,"report/student_report.html",context)

@login_required
def examination_print(request,id=0):
    exam = Examination.objects.get(pk=id)
    venues = exam.examination_venues.all()
    students = []
    for venue in venues:
        students.append(venue.student_examinations.all())
    venues_students = zip(venues,students)
    context = {
        'exam':exam,
        'venues_students':venues_students
    }
    return render(request,"report/examination_report.html",context)

@login_required
def examination_venue_print(request,id=0):
    venue = ExaminationVenueAssignment.objects.get(pk=id)
    students = venue.student_examinations.all()
    context = {
        'venue':venue,
        'students':students
    }
    return render(request,"report/venue_report.html",context)

@login_required
def user_dashboard(request):
    return render(request,"user/user_dashboard.html")
