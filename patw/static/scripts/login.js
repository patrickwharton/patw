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
              $('#invalid_email').show();
          }
      });
    }
    if (email.value.length == 0)
    {
        // show must provide email
        $('#enter_email').show();
    }
    if (password.value.length == 0)
    {
        // show please choose password
        $('#enter_password').show();
    }
});

password.onkeyup = function() {
    if (password.value.length > 0)
    {
        // ALERT must enter a password
        $('#enter_password').hide();
    }
};

email.onkeyup = function() {
    $('#invalid_email').hide();
    if (email.value.length > 0)
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
