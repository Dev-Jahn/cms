from flask import request, send_file
from flask_restplus import Resource
from flask_jwt_extended import jwt_required
from sqlalchemy.orm.exc import NoResultFound

from router.dto.data_dto import ImageMetadataDTO
from service.data.image_service import create_image, read_image_path

api = ImageMetadataDTO.api
_image_metadata = ImageMetadataDTO.model


@api.route('/image/<path>')
@api.doc(params={'path': 'Image path'})
class Image(Resource):
    @api.doc('Query image binary with path')
    @api.response(404, 'No result found for query.')
    @api.produces(['image/jpg', 'image/png'])
    @jwt_required()
    def get(self, path):
        try:
            return send_file('/data/' + path, mimetype='image/jpg')
        except Exception:
            api.abort(404)

    @api.doc('Create new image')
    @api.response(201, 'Created')
    @api.response(400, 'Bad Request')
    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            return create_image(data)
        except NoResultFound:
            api.abort(400, message=f'Cannot find result for keys.')
        except Exception:
            api.abort(500, message='Failed to register image')


@api.route('/image')
class ImageMetadata(Resource):
    @api.doc('Query image path with filters')
    @api.response(404, 'No result found for query.')
    @api.marshal_list_with(_image_metadata, envelope='data')
    @jwt_required()
    def get(self):
        try:
            return read_image_path({
                'cell': request.args.get('cell'),
                'path': request.args.get('path'),
                'device': request.args.get('device'),
                'created': request.args.get('created'),
                'created_by': request.args.get('created_by'),
                'label': request.args.get('label'),
                'offset_x': request.args.get('offset_x'),
                'offset_y': request.args.get('offset_y'),
                'offset_z': request.args.get('offset_z'),
                'pos_x': request.args.get('pos_x'),
                'pos_y': request.args.get('pos_y'),
                'pos_z': request.args.get('pos_z'),
            })
        except Exception:
            api.abort(404)

    @api.doc('Create new image record')
    @api.response(201, 'Created')
    @api.response(400, 'Bad Request')
    @api.expect(_image_metadata, validate=True)
    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            return create_image(data)
        except NoResultFound:
            api.abort(400, message=f'Cannot find result for keys.')
        except Exception:
            api.abort(500, message='Failed to register image')
