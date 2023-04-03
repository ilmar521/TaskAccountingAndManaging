
let input = document.querySelectorAll('input');

input.forEach(element => {
    element.addEventListener('change', function () {
//     $.ajax({
//          type: 'post',
//          url: '/',
//          data: $('#main_form').serialize(),
//           success: function (q) {
//           }
//          });
//         });

//     $.post("/", $('#main_form').serialize());
     $("#main_form").submit();
    });   
});
