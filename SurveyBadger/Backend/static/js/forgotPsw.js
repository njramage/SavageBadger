/**
 * Created by Oliver on 7/19/2017.
 */
function sendEmail() {

         var div = $('<div class = "container-fluid" id ="question" style = "padding:0;margin:0;">');

            var message = $('<p>').html("email has been sent with password instructions" );



            div.append(div);

            div.append(message);


            $('#container').html(div.html());


}