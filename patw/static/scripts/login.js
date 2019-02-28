let validemail ='';
let pw = document.querySelector('#password');
let em = document.querySelector('#email');

document.getElementById("button").addEventListener("click", function(event){
    event.preventDefault();

    if (pw.value.length > 0)
    {
      $.get('/checkemail?email=' + em.value, function(data) {
          validemail = data;

          if (validemail == true || validemail == '2')
          {
              document.getElementById("form").submit();
          }
          else
          {
              $('#6').show();
          }
      });
    }
    if (em.value.length == 0)
    {
        // show must provide email
        $('#5').show();
    }
    if (pw.value.length == 0)
    {
        // show please choose password
        $('#2').show();
    }
});

pw.onkeyup = function() {
    if (pw.value.length > 0)
    {
        // ALERT must enter a password
        $('#2').hide();
    }
};

em.onkeyup = function() {
    $('#6').hide();
    if (em.value.length > 0)
    {
        // ALERT must enter an email
        $('#5').hide();
    }
    else
    {
        // show must provide email
        $('#5').show();
    }
};
