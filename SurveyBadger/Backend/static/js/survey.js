var token;
var survey;
var index;
var answers;
var qID;

var IN = 700;
var OUT = 500;

var authUser = <USER>;
var authPass = <PASS>;


$(document).ready(function(){
    displayLogin();
});

function displayLogin() {
    //new div
    var div = $('<div>');

    //Introduction
    var greating = $('<h1 class="text-center">').text("Welcome to Polavo!");
    var subtext = $('<p class="text-center" style="padding-top:50px">').text("Please enter your survey code below to begin!");

    div.append(greating);
    div.append(subtext);

    //new form
    var form = $('<form action="" class="form-group" method="" style="width:300px">')
 
    //Access Code
    var surveyDiv = $('<div class="form-group" style="margin-bottom: 2px">');
    var survey = $('<input type="password" class="form-control" placeholder = "" name="survey" id="code" style="height: 44px;width: 300px">');
    surveyDiv.append(survey);
    surveyDiv.append($('<br>'));

    //Submit button
    var btn = $('<button type="button" class="btn btn-success btn-lg btn-block" onclick="getSurvey()">Start</button>');

	//Add to form
    form.append(surveyDiv);
    form.append(btn);

    div.append(form);
    
    $('#content').fadeOut(OUT, function() {
        $('#content').html(div.html());
        $('#content').fadeIn(IN);   
    });
};

function updateSlider() {
    //get slider value
    var value = $('#answer').val();
    
    //create display text
    var text;

    if (survey[index]['type'] == "Time_duration") {
        if (value == 0) {
            text = "Less than 1 Hour";
        } else if (value == 1) {
            text = "1 Hour";
        } else {
            text = value + " Hours";
        }
    } else if (survey[index]['type'] == "Dollar_value") {
        text = "$"+value;
        if (value == survey[index]['answers']) {
            text += "+";
        } 
    } else {
        text = value;
        if (value == survey[index]['answers']) {
            text += "+";
        } 
    }

    //Update value
    $('#display').text(text);

}

function checkSelection() {
    if ($('input:radio:checked').length > 0) {
        $('#submit').prop('disabled', false); 
    } else {
        $('#submit').prop('disabled', true); 
    }

}


function getSurvey() {
    //get survey code
    var surveyCode = $('#code').val();
    
    //get survey
    $.ajax
    ({
        type: "GET",
        url: "/getsurveycode/"+surveyCode,
        dataType: 'json',
        async: true,
        headers: {
            "Authorization": "Basic " + btoa(authUser + ":" + authPass)
        },
        success: function (data){
            console.log(data);
            //set token and survey
            token = data.token;
            survey = data.questions;
            
            //reset index and answers, display survey
            index = 0;
            answers = [];
            displaySurvey();
        } 
    });
};

function displaySurvey() {
    //get question from survey list
    var question = survey[index];
    qID = question['id'];

    //create div
    var div = $('<div>');

    //Add question text
    var questionText = $('<h2>').html(question['question']);

    div.append(questionText);
    div.append('<br>');

    //Check question type 
    switch(question['type']) {
        case "Time_duration":
            display = $('<p id="display" style="font-size: 24px">').text("Less than 1 Hour");
            inpt = $('<input type="range" min="0" max="'+question['answers']+'" value="0" id="answer" step="1" onchange="updateSlider()">');
            
            div.append(display);
            div.append($('<br>'));
            div.append(inpt);
            break;
        case "Set_time":
            inpt = $('<input type="time" id="answer">');
            div.append(inpt);
            div.append($('<br>'));
            break;
        case "Selection":
            div.append(createSelection(question['answers']));
            div.append($('<br>'));
            break;
        case "Dollar_value":
            display = $('<p id="display" style="font-size: 24px">').text("$0");
            inpt = $('<input type="range" min="0" max="'+question['answers']+'" value="0" id="answer" step="1" onchange="updateSlider()">');
            
            div.append(display);
            div.append($('<br>'));
            div.append(inpt);
            break;
        case "Number":
            display = $('<p id="display" style="font-size: 24px">').text("0");
            inpt = $('<input type="range" min="0" max="'+question['answers']+'" value="0" id="answer" step="1" onchange="updateSlider()">');
            
            div.append(display);
            div.append($('<br>'));
            div.append(inpt);
            break;
        default:
            break;
    }
 
    //Submit button
    var btn = $('<button type="button" id="submit" class="btn btn-lg" style="width:220px" onclick="submitAnswer()">Submit</button>');
    
    //disable button if type is selection
    if (question['type'] == "Selection") {
        btn.prop('disabled', true);
    }
    
    
    div.append($('<br>'));
    div.append(btn);
    //Change html
    $('#content').fadeOut(OUT, function() {
        $('#content').html(div.html());
        $('#content').fadeIn(IN);   
    });

};

function createSelection(values) {
    //create form
    var form = $('<form action="" onchange="checkSelection()" id="answer" >');
    
    //add values to the form
    for (var option in values) {
        var opt = $('<input type="radio" name="answer" value="'+values[option]+'">')
        var text = "   "+values[option];  
        var lbl = $('<label>').text(text);

        form.append(opt);
        form.append(lbl);
        form.append($('<br>'));
    }

    return form;
}

function submitAnswer() {
    //get answer
    var answer
    if (survey[index]['type'] == "Selection") {
        answer = $('input:radio:checked').val();
    } else {
        answer = $('#answer').val();
    }

    answers.push({'QuestionID' : qID, 'PersonID' : 2, 'Result' : answer});
    console.log(answers[index]);
    index += 1;

    //Check if end of survey
    if (index == survey.length) {
        endSurvey();
    } else {
        displaySurvey();
    }


};

function endSurvey() {
    //send res
    $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        url: "/submitsurvey/",
        data: JSON.stringify({ token : token, answers : answers }),

        success: function (data) {              
            //create div
            var div = $('<div>');
            
            //Completion message
            var greating = $('<h1 class="text-center">').text("You done!");
            var subtext = $('<p class="text-center" style="padding-top:50px">').text("Thank you for completing our survey!");

            div.append(greating);
            div.append(subtext);
            
            //Submit button
            var btn = $('<button type="button" class="btn btn-lg" style="width:220px" onclick="displayLogin()">Submit another survey</button>');
             
            div.append($('<br>'));
            div.append(btn);
            //Change html
            $('#content').fadeOut(OUT, function() {
                $('#content').html(div.html());
                $('#content').fadeIn(IN);   
            });
        },
        dataType: "json" 
    });

}
