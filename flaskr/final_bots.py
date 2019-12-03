import functools

#My own import stuff
from classes import  Boss
from flaskr.db_utils import create_db, get_db, create_character, init_db, create_connection
from forms import ActionsForm, CharacterForm
from flask_sqlalchemy import SQLAlchemy
from models import db as finalbots_db
from models import Character, Actions
import twitter
from turn_result import random_boss_action, get_turn_order, update_health, turn_result

#Flask import stuff
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
)

bp = Blueprint('finalbots', __name__, url_prefix='/finalbots')

# Before and ater 


#############################
#          HomePage         #
#############################
@bp.route('/', methods=('GET', 'POST'))
def homepage():
    if request.method == 'POST':
        # init database here, this is where the relevant game info will be stored
        finalbots_db.drop_all()
        finalbots_db.create_all()
        return redirect(url_for('finalbots.select'))
    return render_template('game/home.html')

#############################
#     Character Creation    #
#############################
@bp.route('/select', methods=('GET', 'POST'))
def select():
    #As soon as we get the page we initialize the db and boss
    if request.method == 'GET':
        #Build the Boss out of twiter bots
        boss = twitter.build_a_boss()
        boss.set_stats(boss, boss.name);

        #create db
        get_db()

        #Create boss entry in the character table
        b1 = Character(title='boss', health=1000, name=boss.name, desc=boss.flavour, pwr=boss.pwr, spd=boss.spd, intel=boss.int, appearance=boss.appearance) #TODO debug this
        finalbots_db.session.add(b1)  
        finalbots_db.session.commit()      

    #Once player chooses their class, create an entry for them in the db
    if request.method == 'POST' and 'class' in request.form:
        session['class'] = request.form.get('class')
        #print(session['class']) #used for debugging

        #Create the character
        if session['class'] == 'warrior':
            p1 = Character(title = 'player1', health = 100, pwr = 15, spd = 10, intel = 5)
        elif session['class'] == 'mage':
            p1 = Character(title = 'player1', health = 100, pwr = 5, spd = 10, intel = 15)
        elif session['class'] == 'thief':
            p1 = Character(title = 'player1', health = 100, pwr = 5, spd = 15, intel = 10)
        
        # Add and commit to db
        finalbots_db.session.add(p1)
        finalbots_db.session.commit() 
        ########################################
        # TESTING
        ########################################


        #proceeed to the choose action page
        return redirect(url_for('finalbots.choose'))

    #else stays on the page until submit is made
    return render_template('game/creation.html')

#############################
#       Choose Actions      #
#############################
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
        ########################################
        # TESTING
        ########################################
        #actions = Actions.query.order_by(Actions.id.desc()).first()
        #print("Boss action:", actions.b_action, "Player action:", actions.p_action)
        #do the turn result calculations

        #calculate turn result (updates tables in the function)
        results = turn_result(turn_order_list)

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

#############################
#       Success screen      #
#############################
@bp.route('/congrats', methods=('GET', 'POST'))
def success():
    if request.method == 'POST':
        return redirect(url_for('finalbots.homepage'))
    return render_template('game/success.html') 

#############################
#       Defeat Screen       #
#############################
@bp.route('/toobad', methods=('GET', 'POST'))
def defeat():
    if request.method == 'POST':
        return redirect(url_for('finalbots.homepage'))
    return render_template('game/defeat.html') 