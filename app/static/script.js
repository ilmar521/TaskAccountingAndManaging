
let input = document.querySelectorAll('input.btn-check');
let tasks = document.querySelectorAll('.task');
let statuses = document.querySelectorAll('.status');

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
        let box = document.getElementById(id)
        alert('We did it! ID ' + id)
    })
});