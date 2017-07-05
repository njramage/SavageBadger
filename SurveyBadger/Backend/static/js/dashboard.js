//Run intial setup and display
$(document).ready(function(){
    //Functions to run off start
    unitCordSetup();


});

function unitCordSetup()
{




        $.get("/getresults/", function (data){

            //console.log(data[0][0]['ID']);

            var units = data["unitData"];

            console.log(units);
            console.log(units[0]["Tutorials"]);
            console.log(units[0]["Tutorials"][0]);
            console.log(units[0]["Tutorials"][0]["ID"]);
              var sum = 0;

            var sumWk1T =0;
            var sumWk2T =0;
            var sumWk3T =0;
            var sumWk4T =0;
            var sumWk5T =0;


            console.log(sum);
            console.log(units[0]["Tutorials"][0]["Surveys"][0]["results"][1]["Result"]);
            console.log(Math.round(units[0]["Tutorials"][0]["Surveys"][0]["results"][1]["Result"]));
            console.log("break");

            // WEEK 1 TEST
            for (var i = 0; i < units[0]["Tutorials"][1]["Surveys"][0]["results"].length; i++)
            {
                sumWk1T += Math.round(units[0]["Tutorials"][1]["Surveys"][0]["results"][i]["Result"]);
               // console.log(sum);

            }

            var resultsAverage = Math.round(sumWk1T/units[0]["Tutorials"][1]["Surveys"][0]["results"].length);
            console.log(resultsAverage);


             // WEEK 2 TEST
              for (var i = 0; i < units[0]["Tutorials"][1]["Surveys"][1]["results"].length; i++)
            {
                sumWk2T += Math.round(units[0]["Tutorials"][1]["Surveys"][1]["results"][i]["Result"]);
               // console.log(sum);

            }
            var resultsAverage = Math.round(sumWk2T/units[0]["Tutorials"][1]["Surveys"][1]["results"].length);
            console.log(resultsAverage);

            //WEEK 3 TEST
            for (var i = 0; i < units[0]["Tutorials"][1]["Surveys"][2]["results"].length; i++)
            {
                sumWk3T += Math.round(units[0]["Tutorials"][1]["Surveys"][2]["results"][i]["Result"]);
               // console.log(sum);

            }

            var resultsAverage = Math.round(sumWk3T/units[0]["Tutorials"][1]["Surveys"][2]["results"].length);
            console.log(resultsAverage);


            // WEEK 4 TEST
            for (var i = 0; i < units[0]["Tutorials"][1]["Surveys"][3]["results"].length; i++)
            {
                sumWk4T += Math.round(units[0]["Tutorials"][1]["Surveys"][3]["results"][i]["Result"]);
               // console.log(sum);

            }

            var resultsAverage = Math.round(sumWk4T/units[0]["Tutorials"][1]["Surveys"][3]["results"].length);
            console.log(resultsAverage);
            console.log("break");




         


           var div = $('<div class = "container-fluid" id ="question" style = "padding:0;margin:0;">');


            //var table = $('<table>');
            //
            // var row = $('<tr>');
            // var row2 = $('<tr>');
            // var cell = $('<td>').html(units[0]["Tutorials"][0]["ID"]);
            // var cell2 = $('<td>').html(units[0]["Tutorials"][0]["Surveys"][0]["results"].length);
            // var cell3 = $('<td>').html(resultsAverage);
            // console.log(resultsAverage);
            //figuring out a way to make more rows then having to type out 43 rows.


          //  var message = $('<p>').html( units[0]["Tutorials"][0]["ID"]);
           // var message2 = $('<p>').html("hello there");

            // var table = '';
            // var rows = 3
            // var cols = 3;
            // for (var r = 0; r < rows; r++)
            // {
            //     table += '<tr>';
            //     for (var c = 0; c < cols; c++)
            //     {
            //         table += '<td>' + c + '</td>'
            //
            //     }
            //
            //
            //     table += '</tr>';
            // }





            var tableBody = '';
            console.log("tutorial");
            console.log(units[0]["Tutorials"].length);
            var rows = 5;

            var cols = 1;
            for (var r = 0; r < rows; r++)
            {
                var sumWk1 =0;
                var sumWk2 =0;
                var sumWk3 =0;
                var sumWk4 =0;
                var sumWk5 =0;
                tableBody +='<tr>';
                for (var c = 0; c < cols; c++) //tutorial name
                {
                    tableBody += '<td style="padding:0 15px 0 15px;">' + units[0]["Tutorials"][r]["ID"] + '</td>';
                   // tableBody += '<td>' + units[0]["Tutorials"][c]["Surveys"][c]["results"].length + '</td>';
                 //   tableBody += '<td>' + resultsAverage + '</td>';


                }


                for (var c = 0; c < cols; c++) //week 1 results
                {
                        for (var i = 0; i < units[0]["Tutorials"][r]["Surveys"][0]["results"].length; i++)
                        {
                            sumWk1 += Math.round(units[0]["Tutorials"][r]["Surveys"][0]["results"][i]["Result"]);


                        }
                    var resultsAverageWk1 = Math.round(sumWk1/units[0]["Tutorials"][r]["Surveys"][0]["results"].length);
                    tableBody += '<td style="padding:0 15px 0 15px;">' + resultsAverageWk1  + '/5'+  '</td>';
                }

                for (var c = 0; c < cols; c++) //week 2 results
                {
                        for (var i = 0; i < units[0]["Tutorials"][r]["Surveys"][1]["results"].length; i++)
                        {
                            sumWk2 += Math.round(units[0]["Tutorials"][r]["Surveys"][1]["results"][i]["Result"]);


                        }
                    var resultsAverageWk2 = Math.round(sumWk2/units[0]["Tutorials"][r]["Surveys"][1]["results"].length);
                    tableBody += '<td style="padding:0 15px 0 15px;">' + resultsAverageWk2  + '/5'+  '</td>';
                }

                for (var c = 0; c < cols; c++) //week 3 results
                {
                        for (var i = 0; i < units[0]["Tutorials"][r]["Surveys"][2]["results"].length; i++)
                        {
                            sumWk3 += Math.round(units[0]["Tutorials"][r]["Surveys"][2]["results"][i]["Result"]);


                        }
                    var resultsAverageWk3 = Math.round(sumWk3/units[0]["Tutorials"][r]["Surveys"][2]["results"].length);
                    tableBody += '<td style="padding:0 15px 0 15px;">' + resultsAverageWk3  + '/5'+  '</td>';
                }

                for (var c = 0; c < cols; c++) //week 4 results
                {
                        for (var i = 0; i < units[0]["Tutorials"][r]["Surveys"][3]["results"].length; i++)
                        {
                            sumWk4 += Math.round(units[0]["Tutorials"][r]["Surveys"][3]["results"][i]["Result"]);


                        }
                    var resultsAverageWk4 = Math.round(sumWk4/units[0]["Tutorials"][r]["Surveys"][3]["results"].length);
                    tableBody += '<td style="padding:0 15px 0 15px;">' + resultsAverageWk4 + '/5'+  '</td>';
                }

                for (var c = 0; c < cols; c++) //week 5 results
                {
                        for (var i = 0; i < units[0]["Tutorials"][r]["Surveys"][4]["results"].length; i++)
                        {
                            sumWk5 += Math.round(units[0]["Tutorials"][r]["Surveys"][4]["results"][i]["Result"]);


                        }
                    var resultsAverageWk5 = Math.round(sumWk5/units[0]["Tutorials"][r]["Surveys"][4]["results"].length);
                    tableBody += '<td style="padding:0 15px 0 15px;">' + resultsAverageWk5  + '/5'+  '</td>';
                }



                tableBody  +='</tr>';
            }


            var tableHeader = '';
            var rowsH = 1;
            var colsH = 1;
            for (var r = 0; r < rowsH; r++)
            {
                tableHeader +='<tr>';
                for (var c = 0; c < colsH; c++) //tutorial name
                {
                     tableHeader += '<td style="padding:0 15px 0 15px;">' + "Tutorial session"  +'</td>';

                }


                for (var c = 0; c < colsH; c++) // week 1
                {
                     tableHeader += '<td style="padding:0 15px 0 15px;">' + "Week 1"  +'</td>';

                }

                for (var c = 0; c < colsH; c++) // week 2
                {
                     tableHeader += '<td style="padding:0 15px 0 15px;">' + "Week 2"  +'</td>';

                }

                for (var c = 0; c < colsH; c++) // week 3
                {
                     tableHeader += '<td style="padding:0 15px 0 15px;">' + "Week 3"  +'</td>';

                }

                for (var c = 0; c < colsH; c++) // week 4
                {
                     tableHeader += '<td style="padding:0 15px 0 15px;">' + "Week 4"  +'</td>';

                }

                for (var c = 0; c < colsH; c++) // week 5
                {
                     tableHeader += '<td style="padding:0 15px 0 15px;">' + "Week 5"  +'</td>';

                }


            tableHeader +='</tr>';

            }






            div.append(div);

            div.append(tableHeader);
            div.append(tableBody);

            // div.append(table);
            // table.append(row);
            // row.append(cell);
            // row.append(cell3);
            // table.append(row2);
            // row2.append(cell2);



         //   div.append(message);
           // div.append(message2);
          //  table.append(row);
         //   row.append(cell);



            $('#unitcord1').html(div.html());


           var div2 = $('<div class = "container-fluid" id ="question" style = "padding:0;margin:0;">');
            var h1 = $('<h1>').html(units[0]["Code"]);
            div2.append(h1);
            $('#header1').html(div2.html());

            var div3 = $('<div class = "container-fluid" id ="question" style = "padding:0;margin:0;">');
            var h2 = $('<h1>').html(units[1]["Code"]);
            div3.append(h2);
            $('#header2').html(div3.html());







            //SECOND TABLE IF THEY HAVE ANOTHER UNIT.
            if (units.length == 2 ) {
                var div4 = $('<div class = "container-fluid" id ="question" style = "padding:0;margin:0;">');




                tableBody = '';
                console.log("tutorial");
                console.log(units[0]["Tutorials"].length);
                rows = units[1]["Tutorials"].length;

                cols = 1;

                for (var r = 0; r < rows; r++) {
                    var sumWk1 = 0;
                    var sumWk2 = 0;
                    var sumWk3 = 0;
                    var sumWk4 = 0;
                    var sumWk5 = 0;
                    tableBody += '<tr>';

                    for (var c = 0; c < cols; c++) //tutorial name
                    {

                        tableBody += '<td style="padding:0 15px 0 15px;">' + units[1]["Tutorials"][r]["ID"] + '</td>';
                        // tableBody += '<td>' + units[0]["Tutorials"][c]["Surveys"][c]["results"].length + '</td>';
                        //   tableBody += '<td>' + resultsAverage + '</td>';


                    }


                    for (var c = 0; c < cols; c++) //week 1 results
                    {
                        for (var i = 0; i < units[1]["Tutorials"][r]["Surveys"][0]["results"].length; i++) {
                            sumWk1 += Math.round(units[1]["Tutorials"][r]["Surveys"][0]["results"][i]["Result"]);


                        }
                        var resultsAverageWk1 = Math.round(sumWk1 / units[1]["Tutorials"][r]["Surveys"][0]["results"].length);
                        tableBody += '<td style="padding:0 15px 0 15px;">' + resultsAverageWk1 + '/5' + '</td>';
                    }

                    for (var c = 0; c < cols; c++) //week 2 results
                    {
                        for (var i = 0; i < units[1]["Tutorials"][r]["Surveys"][1]["results"].length; i++) {
                            sumWk2 += Math.round(units[1]["Tutorials"][r]["Surveys"][1]["results"][i]["Result"]);


                        }
                        var resultsAverageWk2 = Math.round(sumWk2 / units[1]["Tutorials"][r]["Surveys"][1]["results"].length);
                        tableBody += '<td style="padding:0 15px 0 15px;">' + resultsAverageWk2 + '/5' + '</td>';
                    }

                    for (var c = 0; c < cols; c++) //week 3 results
                    {
                        for (var i = 0; i < units[1]["Tutorials"][r]["Surveys"][2]["results"].length; i++) {
                            sumWk3 += Math.round(units[1]["Tutorials"][r]["Surveys"][2]["results"][i]["Result"]);


                        }
                        var resultsAverageWk3 = Math.round(sumWk3 / units[1]["Tutorials"][r]["Surveys"][2]["results"].length);
                        tableBody += '<td style="padding:0 15px 0 15px;">' + resultsAverageWk3 + '/5' + '</td>';
                    }

                    for (var c = 0; c < cols; c++) //week 4 results
                    {
                        for (var i = 0; i < units[1]["Tutorials"][r]["Surveys"][3]["results"].length; i++) {
                            sumWk4 += Math.round(units[1]["Tutorials"][r]["Surveys"][3]["results"][i]["Result"]);


                        }
                        var resultsAverageWk4 = Math.round(sumWk4 / units[1]["Tutorials"][r]["Surveys"][3]["results"].length);
                        tableBody += '<td style="padding:0 15px 0 15px;">' + resultsAverageWk4 + '/5' + '</td>';
                    }

                    for (var c = 0; c < cols; c++) //week 5 results
                    {
                        for (var i = 0; i < units[1]["Tutorials"][r]["Surveys"][4]["results"].length; i++) {
                            sumWk5 += Math.round(units[1]["Tutorials"][r]["Surveys"][4]["results"][i]["Result"]);


                        }
                        var resultsAverageWk5 = Math.round(sumWk5 / units[1]["Tutorials"][r]["Surveys"][4]["results"].length);
                        tableBody += '<td style="padding:0 15px 0 15px;">' + resultsAverageWk5 + '/5' + '</td>';
                    }


                    tableBody += '</tr>';
                }


                tableHeader = '';
                var rowsH = 1;
                var colsH = 1;
                for (var r = 0; r < rowsH; r++) {
                    tableHeader += '<tr>';
                    for (var c = 0; c < colsH; c++) //tutorial name
                    {
                        tableHeader += '<td style="padding:0 15px 0 15px;">' + "Tutorial session" + '</td>';

                    }


                    for (var c = 0; c < colsH; c++) // week 1
                    {
                        tableHeader += '<td style="padding:0 15px 0 15px;">' + "Week 1" + '</td>';

                    }

                    for (var c = 0; c < colsH; c++) // week 2
                    {
                        tableHeader += '<td style="padding:0 15px 0 15px;">' + "Week 2" + '</td>';

                    }

                    for (var c = 0; c < colsH; c++) // week 3
                    {
                        tableHeader += '<td style="padding:0 15px 0 15px;">' + "Week 3" + '</td>';

                    }

                    for (var c = 0; c < colsH; c++) // week 4
                    {
                        tableHeader += '<td style="padding:0 15px 0 15px;">' + "Week 4" + '</td>';

                    }

                    for (var c = 0; c < colsH; c++) // week 5
                    {
                        tableHeader += '<td style="padding:0 15px 0 15px;">' + "Week 5" + '</td>';

                    }


                    tableHeader += '</tr>';

                }

                div4.append(div4);
                div4.append(tableHeader);
                div4.append(tableBody);

                $('#unitcord2').html(div4.html());

            }


















    });



}