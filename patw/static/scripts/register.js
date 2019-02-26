let validuser ='';
let validemail ='0';
let inn = document.querySelector('#username');
let co = document.querySelector('#confirm_password');
let pw = document.querySelector('#password');
let em = document.querySelector('#email');

document.getElementById("button").addEventListener("click", function(event){
    event.preventDefault();
    if (validemail == true && validuser == true && pw.value.length > 0 && pw.value == co.value)
    {
        document.getElementById("form").submit();
    }
        if (inn.value.length < 2 || inn.value.length > 20)
        {
            // show must provide username
            $('#4').show();
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
        if (co.value.length == 0 && pw.value.length != 0)
        {
            // show passwords must match
            $('#3').show();
        }
});

inn.onkeyup = function() {
    if (inn.value.length >= 2 && inn.value.length <= 20)
    {
        // hide please choose username
        $('#4').hide();
        $.get('/check?username=' + inn.value, function(data) {
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

pw.onkeyup = function() {
    if (pw.value.length > 0)
    {
        // ALERT must enter a password
        $('#2').hide();
    }
};

em.onkeyup = function() {
    if (em.value.length > 0)
    {
        // ALERT must enter an email
        $('#5').hide();
        $('#7').hide();
        $.get('/checkemail?email=' + em.value, function(data) {
            validemail = data;

            if (validemail == true)
            {
                $('#6').hide();
            }
            else if (validemail == '2')
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

co.onkeyup = function() {
    if (pw.value != co.value)
    {
        // ALERT passwords must match
        $('#3').show();
    }
    else
    {
      $('#3').hide();
    }
};
