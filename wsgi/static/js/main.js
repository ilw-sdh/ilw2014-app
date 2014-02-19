//main.js
/*var flights = [[{dest: "Poland", price: "242", carrier: "Ryan Air"},
                    {dest: "Poland", price: "60", carrier: "British Airways"},
                    {dest: "Poland", price: "260", carrier: "Joe's Hardware"}],
            [ {dest: "Bristol", price: "160", carrier: "British Airways"},
                    {dest: "Bristol", price: "20", carrier: "Joe's Hardware"}]];
*/
var flights = get_flight_data();
$(document).ready( function () {

    $(".btn-modal").on("click", function () {
        //set modal to loading!
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
function get_flight_data() {
    console.log($.get("/top_flights"));
    return 0;
}
