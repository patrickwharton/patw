
let pw = document.querySelector('#password');
let em = document.querySelector('#email');

document.getElementById("button").addEventListener("click", function(event){
    event.preventDefault();
    if (pw.value.length > 0 && em.value.length > 0)
    {
        document.getElementById("form").submit();
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
    if (em.value.length > 0)
    {
        // ALERT must enter an email
        $('#5').hide();
    }
};
