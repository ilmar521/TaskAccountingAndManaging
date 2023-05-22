const variantDropdown = document.getElementById('variantDropdown');
variantDropdown.value = 'main'

document.addEventListener('DOMContentLoaded', function () {
  var makeReportBtn = document.getElementById('makeReportBtn');
  makeReportBtn.addEventListener('click', sendReportRequest);
});

function toggleProject() {
  var projectRow = this.parentNode.parentNode;
  var nextRow = projectRow.nextElementSibling;

  while (nextRow && !nextRow.classList.contains('project-row') && !nextRow.classList.contains('total-row')) {
    if (nextRow.classList.contains('task-row')) {
      if (nextRow.classList.contains('hidden')) {
        nextRow.classList.remove('hidden');
      } else {
        nextRow.classList.add('hidden');
      }
    }
    nextRow = nextRow.nextElementSibling;
  }

  if (projectRow.classList.contains('collapsed')) {
    projectRow.classList.remove('collapsed');
    this.textContent = '-';
  } else {
    projectRow.classList.add('collapsed');
    this.textContent = '+';
  }
}

function toggleUser() {
  var userRow = this.parentNode.parentNode;
  var nextRow = userRow.nextElementSibling;

  while (nextRow && !nextRow.classList.contains('user-row')) {
    if (nextRow.classList.contains('project-row')) {
      if (nextRow.classList.contains('hidden')) {
        nextRow.classList.remove('hidden');
      } else {
        nextRow.classList.add('hidden');
      }

      var nextRowTask = nextRow.nextElementSibling;
      while (nextRowTask && !nextRowTask.classList.contains('project-row') && !nextRowTask.classList.contains('user-row')  && !nextRowTask.classList.contains('total-row')) {
        if (nextRowTask.classList.contains('task-row')) {
          if (nextRow.classList.contains('hidden')) {
            nextRowTask.classList.add('hidden');
          } else {
            if (nextRow.classList.contains('collapsed')) {
              nextRowTask.classList.add('hidden'); 
            } else { 
              nextRowTask.classList.remove('hidden');   
            }         
          }  
        }
        nextRowTask = nextRowTask.nextElementSibling;     
      }
    }
    nextRow = nextRow.nextElementSibling;
  }

  if (userRow.classList.contains('collapsed')) {
    userRow.classList.remove('collapsed');
    this.textContent = '-';
  } else {
    userRow.classList.add('collapsed');
    this.textContent = '+';
  }
}

function sendReportRequest() {
  var userDropdown = document.getElementById('userDropdown');
  var statusCheckboxes = document.querySelectorAll('input[name="status[]"]:checked');
  var variantDropdown = document.getElementById('variantDropdown');

  var selectedUserId = '';
  if (document.getElementById('userDropdown')) {
    selectedUserId = userDropdown ? userDropdown.value : '';
  } else {
    selectedUserId = 'none';
  }
  var selectedStatuses = Array.from(statusCheckboxes, function (checkbox) {
    return checkbox.value;
  });
  var selectedVariant = variantDropdown ? variantDropdown.value : '';

  if (selectedUserId === 'Select User' || !selectedUserId || !selectedVariant || selectedStatuses.length === 0) {
    var errorMessage = document.getElementById('error-message');
    errorMessage.textContent = 'Please fill in all the required fields.';
    errorMessage.style.display = 'block';
    return;
  }

  var errorMessage = document.getElementById('error-message');
  errorMessage.textContent = '';
  errorMessage.style.display = 'none';

  var data = {
    user_id: selectedUserId,
    statuses: selectedStatuses,
    variant: selectedVariant
  };

  fetch(`/task_execution_report/${selectedVariant}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
    .then(response => response.text())
    .then(tableHtml => {
      var reportArea = document.getElementById('report_area');
      reportArea.innerHTML = tableHtml;
    })
    .catch(error => {
      console.error('Error:', error);
    });
}