from datetime import date
from ntpath import join
from flask_app import app
from flask import render_template, redirect, request, session, flash
import flask_app
from flask_app.model.user_model import User
from flask_app.model.workout_model import Workout



## WORKOUT DASHBOARD
@app.route('/workouts')
def workouts_listed():
    if not "user_id" in session:
        return redirect('/registration_page')
    user = User.get_by_id({'id': session['user_id']})
    return render_template('workouts.html', user=user)


## CREATE WORKOUT
@app.route('/workouts/new')
def new_workout_form():
    if not "user_id" in session:
        return redirect('/registration_page')
    return render_template('workout_new.html')

@app.route('/workouts/create', methods=['POST'])
def create_workout():
    if not "user_id" in session:
        return redirect('/registration_page')
    if not Workout.validator(request.form):
        return redirect('/workouts/new')
    ## if form is good, add user id into our data -> know who created it
    data = {
        **request.form,
        'user_id' : session['user_id']
    }
    Workout.create(data)
    return redirect('/welcome')


## DELETE WORKOUT
@app.route('/workouts/<int:id>/delete')
def delete_workout(id):
    if not "user_id" in session:
        return redirect('/registration_page')
    data = {
        'id' : id
    }
    to_be_deleted = Workout.get_workout_by_id(data)
    if not session['user_id'] == to_be_deleted.user_id:
        flash("Cannot delete another user's workout.")
        return redirect('/registration_page')
    Workout.delete(data)
    return redirect ('/welcome')


## EDIT A WORKOUT
@app.route('/workouts/<int:id>/edit')
def edit_workout_form(id):
    if not "user_id" in session:
        return redirect('/registration_page')
    workout = Workout.get_workout_by_id({'id': id})
    user = User.get_by_id({'id':session['user_id']})
    return render_template('workout_edit.html', workout=workout, user=user)

@app.route('/workouts/<int:id>/update', methods=['POST'])
def update_workout(id):
    if not "user_id" in session:
        return redirect('/registration_page')
    if not Workout.validator(request.form):
        return redirect(f'/workout/{id}/edit')
    data = {
        **request.form,
        'id': id
    }
    Workout.update(data)
    return redirect('/welcome')


## SHOW ONE WORKOUT BY ID
@app.route('/workouts/<int:id>')
def show_one_workout(id):
    if not "user_id" in session:
        return redirect('/registration_page')
    data = {
        'id' : id
    }
    user = User.get_by_id({'id':session['user_id']})
    workout = Workout.get_by_id_join(data)
    return render_template('show_one_workout.html', workout=workout, user=user)


## SHOW ALL WORKOUTS BY DATE
@app.route('/workouts/<date>/by_date')
def show_workout_by_date(date):
    if not "user_id" in session:
        return redirect('/registration_page')
    data = {
        'date' : date
    }
    user = User.get_by_id({'id':session['user_id']})
    workouts = Workout.get_workout_by_date_join(data)
    return render_template('show_workouts_by_date.html', workouts=workouts, user=user)


## ADMIN COMMENT ON WORKOUT
@app.route('/workouts/<int:id>/comment')
def new_comment_form(id):
    if not "user_id" in session:
        return redirect('/registration_page')
    data = {
        'id' : id
    }
    user = User.get_by_id({'id':session['user_id']})
    workout = Workout.get_workout_by_id(data)
    return render_template('comment_on.html', workout=workout, user=user)

@app.route('/workouts/<int:id>/create_comment', methods=['POST'])
def leave_comment(id):
    if not "user_id" in session:
        return redirect('/registration_page')
    if not Workout.comment_validator(request.form):
        return redirect(f'/workouts/{id}/comment')
    data = {
        **request.form,
        'id' : id,
        'user_id' : session['user_id']
    }
    Workout.leave_comment(data)
    return redirect('/welcome')





## VIEW WORKOUTS
@app.route('/workouts/squats')
def squats_video():
    if not "user_id" in session:
        return redirect('/')
    user = User.get_by_id({'id': session['user_id']})
    return render_template('workouts_squats.html', user=user)

@app.route('/workouts/chest_presses')
def chest_presses_video():
    if not "user_id" in session:
        return redirect('/')
    user = User.get_by_id({'id': session['user_id']})
    return render_template('workouts_chest_presses.html', user=user)

@app.route('/workouts/core')
def core_video():
    if not "user_id" in session:
        return redirect('/')
    user = User.get_by_id({'id': session['user_id']})
    return render_template('workouts_core.html', user=user)

@app.route('/workouts/rdl')
def rdl_video():
    if not "user_id" in session:
        return redirect('/')
    user = User.get_by_id({'id': session['user_id']})
    return render_template('workouts_rdl.html', user=user)

@app.route('/workouts/warm_ups')
def warm_ups_video():
    if not "user_id" in session:
        return redirect('/')
    user = User.get_by_id({'id': session['user_id']})
    return render_template('workouts_warm_ups.html', user=user)

@app.route('/workouts/self_asssessments')
def self_assessment_video():
    if not "user_id" in session:
        return redirect('/')
    user = User.get_by_id({'id': session['user_id']})
    return render_template('workouts_self_assessments.html', user=user)

@app.route('/workouts/regression')
def regression_video():
    if not "user_id" in session:
        return redirect('/')
    user = User.get_by_id({'id': session['user_id']})
    return render_template('workouts_regression.html', user=user)

@app.route('/workouts/mistakes')
def mistakes_video():
    if not "user_id" in session:
        return redirect('/')
    user = User.get_by_id({'id': session['user_id']})
    return render_template('workouts_mistakes.html', user=user)