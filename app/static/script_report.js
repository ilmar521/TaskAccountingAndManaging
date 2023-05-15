
document.addEventListener('DOMContentLoaded', function() {
  var toggleIcons = document.getElementsByClassName('toggle-icon');
  for (var i = 0; i < toggleIcons.length; i++) {
    toggleIcons[i].addEventListener('click', toggleProject);
  }
});

function toggleProject() {
  var projectRow = this.parentNode.parentNode;
  var nextRow = projectRow.nextElementSibling;

  while (nextRow && !nextRow.classList.contains('project-row')) {
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