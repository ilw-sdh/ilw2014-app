//main.js
var flights;
var ready = false;
var g_city_code;
var friend_flights;
//get flight data
$.get( "/top_flights", function( data ) {
    flights = JSON.parse(data);
    populate_data();
});
$(document).ready( function () {
    
    $("#tab-friends").addClass("hide");
    $('#chooser a').click(function (e) {
	e.preventDefault();
	$(this).tab('show');
    if(!$("#tab-main").hasClass("active")){ $("#tab-main").removeClass("hide");}
        else { $("#tab-main").addClass("hide"); }
    if(!$("#tab-friends").hasClass("active")){ $("#tab-friends").removeClass("hide");}
        else { $("#tab-friends").addClass("hide"); }
    });

    $(".btn-modal").on("click", function () {
        //set modal to loading!
        if(ready) {
            reset_modal();
            $('#myModal').modal('toggle');
            //populate the modal here!!!
            populate_modal($(this).attr("location"));
        }
    });

    $(".friendlist tr").on("click", function() {
        //open up a modal with that locations prices
        if(ready) {
            reset_modal();
            $("#myModal").modal('toggle');
            var country = $(this).find(".friend-location").attr("data-country");
            var lat = $(this).find(".friend-location").attr("data-lat");
            var lon = $(this).find(".friend-location").attr("data-lon");
            $.get( "friend_flights/?country="+country+"&lat="+lat+"&lon="+lon, function( data ) {
                //do stuff!! probs using modals
                friend_flights = data;
            });
        }
    });
    $('#search').on("keyup", function () {
        var q = $('#search').val();
        $(".friend-name").each(function () {
            if ($(this).text().toLowerCase().indexOf(q.toLowerCase()) != -1) {
                $(this).parent().parent().show();
            }
            else {
                $(this).parent().parent().hide();
            }
        });
    });
});
function reset_modal() {
    //resets the modal to a loading screen
    $("#modalTitle").text("Loading...");
    $("#flight-data tr").remove();
    $("#flight-data").html("<tr><th>Date</th><th>Airline</th><th>Fly Now!</th></tr>");
    $("#skyscanner-url").attr("disabled", true);
}
function populate_modal(city_id) {
    //this gets all relevant data for the modal
    var data = flights[city_id];
    configure_modal(data);
    /*g_city_code = data.iata;
    $("#skyscanner-url").attr("disabled", false);
    $("#modalTitle").text(data.name[0]+", "+data.name[1]+", "+data.name[2]);
    $("#skyscanner-url").attr('href', flights[city_id]['url']);
    $("#flight-data tr:last").after(prepare_flight(data.cheapest_quote));
    data.quotes.forEach(function (entry) { 
        $("#flight-data tr:last").after(prepare_flight(entry)); 
    });
    $(".date-tooltip").tooltip();
    g_city_code = undefined;*/
}
function configure_modal(data) {
    //this function takes in an object of flights and respective data
    g_city_code = data.iata;
    $("#skyscanner-url").attr("disabled", false);
    $("#modalTitle").text(data.name[0]+", "+data.name[1]+", "+data.name[2]);
    $("#skyscanner-url").attr('href', data.url);
    $("#flight-data tr:last").after(prepare_flight(data.cheapest_quote));
    data.quotes.forEach(function (entry) { 
        $("#flight-data tr:last").after(prepare_flight(entry)); 
    });
    $(".date-tooltip").tooltip();
    g_city_code = undefined;
}
function populate_data() {
    ready = true;

    var locationDescription = function (flight) {
        return "You have <em>"+flight.friends.length+"</em> friends near "+flight.name[1];
    }

    $("#chooser").removeClass("hidden");
    $("#Loading-Content").addClass("hidden");
    $("#first-location h1").html(flights[0].name[1] + "<br />&pound;"+flights[0].cheapest_quote.MinPrice);
    $("#first-location p").html(locationDescription(flights[0]));
    $("#first-location button").attr("location", 0);
    $("#first-location").removeClass("hidden");
    var x = 0;
    $("#first-location .img-thumbnail").each(function (e) {
        if (flights[0].friends.length > x) {
            $(this).attr("src",flights[0].friends[x].pic);
        }
        else {
            $(this).hide();
        }
        x++;
    });
    $("#second-location h1").html(flights[1].name[1] + "<br />&pound;"+flights[1].cheapest_quote.MinPrice);
    $("#second-location p").html(locationDescription(flights[1]));
    $("#second-location button").attr("location", 1);
    $("#second-location").removeClass("hidden");
    var x = 0;
    $("#second-location .img-thumbnail").each(function (e) {
        if (flights[1].friends.length > x) {
            $(this).attr("src",flights[1].friends[x].pic);
        }
        else {
            $(this).hide();
        }
        x++;
    });
    $("#third-location h1").html(flights[2].name[1] + "<br />&pound;"+flights[2].cheapest_quote.MinPrice);
    $("#third-location p").html(locationDescription(flights[2]));
    $("#third-location button").attr("location", 2);
    $("#third-location").removeClass("hidden");
    var x = 0;
    $("#third-location .img-thumbnail").each(function (e) {
        if (flights[2].friends.length > x) {
            $(this).attr("src",flights[2].friends[x].pic);
        }
        else {
            $(this).hide();
        }
        x++;
    });
}
function prepare_flight(dest) {
    var date = moment(dest.OutboundLeg.DepartureDate).format('ll');
    var ret_date = moment(dest.InboundLeg.DepartureDate).format('ll');
    var rel_date = moment(dest.OutboundLeg.DepartureDate).fromNow();
    var ss_date = moment(dest.OutboundLeg.DepartureDate).format('YYYY-MM-DD');
    var ss_ret_date = moment(dest.InboundLeg.DepartureDate).format('YYYY-MM-DD');
    var city_code = g_city_code;
    //add a 'time until' event using .fromNow() as a tooltip
    var r = "<tr>";
    r += "<td class=\"date\"><div class=\"date-tooltip\" data-toggle=\"tooltip\" data-placement=\"left\" title=\""+rel_date+"\"></div>"+date+"<small style=\"color: #666;\"> to "+ret_date+"</small></td>";
    r += "<td class=\"carrier\">"+dest.InboundLeg.Carrier+"</td>";
    r += "<td class=\"price\"><a href=\"http://partners.api.skyscanner.net/apiservices/referral/v1.0/GB/GBP/en-GB/edi/"+city_code+"/"+ss_date+"/"+ss_ret_date+"\" class=\"btn btn-success\" target=\"_blank\">&pound;"+dest.MinPrice+"</a></td>";
    r += "</tr>";
    return r;
}
