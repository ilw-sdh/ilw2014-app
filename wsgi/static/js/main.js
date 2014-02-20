//main.js
/*var flights = [[{dest: "Poland", price: "242", carrier: "Ryan Air"},
                    {dest: "Poland", price: "60", carrier: "British Airways"},
                    {dest: "Poland", price: "260", carrier: "Joe's Hardware"}],
            [ {dest: "Bristol", price: "160", carrier: "British Airways"},
                    {dest: "Bristol", price: "20", carrier: "Joe's Hardware"}]];
*/
var flights;
var ready = false;
//get flight data
$.get( "/top_flights", function( data ) {
    flights = JSON.parse(data);
    populate_data();
});
$(document).ready( function () {
    
    $('#chooser a').click(function (e) {
	e.preventDefault();
	$(this).tab('show');
    if($("#tab-main").hasClass("active")){ $("#tab-main").removeClass("hidden");}
        else { $("#tab-main").addClass("hidden"); }
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

});
function reset_modal() {
    //resets the modal to a loading screen
    $("#modalTitle").text("Loading...");
    $("#flight-data tr").remove();
    $("#flight-data").html("<tr><th>Date</th><th>Agent</th><th>Fly Now!</th></tr>");
}
function populate_modal(city_id) {
    //this gets all relevant data for the modal
    var data = flights[city_id];
    $("#modalTitle").text(data.name[0]+", "+data.name[1]+", "+data.name[2]);
    $("#flight-data tr:last").after(prepare_flight(data.cheapest_quote));
    data.quotes.forEach(function (entry) { 
        $("#flight-data tr:last").after(prepare_flight(entry)); 
    });
    $(".date-tooltip").tooltip();
}
function populate_data() {
    ready = true;
    $("#Loading-Content").addClass("hidden");
    $("#first-location h1").html(flights[0].name[1] + "<br />&pound;"+flights[0].cheapest_quote.MinPrice);
    $("#first-location p").html("Go and see <em>"+flights[0].friends[0].name+"</em> in "+flights[0].name[1]+", "+flights[0].name[2]);
    $("#first-location button").attr("location", 0);
    $("#first-location").removeClass("hidden");
    $("#second-location h1").html(flights[1].name[1] + "<br />&pound;"+flights[1].cheapest_quote.MinPrice);
    $("#second-location p").html("You have <em>"+flights[1].friends.length+"</em> friends near "+flights[1].name[1]);
    $("#second-location button").attr("location", 1);
    $("#second-location").removeClass("hidden");
    $("#third-location h1").html(flights[2].name[1] + "<br />&pound;"+flights[2].cheapest_quote.MinPrice);
    $("#third-location p").html("Flights available to go and see <em>"+flights[2].friends[0].name+"</em> in "+flights[2].name[1]);
    $("#third-location button").attr("location", 2);
    $("#third-location").removeClass("hidden");
}
function prepare_flight(dest) {
    var date = moment(dest.InboundLeg.DepartureDate).format('ll');
    var rel_date = moment(dest.InboundLeg.DepartureDate).fromNow();
    //add a 'time until' event using .fromNow() as a tooltip
    var r = "<tr>";
    r += "<td class='date'><div class='date-tooltip' data-toggle='tooltip' data-placement='auto left' title='"+rel_date+"'></div>"+date+"</td>";
    r += "<td class='carrier'>"+dest.InboundLeg.CarrierIds[0]+"</td>";
    r += "<td class='price'><button class='btn btn-success'>&pound;"+dest.MinPrice+"</button></td>";
    r += "</tr>";
    return r;
}
