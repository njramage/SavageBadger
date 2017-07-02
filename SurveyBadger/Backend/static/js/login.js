//Login into website
function login() {
    
    var creds = {'Username' : $("#username").val(),'Password' : $("#password").val()};
    $.post("/login", creds, function(data){ 
        if (data["status"] == true) {
            //if the user is a UC, give them the option to login as a tutor
            if (data["choice"] == true){
                chooseLoginType();
            } else {
                //redirect
                window.location.replace("/survey");
            }
        } else {
            //display alert
            $("#failed").toggle();
            //clear password field
            $("#password").val("");
        }
    });
        
}


//Allow UC to pick login type
function chooseLoginType() {
    //New div and with choice buttons
    var div = $('<div id="content" class="container-fluid" align="center" style="margin-top: 120px">');
    var header = $('<h1>').html("Which user type would you like to use?");
    var btnText = '<btn class="btn btn-success" style="width:300px; font-size:26px; text-align:center; margin-left:50px; margin-right:50px;" onclick="submitLoginType(';
    var tutorBtn = $(btnText+'\'tutor\')">').html('Tutor');
    var ucBtn = $(btnText+'\'uc\')">').html('Unit Coordinator');
    div.append(header);
    div.append($('<br>'));
    div.append(tutorBtn);
    div.append(ucBtn);

    //hide error message if visable
    $("#failed").hide();

    //replace html
    $("#content").html(div.html());
}

//process choice
function submitLoginType(choice) {
    //unit coordinator
    if (choice == "uc") {
        window.location.replace("/dashboard");
    } else {
        $.get("/tutormode",function(data) {
            window.location.replace("/tutor");
        });
    }
}
