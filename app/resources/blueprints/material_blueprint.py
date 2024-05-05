from flask import jsonify 
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, current_user

from resources.data import system_db
from resources.models import MaterialModel, MaterialSchema, UserRoleEnum 

MaterialBlueprint = Blueprint('material', __name__, url_prefix='/api/material')

@MaterialBlueprint.route('/')
class RootMaterialMethodView(MethodView):
    @jwt_required()
    @MaterialBlueprint.response(200, MaterialSchema(many=True))
    def get(self):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get this information.')

        materials = MaterialModel.query.all()
        return materials

    @jwt_required()
    @MaterialBlueprint.arguments(MaterialSchema)
    @MaterialBlueprint.response(201, MaterialSchema)
    def post(self, new_material_data):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get materials information.')

        materials = MaterialModel(**new_material_data) 

        system_db.session.add(materials)
        system_db.session.commit()

        return materials
    
@MaterialBlueprint.route('/<int:material_id>')
class SingleMaterialMethodView(MethodView):
    @jwt_required()
    @MaterialBlueprint.response(200, MaterialSchema)
    def get(self, material_id):
        material = MaterialModel.query.get(material_id)
        if not material:
            abort(404, message='material not found.')

        return material

    @jwt_required()
    @MaterialBlueprint.arguments(MaterialSchema)
    @MaterialBlueprint.response(200, MaterialSchema)
    def put(self, material_data, material_id):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get material information.')

        db_material = MaterialModel.query.get(material_id)
        if not db_material:
            abort(404, message='material not found.')

        if 'name' in material_data:
            db_material.name = material_data['name']

        if 'description' in material_data:
            db_material.description = material_data['description']

        if 'price_per_kg' in material_data:
            db_material.price_per_kg = material_data['price_per_kg']

        system_db.session.add(db_material)
        system_db.session.commit()

        return material_data

    @jwt_required()
    @MaterialBlueprint.response(201, MaterialSchema)
    def delete(self, material_id):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get material information.')

        db_material = MaterialModel.query.get(material_id)
        if not db_material:
            abort(404, message='material not found.')

        system_db.session.delete(db_material)
        system_db.session.commit()

        return db_material

