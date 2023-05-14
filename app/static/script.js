
let input = document.querySelectorAll('input.btn-check');
let tasks = document.querySelectorAll('.task');
let statuses = document.querySelectorAll('.status');


function openFile(fileId, prj) {
    var path = prj ? "open_prj" : "open";
    window.open(`/${path}/` + fileId, '_blank');
}

function downloadFile(fileId, prj) {
    var path = prj ? "download_prj" : "download";
    window.location.href = `/${path}/${fileId}`
}

function deleteFile(fileId, prj) {
    var  result = confirm('Are you sure?');
    if (result) {
        var path = prj ? "delete_prj_file" : "delete_file";
        $.post(`/${path}/${fileId}`, function(response) {
          if (response.success) {
            var listItem = $('#file-list li[data-file-id="' + fileId + '"]');
            listItem.remove();
          }
        });
    }
}

function uploadFile(prj) {
    var formData = new FormData();
    var idTask = document.getElementById('button_upload').getAttribute('data-id-task');

    var fileInput = document.getElementById('file-input');
    formData.append('file', fileInput.files[0]);

    var path = prj ? "upload_prj" : "upload";
    var xhr = new XMLHttpRequest();
    xhr.open('POST', `/${path}/${idTask}`, true);
    xhr.onload = function () {
      var response = JSON.parse(xhr.responseText);
      var fileList = document.getElementById('file-list');
      var myHtml = `
           <li class="list-group-item d-flex justify-content-between align-items-center" data-file-id="${response.id}">
            ${response.name}
            <div class="btn-group" role="group" aria-label="File Actions">
              <button type="button" onclick="openFile(${response.id})" data-id-file="${response.id}" class="btn btn-primary"><i class="fas fa-eye"></i></button>
              <button type="button" onclick="downloadFile(${response.id})" data-id-file="${response.id}" class="btn btn-secondary"><i class="fas fa-download"></i></button>
              <button type="button" onclick="deleteFile(${response.id})"  data-id-file="${response.id}" class="btn btn-danger"><i class="fas fa-trash"></i></button>
            </div>
          </li>
      `;

      fileList.insertAdjacentHTML('beforeend', myHtml);
      $('#upload-form')[0].reset();
    };
    xhr.send(formData);
}

function addNote(prj) {
    var formData = new FormData();
    var idTask = document.getElementById('button_add_note').getAttribute('data-id-task');

    var detail = document.getElementById('input_add_note').value;
    formData.append('detail', detail);

    var xhr = new XMLHttpRequest();
    var path = prj ? "add_note_prj" : "add_note";
    xhr.open('POST', `/${path}/${idTask}`, true);
    xhr.onload = function () {
      var response = JSON.parse(xhr.responseText);
      var notesList = document.getElementById('notes_list');
      var myHtml = `
         <div class="message-item">
          <div class="message-inner">
            <div class="message-head clearfix">
              <div class="user-detail">
                <div class="post-meta">
                  <div class="asker-meta">
                    <span class="qa-message-what"></span>
                    <span class="qa-message-when">
                      <span class="qa-message-when-data">${response.date}</span>
                    </span>
                  </div>
                </div>
              </div>
            </div>
            <div class="qa-message-content">
              ${response.detail}
            </div>
          </div>
        </div>
      `;
      notesList.insertAdjacentHTML('afterbegin', myHtml);
      $('#input_add_note').val('');
    };
    xhr.send(formData);
}

$(document).ready(function () {
    $('.btn_edit_task').click(function () {
        var url = $(this).data('whatever');
        var id_task = $(this).data('id');
        $.ajaxSetup({ cache: false });
        $('#Modal_layout_task').off('hidden.bs.modal');
        $.get(url, function (data) {
            $('#Modal_layout_task .modal-content').html(data);
            $('#Modal_layout_task').modal('show');
            $("#Modal_layout_task").on('hidden.bs.modal', function (e) {
                $.post(url, data = $('#ModalForm_edit_task').serialize(), function (
                    data) {
                    if (data.status == 'updated') {
                        $("#main_form").submit();
                    }
                 })
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
        })
    });

    $('.btn_edit_prj').click(function () {
        var url = $(this).data('whatever');
        var id_prj = $(this).data('id');
        $.ajaxSetup({ cache: false });
        $('#Modal_layout_prj').off('hidden.bs.modal');
        $.get(url, function (data) {
            $('#Modal_layout_prj .modal-content').html(data);
            $('#Modal_layout_prj').modal('show');
            $("#Modal_layout_prj").on('hidden.bs.modal', function (e) {
                $.post(url, data = $('#ModalForm_edit_project').serialize(), function (
                    data) {
                    if (data.status == 'updated') {
                        $("#main_form").submit();
                    }
                 })
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
        setTimeout(() => $("#main_form").submit(), 10);
    })
});