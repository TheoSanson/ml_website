$('#add_more').click(function() {
    cloneMore('div.table:last', 'subject_formset');
});

$('#new_add_more').click(function() {
    cloneMore('div.table-new:last', 'newsubject_formset');
});

function cloneMore(selector, type) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + type + '-TOTAL_FORMS').val();
    newElement.find(':input').each(function() {
        var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
    newElement.find('label').each(function() {
        var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
        $(this).attr('for', newFor);
    });
    total++;
    $('#id_' + type + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
}

$(document).on('click', '.remove-form-row', function (e) {
    //{#console.log(".remove-form-row click clicked");#}
    e.preventDefault();
    deleteForm('subject_formset', $(this));
    return false;
});

$(document).on('click', '.new-remove-form-row', function (e) {
    //{#console.log(".remove-form-row click clicked");#}
    e.preventDefault();
    newDeleteForm('newsubject_formset', $(this));
    return false;
});

function newDeleteForm(prefix_tag, btn) {
    //https://medium.com/all-about-django/adding-forms-dynamically-to-a-django-formset-375f1090c2b0
    //Get total number of forms counted by management form TOTAL_FORMS
    var total = parseInt($('#id_' + prefix_tag + '-TOTAL_FORMS').val());
    if(total == 1) {
        alert('Please add more subjects before deleting!');
        return false
    }

    //Remove the closests element with class form-row
    btn.closest('.new-form-row').remove();
    var forms = $('.new-form-row');
    //subtract an extra 1 to account for the hidden empty_form;
    var formlength = forms.length;
    var idstring = '#id_' + prefix_tag + '-TOTAL_FORMS';
    $(idstring).val(parseInt(formlength));
    console.log("formlength: ", formlength)
    for (var i = 0, formCount = formlength; i < formCount; i++) {
        $(forms.get(i)).find(':input').each(function () {
            updateElementIndex(this, prefix_tag, i);
        });
    }
    return false;
};

function deleteForm(prefix_tag, btn) {
    //https://medium.com/all-about-django/adding-forms-dynamically-to-a-django-formset-375f1090c2b0
    //Get total number of forms counted by management form TOTAL_FORMS
    var total = parseInt($('#id_' + prefix_tag + '-TOTAL_FORMS').val());
    if(total == 4) {
        alert('You need to input your Grade 12, 1st or 2nd Sem Grades!');
        return false
    }

    //Remove the closests element with class form-row
    btn.closest('.form-row').remove();
    var forms = $('.form-row');
    //subtract an extra 1 to account for the hidden empty_form;
    var formlength = forms.length;
    var idstring = '#id_' + prefix_tag + '-TOTAL_FORMS';
    $(idstring).val(parseInt(formlength));
    console.log("formlength: ", formlength)
    for (var i = 0, formCount = formlength; i < formCount; i++) {
        $(forms.get(i)).find(':input').each(function () {
            updateElementIndex(this, prefix_tag, i);
        });
    }
    return false;
};

function updateElementIndex(el, prefix_tag, ndx) {
    //Replace/reorder the numbers of the forms in formset#}
    //I.E. inspection_report_form-0, ... -1, ... -2 if you delete -1 then two forms are left and reorder:#}
    //inspection_report_form-0, and then inspection_report_form-2 becomes -1#}
    var id_regex = new RegExp('(' + prefix_tag + '-\\d+)');
    console.log("updateElementIndex id_regex: ", id_regex)
    var replacement = prefix_tag + '-' + ndx;
    console.log("updateElementIndex replacmenet: ", replacement)
    console.log("updateElementIndex el: ", el)
    //console.log("replacement: ", replacement);#}
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
};

// $('#test-div').click(function() {
//     fieldsetIsDisabled = document.getElementById('school-fieldset').getAttribute('disabled');
//     if(fieldsetIsDisabled != null){
//         setSchoolEnabled();
//     }
//     else{
//         setSchoolDisabled();
//     }
// });

$('#id_school').change(function() {
    var value = $("#id_school").children("option").filter(":selected").text()
    if(value == 'Other (Specify)'){
        setSchoolEnabled();
    }
    else{
        setSchoolDisabled();
    }
});

$('#new-subject-checkbox').click(function(){
    if($(this).is(':checked')){
        setNewSubjectEnabled();
    } else {
        setNewSubjectDisabled();
    }
});

function setSchoolEnabled() {
    document.getElementById('id_other_school_boole').value = true
    document.getElementById('school-fieldset').classList.remove("hidden");
    document.getElementById('school-fieldset').classList.add("show");
    document.getElementById('school-fieldset').disabled = false;
}

function setSchoolDisabled() {
    document.getElementById('id_other_school_boole').value = false
    document.getElementById('school-fieldset').classList.add("hidden");
    document.getElementById('school-fieldset').classList.remove("show");
    document.getElementById('school-fieldset').disabled = true;
}

function setNewSubjectEnabled() {
    document.getElementById('id_other_subject_boole').value = true
    document.getElementById('new-subject-fieldset').classList.remove("hidden");
    document.getElementById('new-subject-fieldset').classList.add("show");
    document.getElementById('new-subject-fieldset').disabled = false;
}

function setNewSubjectDisabled() {
    document.getElementById('id_other_subject_boole').value = false
    document.getElementById('new-subject-fieldset').classList.add("hidden");
    document.getElementById('new-subject-fieldset').classList.remove("show");
    document.getElementById('new-subject-fieldset').disabled = true;
}