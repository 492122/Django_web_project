$('.post-check').click(function (ev) {
    var box = $(this);
    var id = box.val();
    var status = box.prop('checked');
    $.ajax('/app/check/', {
        method: 'POST',
        data: {
            id: id,
            status: status ? "True" : "False",
        }
    }).done(function (data) {
        document.getElementById(id).classList.add('correct');
        $('.check-block').hide();
    })

});


