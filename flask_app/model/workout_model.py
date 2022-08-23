from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.model import user_model
from flask_app import DATABASE


class Workout:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.date = data['date']
        self.reps = data['reps']
        self.description = data['description']
        self.comments = data['comments']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']


    ## CLASS METHODS:
    @classmethod
    def create(cls, data):
        query = "INSERT INTO workouts (name, date, reps, description, user_id) VALUES ( %(name)s, %(date)s, %(reps)s, %(description)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE workouts SET name = %(name)s, date = %(date)s, reps = %(reps)s, description = %(description)s" \
            "WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM workouts WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_workout_with_users(cls, data):
        query = "SELECT * FROM workouts JOIN users on users.id = workouts.user_id WHERE workouts.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1:
            return False
        row = results[0]
        this_workout = cls(row)
        user_data = {
            **row,
            'id' : row['users.id'],
            'created_at' : row['users.created_at'],
            'updated_at' : row['users.updated_at']
        }
        workout_athlete = user_model.User(user_data)
        this_workout.athlete = workout_athlete
        return this_workout

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM workouts JOIN users ON users.id = workouts.user_id ORDER BY date DESC;"
        results =  connectToMySQL(DATABASE).query_db(query)
        if results:
            all_workouts = []
            for row_in_db in results:
                this_workout = cls(row_in_db)
                user_data = {
                    **row_in_db,
                    'id' : row_in_db['users.id'],
                    'created_at' : row_in_db['users.created_at'],
                    'updated_at' : row_in_db['users.updated_at']
                }
                this_user = user_model.User(user_data)
                this_workout.athlete = this_user
                all_workouts.append(this_workout)
            return all_workouts
        return results

    @classmethod
    def get_workout_by_id(cls, data):
        query = "SELECT * FROM workouts WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id_join(cls, data):
        query = "SELECT * FROM workouts LEFT JOIN users ON users.id = workouts.user_id WHERE workouts.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1:
            return False
        row_in_db = results[0]
        this_workout = cls(row_in_db)
        user_data = {
            **row_in_db,
            'id' : row_in_db['users.id'],
            'created_at' : row_in_db['users.created_at'],
            'updated_at' : row_in_db['users.updated_at']
        }
        workout_athlete = user_model.User(user_data)
        this_workout.athlete = workout_athlete
        return this_workout

    @classmethod
    def get_workout_by_date(cls, data):
        query = "SELECT * FROM workouts WHERE date = %(date)s ORDER BY date DESC;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1:
            return False
        workout_list = []
        for result in results:
            result_instance = cls(result)
            workout_list.append(result_instance)
        print(workout_list)
        return workout_list


    @classmethod
    def get_workout_by_date_join(cls, data):
        query = "SELECT * FROM workouts LEFT JOIN users ON users.id = workouts.user_id WHERE date = %(date)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1:
            return False
        if results:
            row = results[0]
            this_workout = cls(row)
            user_data = {
                **row,
                'id' : row['users.id'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }
        workout_athlete = user_model.User(user_data)
        this_workout.athlete = workout_athlete
        return this_workout

    @classmethod
    def leave_comment(cls, data):
        query = "UPDATE workouts SET comments = %(comments)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)






    ## STATIC METHODS:
    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data['name']) < 1:
            is_valid = False
            flash('Workout name is required')
        if len(form_data['date']) < 1:
            is_valid = False
            flash('Please fill in the date you completed this workout')
        if len(form_data['reps']) < 1:
            is_valid = False
            flash('Please fill in the number of reps you completed')
        # if "complete" not in form_data:
        #     is_valid = False
        #     flash("Please mark if you completed the workout")
        if len(form_data['description']) < 1:
            is_valid = False
            flash('Please add some notes to your description. How many reps, how you were feelings, etc.')
        return is_valid

    @staticmethod
    def comment_validator(form_data):
        is_valid = True
        if len(form_data['comments']) < 1:
            is_valid = False
            flash('Please add some notes to your comments.')
        return is_valid