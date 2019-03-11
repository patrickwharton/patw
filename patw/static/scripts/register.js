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
            $('#invalid_username').show();
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
        if (confirm_password.value.length == 0 && password.value.length != 0)
        {
            // show passwords must match
            $('#password_match').show();
        }
});

username.onkeyup = function() {
    if (username.value.length >= 2 && username.value.length <= 20)
    {
        // hide please choose username
        $('#invalid_username').hide();
        $.get('/check?username=' + username.value, function(data) {
            validuser = data;

            if (validuser == true)
            {
                $('#duplicate_username').hide();
            }
            else
            {
                $('#duplicate_username').show();
            }
        });
    }
    else
    {
      $('#invalid_username').show();
    }
};

password.onkeyup = function() {
    if (password.value.length > 0)
    {
        // ALERT must enter a password
        $('#enter_password').hide();
    }
};

email.onkeyup = function() {
    if (email.value.length > 0)
    {
        // ALERT must enter an email
        $('#enter_email').hide();
        $('#duplicate_email').hide();
        $.get('/checkemail?email=' + email.value, function(data) {
            validemail = data;

            if (validemail == true)
            {
                $('#invalid_email').hide();
            }
            else if (validemail == 'used')
            {
                $('#duplicate_email').show();
                $('#invalid_email').hide();
            }
            else
            {
                $('#invalid_email').show();
            }

        });
    }
    else
    {
        // show must provide email
        $('#enter_email').show();
        $('#invalid_email').hide();
        $('#duplicate_email').hide();
    }
};

confirm_password.onkeyup = function() {
    if (password.value != confirm_password.value)
    {
        // ALERT passwords must match
        $('#password_match').show();
    }
    else
    {
      $('#password_match').hide();
    }
};
