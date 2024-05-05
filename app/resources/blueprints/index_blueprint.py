from flask import render_template, redirect
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required

from ..models import UserModel, TruckModel, StorageHistoryModel, ClientModel, CollaboratorModel, MaterialModel, MaterialCollectSiteModel, MaterialCollectionModel, MaterialTriageModel, TransactionModel

IndexBlueprint = Blueprint('index', 'index', url_prefix='/', template_folder='app/resources/templates')

class Utils:
    def GetElementName(element_name):
        name_dict = {
            'user': 'usuário',
            'truck': 'caminhão',
            'storage_history': 'armazém',
            'client': 'cliente',
            'collaborator': 'colaborador',
            'material': 'material',
            'material_collect_site': 'local de coleta',
            'material_collection': 'coleta de material',
            'material_triage': 'triagem de material',
            'transaction': 'transação comercial'
        }

        return name_dict.get(element_name, None)
    
    def GetColumnNames(element_name):
        if element_name == 'user':
            return UserModel.GetColumnsNames()
        elif element_name == 'truck':
            return TruckModel.GetColumnsNames()
        elif element_name == 'storage_history':
            return StorageHistoryModel.GetColumnsNames()
        elif element_name == 'client':
            return ClientModel.GetColumnsNames()
        elif element_name == 'collaborator':
            return CollaboratorModel.GetColumnsNames()
        elif element_name == 'material':
            return MaterialModel.GetColumnsNames()
        elif element_name == 'material_collect_site':
            return MaterialCollectSiteModel.GetColumnsNames()
        elif element_name == 'material_collection':
            return MaterialCollectionModel.GetColumnsNames()
        elif element_name == 'material_triage':
            return MaterialTriageModel.GetColumnsNames()
        elif element_name == 'transaction':
            return TransactionModel.GetColumnsNames()
        else:
            return None

@IndexBlueprint.route('/')
class Index(MethodView):
    @jwt_required()
    def get(self):
       return ElementView.get(self, 'user')

@IndexBlueprint.route('/element/<string:element>')
class ElementView(MethodView):
    @jwt_required()
    def get(self, element):
        element_name = Utils.GetElementName(element)
        if not element_name:
            abort(404, message='Element not found.')
        columns = Utils.GetColumnNames(element)
        if not columns:
            abort(404, message='Element columns not found.')
        context = {
            'element': element,
            'element_name': element_name,
            'data_path': '/api/' + element,
            'columns_names': columns
        }
        return render_template('element_content.html', **context)
    
@IndexBlueprint.route('/element/create/<string:element>')
class CreateElementView(MethodView):
    @jwt_required()
    def get(self, element):
        element_name = Utils.GetElementName(element)
        if not element_name:
            abort(404, message='Element not found.')
        columns = Utils.GetColumnNames(element)
        if not columns:
            abort(404, message='Element columns not found.')
        context = {
            'element': element,
            'element_name': element_name,
            'data_path': '/api/' + element,
            'columns_names': columns
        }
        return render_template('add_element.html', **context)

@IndexBlueprint.route('/login')
class Login(MethodView):
    def get(self):
        return render_template('login.html')
