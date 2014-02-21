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
        var any_selected = false;
        var q = $(this).children(":last").children(".friend-location").text();
        $(".friend-location").each(function () {
            if($(this).hasClass("selected")) {any_selected = true; }
            if($(this).text().toLowerCase().indexOf(q.toLowerCase()) != -1) {
                $(this).parent().parent().show();
            } else {
                $(this).parent().parent().hide();
            }
            console.log(any_selected);
        });
        $(this).toggleClass("selected");
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
    $("#flight-data").html("<tr><th>Date</th><th>Agent</th><th>Fly Now!</th></tr>");
}
function populate_modal(city_id) {
    //this gets all relevant data for the modal
    var data = flights[city_id];
    $("#modalTitle").text(data.name[0]+", "+data.name[1]+", "+data.name[2]);
    $("#skyscanner-url").attr('href', flights[city_id]['url']);
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
    $("#first-location p").html("Go and see <em>"+flights[0].friends[0].name+", "+flights[0].friends[1].name+"</em> and "+(flights[0].friends.length - 2)+" others in "+flights[0].name[1]+", "+flights[0].name[2]);
    $("#first-location button").attr("location", 0);
    $("#first-location").removeClass("hidden");
    $("#second-location h1").html(flights[1].name[1] + "<br />&pound;"+flights[1].cheapest_quote.MinPrice);
    $("#second-location p").html("You have <em>"+flights[1].friends.length+"</em> friends near "+flights[1].name[1]+", including <em>"+flights[1].friends[0].name+"</em>");
    $("#second-location button").attr("location", 1);
    $("#second-location").removeClass("hidden");
    $("#third-location h1").html(flights[2].name[1] + "<br />&pound;"+flights[2].cheapest_quote.MinPrice);
    $("#third-location p").html("Flights available to go and see <em>"+flights[2].friends[0].name+"</em> and "+(flights[2].friends.length -1)+" others in "+flights[2].name[1]);
    $("#third-location button").attr("location", 2);
    $("#third-location").removeClass("hidden");
}
function prepare_flight(dest) {
    var date = moment(dest.OutboundLeg.DepartureDate).format('ll');
    var ret_date = moment(dest.InboundLeg.DepartureDate).format('ll');
    var rel_date = moment(dest.OutboundLeg.DepartureDate).fromNow();
    //add a 'time until' event using .fromNow() as a tooltip
    var r = "<tr>";
    r += "<td class=\"date\"><div class=\"date-tooltip\" data-toggle=\"tooltip\" data-placement=\"auto left\" title=\""+rel_date+"\"></div>"+date+" to "+ret_date+"</td>";
    r += "<td class=\"carrier\">"+dest.InboundLeg.Carrier+"</td>";
    r += "<td class=\"price\"><strong>&pound;"+dest.MinPrice+"</strong></td>";
    r += "</tr>";
    return r;
}
