//Run intial setup and display
$(document).ready(function(){
    //Functions to run off start
    unitCordSetup();


});

function unitCordSetup()
{




        $.get("/getresults/", function (data){

            //console.log(data[0][0]['ID']);

           //  console.log(data[0][0]);
            console.log(data);
                    console.log(data[data[0]]);
            console.log(data[data.unitData["0"]]);
            console.log(data[0]["Tutorials"][0]["ID"]);

             console.log(data['ID']);

           var div = $('<div class = "container-fluid" id ="question" style = "padding:0;margin:0;">');
            var table = $('<table>');
            var row = $('<tr>');
            var cell = $('<td>').html(data[0][0]['ID']);

            div.append(div);
            row.append(cell);
            table.append(row);

            $('#unitcord').html(div.html());
    });



}