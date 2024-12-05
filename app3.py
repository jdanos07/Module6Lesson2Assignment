from flask import jsonify, request, Flask
from marshmallow import ValidationError, fields
from mysqlConnect import connect_database, Error
from flask_marshmallow import Marshmallow

app2 = Flask(__name__)
ma = Marshmallow(app2)

class WorkoutSchema(ma.Schema):
    date = fields.String(required=True)
    duration_minutes = fields.String(required=True)
    calories_burned = fields.String(required=True)

    class Meta:
        fields = ('duration_minutes', 'date', 'member_id', 'workout_id', 'calories_burned')

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

@app2.route('/')
def home():
    return "Fitness Center Database"

@app2.route('/workouts/<int:member_id>', methods=['POST'])
def add_workout(member_id):
    try:
        workout_data = workout_schema.load(request.json)

    except ValidationError as e:
        print(f'Error: {e}')
        return jsonify(e.messages), 400
        
    try:
        conn = connect_database()
        if conn is None:
            return jsonify({'error': 'Database connection failed.'}), 500
        cursor = conn.cursor()

        new_workout = (member_id, workout_data['duration_minutes'], workout_data['calories_burned'], workout_data['date'])

        query = 'INSERT INTO workoutsessions (member_id, duration_minutes, calories_burned, date) VALUES (%s, %s, %s, %s)'

        cursor.execute(query, new_workout)
        conn.commit()
        return jsonify ({'message': 'New workout recorded successfully.'}), 200
    
    except Error as e:
        print(f'Error: {e}')

        return jsonify({'message': 'Internal server error.'}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app2.route('/workouts', methods=['GET'])
def get_workouts():
    try:
        conn = connect_database()
        if conn is None:
            return jsonify({'error': 'Database conn failed.'}), 500
        cursor = conn.cursor(dictionary=True)

        query = 'SELECT * FROM workoutsessions'

        cursor.execute(query)
        
        workouts = cursor.fetchall()

        return workouts_schema.jsonify(workouts)    

    except Error as e:
        print(f'Error: {e}')
        return jsonify({'message': 'Internal server error.'}), 500
    
    finally:
        if conn and conn.is_connected:
            cursor.close()
            conn.close()

@app2.route('/workouts/<int:member_id>/<int:workout_id>', methods=['GET'])
def get_workout_details(member_id, workout_id):
    try:
        conn = connect_database()
        if conn is None:
            return jsonify({'error': 'Database connection failed.'}), 500
        cursor = conn.cursor(dictionary=True)

        workout_detail = (member_id, workout_id)
        query = 'SELECT * FROM workoutsessions WHERE member_id = %s AND workout_id = %s;'
        
        cursor.execute(query, (workout_detail))
        
        workout = cursor.fetchone()
        
        
        if not workout:
            print('Workout not found.')
            return jsonify({'error': 'Workout not found.'}), 404
        
        return workout_schema.jsonify(workout), 200       
    
    except Error as e:
        print(f'Error: {e}')
        return jsonify({'message': 'Internal server error.'}), 500
    
    finally:
        if conn and conn.is_connected:
            cursor.close()
            conn.close()

@app2.route('/workouts/<int:member_id>/<int:workout_id>', methods=['PUT'])
def update_member(member_id, workout_id):
    try:
        workout_data = workout_schema.load(request.json)

    except ValidationError as e:
        print(f'Error: {e}')
        return jsonify(e.messages), 400
        
    try:
        conn = connect_database()
        if conn is None:
            return jsonify({'error': 'Database connection failed.'}), 500
        cursor = conn.cursor(dictionary=True)

        updated_workout = (workout_data['duration_minutes'], workout_data['calories_burned'], workout_data['date'], member_id, workout_id)

        query = 'UPDATE workoutsessions SET duration_minutes = %s, calories_burned = %s, date = %s WHERE member_id = %s AND workout_id = %s'

        cursor.execute(query, updated_workout)

        conn.commit()
        return jsonify({'message': 'Workout details update successfully'}), 200
       
    
    except Error as e:
        print(f'Error: {e}')

        return jsonify({'message': 'Internal server error.'}), 500
    
    finally:
        if conn and cursor:
            cursor.close()
            conn.close()

@app2.route('/workouts/<int:member_id>/<int:workout_id>', methods=['DELETE'])
def delete_workout(member_id, workout_id):
    try:
        conn = connect_database()
        if conn is None:
            return jsonify({'error': 'Database conn failed.'}), 500
        cursor = conn.cursor()

        workout_to_remove = (member_id, workout_id)

        query = 'DELETE FROM workoutsessions WHERE member_id = %s AND workout_id = %s'

        cursor.execute(query, workout_to_remove)
        conn.commit()
        return jsonify ({'message': 'Workout session deleted successfully.'}), 200
    
    except Error as e:
        print(f'Error: {e}')
        return jsonify({'message': 'Internal server error.'}), 500
    
    finally:
        if conn and cursor:
            cursor.close()
            conn.close()


if __name__=='__main__':
    app2.run(debug=True)
