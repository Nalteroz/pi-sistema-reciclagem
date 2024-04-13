from flask import jsonify 
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, create_access_token, current_user

from bcrypt import hashpw, gensalt, checkpw

from resources.data import system_db
from resources.models import CollaboratorModel, CollaboratorSchema, UserRoleEnum 

CollaboratorBlueprint = Blueprint('collaborator', __name__, url_prefix='/collaborator')

@CollaboratorBlueprint.route('/')
class RootCollaboratorMethodView(MethodView):
    """
        Root route, for collaborator creation and listing.
    """
    @jwt_required()
    @CollaboratorBlueprint.response(200, CollaboratorSchema(many=True))
    def get(self):
        """
            Return all collaborators on the system, depending on the user's role.
        """
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get collaborators information.')

        collaborators = CollaboratorModel.query.all()
        return collaborators

    @jwt_required()
    @CollaboratorBlueprint.arguments(CollaboratorSchema)
    @CollaboratorBlueprint.response(201, CollaboratorSchema)
    def post(self, new_collaborator):
        """
            Create a new collaborator.

            Arguments:
            ------------
            new_collaborator : dictionary of collaborator information
        """
        
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get collaborators information.')

        if CollaboratorModel.query.filter_by(name=new_collaborator['name'], surname = new_collaborator['surname']).first():
            abort(409, message='Collaborator already exists. If you want to reactivate and you are an admin, update the collaborator instead.')

        collaborator = CollaboratorModel(**new_collaborator) 

        system_db.session.add(collaborator)
        system_db.session.commit()

        return collaborator
    
@CollaboratorBlueprint.route('/<int:collaborator_id>')
class SingleCollaboratorMethodView(MethodView):
    """
        Route for a single collaborator operations.
    """
    @jwt_required()
    @CollaboratorBlueprint.response(200, CollaboratorSchema)
    def get(self, collaborator_id):
        """
            Return a single collaborator information.
        """

        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get collaborators information.')

        collaborator = CollaboratorModel.query.get(collaborator_id)
        if not collaborator:
            abort(404, message='Collaborator not found.')

        return collaborator

    @jwt_required()
    @CollaboratorBlueprint.arguments(CollaboratorSchema)
    @CollaboratorBlueprint.response(200, CollaboratorSchema)
    def put(self, collaborator, collaborator_id):
        """
            Update a collaborator information.

            Arguments:
            ------------
            collaborator_id : int
            collaborator : dictionary of collaborator information
        """ 
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get collaborators information.')

        dbcollaborator = CollaboratorModel.query.get(collaborator_id)
        if not dbcollaborator:
            abort(404, message='Collaborator not found.')

        if 'name' in collaborator:
            dbcollaborator.name = collaborator['name']

        if 'surname' in collaborator:
            dbcollaborator.surname = collaborator['surname']

        if 'date_of_birth' in collaborator:
            dbcollaborator.date_of_birth = collaborator['date_of_birth']

        if 'role' in collaborator:
            dbcollaborator.role = collaborator['role']

        system_db.session.add(dbcollaborator)
        system_db.session.commit()

        return collaborator

    @jwt_required()
    @CollaboratorBlueprint.response(201, CollaboratorSchema)
    def delete(self, collaborator_id):
        """
            Delete a collaborator.

            Arguments:
            ------------
            collaborator_id : int
        """
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get collaborators information.')

        dbcollaborator = CollaboratorModel.query.get(collaborator_id)
        if not dbcollaborator:
            abort(404, message='Collaborator not found.')

        system_db.session.delete(dbcollaborator)
        system_db.session.commit()

        return dbcollaborator

