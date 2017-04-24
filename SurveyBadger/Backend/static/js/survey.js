//Globals
var survey;
var answers;
var token;
var questionIndex;

$(document).ready(function(){
    startPage();
});

function getSurvey() {
    var code = $('#code').val();
    //$('#question').html('<h2>Please wait</h2>'); 
    $('#wait').toggle();
    $('#code').val("");
    //get data
    $.ajax({
            type: 'GET',
            url: '/getsurveycode/',
            beforeSend: function (xhr) {
                xhr.setRequestHeader ("Authorization", "Basic " + btoa('WEBCODE' + ":" + code));
            },
            success: function(data) {
                console.log(data);
                if (data.status == "Failed") {
                    alert("An error occured geting the survey. Please ensure the code you entered is correct");
                    $('#wait').toggle();
                    $('#code').val(code);
                } else {
                    survey = data.questions;
                    token = data.token;
                    console.log(survey);
                    //reset question index and answers
                    questionIndex = 0;
                    answers = [];
                    displayQuestion();
                }
            },
            contentType: "application/json",
            dataType: 'json'            
    });
};

function submitSurvey() {
    //Notify user that survey is being submitted
    $('#question').html('<h2>Please wait</h2>');

    //var submitData = {'token' : token, 'answers' : answers};
    var submitData = {'answers' : answers};
    console.log(submitData);
    $.ajax({
            type: 'POST',
            url: '/submitsurvey/',
            beforeSend: function (xhr) {
                xhr.setRequestHeader ("Authorization", "Basic " + btoa('SBSENT' + ":" + token));
            },
            data: JSON.stringify(submitData), 
            success: function(data) { 
                console.log(data);
                var div = $('<div class="container-fluid" id="question" style="padding:0;margin:0;">');
                var header = $('<h1>').html("Survey Submitted!");
                var logo = $('<img alt="Polavo Logo" src="../../static/images/badger.png">');
                var thank = $('<p>').html("Thank you for completing our survey! We appreicate your generosity.");
                var next = $('<a href="/">').html("Click here to fill out another survey");

                div.append(div);
                div.append(header);
                div.append(logo);
                div.append(thank);
                div.append(next);
                
                $('#question').fadeOut('slow', function() {
                    $('#question').html(div.html());
                    $('#question').fadeIn('slow');
                });
            },
            statusCode: {
                401: function() {
                    alert("Failed to submit survey results. Please try again later");
                    startPage();
                },
            },
            contentType: "application/json",
            dataType: 'json'
    });
}

function updateSliderValue() {
    //Get current and max values
    var val = parseInt($('#slide').val());
    var max = survey[questionIndex]['answers'][0];
    //Check if equal to max
    var text = '';
    if (val == max) {
        text += 'Over ';
    }
    
    if (val >= 60) {
        var hrs = Math.floor(val / 60);
        var mins = val % 60;
        text += hrs.toString()+" hour";
        if (mins != 0) {
            text += " "+mins.toString()+" minutes";
        } 
    } else {
        text += val.toString()+" minutes";
    }
    $('#sliderText').html(text); 
}

/*
 * Check if there is atleast one checkbox selected to reanable the submit button
 *
*/
function checkSelectionSubmit() {
    for (var opt in survey[questionIndex]['answers']) {
        if($("#Select"+opt).is(':checked')) {
            $('#submit').attr('disabled',false);
            return;
        }
    } 
    $('#submit').attr('disabled',true);
}


function applyEvents(type) {
    switch(survey[questionIndex]['type']) {
        case 'Time_duration':
            //Add live update for slider if any
            $('#slide').mousemove(function() {
                updateSliderValue();
            }); 
            break;
        case 'Selection':
            for (var opt in survey[questionIndex]['answers']) {
                $('#Select'+opt).click(function() {
                    checkSelectionSubmit();
                });
            }
            break; 
        default:
    }
}

function displayQuestion() {
    console.log(survey[questionIndex]['type'])
    //New div and question header
    var div = $('<div class="container-fluid" id="question" style="padding:0;margin:0;">');
    var ques = $('<h1>').html(survey[questionIndex]['question']);
    div.append(ques);
    //Submit button
    var next = $('<button class="btn" id="submit" onclick="getAnswer()" style="margin-top:20px"  >').html("Submit");
    //Determine type of question
    switch(survey[questionIndex]['type']) {
        case 'Time_duration':
            //Create slider
            var max = survey[questionIndex]['answers'][0].toString();
            var slider = $('<input id="slide" type="range" min="0" max="'+max+'" step="1" value="0">');
            var amt = $('<h2 id="sliderText">').html("0 minutes");
            div.append(amt);
            div.append(slider);
            break;
        case 'Set_time':
            var container = $('<div class="container-fluid" style="padding:0;margin:0;">'); 
            container.attr('horizontal', '');
            container.attr('layout', '');
            var hrs = $('<input type="number" id="hrs" min="1" max="12" value="9" >');
            var mins = $('<input type="number" id="minutes" min="00" max="60" value="00">');
            var apm = $('<select id="apm">');
            apm.append($('<option value="am">').html('AM'));
            apm.append($('<option value="pm">').html('PM'));
            container.append(hrs);
            container.append(mins);
            container.append(apm);
            div.append(container);
            break;
        case 'Selection':
            var container = $('<div class="container-fluid" style="padding-left:0;margin:0;">'); 
            //container.attr('horizontal', '');
            //container.attr('layout', '');
            for (var opt in survey[questionIndex]['answers']) {
                var id = 'Select'+opt;
                var val = survey[questionIndex]['answers'][opt]
                var checkopt = $('<label>').html(" "+val).prepend($('<input type="checkbox" id="'+id+'" value="'+val+'">'));
                container.append(checkopt);
                container.append($('<br/>'));
            }
            next.attr('disabled',true);
            div.append(container);
            div.append($('<br/>'));
            break;
        case 'Dollar_value':
            var entry = $('<label>').html("$").append($('<input type="number" id="entry" value="0.0">'));
            div.append(entry);
            div.append($('<br/>'));
        default:
    }
    //add Submit button
    div.append(next);

    //Display question
    $('#question').fadeOut('slow', function() {
        $('#question').html(div.html());
        $('#question').fadeIn('slow');
        //Apply any events to elements
        applyEvents(survey[questionIndex]['type']);
    });

}

function getAnswer() {
    //Create answer object
    var ans = {QuestionID : questionIndex, PersonID : 1, Result : ''};

    //Get Result based on question type 
    switch(survey[questionIndex]['type']) {
        case 'Time_duration':
            ans.Result = $('#slide').val();
            break;
        case 'Set_time':
            var hr = parseInt($('#hrs').val());
            var min = parseInt($('#minutes').val());
            //Error check
            if (isNaN(hr) || isNaN(min)) {
                return;
            }
            //check if AM or PM and convert to 24hour time
            if ($('#apm').val() == "pm") {
                hr += 12;
            }
            console.log(hr);
            //Add leading zeros and create answer string
            var ansStr = '';
            if (hr < 10) {
                ansStr += '0'+hr.toString();
            } else {
                ansStr += hr.toString();
            }

            if (min < 10) {
                ansStr += "0"+min.toString();
            } else {
                ansStr += min.toString();
            }
            ans.Result = ansStr;
            break;
        case 'Selection':
            selected = [];
            for (var opt in survey[questionIndex]['answers']) {
                if($("#Select"+opt).is(':checked')) {
                    selected.push($("#Select"+opt).val());
                }
            } 
            ans.Result = selected;
            break;
        case 'Dollar_value':
            ans.Result = "$"+$('#entry').val();
            break;
        default:
    }
    
    //Add answer to the answers list
    answers.push(ans);
    console.log(ans);
    //Update question index
    questionIndex++;
    
    //Check if the survey is complete, else display next question
    if (questionIndex == survey.length) {
        submitSurvey();
    } else {
        displayQuestion();
    }
}


function startPage() {
    var div = $('<div class="container-fluid" id="question" style="padding:0;margin:0;">');
    
    var heading = $('<h1>').html("Welcome to Povalo!");
    var instruction = $('<p>').html("Please enter the code for the survey you wish to complete");
    var wait = $('<p id="wait" hidden>').html("Please Wait");
    var codeEntry = $('<input type="text" id="code" size="20" style="font-size:28px;">');
    var button = $('<button class="btn" onclick="getSurvey()">').html("Enter");

    div.append(heading);
    div.append($('<br/>'));
    div.append(instruction);
    //div.append($('<br/>'));
    div.append(wait);
    div.append(codeEntry);
    div.append($('<br/>'));
    div.append($('<br/>'));
    div.append(button);

    $('#question').html(div); 
}
