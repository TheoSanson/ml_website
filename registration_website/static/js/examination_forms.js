$(document).on('click', '.venue_form_row', function (e) {
    //{#console.log(".remove-form-row click clicked");#}
    e.preventDefault();
    if($(this).hasClass('selected')){
        venueUnselect($(this));
    }
    else{
        venueSelect($(this));
    }
    return false;
});

function venueSelect(btn){
    btn.addClass('selected');
    id = btn.attr('id');
    document.getElementById('id_venueBoole_formset-'+ id +'-venue_boole').value = 'true';
}

function venueUnselect(btn){
    btn.removeClass('selected');
    id = btn.attr('id');
    document.getElementById('id_venueBoole_formset-'+ id +'-venue_boole').value = 'false';
}