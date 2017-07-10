/**
 * Created by Oliver on 7/2/2017.
 */





$(document).ready(function() {

    $('#Rank').bind('change', function() {
        var elements = $('div.container').children().hide(); // hide all the elements
        var value = $(this).val();

        if (value.length) { // if somethings' selected
            elements.filter('.' + value).show(); // show the ones we want
        }
    }).trigger('change');

    //
    //
    // $('.ClassCode').bind('change', function () {
    //      elementsForCode = $('div.ClassCode').children().hide(); //HIDING THE CLASS CODE DIV.
    //
    //
    //
    //
    // }).trigger('change');

    $('.second-level-select').bind('change', function() {
        var elements = $('div.second-level-container').children().hide(); // hide all the elements
        var value = $(this).val();

        if (value.length) { // if somethings' selected
            elements.filter('.' + value).show(); // show the ones we want
        }
    }).trigger('change');



});
function classCode()
{
    attendance = parseInt(document.getElementById("Attendance").value);

    var divDisplay = document.getElementById("tutorCode");
    var left = parseInt(document.getElementById("Left").value);
    var tutorSession = document.getElementById("TutorSession");
    var tutorialSession = jQuery("#Rank option:selected").val();

    var tutorial = {"tutorial": tutorialSession, "attendance":attendance, "early": left};
/// PUT IN ERROR CODE IF ATTENDANCE AND LEFT ARENT INTS.

      console.log(tutorial);

    $.ajax({
        type: 'Post',
        url: '/submitattendance/',

        data: JSON.stringify(tutorial),
        success: function (data)
        {
              console.log(data);
            var div = $('<div class = "container-fluid" id ="question" style = "padding:0;margin:0;">');
           
            var error = $('<p>').html(data["error"] );
            var code = $('<p>').html( data.code);


            div.append(div);
   
            div.append(error);
            div.append(code);

            $('#TutorT1').html(div.html());
        },
        contentType: "application/json",
        dataType: 'json'
    });

}