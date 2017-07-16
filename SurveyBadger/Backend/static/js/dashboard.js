//Global constants 
var weeks = 13;
var units = [];
var intel = 0;


//Run intial setup and display
$(document).ready(function(){
    //Functions to run off start
    unitCordSetup();
});

function unitCordSetup()
{
    $.get("/getresults/", function (data) {
        try {
           //Save unit data for later
           units = data["unitData"];

           //Display the overview
           displayOverview();
        } catch(err) {
            //Else display error
            $('#status').html("An error occured getting the results. Please try again later"); 
        }
    });//End get
}//End unitCordSetup 

//Displays and overview of all the data
function displayOverview() {
    //Makes a main content div
    var main = $('<div>');


    //Loops over all the units given
    for (unitIndex in units) {

        //get unit object
        var unit = units[unitIndex];
    
        //Get the unit code as a header
        var unitHeader = $('<h1>').text(unit["Code"]);

        //make a table for storing results
        var table = $('<table>');

        //header row
        var header = $('<tr>');

        //Leave an empty cell for tutorials        
        header.append($('<th style="width:auto;white-space:nowrap;">'));

        for (var i = 1; i <= weeks; i++) {
            header.append($('<th style="width:auto;white-space:nowrap;">').html("Week "+i.toString()));
        }
        table.append(header);
        console.log(unit["Tutorials"]);
        //Loop over tutorials and make rows with results
        for (tuteIndex in unit["Tutorials"]) {
            var tute = unit["Tutorials"][tuteIndex];
            var row = $('<tr onclick="detailedTutorial(this,unitIndex)">');


            //Tutorial name
            row.append($('<td style="width:auto;white-space:nowrap;text-align:right;" ">').html(tute["ID"]));

            //Iterate over each week and generate an average score
            for (week = 0; week < weeks; week++) {
                //Check if the there is results for this tutorial for that week

                var cell = $('<td style="width:auto;white-space:nowrap;text-align:center;" >');
                if (week >= tute["Surveys"].length) {
                    cell.html("-");
                } else {
                    cell.html(getWeekScore(tute["Surveys"][week]["results"]).toString());
                }
                row.append(cell);
            }
            console.log(intel);
            
            table.append(row);
            intel++;
        } 

        //Place unit elements into the div
        main.append(unitHeader);
        main.append(table);

    }//end for
    
    //replace content div
    var mainhtml = main.html();
    $('#content').html(mainhtml);
}//End displayOverview

//displays a detailed review for each tutorial.


function detailedTutorial(intel, tut)
{
    var x = intel.rowIndex - 1;
    console.log ("what is XXx", x);


        //var unit = units[unitIndex]["Tutorials"][x];
        var unit = units[unitIndex]["Tutorials"][x];
    console.log (unit["Surveys"][0]["results"].length);
    var questionAverages = getQuestionScores(unit["Surveys"][0]["results"]);

    console.log ("question 1 score");
    console.log(questionAverages[1]);
    console.log(questionAverages[2]);
    console.log(questionAverages[3]);
    console.log(questionAverages[4]);
    console.log(questionAverages[5]);
    console.log("week 2 questions")
     questionAverages = getQuestionScores(unit["Surveys"][1]["results"]);
    console.log(questionAverages[1]);
    console.log(questionAverages[2]);
    console.log(questionAverages[3]);
    console.log(questionAverages[4]);
    console.log(questionAverages[5]);
    console.log("break again");
      console.log ("what is x", x);
    console.log ("what is Intel", intel);
    console.log("tutorial id", tut);
  //  console.log(unit);
    //console.log(unit["Surveys"][0]["Attendance"]);
   // console.log(unit["Surveys"][0]["Early_leavers"]);
   // console.log (unit["ID"]);
   // console.log(unit["Tutor"]);

    //console.log (unit);
    //console.log(units[0]);
  //  console.log (unit["ID"]);





    var main = $('<div>');
    var unitHeader = $('<h1>').text(unit["ID"]);

    var table = $('<table>');

    var header = $('<tr>');

      header.append($('<th style="width:auto;white-space:nowrap;">'));

         //for (var i = 1; i <= weeks; i++) {
            header.append($('<th style="width:auto;white-space:nowrap;">').html("Question 1"));
            header.append($('<th style="width:auto;white-space:nowrap;">').html("Question 2"));
            header.append($('<th style="width:auto;white-space:nowrap;">').html("Question 3"));
            header.append($('<th style="width:auto;white-space:nowrap;">').html("Question 4"));
            header.append($('<th style="width:auto;white-space:nowrap;">').html("Question 5"));
            header.append($('<th style="width:auto;white-space:nowrap;">').html("Attendance"));
            header.append($('<th style="width:auto;white-space:nowrap;">').html("Early Leavers"));
            header.append($('<th style="width:auto;white-space:nowrap;">').html("Tutor"));
         //}
         table.append(header);

    for (i = 0; i <= weeks; i++)
    {
        var num = i+1;

         console.log("i start " + i );
        var row = $('<tr>');

         row.append($('<td style="width:auto;white-space:nowrap;text-align:right;" ">').html("weeks" + num.toString()));

        var cell1 = $('<td style="width:auto;white-space:nowrap;text-align:center;" >');
        var cell2 = $('<td style="width:auto;white-space:nowrap;text-align:center;" >');
        var cell3 = $('<td style="width:auto;white-space:nowrap;text-align:center;" >');
        var cell4 = $('<td style="width:auto;white-space:nowrap;text-align:center;" >');
        var cell5 = $('<td style="width:auto;white-space:nowrap;text-align:center;" >');
        var cell6 = $('<td style="width:auto;white-space:nowrap;text-align:center;" >');
        var cell7 = $('<td style="width:auto;white-space:nowrap;text-align:center;" >');
        var cell8 = $('<td style="width:auto;white-space:nowrap;text-align:center;" >');
        //console.log(unit["Surveys"].length);
        if (i >= unit["Surveys"].length)
        {
            cell1.html("-");
             cell2.html("-");
             cell3.html("-");
             cell4.html("-");
             cell5.html("-");
             cell6.html("-");
             cell7.html("-");
             cell8.html("-");
        }
        //  console.log(unit["Surveys"][0]["results"].length);
       // console.log(unit["Surveys"][i-1]["results"].length);
        else
        {
           console.log("here is num"+num);
            console.log ("i before QA" + i);
             questionAverages = getQuestionScores(unit["Surveys"][i]["results"]);
                console.log ("i after QA" + i);
                cell1.html(questionAverages[1]+"/5");
                cell2.html(questionAverages[2]+"/5");
                cell3.html(questionAverages[3]+"/5");
                cell4.html(questionAverages[4]+"/5");
                cell5.html(questionAverages[5]+"/5");
                cell6.html(unit["Surveys"][i]["Attendance"]);
                cell7.html(unit["Surveys"][i]["Early_leavers"]);
                cell8.html(unit["Tutor"]);

        }
         console.log("i after " + i );
        row.append(cell1);
        row.append(cell2);
        row.append(cell3);
        row.append(cell4);
        row.append(cell5);
        row.append(cell6);
        row.append(cell7);
        row.append(cell8);

        table.append(row);

    }
    main.append(unitHeader);
    main.append(table);

    var mainhtml = main.html();
    $('#content').html(mainhtml);





}

function getQuestionScores(answers)
{
    var score = [];
    var average = [];
    for (t = 0; t <= 5; t++)
    {
        score[t] = 0;
        average[t] = 0;

    }


    for (answer in answers)
    {
        score[answers[answer]["Question"]] += Math.round(answers[answer]["Result"]);


    }

    for (total in score)
    {
       // average[total] = Math.round(score[total]/(result.length/score.length - 1))
       // console.log(score[total]);
        average[total] = Math.round(score[total]/30);
    }

    return average;

}


//Calculates the average score for a week for a particular tutorial
function getWeekScore(results) {
    var score = 0;
    var average = 0;

    for (result in results) {
        score += Math.round(results[result]["Result"]);
    }

    average = Math.round(score/results.length);
    return average;
}//End getWeekScore
