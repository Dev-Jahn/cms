from flask import request, send_file
from flask_restplus import Resource, reqparse
from flask_jwt_extended import jwt_required
from sqlalchemy.orm.exc import NoResultFound

from router.dto.data_dto import ImageMetadataDTO
from service.data.image_service import create_image_metadata, read_image_metadata

api = ImageMetadataDTO.api
_image_metadata = ImageMetadataDTO.model

parser_path = reqparse.RequestParser()
parser_path.add_argument('path', type=str, location='args', required=True)

# TODO
# created 시간 쿼리 가능하게 수정
parser_metadata = reqparse.RequestParser()
parser_metadata.add_argument('cell', type=str, location='args', required=False)
parser_metadata.add_argument('path', type=str, location='args', required=False)
parser_metadata.add_argument('device', type=str, location='args', required=False)
parser_metadata.add_argument('created', type=str, location='args', required=False)
parser_metadata.add_argument('created_by', type=str, location='args', required=False)
parser_metadata.add_argument('label', type=str, location='args', required=False)


@api.route('/image')
class Image(Resource):
    @api.response(404, 'No result found for query.')
    @api.produces(['image/jpg', 'image/png'])
    @api.expect(parser_path)
    @jwt_required()
    def get(self):
        try:
            path = parser_path.parse_args().get('path')
            return send_file('/data/' + path, mimetype='image/jpg')
        except NoResultFound as e:
            api.abort(404, message=f'Cannot find image.', reason=str(type(e)))
        except Exception as e:
            api.abort(500, message=f'Something went wrong.', reason=str(type(e)))

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

    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.expect(parser_path)
    @jwt_required()
    def delete(self):
        try:
            args = parser_path.parse_args()
            return delete_image(**args)
        except NoResultFound as e:
            api.abort(400, message=f'Cannot find image<{args.get("path")}>.', reason=str(type(e)))
        except Exception as e:
            api.abort(500, message='Something went wrong.', reason=str(type(e)))


@api.route('/image/metadata')
class ImageMetadata(Resource):
    @api.response(404, 'No result found for query.')
    @api.marshal_list_with(_image_metadata, envelope='data')
    @jwt_required()
    def get(self):
        try:
            return read_image_metadata({
            })
        except Exception:
            api.abort(404)

    @api.response(201, 'Created')
    @api.response(400, 'Bad Request')
    @api.expect(_image_metadata, validate=True)
    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            return create_image_metadata(**data)
        except NoResultFound:
            api.abort(400, message=f'Cannot find result for keys.')
        except Exception:
            api.abort(500, message='Failed to register image')
