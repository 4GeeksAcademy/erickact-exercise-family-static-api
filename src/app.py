"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():
    try:
        # this is how you can use the Family datastructure by calling its methods
        members = jackson_family.get_all_members()
    
        if members == []:
            return jsonify({"msg": "Members not found"}), 404

        return jsonify(members), 200
         
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if not member:
            return jsonify({"msg": "Member not found"}), 404

        return jsonify({"member": member}), 200
        
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        delete_member = jackson_family.delete_member(member_id)

        if not delete_member:
            return jsonify({"msg": "Member not found"}), 404
        return jsonify({'done':True}), 200
        
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@app.route('/member', methods=['POST'])
def add_member():
    try:
        new_member = request.get_json()

        if not new_member:
            return jsonify({"error": "Invalid input"}), 400
        
        updated_members = jackson_family.add_member(new_member)

        return jsonify({"members": updated_members}), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
