//hi

$( document ).ready( function () {
    $("#content").text("loading");
    f = populate_flights();
    $("#content").text("");
    for (i = 0; i < f.length; i++) {
        $("#content").append("<li>"+f[i].location+"</li>");
    }
});

function populate_flights() {
    //gets all the flight data from a variable and displays them x at a time
    //in a json, which can be loaded into an array that can then be changed,
    //depending on stuff.
    return [{location: 'Edinburgh', friends: ["james","hamish"]},
           {location: 'London',     friends: ["charles","bob"]}];
} 
