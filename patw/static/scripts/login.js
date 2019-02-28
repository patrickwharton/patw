let validemail ='';
let password = document.querySelector('#password');
let email = document.querySelector('#email');

document.getElementById("button").addEventListener("click", function(event){
    event.preventDefault();

    if (password.value.length > 0)
    {
      $.get('/checkemail?email=' + email.value, function(data) {
          validemail = data;

          if (validemail == true || validemail == 'used')
          {
              document.getElementById("form").submit();
          }
          else
          {
              $('#6').show();
          }
      });
    }
    if (email.value.length == 0)
    {
        // show must provide email
        $('#5').show();
    }
    if (password.value.length == 0)
    {
        // show please choose password
        $('#2').show();
    }
});

password.onkeyup = function() {
    if (password.value.length > 0)
    {
        // ALERT must enter a password
        $('#2').hide();
    }
};

email.onkeyup = function() {
    $('#6').hide();
    if (email.value.length > 0)
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
