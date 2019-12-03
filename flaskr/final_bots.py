import functools

#My own import stuff
from classes import  Boss
from flaskr.db_utils import create_db, get_db, create_character, init_db, create_connection
from forms import ActionsForm, CharacterForm
from flask_sqlalchemy import SQLAlchemy
from models import db as finalbots_db
from models import Character, Actions
from turn_result import random_boss_action, get_turn_order, update_health, turn_result
import twitter

#Flask import stuff
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
)

#init flask bluprint
bp = Blueprint('finalbots', __name__, url_prefix='/finalbots')


####################################################################
#                            Homepage                              #
####################################################################
#
#   Purpose:      The homepage is the designated beginning of the
#                 game. This is where the databases are initialized
#                 (cleared) and the player has the option to start
#                 the game. This is also the page where the Success
#                 and Defeat pages re-direct to for re-starting the
#                 game.
#
#   Explanation:  Once the player presses the "Submit" button, the
#                 the database is cleared and re-initialized and the
#                 player is sent to the character creation page
#
@bp.route('/', methods=('GET', 'POST'))
def homepage():
    if request.method == 'POST':
        # Clear the database
        finalbots_db.drop_all()
        finalbots_db.create_all()
        return redirect(url_for('finalbots.select'))
    return render_template('game/home.html')


####################################################################
#                       Character Creation                         #
####################################################################
#
#   Purpose:      This page is where the player decides to choose their
#                 character class. This decides the players stats for 
#                 the duration of the game. This page also performs the
#                 Twitter info requests and initializes the boss for this
#                 game session. Boss and Character information is stored in
#                 the SQL "Character" table.
#
#   Explanation:  As soon as the page is loaded, the game server sends the
#                 request to the Twitter servers and creates a boss object.
#                 This boss object is then used to save the boss in the SQL
#                 Character table. Once the player chooses their class and 
#                 presses "Submit", their choice is used to create a player
#                 entry in the "Character" table. The player is then redirected
#                 to the Actions Choice page. 
#
#

@bp.route('/select', methods=('GET', 'POST'))
def select():
    #Run as soon as the page is grabbed
    if request.method == 'GET':
        #Build the Boss out of the twiter bots
        boss = twitter.build_a_boss()
        #Give the boss its stats
        boss.set_stats(boss, boss.name);

        #Get the database
        get_db()

        #Create boss entry in the character SQL table (Use SQLAlchemy-flask)
        b1 = Character(title='boss', health=1000, name=boss.name, desc=boss.flavour, pwr=boss.pwr, spd=boss.spd, intel=boss.int, appearance=boss.appearance) #TODO debug this
        finalbots_db.session.add(b1)  
        finalbots_db.session.commit()      

    #Run when player presses "Submit"
    if request.method == 'POST' and 'class' in request.form:
        session['class'] = request.form.get('class')

        #Create player entry in the Character SQL table
        if session['class'] == 'warrior':
            p1 = Character(title = 'player1', health = 100, pwr = 15, spd = 10, intel = 5)
        elif session['class'] == 'mage':
            p1 = Character(title = 'player1', health = 100, pwr = 5, spd = 10, intel = 15)
        elif session['class'] == 'thief':
            p1 = Character(title = 'player1', health = 100, pwr = 5, spd = 15, intel = 10)
        
        # Add and commit to db
        finalbots_db.session.add(p1)
        finalbots_db.session.commit() 

        #proceeed to the choose action page
        return redirect(url_for('finalbots.choose'))

    return render_template('game/creation.html')


####################################################################
#                         Choose Actions                           #
####################################################################
#
#   Purpose:      This page is where the player spends the majority
#                 of the game. It displays the boss information,
#                 information about the previous turn, both characters
#                 health total and the current choices availble to the
#                 player.
#
#   Explanation:  Every time the page loads it uses the most recent
#                 information from the SQL databases.
#                 Upon choosing an action, the turn calculation is 
#                 made (which updates the SQL tables) and the page 
#                 is reloaded. This continues until either the player
#                 or the boss is defeated.
#

@bp.route('/choose', methods=('GET', 'POST'))
def choose():
    # Update the boss class with the newest info from db
    boss_new = Character.query.filter_by(title='boss').first()
    appearance_list = boss_new.appearance.split('\\n')

    #get the most recent character info from db
    player = Character.query.filter_by(title='player1').first()

    result_dialogue = []
    # Do turn calculation upon recieving input
    if request.method == 'POST' and 'action' in request.form:
        player_action = request.form.get('action')
        print("Player has chosen:",player_action)
        #Boss Chooses action (weighted)
        boss_action = random_boss_action()
        #Calculate turn order
        turn_order_list = get_turn_order()
        #Store actions in the Actions table
        new_actions = Actions(p_action = player_action, b_action= boss_action)
        finalbots_db.session.add(new_actions)
        finalbots_db.session.commit()

        #calculate turn result (updates tables in the function)
        results = turn_result(turn_order_list)

        #Get the dialogue from the turn
        result_dialogue = results[1]

        #check results for deaths
        if results[0].get('boss') == False and results[0].get('player1') == True:
            #SUCCESS
            print("Player1 Victory!")
            #Redirect to success screen
            return redirect(url_for('finalbots.success'))
        elif results[0].get('boss') == False and results[0].get('player1') == False:
            #BOSS MOVES FIRST AND KILLS PLAYER
            # redirect to failure screen
            print("Player1 Defeat")
            return redirect(url_for('finalbots.defeat'))
        elif results[0].get('boss') == True and results[0].get('player1') == False:
            #DEFEAT
            # Boss defeats you
            print("Player1 Defeat")
            return redirect(url_for('finalbots.defeat'))
        elif results[0].get('player1') == False and results[0].get('boss') == False:
            #YOU KILL BOSS AT LAST SECOND
            #redirect to success screen
            print("Player1 Narrow Victory!")
            return redirect(url_for('finalbots.success'))
        elif results[0].get('player1') == True and results[0].get('boss') == False:
            #SUCCESS
            #Redirect to success screen
            print("Player1 Victory!")
            return redirect(url_for('finalbots.success'))

        # If both still alive we continue!

    return render_template(
        'game/actions.html',
        turn_dialogue=result_dialogue,
        b_appearance=appearance_list,
        b_flavour=boss_new.desc,
        b_health=boss_new.health,
        p1_health=player.health,
        b_name=boss_new.name
        )    

####################################################################
#                         Success Screen                           #
####################################################################
#
#   Purpose:      This page diplays the Congratulation message for if
#                 the player succesfully defeats the boss. The player
#                 can also choose to re-start the game from this page.
#

@bp.route('/congrats', methods=('GET', 'POST'))
def success():
    if request.method == 'POST':
        return redirect(url_for('finalbots.homepage'))
    return render_template('game/success.html') 

####################################################################
#                          Defeat Screen                           #
####################################################################
#
#   Purpose:      This page diplays the Condolances message for if the
#                 player sis killed by the boss. The player can also
#                 choose to re-start the game from this page.
#
@bp.route('/toobad', methods=('GET', 'POST'))
def defeat():
    if request.method == 'POST':
        return redirect(url_for('finalbots.homepage'))
    return render_template('game/defeat.html') 