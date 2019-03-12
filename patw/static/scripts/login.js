let login_validemail ='';
let login_password = document.querySelector('#login_password');
let login_email = document.querySelector('#login_email');

document.getElementById("button").addEventListener("click", function(event){
    event.preventDefault();

    if (login_password.value.length > 0)
    {
      $.get('/checkemail?email=' + login_email.value, function(data) {
          login_validemail = data;

          if (login_validemail == true || login_validemail == 'used')
          {
              document.getElementById("loginform").submit();
          }
          else
          {
              $('#invalid_email').show();
          }
      });
    }
    if (login_email.value.length == 0)
    {
        // show must provide email
        $('#enter_email').show();
    }
    if (login_password.value.length == 0)
    {
        // show please choose password
        $('#enter_password').show();
    }
});

login_password.onkeyup = function() {
    if (login_password.value.length > 0)
    {
        // ALERT must enter a password
        $('#enter_password').hide();
    }
};

login_email.onkeyup = function() {
    $('#invalid_email').hide();
    if (login_email.value.length > 0)
    {
        // ALERT must enter an email
        $('#enter_email').hide();
    }
    else
    {
        // show must provide email
        $('#enter_email').show();
    }
};
