
let input = document.querySelectorAll('input.btn-check');
let tasks = document.querySelectorAll('.task');
let statuses = document.querySelectorAll('.status');

$(document).ready(function () {
    $('.btn_edit_task').click(function () {
        var url = $(this).data('whatever');
        $.get(url, function (data) {
            $('#Modal_layout .modal-content').html(data);
            $('#Modal_layout').modal('show');
//            $('#Modal_layout').reveal({
//                        close: function () { alert("модальное окно начинает скрываться"); },
//                        closed: function () { alert("модальное окно только что скрылось"); },
//                    });

            $("#Modal_layout").on('hidden.bs.modal', function (e) {
                $.post(url, data = $('#ModalForm_edit_task').serialize());
                $("#main_form").submit();
            });
//            $('#submit').click(function (event) {
//                event.preventDefault();
//                $.post(url, data = $('#ModalForm_edit_task').serialize(), function (
//                    data) {
//                    if (data.status == 'ok') {
//                        $('#Modal_layout').modal('hide');
//                        location.reload();
//                    } else {
//                        var obj = JSON.parse(data);
//                        for (var key in obj) {
//                            if (obj.hasOwnProperty(key)) {
//                                var value = obj[key];
//                            }
//                        }
//                        $('.help-block').remove()
//                        $('<p class="help-block">' + value + '</p>')
//                            .insertAfter('#' + key);
//                        $('.form-group').addClass('has-error')
//                    }
//                })
//            });
        })
    });
});

input.forEach(element => {
    element.addEventListener('change', function () {
     $("#main_form").submit();
    });   
});

tasks.forEach(element => {
    element.addEventListener('dragstart', function (event) {
        event.dataTransfer.setData('id', event.target.id);
    });
});

statuses.forEach(element => {
    element.addEventListener('dragover', function (event) {
        event.preventDefault();
    })

    element.addEventListener('drop', function (event) {
        event.preventDefault();
        let id = event.dataTransfer.getData("id");
        $.post(`/change_status/${id}/${event.target.id}`);
        $("#main_form").submit();
    })
});