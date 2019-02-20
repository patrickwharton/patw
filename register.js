alert('It works!');

let validuser ='';
let inn = document.querySelector('#in');
let co = document.querySelector('#co');
let pw = document.querySelector('#pw');

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
    else
    {
        $('#2').show();
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
