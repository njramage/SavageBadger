//Display login
function displayLogin() {
    //Make elements
    div = $('<div class="container" align="center">');
    username = $('<input type="text" class="form-control" placeholder = "Username" id="username" style="height: 44px;width: 300px">');
    password = $('<input type="password" class="form-control" placeholder = "Password" id="password" style="height: 44px;width: 300px">');
    submit = $('<button class="btn btn-success btn-lg btn-block" style="width: 300px;" onclick="login()">').html("Login");
    SignUp = $('<button class="btn btn-success btn-lg btn-block" style="width: 300px;" onclick="signup()">').html("Sign Up");

    //Place and display them
    div.append(username);
    div.append($('<br>'));
    div.append(password);
    div.append($('<br>'));
    div.append(submit);
    div.append($('<br>'));
    div.append(SignUp);

    $('#content').fadeOut('medium', function() {
        $('#content').html(div.html());
        $('#content').fadeIn('medium');
    });
}



//Login into website
function login() {
    
    var creds = {'Username' : $("#username").val(),'Password' : $("#password").val()};
    $.post("/login", creds, function(data){ 
        if (data["status"] == true) {
            //Redirect them to the correct page
            window.location.replace("/survey");
        } else {
            //display alert
            $("#failed").show();
            //clear password field
            $("#password").val("");
        }
    });

}

function signup()
{
       window.location='/signup/';
}



