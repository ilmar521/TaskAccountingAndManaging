
let input = document.querySelectorAll('input.btn-check');
let tasks = document.querySelectorAll('.task');
let statuses = document.querySelectorAll('.status');


$(document).ready(function () {
    $('.btn_edit_task').click(function () {
        var url = $(this).data('whatever');
        var id_task = $(this).data('id');
        $.get(url, function (data) {
            $('#Modal_layout_task .modal-content').html(data);
            $('#Modal_layout_task').modal('show');
            $("#Modal_layout_task").on('hidden.bs.modal', function (e) {
                $.post(url, data = $('#ModalForm_edit_task').serialize());
                $("#main_form").submit();
            });
            $('#delete_task').click(function (event) {
                event.preventDefault();
                result = confirm('Are you sure?');
                if (result) {
                    $.post(`/delete_task/${id_task}`);
                    $("#main_form").submit();
                    $("#Modal_layout_task").hide();
                }
            })


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

    $('.btn_edit_prj').click(function () {
        var url = $(this).data('whatever');
        var id_prj = $(this).data('id');
        $.get(url, function (data) {
            $('#Modal_layout_prj .modal-content').html(data);
            $('#Modal_layout_prj').modal('show');
            $("#Modal_layout_prj").on('hidden.bs.modal', function (e) {
                $.post(url, data = $('#ModalForm_edit_project').serialize());
                $("#main_form").submit();
            });
            $('#delete_project').click(function (event) {
                event.preventDefault();
                result = confirm('Are you sure? All tasks included in this project will also be deleted.');
                if (result) {
                    $.post(`/delete_project/${id_prj}`);
                    $("#main_form").submit();
                    $("#Modal_layout_prj").hide();
                }
            })
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