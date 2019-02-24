let validuser ='';
let inn = document.querySelector('#username');
let co = document.querySelector('#confirm_password');
let pw = document.querySelector('#password');
let em = document.querySelector('#email');

document.getElementById("button").addEventListener("click", function(event){
    event.preventDefault();
    if (validuser == true && pw.value.length > 0 && pw.value == co.value)
    {
        document.getElementById("form").submit();
    }
        if (inn.value.length == 0)
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
    if (inn.value.length > 0)
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
    }
};

co.onkeyup = function() {
    if (pw.value != co.value)
    {
        // ALERT passwords must match
        $('#3').show();
    }
};
