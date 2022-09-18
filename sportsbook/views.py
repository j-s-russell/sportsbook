from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
import requests

from .models import User, League, Game, Bet, Market, Update

from datetime import datetime, timedelta, timezone
from dateutil.parser import parse

# Create your views here.

def index(request):

    # UPDATE AT 1:00AM PST
    now = datetime.now(timezone.utc) - timedelta(hours=4)
    if Update.objects.exists() == False:
        init_models()
        update_games()
        update_scores()
        update_bets()
    update = Update.objects.get().update_time

    if now > update:
        Update.objects.filter(update_time=update).delete()
        next_update = now.replace(hour=4, minute=0) + timedelta(days=1)
        new = Update.objects.create(update_time=next_update)
        new.save()
        # Update all games, scores, and bets from previous day
        update_games()
        update_scores()
        update_bets()

    # Time to close bets
    update_display = update
    update_end = update + timedelta(hours=1)

    # Get games
    available_games = Game.objects.filter(commence_time__gte=now).order_by("commence_time")
    nba_games = Game.objects.filter(commence_time__gte=now, league=League.objects.get(league="NBA")).order_by("commence_time")
    nfl_games = Game.objects.filter(commence_time__gte=now, league=League.objects.get(league="NFL")).order_by("commence_time")
    mlb_games = Game.objects.filter(commence_time__gte=now, league=League.objects.get(league="MLB")).order_by("commence_time")
    nhl_games = Game.objects.filter(commence_time__gte=now, league=League.objects.get(league="NHL")).order_by("commence_time")
    past_games = Game.objects.filter(completed=True).order_by("-commence_time")

    # Search
    if request.method == "POST":
        search = request.POST["search"].lower()
        available_games = [game for game in available_games if (search in game.home_team.lower()) or (search in game.away_team.lower())]
        nba_games = [game for game in nba_games if (search in game.home_team.lower()) or (search in game.away_team.lower())]
        nfl_games = [game for game in nfl_games if (search in game.home_team.lower()) or (search in game.away_team.lower())]
        mlb_games = [game for game in mlb_games if (search in game.home_team.lower()) or (search in game.away_team.lower())]
        nhl_games = [game for game in nhl_games if (search in game.home_team.lower()) or (search in game.away_team.lower())]
        past_games = [game for game in past_games if (search in game.home_team.lower()) or (search in game.away_team.lower())]

    # Bets
    if request.user.is_authenticated:
        pending_bets = Bet.objects.filter(bettor=request.user, status="Pending")
        completed_bets = Bet.objects.filter(bettor=request.user).exclude(status="Pending")
    else:
        pending_bets = None
        completed_bets = None

    # Clear Messages
    #list(messages.get_messages(request))


    return render(request, "sportsbook/index.html", {
        "all_games": available_games,
        "nba_games": nba_games,
        "nfl_games": nfl_games,
        "mlb_games": mlb_games,
        "past_games": past_games,
        "update_display": update_display,
        "update_end": update_end,
        "pending_bets": pending_bets,
        "completed_bets": completed_bets
    })

def place_bet(request, id):
    if request.method == "POST":
        bettor = request.user
        game = Game.objects.get(pk=id)
        wager = float(request.POST["wager"])

        # Subtract from balance
        bettor.balance -= wager
        bettor.pending += wager
        bettor.save()

        bet_info = request.POST[f"bet-select-{id}"]
        market = Market.objects.get(market=bet_info[5:])
        
        if bet_info[:4] == "home":
            home_bet = True
        else:
            home_bet = False

        # Create Bet
        bet = Bet.objects.create(bettor=request.user,
                                 game=game,
                                 wager=wager,
                                 market=market,
                                 home_bet=home_bet)
        bet.save()
        bets = Bet.objects.filter(bettor=request.user)

        # Message
        messages.success(request, "Bet placed successfully!")
        return HttpResponseRedirect(reverse("index"))



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "sportsbook/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "sportsbook/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "sportsbook/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "sportsbook/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "sportsbook/register.html")


# INITIALIZE MODELS
def init_models():
    # Update Time
    now = datetime.now(timezone.utc) - timedelta(hours=4)
    first_update_time = now.replace(hour=4, minute=0) + timedelta(days=1)
    first_update = Update.objects.create(update_time=first_update_time)
    first_update.save()

    # Leagues
    for league in ["NBA", "NFL", "MLB", "NHL"]:
        newleague = League.objects.create(league=league)
        newleague.save()
    
    # Markets
    ml = Market.objects.create(market="ml")
    ml.save()
    spread = Market.objects.create(market="spread")
    spread.save()




# NON-VIEW FUNCTIONS


# RETURN ACTIVE SPORTS
def get_active_sports():
    key = settings.ODDS_KEY
    sports_url = f"https://api.the-odds-api.com/v4/sports/?apiKey={key}&all=true"
    sports = requests.get(sports_url).json()
    all_leagues = ["NBA", "NFL", "MLB", "NHL"]
    major_sports = [sport for sport in sports if sport['title'] in all_leagues]
    active_sports = [sport['title'] for sport in major_sports if sport['active']]
    return active_sports


# UPDATE GAMES
def update_games():

    # Delete old games
    now = datetime.now(timezone.utc)
    for expired in [game for game in Game.objects.all() if game.commence_time + timedelta(days=30) < now]:
        expired.delete()

    key = settings.ODDS_KEY
    odds_dict = {
        "NBA": f"https://api.the-odds-api.com/v4/sports/basketball_nba/odds/?apiKey={key}&regions=us&markets=h2h,spreads&oddsFormat=american",
        "NFL": f"https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/?apiKey={key}&regions=us&markets=h2h,spreads&oddsFormat=american",
        "MLB": f"https://api.the-odds-api.com/v4/sports/baseball_mlb/odds/?apiKey={key}&regions=us&markets=h2h,spreads&oddsFormat=american",
        "NHL": f"https://api.the-odds-api.com/v4/sports/icehockey_nhl/odds/?apiKey={key}&regions=us&markets=h2h,spreads&oddsFormat=american"
    }

    active_sports = get_active_sports()
    for league in active_sports:
        url = odds_dict[league]
        response = requests.get(url).json()
        games = [game for game in response if (Game.objects.filter(api_id=game['id']).exists() == False) and (parse(game['commence_time']) - timedelta(days=10) < now)]
        for game in games:
            api_id = game['id']
            commence_time = parse(game['commence_time']) - timedelta(hours=4)
            home_team = game['home_team']
            away_team = game['away_team']

            # Get Odds
            odds = game['bookmakers'][0]
            ml = next((market for market in odds['markets'] if market['key'] == 'h2h'), None)
            spread = next((market for market in odds['markets'] if market['key'] == 'spreads'), None)
            
            # Money Line
            if ml is not None:
                home_ml_dict = next(d for d in ml['outcomes'] if d['name'] == home_team)
                home_ml = home_ml_dict['price']
                away_ml_dict = next(d for d in ml['outcomes'] if d['name'] == away_team)
                away_ml = away_ml_dict['price']
            else:
                home_ml = None
                away_ml = None

            # Spread
            if spread is not None:
                home_spr_dict = next(d for d in spread['outcomes'] if d['name'] == home_team)
                home_price = home_spr_dict['price']
                home_point = home_spr_dict['point']
                away_spr_dict = next(d for d in spread['outcomes'] if d['name'] == away_team)
                away_price = away_spr_dict['price']
                away_point = away_spr_dict['point']
            else:
                home_price = None
                away_price = None
                home_point = None
                away_point = None


            # Create Game instance
            new_game = Game.objects.create(api_id=api_id,
                                           league=League.objects.get(league=league),
                                           commence_time=commence_time,
                                           home_team=home_team,
                                           away_team=away_team,
                                           home_ml=home_ml,
                                           away_ml=away_ml,
                                           home_price=home_price,
                                           away_price=away_price,
                                           home_point=home_point,
                                           away_point=away_point)
            new_game.save()



# UPDATE SCORES

def update_scores():
    key = settings.ODDS_KEY
    scores_dict = {
        "NBA": f"https://api.the-odds-api.com/v4/sports/basketball_nba/scores/?daysFrom=3&apiKey={key}",
        "NFL": f"https://api.the-odds-api.com/v4/sports/americanfootball_nfl/scores/?daysFrom=3&apiKey={key}",
        "MLB": f"https://api.the-odds-api.com/v4/sports/baseball_mlb/scores/?daysFrom=3&apiKey={key}",
        "NHL": f"https://api.the-odds-api.com/v4/sports/icehockey_nhl/scores/?daysFrom=3&apiKey={key}"
    }

    active_sports = get_active_sports()
    for league in active_sports:
        url = scores_dict[league]
        response = requests.get(url).json()
        for score in response:
            api_id = score['id']
            if Game.objects.filter(api_id=api_id).exists():
                game = Game.objects.get(api_id=api_id)
                game.completed = score['completed']
                if score['completed']:
                    home_score = score['scores'][0]['score']
                    away_score = score['scores'][1]['score']

                    game.home_score = home_score
                    game.away_score = away_score
                game.save()



# UPDATE BETS

# Calculate payout
def payout(line, wager):
    mult = line / 100
    if mult > 0:
        to_win = round(wager * mult, 2)
    else:
        to_win = round(wager / abs(mult), 2)
    return to_win + wager


def update_bets():
    now = datetime.now(timezone.utc) - timedelta(hours=4)
    pending_bets = Bet.objects.filter(status="Pending")
    bets = [bet for bet in pending_bets if bet.game.completed]

    for bet in bets:
        game_id = bet.game.id
        game = Game.objects.get(id=game_id)
        
        # Delete expired bets
        if (now - game.commence_time).days > 2:
            bet.delete()
        
        # Money Line Bets
        if bet.market == Market.objects.get(market="ml"):

            if game.home_score - game.away_score > 0:
                home_won = True
            else:
                home_won = False

            if bet.home_bet and home_won:
                winnings = payout(game.home_ml, bet.wager)
            elif (bet.home_bet == False) and (home_won == False):
                winnings = payout(game.away_ml, bet.wager)
            else:
                winnings = 0

        # Spread Bets
        elif bet.market == Market.objects.get(market="spread"):
            if bet.home_bet:
                if game.away_score - game.home_score < game.home_point:
                    winnings = payout(game.home_price, bet.wager)
                elif game.away_score - game.home_score > game.home_point:
                    winnings = 0
                else:
                    winnings = bet.wager
            else:
                if game.home_score - game.away_score < game.away_point:
                    winnings = payout(game.away_price, bet.wager)
                elif game.home_score - game.away_score > game.away_point:
                    winnings = 0
                else:
                    winnings = bet.wager

        # Update Bet Objects and Balance
        if winnings > bet.wager:
            bet.status =  "Won"
        elif winnings < bet.wager:
            bet.status = "Lost"
        else:
            bet.status = "Pushed"
        bet.profit = round(winnings, 2) - bet.wager
        bet.save()

        # Update balance
        bettor = bet.bettor
        bettor.balance += winnings
        bettor.pending -= bet.wager
        bettor.save()

            






        


        