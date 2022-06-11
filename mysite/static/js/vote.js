var questions = document.getElementsByClassName('question_id')

for (let id of questions) {
    document.getElementById("like_" + id.value).style.color = localStorage.getItem(id.value);
}

$('.js-vote').click(function (ev) {
    ev.preventDefault();
    var vote = $(this);
    var action = vote.data('action');
    var qid = vote.data('qid');
    $.ajax('/app/vote/', {
        method: 'POST',
        data: {
            action: action,
            qid: qid
        }
    }).done(function (data) {
        var ratingName = ".rating_" + qid;
        var actionName = action + "_" + qid;
        document.querySelector(ratingName).innerHTML = data['rating'];
        switch (data['status']) {
            case "0":
                document.getElementById(actionName).style.color = '';
                localStorage.setItem(qid, '');
                break;
            case "1":
                document.getElementById(actionName).style.color = 'red';
                localStorage.setItem(qid, 'red');
                break;
            default:
                break;
        }

    });
});


