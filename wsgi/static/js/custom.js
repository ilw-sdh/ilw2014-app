//hi

$( document ).ready( function () {
    $("#content").text("loading");
    fs = populate_flights();
    $("#content").text("");
    for (i = 0; i < fs.length; i++) {
        $("#content").append(format_flight(fs[i]));
    }
});

function populate_flights() {
    //gets all the flight data from a variable and displays them x at a time
    //in a json, which can be loaded into an array that can then be changed,
    //depending on stuff.
    return [{location: 'Edinburgh', friends: ["james","hamish"]},
           {location: 'London',     friends: ["charles","bob"]}];
} 
function format_flight(f) {
    var r = "<li><h1>"+f.location+"</h1>";
    r += "<ul class='friends'>";
    for (j = 0; j < f.friends.length; j++) {
        r += "<li>"+f.friends[j]+"</li>";
    }
    r += "</ul>";
    r += "</li>";
    return r;
}
