let validuser ='';
let validemail ='0';
let username = document.querySelector('#username');
let confirm_password = document.querySelector('#confirm_password');
let password = document.querySelector('#password');
let email = document.querySelector('#email');

document.getElementById("button").addEventListener("click", function(event){
    event.preventDefault();
    if (validemail == true && validuser == true && password.value.length > 0 && password.value == confirm_password.value)
    {
        document.getElementById("form").submit();
    }
        if (username.value.length < 2 || username.value.length > 20)
        {
            // show must provide username
            $('#4').show();
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
        if (confirm_password.value.length == 0 && password.value.length != 0)
        {
            // show passwords must match
            $('#3').show();
        }
});

username.onkeyup = function() {
    if (username.value.length >= 2 && username.value.length <= 20)
    {
        // hide please choose username
        $('#4').hide();
        $.get('/check?username=' + username.value, function(data) {
            validuser = data;

            if (validuser == true)
            {
                $('#1').hide();
            }
            else
            {
                $('#1').show();
            }
        });
    }
    else
    {
      $('#4').show();
    }
};

password.onkeyup = function() {
    if (password.value.length > 0)
    {
        // ALERT must enter a password
        $('#2').hide();
    }
};

email.onkeyup = function() {
    if (email.value.length > 0)
    {
        // ALERT must enter an email
        $('#5').hide();
        $('#7').hide();
        $.get('/checkemail?email=' + email.value, function(data) {
            validemail = data;

            if (validemail == true)
            {
                $('#6').hide();
            }
            else if (validemail == 'used')
            {
                $('#7').show();
            }
            else
            {
                $('#6').show();
            }

        });
    }
    else
    {
        // show must provide email
        $('#5').show();
        $('#6').hide();
        $('#7').hide();
    }
};

confirm_password.onkeyup = function() {
    if (password.value != confirm_password.value)
    {
        // ALERT passwords must match
        $('#3').show();
    }
    else
    {
      $('#3').hide();
    }
};
