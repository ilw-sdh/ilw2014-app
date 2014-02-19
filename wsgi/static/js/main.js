//main.js
/*var flights = [[{dest: "Poland", price: "242", carrier: "Ryan Air"},
                    {dest: "Poland", price: "60", carrier: "British Airways"},
                    {dest: "Poland", price: "260", carrier: "Joe's Hardware"}],
            [ {dest: "Bristol", price: "160", carrier: "British Airways"},
                    {dest: "Bristol", price: "20", carrier: "Joe's Hardware"}]];
*/
var flights;
var keys = [];
//get flight data
$.get( "/top_flights", function( data ) {
    flights = JSON.parse(data);
    populate_data();
});
$(document).ready( function () {

    $(".btn-modal").on("click", function () {
        //set modal to loading!
        console.log(flights);
        reset_modal();
        $('#myModal').modal('toggle');
        //populate the modal here!!!
        populate_modal($(this).attr("location"));
    });

});
function reset_modal() {
    //resets the modal to a loading screen
    $("#modalTitle").text("Loading...");
    $("#flight-data tr").remove();
    $("#flight-data").html("<tr></tr>");
}
function populate_modal(city) {
    //this gets all relevant data for the modal
    var data = flights[city];
    $("#modalTitle").text("Flying to "+data[0].dest);
    data.forEach(function(entry) {
        $("#flight-data tr:last").after(prepare_flight(entry));
    });
}
function populate_data() {
    console.log(flights);
    for (var data in flights) {
        keys.push(data);
    }
    $("#first-location h1").html(flights[keys[0]].name[1] + "<br />&pound;"+flights[keys[0]].cheapest_quote.MinPrice);
    $("#first-location p").html("Go and see <em>"+flights[keys[0]].friends[0].name+"</em> in "+flights[keys[0]].name[1]+", "+flights[keys[0]].name[2]);
    $("#second-location h1").html(flights[keys[1]].name[1] + "<br />&pound;"+flights[keys[1]].cheapest_quote.MinPrice);
    $("#second-location p").html("You have <em>"+flights[keys[1]].friends.length+"</em> friends near "+flights[keys[1]].name[1]);
    $("#third-location h1").html(flights[keys[2]].name[1] + "<br />&pound;"+flights[keys[2]].cheapest_quote.MinPrice);
    $("#third-location p").html("Flights available to go and see <em>"+flights[keys[2]].friends[0].name+"</em> in "+flights[keys[2]].name[1]);
}
function prepare_flight(dest) {
    var r = "<tr>";
    r += "<td class='date'>Today</td>";
    r += "<td class='carrier'>"+dest.carrier+"</td>";
    r += "<td class='begin'>Current</td>";
    r += "<td class='dest'>"+dest.dest+"</td>";
    r += "<td class='book'><button class='btn btn-success'>BA760</button></td>";
    r += "</tr>";
    return r;
}
