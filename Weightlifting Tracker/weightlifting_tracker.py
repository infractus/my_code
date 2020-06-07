#! python3

import os, sys
import pyinputplus as pyip
from datetime import datetime
from pathlib import Path

import shinsai

TRACK_FILE = 'tracking.json'
NOW = str(datetime.now().date())

p = Path(__file__).parent
os.chdir(p)


def greeting():
    """Choose a user, create profile if not returning."""
    print("Welcome to Shinsai's Weighlifting Tracker!")
    if tracking:
        returning = pyip.inputYesNo('Are you a returning user? ', blank=True)
    else:
        returning = 'no'
    if returning == 'no':
        create_new_user()
    users = []
    for k in tracking.keys():
        users.append(k)
    while True:
        user = pyip.inputMenu(users, numbered=True, blank=True)
        if user:
            return user


def create_new_user():
    """Create a new user profile."""
    while True:
        user = pyip.inputStr('Please enter your name: ').title()
        tracking[user] = {}
        the_program.write_to_tracking(TRACK_FILE, tracking)
        weight = pyip.inputFloat('Please enter your body weight: ')
        body_fat = pyip.inputFloat('Please enter your body fat %: ')
        print(f'Name: {user}\nCurrent weight: {weight}\nBody fat: {body_fat}%')
        verify = pyip.inputYesNo(
            'Is this information correct (y/n)? ', blank=True
                )
        if verify == 'yes':
            tracking[user]['body_weight'] = {NOW: weight}
            tracking[user]['body_fat'] = {NOW: body_fat}
            the_program.write_to_tracking(TRACK_FILE, tracking)
            break


def show_menu():
    """
    Show the menu of options based upon the state of the user's profile.
    """
    menu_choices = ['Add exercises']
    if 'exercises' in tracking[active_user].keys():
        menu_choices.append('List exercises')
        menu_choices.append('Log a workout')
        for exercise in tracking[active_user]['exercises'].values():
            # If any active exercises, show "deactivate exercises"
            if exercise['active'] == True:
                menu_choices.append('Deactivate exercises from routine')
                break
        for exercise in tracking[active_user]['exercises'].values():
            if exercise['active'] == False:
                menu_choices.append('Reactivate a deactivated exercise')
                break
        if len(tracking[active_user]['exercises'].items()) > 1:
            menu_choices.append('Change exercise order')
    if 'workouts' in tracking[active_user].keys():
        if len(tracking[active_user]['workouts']) > 1:
            menu_choices.append('View a previous workout')
    menu_choices.append('Quit')
    print()
    choice = pyip.inputMenu(menu_choices, numbered=True)
    menu_select(choice)
    

def menu_select(choice):
    """Call the appropriate function based on choice selected."""
    if choice == 'Quit':
        sys.exit()
    if choice == 'Add exercises':
        add_exercises()
    if choice == 'List exercises':
        list_user_exercises()
    if choice == 'Change exercise order':
        adjust_exercise_order()
    if choice == 'Deactivate exercises from routine':
        deactivate_exercises()
    if choice == 'Reactivate a deactivated exercise':
        reactivate_an_exercise()
    if choice == 'Log a workout':
        log_a_workout()
    if choice == 'View a previous workout':
        view_a_previous_workout()


def add_exercises():
    """Add exercises to the users exercise list."""
    if 'exercises' not in tracking[active_user].keys():
        tracking[active_user]['exercises'] = {}
        tracking[active_user]['num_exercises'] = 0
        the_program.write_to_tracking(TRACK_FILE, tracking)
    new_exercise_list = tracking[active_user]['exercises']
    adding_exercises = True
    while adding_exercises:
        while True:
            exercise = pyip.inputStr(
                'What is the name of the exercise? '
                    ).title()
            verify = pyip.inputYesNo(
                f'You entered {exercise}. Is this correct (y/n)? ', blank=True
                    )
            if verify == 'yes':
                break
        new_tracking = input_exercise_details(exercise, new_exercise_list)
        add_another = pyip.inputYesNo(f'Add another exercise? ')
        if add_another == 'no':
            adding_exercises = False
    the_program.write_to_tracking(TRACK_FILE, new_tracking)
    input('Exercises added. Press ENTER to return to menu.')
    show_menu()


def input_exercise_details(exercise, new_exercise_list):
    """
    Enter the details of the new exercise, and handle if it has a
    variant.
    """
    print('\nInput the type of exercise: ')
    exercise_types = ['Body Weight', 'Weights']
    exercise_type = pyip.inputMenu(exercise_types, numbered=True)
    variant = pyip.inputYesNo(
        'Does this exercise have a variant that you alternate? (y/n) '
        )
    if variant == 'no':
        new_exercise_list[exercise] = {
            'active': True, 'variant': None, 
            'exercise_type': exercise_type
            }
        print(f'{exercise} queued to be added.')
        tracking[active_user]['num_exercises'] += 1
        return tracking
    else:
        new_tracking = handle_variant(
            exercise, new_exercise_list, exercise_types, exercise_type
                )
        return new_tracking


def handle_variant(exercise, new_ex_list, ex_types, ex_type):
    """Handling of variant exercises."""
    while True:
        variant_name = pyip.inputStr(
            'What is the name of the variant? '
                ).title()
        verify = pyip.inputYesNo(
            f'You entered {variant_name}. Is this correct (y/n)? '
                )
        if verify == 'yes':
            print('\nInput the type of exercise: ')
            variant_ex_type = pyip.inputMenu(
                ex_types, numbered=True
                    )
            new_ex_list[exercise] = {
                'active': True, 'variant': variant_name,
                'did_last_session': False, 'parent': True,
                'exercise_type': ex_type
                    }
            new_ex_list[variant_name] = {
                'active': True, 'variant': exercise,
                'did_last_session': True, 'parent': False,
                'exercise_type': variant_ex_type
                    }
            print(
                f'Exercises {exercise} and {variant_name} queued to be added.'
                    )
            tracking[active_user]['num_exercises'] += 2
            break
    return tracking


def list_user_exercises():
    """List user exercises."""
    exercises = tracking[active_user]['exercises']
    
    print('\nList of exercises:')
    for k in exercises.keys():
        if exercises[k]['variant'] != None:
            if exercises[k]['parent'] == False:
                print(
                    f"{k} (Variant of {exercises[k]['variant']}) - Active: " 
                    f"{exercises[k]['active']}"
                        )
                continue				
        print(f"{k} - Active: {exercises[k]['active']}")
    input('\nPress ENTER to go back to main menu.')
    show_menu()


def adjust_exercise_order():
    """Adjust the order of active exercises in a routine."""
    while True:
        exercises = tracking[active_user]['exercises']
        exercise_list, new_exercise_list, new_exercises = [], [], {}
        
        for key in exercises.keys():
            if exercises[key]['active']:
                exercise_list.append(key)
        
        while len(exercise_list) > 1:
            print('Select the next exercise:')
            choice = pyip.inputMenu(exercise_list, numbered=True)
            new_exercise_list.append(choice)
            exercise_list.remove(choice)
        new_exercise_list.append(exercise_list[0])

        exercise_list_string = "\n".join(new_exercise_list)
        print(f'You have chosen the new order:\n{exercise_list_string}')
        verify = pyip.inputYesNo('Is this correct? ')
        if verify:
            break	
    
    for key in exercises.keys():
        if not exercises[key]['active']:		
            new_exercise_list.append(key)
    for exercise in new_exercise_list:
        for k, v in exercises.items():
            if exercise == k:
                new_exercises.update({k: v})

    tracking[active_user]['exercises'] = new_exercises
    the_program.write_to_tracking(TRACK_FILE, tracking)
    show_menu()


def deactivate_exercises():
    """Set Active to False for exercises not part of routine."""
    exercises = tracking[active_user]['exercises']

    choosing = True
    while choosing:
        active = display_active(exercises)
        while True:
            print('Which exercise would you like to deactivate?')
            exercise = pyip.inputMenu(active, numbered=True, blank=True)
            print(f"You indicated you would like to deactivate {exercise}.")
            if exercise == '':
                print('No exercise selected.')
                break
            else:
                verify = pyip.inputYesNo('Is this correct? (y/n) ')
                if verify == 'yes':
                    exercises[exercise]['active'] = False
                    print(f'{exercise} has been deactivated.')
                    break
        another = pyip.inputYesNo(
            'Would you like to choose another? (y/n) ', blank=True
            )
        if another == 'no':
            choosing = False
        
    the_program.write_to_tracking(TRACK_FILE, tracking)
    input('\nPress ENTER to go back to main menu.')
    show_menu()


def display_active(exercises):
    """Show active exercises."""
    active = []
    for k in exercises.keys():
        if exercises[k]['active'] == True:
            active.append(k)
    return active


def reactivate_an_exercise():
    """Set active to True for exercises not part of routine."""
    exercises = tracking[active_user]['exercises']

    choosing = True
    while choosing:
        inactive = display_inactive(exercises)
        while True:
            print('Which exercise would you like to activate?')
            exercise = pyip.inputMenu(inactive, numbered=True, blank=True)
            if exercise == '':
                print('No exercise selected.')
                break
            else:
                print(f"You indicated you would like to activate {exercise}.")
                verify = pyip.inputYesNo('Is this correct? (y/n) ')
                if verify == 'yes':
                    exercises[exercise]['active'] = True
                    print(f'{exercise} has been activated.')
                    the_program.write_to_tracking(TRACK_FILE, tracking)
                    break
        another = pyip.inputYesNo(
            'Would you like to choose another? (y/n) ', blank=True)
        if another == 'no':
            choosing = False
    
    input('\nPress ENTER to go back to main menu.')
    show_menu()


def display_inactive(exercises):
    """Show inactive exercises."""
    inactive = []
    for k in exercises.keys():
        if exercises[k]['active'] == False:
            inactive.append(k)
    return inactive


def log_a_workout():
    """Log a workout for a user."""
    select_date = ['Today', 'Log another date']
    when = pyip.inputMenu(select_date, numbered=True)
    if when == 'Log another date':
        workout_input = pyip.inputDate('Enter a date (mm/dd/yy): ')
        workout_date = str(workout_input)
    else:
        workout_date = NOW
    current_weight = pyip.inputFloat(
        'Morning body weight at date of workout? '
            )
    body_fat = pyip.inputFloat('Body fat % at date of workout? ' )
    workout_weight = pyip.inputFloat(
        'Body weight at time of workout? '
            )
    tracking[active_user]['body_weight'][workout_date] = current_weight
    tracking[active_user]['body_fat'][workout_date] = body_fat
    if 'workouts' in tracking[active_user].keys():
        tracking[active_user]['workouts'].append({
            'workout_number': len(tracking[active_user]['workouts']) + 1,
            'workout_date': workout_date, 'workout_weight': workout_weight
                })
    else:
        tracking[active_user]['workouts'] = [{
            'workout_number': 1,
            'workout_date': workout_date,
            'workout_weight': workout_weight
                }]
    the_program.write_to_tracking(TRACK_FILE, tracking)
    select_exercises(workout_date)
    show_menu()
    

def select_exercises(workout_date):
    """Choose which exercises to do."""
    workout_number = tracking[active_user]['workouts'][-1]['workout_number']
    exercises = tracking[active_user]['exercises']
    routine = []
    
    routine = set_exercises(exercises, routine)

    routine_str = "\n".join(routine)
    print(f'\nRoutine is: \n\n{routine_str}')

    for i in exercises.keys():
        if exercises[i]['variant']:
            if i in routine:
                exercises[i]['did_last_session'] = True
                continue
            else:
                exercises[i]['did_last_session'] = False
                continue				
    the_program.write_to_tracking(TRACK_FILE, tracking)
    input('Press ENTER to start.')
    log_exercises(routine, workout_number, workout_date)
    

def set_exercises(exercises, routine):
    """Set the exercises for the routine."""
    for exercise in exercises.keys():
        is_active = exercises[exercise]['active']
        variant = exercises[exercise]['variant']
        if 'sessions_done' not in exercises[exercise].keys():
            exercises[exercise]['sessions_done'] = [] 
        if is_active == True:
            if variant:
                if not exercises[exercise]['did_last_session']:
                    print(
                        f'You are scheduled to do {exercise} this session. '
                        f'Its variant {variant} will be done next session.'
                            )
                    keep_exercise = pyip.inputYesNo(
                        'Is this okay? ', blank=True
                            )
                    if keep_exercise == 'yes' or keep_exercise == '':
                        routine.append(exercise)
                        print(f'Keeping {exercise}.')
                        continue
                    else:
                        exercise = variant
                        routine.append(variant)
                        print(f'Doing {exercise} instead.')
                else:
                    continue
            else:
                routine.append(exercise)
    return routine


def log_exercises(routine, workout_number, workout_date):
    """Log the exercises done."""
    exercises = tracking[active_user]['exercises']
    if tracking[active_user]['workouts'][-2]:
        if 'workout_notes' in tracking[active_user]['workouts'][-2].keys():
            if tracking[active_user]['workouts'][-2]['workout_notes'] != '':
                print('\nNotes from last session:')
                print(
                    f"{tracking[active_user]['workouts'][-2]['workout_notes']}"
                        )
                input('\nPress ENTER to continue.')

    for exercise in exercises.keys():
        if exercise in routine:
            if 'workouts' not in exercises[exercise].keys():
                first_time_exercise(
                    exercises, exercise, routine, workout_number
                        )
                continue_routine = pyip.inputYesNo(
                    'Move to next exercise? (y/n) ', blank=True
                        )
                if continue_routine == 'no':
                    show_workout_summary(workout_number)
            else:
                log_exercise(exercises, exercise, workout_number)
                continue_routine = pyip.inputYesNo(
                    'Move to next exercise? (y/n) ', blank=True
                        )
                if continue_routine == 'no':
                    show_workout_summary(workout_number)
    show_workout_summary(workout_number)


def first_time_exercise(exercises, exercise, routine, wk_number):
    """Log exercise if it's the first time."""
    print(f'\nExercise: {exercise}')
    weight_lifted = pyip.inputFloat('Input weight lifted: ')
    amount = pyip.inputFloat('Input seconds or reps done: ')
    exercises[exercise]['sessions_done'].append(wk_number)
    exercises[exercise]['workouts'] = {
        wk_number: {'weight_lifted': weight_lifted, 'amount': amount}
            }
    vol = weight_lifted * amount
    exercises[exercise]['workouts'][wk_number]['volume'] = vol
    print(f'Volume moved: {vol}\n')		
    exercises[exercise]['workouts'][wk_number]['notes'] = \
        pyip.inputStr('\nNotes for this exercise: ', blank=True)
    the_program.write_to_tracking(TRACK_FILE, tracking)


def show_workout_summary(workout_number):
    """
    Show a summary of the workout.
    Allows suggesting a change in weight next time.
    """
    input('Press ENTER to see workout summary.')
    exercises = tracking[active_user]['exercises']
    notes = tracking[active_user]['workouts'][-1]

    for exercise in exercises:
        if 'workouts' in exercises[exercise].keys():
            if workout_number in exercises[exercise]['workouts'].keys():
                workout = exercises[exercise]["workouts"][workout_number]
                prev_workouts = exercises[exercise]["sessions_done"]
                prev_workout_list = []
                if 5 > len(prev_workouts) > 1:
                    for item in prev_workouts[0:-1]:
                        prev_workout_list.append(item)
                if len(prev_workouts) >= 5:
                    for item in prev_workouts[-4:-1]:
                        prev_workout_list.append(item)
                previous_weight, previous_amount, previous_volume = [], [], []

                for num in prev_workout_list:
                    wkout_path = exercises[exercise]["workouts"][str(num)]
                    previous_weight.append(str(wkout_path['weight_lifted']))
                    previous_amount.append(str(wkout_path['amount']))
                    previous_volume.append(str(wkout_path['volume']))	
            
                print(f'\n{exercise}:')
                print(f'Weight lifted: {workout["weight_lifted"]}', end="\t")
                print(
                    f'Previous 3 sessions: {", ".join(previous_weight[::-1])}'
                        )
                print(f'Reps or seconds: {workout["amount"]}', end="\t")
                print(
                    f'Previous 3 sessions: {", ".join(previous_amount[::-1])}'
                        )
                print(f'Volume: {workout["volume"]}', end="\t\t")
                print(
                    f'Previous 3 sessions: {", ".join(previous_volume[::-1])}'
                        )
                print(f'\nNotes from this session: {workout["notes"]}')
                change = pyip.inputYesNo(
                    '\nChange weight amount for next session? ', blank=True
                        )
                if change == 'yes':
                    exercises[exercise]['workouts'][workout_number]\
                        ["weight_change"] = pyip.inputFloat(
                            "Enter new weight: "
                            )
    prompt_notes = pyip.inputYesNo(
        'Would you like to leave notes for this workout session? '
            )
    if prompt_notes == 'yes':
        notes['workout_notes'] = pyip.inputStr('Notes: ')    
    the_program.write_to_tracking(TRACK_FILE, tracking)			
    input('Press ENTER to return to main menu.')
    show_menu()


def log_exercise(exercises, exercise, workout_number):
    """Log an exercise."""
    print(f'\nExercise: {exercise}')
    last_done = exercises[exercise]['sessions_done'][-1]
    workout = exercises[exercise]['workouts']
    last_weight = workout[str(last_done)]['weight_lifted']
    if "notes" in workout[str(last_done)].keys():
        last_notes = workout[str(last_done)]['notes']
        if last_notes != '':
            print('\nNotes from last time:')
            print(last_notes)
            input('Press ENTER to continue.')
    print(f'\nLifted last time: {last_weight}')

    if "weight_change" in workout[str(last_done)].keys():
        print('Suggested change from last session:')
        print(f'{workout[str(last_done)]["weight_change"]}')
    print('')
    if exercises[exercise]['exercise_type'] == 'Weights':
        change = pyip.inputYesNo('Change? (y/n) ', blank=True)
        if change == 'yes':
            new_weight = pyip.inputFloat('Weight to lift: ')
        else:
            new_weight = last_weight
    else:
        new_weight = \
            tracking[active_user]['workouts'][-1]['workout_weight']
        change = pyip.inputYesNo(
            f'Setting to body weight {new_weight}.\n'
            'Change? (y/n) ', blank=True
                )
        if change == 'yes':
            new_weight = pyip.inputFloat('Weight to lift: ')
    reps_done = pyip.inputFloat('\nSeconds or reps done: ')
    exercises[exercise]['sessions_done'].append(workout_number)
    workout[workout_number] = {	 
            'weight_lifted': new_weight,
            'amount': reps_done
                }
    vol = new_weight * reps_done			
    workout[workout_number]['volume'] = vol
    print(f'Volume moved: {vol}')
    workout[workout_number]['notes'] = \
        pyip.inputStr('Notes for this exercise: ', blank=True)
    the_program.write_to_tracking(TRACK_FILE, tracking)


def view_a_previous_workout():
    """View a user's previous workouts."""
    while True:
        workouts = tracking[active_user]['workouts']
        exercises = tracking[active_user]['exercises']
        workout_list = []
        for workout in workouts:
            if workout["workout_date"] not in workout_list:
                workout_list.append(workout["workout_date"])
        choice = pyip.inputMenu(workout_list, numbered=True)
        for workout in workouts:
            if choice in workout["workout_date"]:
                new_choice = str(workout["workout_number"])
                break
        if 'workout_notes' in workout.keys():
            print('\nSession Notes:')
            print(workout['workout_notes'])
            input(f'Enter to continue.')
        if "workout_weight" in workout.keys():	
            print(f'\nWeight at date of workout: {workout["workout_weight"]}')
        
        for exercise in exercises:
            if new_choice in exercises[exercise]["workouts"].keys():
                choice_str = exercises[exercise]["workouts"][new_choice]
                print(f'\n{exercise}')
                print(f'Weight lifted: {choice_str["weight_lifted"]}')
                print(f'Reps/seconds: {choice_str["amount"]}')
                print(f'Volume: {choice_str["volume"]}')
                if "notes" in choice_str.keys():
                    print(f'Notes: {choice_str["notes"]}')
                input(f'Enter to continue.')
        verify = pyip.inputYesNo('View another session? ', blank=True)
        if verify == 'no' or verify == '':
            break
    show_menu()

the_program = shinsai.Program()

tracking = the_program.get_stored_tracking(TRACK_FILE)
active_user = greeting()
show_menu()