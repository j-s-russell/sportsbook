document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#all').addEventListener('click', () => load_page('all'));
    document.querySelector('#nba').addEventListener('click', () => load_page('nba'));
    document.querySelector('#nfl').addEventListener('click', () => load_page('nfl'));
    document.querySelector('#mlb').addEventListener('click', () => load_page('mlb'));
    document.querySelector('#nhl').addEventListener('click', () => load_page('nhl'));
    document.querySelector('#past').addEventListener('click', () => load_page('past'));
    document.querySelector('#profile').addEventListener('click', () => load_page('profile'));
    document.querySelector('#games-page').addEventListener('click', () => load_page('all'));

    // Show bets on profile (default pending)

    document.querySelector('#pending-bets').style.display = 'block';
    document.querySelector('#completed-bets').style.display = 'none';

    // Clear bet inputs
    document.querySelector('.clear-bet').addEventListener('click', () => clearInput());

    // By default, load all games
    load_page('all');

});


function load_page(league) {
    if (league === "all") {
        document.querySelector('#allgames-view').style.display = 'block';
        document.querySelector('#nba-view').style.display = 'none';
        document.querySelector('#nfl-view').style.display = 'none';
        document.querySelector('#mlb-view').style.display = 'none';
        document.querySelector('#nhl-view').style.display = 'none';
        document.querySelector('#pastgames-view').style.display = 'none';
        document.querySelector('#profile-view').style.display = 'none';
    } else if (league === "nba") {
        document.querySelector('#allgames-view').style.display = 'none';
        document.querySelector('#nba-view').style.display = 'block';
        document.querySelector('#nfl-view').style.display = 'none';
        document.querySelector('#mlb-view').style.display = 'none';
        document.querySelector('#nhl-view').style.display = 'none';
        document.querySelector('#pastgames-view').style.display = 'none';
        document.querySelector('#profile-view').style.display = 'none';
    } else if (league === "nfl") {
        document.querySelector('#allgames-view').style.display = 'none';
        document.querySelector('#nba-view').style.display = 'none';
        document.querySelector('#nfl-view').style.display = 'block';
        document.querySelector('#mlb-view').style.display = 'none';
        document.querySelector('#nhl-view').style.display = 'none';
        document.querySelector('#pastgames-view').style.display = 'none';
        document.querySelector('#profile-view').style.display = 'none';
    } else if (league === "mlb") {
        document.querySelector('#allgames-view').style.display = 'none';
        document.querySelector('#nba-view').style.display = 'none';
        document.querySelector('#nfl-view').style.display = 'none';
        document.querySelector('#mlb-view').style.display = 'block';
        document.querySelector('#nhl-view').style.display = 'none';
        document.querySelector('#pastgames-view').style.display = 'none';
        document.querySelector('#profile-view').style.display = 'none';
    } else if (league === "nhl") {
        document.querySelector('#allgames-view').style.display = 'none';
        document.querySelector('#nba-view').style.display = 'none';
        document.querySelector('#nfl-view').style.display = 'none';
        document.querySelector('#mlb-view').style.display = 'none';
        document.querySelector('#nhl-view').style.display = 'block';
        document.querySelector('#pastgames-view').style.display = 'none';
        document.querySelector('#profile-view').style.display = 'none';
    } else if (league === "past") {
        document.querySelector('#allgames-view').style.display = 'none';
        document.querySelector('#nba-view').style.display = 'none';
        document.querySelector('#nfl-view').style.display = 'none';
        document.querySelector('#mlb-view').style.display = 'none';
        document.querySelector('#nhl-view').style.display = 'none';
        document.querySelector('#pastgames-view').style.display = 'block';
        document.querySelector('#profile-view').style.display = 'none';
    } else if (league === "profile") {
        document.querySelector('#allgames-view').style.display = 'none';
        document.querySelector('#nba-view').style.display = 'none';
        document.querySelector('#nfl-view').style.display = 'none';
        document.querySelector('#mlb-view').style.display = 'none';
        document.querySelector('#nhl-view').style.display = 'none';
        document.querySelector('#pastgames-view').style.display = 'none';
        document.querySelector('#profile-view').style.display = 'block';
    } else {
        document.querySelector('#allgames-view').style.display = 'none';
        document.querySelector('#nba-view').style.display = 'none';
        document.querySelector('#nfl-view').style.display = 'none';
        document.querySelector('#mlb-view').style.display = 'none';
        document.querySelector('#nhl-view').style.display = 'none';
        document.querySelector('#pastgames-view').style.display = 'none';
    }
};


// Unchecking ALL Radio Buttons

function clearInput() {

    console.log("Input cleared");

    var elements = document.getElementsByTagName("input");

    for (var i = 0; i < elements.length; i++) {
        if (elements[i].type == "radio") {
            elements[i].checked = false;
        }
    }

    var inputs = document.getElementsByClassName("wager_input");
    for(var i = 0; i < inputs.length; i++) {
        inputs[i].style.visibility = 'hidden';
    }

    var wagers = document.getElementsByClassName("btn btn-dark");
    for (var i = 0; i < wagers.length; i++) {
        wagers[i].style.visibility = 'hidden';
    }
}

// Display wager input and Bet button

function displayWager(league, game_id) {

    wager_input = document.getElementById(`${league}-wager-${game_id}`);
    wager_input.style.visibility = 'visible';

    bet = document.getElementById(`${league}-bet-submit-${game_id}`);
    bet.style.visibility = 'visible';

}

function displayPending() {
    console.log("DP");
    document.querySelector('#pending-bets').style.display = 'block';
    document.querySelector('#completed-bets').style.display = 'none';
}

function displayCompleted() {
    console.log("DC");
    document.querySelector('#completed-bets').style.display = 'block';
    document.querySelector('#pending-bets').style.display = 'none';
}
