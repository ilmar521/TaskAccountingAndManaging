
function addUser() {
  var userSelect = document.getElementById("user-select");
  var userTable = document.getElementById("user-table");
  var userId = userSelect.value;
  var userName = userSelect.options[userSelect.selectedIndex].text;

  var userRows = userTable.getElementsByTagName("tr");
  for (var i = 0; i < userRows.length; i++) {
    if (userRows[i].getAttribute("data-id") == userId) {
      return;
    }
  }

  var newRow = document.createElement("tr");
  newRow.setAttribute("data-id", userId);
  newRow.innerHTML = "<td>" + userName + "</td>" +
    "<td><button  type='button' class='btn btn-danger' onclick='deleteRow(" + userId + ")'>X</button></td>";
  userTable.appendChild(newRow);
}

function deleteRow(id) {
  var row = document.querySelector("tr[data-id='" + id + "']");
  if (row) {
    row.parentNode.removeChild(row);
  }
}

function openFile(fileId, prj) {
  var path = prj ? "open_prj" : "open";
  window.open(`/${path}/` + fileId, '_blank');
}

function downloadFile(fileId, prj) {
  var path = prj ? "download_prj" : "download";
  window.location.href = `/${path}/${fileId}`
}

function deleteFile(fileId, prj) {
  var result = confirm('Are you sure?');
  if (result) {
    var path = prj ? "delete_prj_file" : "delete_file";
    $.post(`/${path}/${fileId}`, function (response) {
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

    var fileInput = document.getElementById('file-input');
    fileInput.value = null;
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

function handleChange(event) {
  var form = document.getElementById('main_form');
  var formData = new FormData(form);

  fetch(`/change_task_area`, {
    method: 'POST',
    body: formData,
  })
    .then(response => response.text())
    .then(tableHtml => {
      var reportArea = document.getElementById('task_area');
      reportArea.innerHTML = tableHtml;
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

$(document).ready(function () {
  $('#main_form').on('click', '.btn_edit_task', function (event) {
    event.preventDefault();
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
            handleChange(event);
          }
        })
      });

      $('#delete_task').click(function (event) {
        event.preventDefault();
        result = confirm('Are you sure?');
        if (result) {
          $.post(`/delete_task/${id_task}`, function (data) {
            $("#Modal_layout_task").modal('hide');
            handleChange(event);
          });
        }
      })
    })
  });

  $('#main_form').on('click', '.btn_edit_prj', function (event) {
    event.preventDefault();
    var url = $(this).data('whatever');
    var id_prj = $(this).data('id');
    $.ajaxSetup({ cache: false });
    $('#Modal_layout_prj').off('hidden.bs.modal');
    $.get(url, function (data) {
      $('#Modal_layout_prj .modal-content').html(data);
      $('#Modal_layout_prj').modal('show');
      $("#Modal_layout_prj").on('hidden.bs.modal', function (e) {
        var formData = $('#ModalForm_edit_project').serialize();
        $('#user-table tr').each(function () {
          var rowId = $(this).attr('data-id');
          formData += '&user_ids[]=' + parseInt(rowId);
        });
        $.post(url, data = formData, function (data) {
          if (data.status == 'updated') {
            handleChange(event);
          }
        }, 'json');
      });
      $('#delete_project').click(function (event) {
        event.preventDefault();
        result = confirm('Are you sure? All tasks included in this project will also be deleted.');
        if (result) {
          $.post(`/delete_project/${id_prj}`, function (data) {
            $("#Modal_layout_prj").modal('hide');
            handleChange(event);
          });
        }
      })
    })
  });

});

function startDragTask(event) {
  event.dataTransfer.setData('id', event.target.id);
}

function dragOverTask(event) {
  event.preventDefault();
}

function dropTask(event) {
  event.preventDefault();
  let id = event.dataTransfer.getData("id");
  $.post(`/change_status/${id}/${event.target.id}`);
  setTimeout(function () {
    handleChange(event);
  }, 10);
}

function addTask(event) {
  addTaskMain();
}

function handleKeyDown(event) {
  if (event.key === 'Enter') {
    event.preventDefault();
    addTaskMain();
  }
}

function addTaskMain() {
  var form = document.getElementById('main_form');
  var formData = new FormData(form);

  fetch(`/add_task`, {
    method: 'POST',
    body: formData,
  })
    .then(response => response.text())
    .then(tableHtml => {
      var reportArea = document.getElementById('task_area');
      reportArea.innerHTML = tableHtml;
    })
    .catch(error => {
      console.error('Error:', error);
    });
}