//Global constants 
var weeks = 13;
var units = [];


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
            var row = $('<tr>');

            //Tutorial name
            row.append($('<td style="width:auto;white-space:nowrap;text-align:right;">').html(tute["ID"]));

            //Iterate over each week and generate an average score
            for (week = 0; week < weeks; week++) {
                //Check if the there is results for this tutorial for that week
                var cell = $('<td style="width:auto;white-space:nowrap;text-align:center;">'); 
                if (week >= tute["Surveys"].length) {
                    cell.html("-");
                } else {
                    cell.html(getWeekScore(tute["Surveys"][week]["results"]).toString());
                }
                row.append(cell);
            }
            
            table.append(row);
        } 

        //Place unit elements into the div
        main.append(unitHeader);
        main.append(table);

    }//end for
    
    //replace content div
    var mainhtml = main.html();
    $('#content').html(mainhtml);
}//End displayOverview

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
