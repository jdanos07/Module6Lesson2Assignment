from flask import jsonify, request, Flask
from marshmallow import ValidationError, fields
from mysqlConnect import connect_database, Error
from flask_marshmallow import Marshmallow

app = Flask(__name__)
ma = Marshmallow(app)

class MemberSchema(ma.Schema):
    name = fields.String(required=True)
    age = fields.String(required=True)
    
    class Meta:
        fields = ('name', 'age', 'id')

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

@app.route('/')
def home():
    return "Fitness Center Database"

@app.route('/members', methods=['POST'])
def add_member():
    try:
        member_data = member_schema.load(request.json)

    except ValidationError as e:
        print(f'Error: {e}')
        return jsonify(e.messages), 400
        
    
    try:
        conn = connect_database()
        if conn is None:
            return jsonify({'error': 'Database connection failed.'}), 500
        cursor = conn.cursor()

        new_member = (member_data['name'], member_data['age'])

        query = 'INSERT INTO Members (name, age) VALUES (%s, %s)'

        cursor.execute(query, new_member)
        conn.commit()
        return jsonify ({'message': 'New Member registered successfully.'}), 200
    
    except Error as e:
        print(f'Error: {e}')

        return jsonify({'message': 'Internal server error.'}), 500
    
    finally:
        if conn and conn.is_connected:
            cursor.close()
            conn.close()

@app.route('/members', methods=['GET'])
def get_members():
    try:
        conn = connect_database()
        if conn is None:
            return jsonify({'error': 'Database conn failed.'}), 500
        cursor = conn.cursor(dictionary=True)

        query = 'SELECT * FROM Members'

        cursor.execute(query)
        
        members = cursor.fetchall()

        return members_schema.jsonify(members)    

    except Error as e:
        print(f'Error: {e}')
        return jsonify({'message': 'Internal server error.'}), 500
    
    finally:
        if conn and conn.is_connected:
            cursor.close()
            conn.close()

@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    try:
        conn = connect_database()
        if conn is None:
            return jsonify({'error': 'Database connection failed.'}), 500
        cursor = conn.cursor(dictionary=True)

        query = 'SELECT * FROM Members WHERE id = %s;'
        
        cursor.execute(query, (id,))
        
        member = cursor.fetchone()
        
        
        if not member:
            print('Member not found.')
            return jsonify({'error': 'Member not found.'}), 404
        
        return member_schema.jsonify(member), 200       
    
    except Error as e:
        print(f'Error: {e}')
        return jsonify({'message': 'Internal server error.'}), 500
    
    finally:
        if conn and conn.is_connected:
            cursor.close()
            conn.close()

@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    try:
        member_data = member_schema.load(request.json)

    except ValidationError as e:
        print(f'Error: {e}')
        return jsonify(e.messages), 400
        
    try:
        conn = connect_database()
        if conn is None:
            return jsonify({'error': 'Database connection failed.'}), 500
        cursor = conn.cursor(dictionary=True)

        updated_member = (member_data['name'], member_data['age'], id)

        query = 'UPDATE Members SET name = %s, age = %s WHERE id = %s'

        cursor.execute(query, updated_member)

        conn.commit()
        return jsonify({'message': 'Member details update successfully'}), 200
       
    
    except Error as e:
        print(f'Error: {e}')

        return jsonify({'message': 'Internal server error.'}), 500
    
    finally:
        if conn and cursor:
            cursor.close()
            conn.close()

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    try:
        conn = connect_database()
        if conn is None:
            return jsonify({'error': 'Database conn failed.'}), 500
        cursor = conn.cursor()

        member_to_remove = (id,)

        query = 'DELETE FROM Members where id = %s'

        cursor.execute(query, member_to_remove)
        conn.commit()
        return jsonify ({'message': 'Member deleted successfully.'}), 200
    
    except Error as e:
        print(f'Error: {e}')
        return jsonify({'message': 'Internal server error.'}), 500
    
    finally:
        if conn and cursor:
            cursor.close()
            conn.close()


if __name__=='__main__':
    app.run(debug=True)

