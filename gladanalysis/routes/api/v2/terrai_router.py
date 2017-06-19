import os
import logging
import datetime

from flask import jsonify, request

from . import endpoints
from gladanalysis.services import GeostoreService
from gladanalysis.services import DateService
from gladanalysis.services import SqlService
from gladanalysis.services import AnalysisService
from gladanalysis.services import ResponseService
from gladanalysis.responders import ErrorResponder
from gladanalysis.validators import validate_geostore, validate_terrai_period, validate_admin, validate_use, validate_wdpa

"""TERRA I ENDPOINTS"""

@endpoints.route('/terrai-alerts', methods=['GET'])
@validate_geostore
@validate_terrai_period

def query_terrai():
    """Query Terra I"""

    logging.info('Query Terra I by Geostore')

    geostore = request.args.get('geostore', None)
    period = request.args.get('period', None)

    #format period request to julian dates
    from_year, from_date, to_year, to_date = DateService.date_to_julian_day(period)

    #grab query and download sql from sql service
    sql, download_sql = SqlService.format_terrai_sql(from_year, from_date, to_year, to_date)

    #send query to terra i elastic database
    data = AnalysisService.make_terrai_request(sql, geostore)

    #get area of request in hectares from geostore
    area = GeostoreService.make_area_request(geostore)

    #standardize response
    datasetID = '{}'.format(os.getenv('TERRAI_DATASET_ID'))
    standard_format = ResponseService.standardize_response('Terrai', data, "COUNT(day)", datasetID, download_sql, area, geostore)

    return jsonify({'data': standard_format}), 200

@endpoints.route('/terrai-alerts/admin/<iso_code>', methods=['GET'])
@validate_terrai_period
@validate_admin

def terrai_country(iso_code):

    logging.info('Running Terra I country analysis')

    period = request.args.get('period', None)

    #format period request to julian dates
    from_year, from_date, to_year, to_date = DateService.date_to_julian_day(period)

    #get query and download sql from sql format service
    sql, download_sql = SqlService.format_terrai_sql(from_year, from_date, to_year, to_date, iso_code)

    #get area in hectares of response from geostore
    area_ha = GeostoreService.make_gadm_request(iso_code)

    #send query to terra i elastic database
    data = AnalysisService.make_terrai_request(sql)

    #standardize response
    datasetID = '{}'.format(os.getenv('TERRAI_DATASET_ID'))
    standard_format = ResponseService.standardize_response('Terrai', data, "COUNT(day)", datasetID, download_sql, area_ha)

    return jsonify({'data': standard_format}), 200

@endpoints.route('/terrai-alerts/admin/<iso_code>/<admin_id>', methods=['GET'])
@validate_terrai_period
@validate_admin

def terrai_admin(iso_code, admin_id):
    logging.info('Running Terra I state analysis')

    period = request.args.get('period', None)

    #format period request to julian dates
    from_year, from_date, to_year, to_date = DateService.date_to_julian_day(period)

    #get query and download sql from sql format service
    sql, download_sql = SqlService.format_terrai_sql(from_year, from_date, to_year, to_date, iso_code, admin_id)

    #get area in hectares of request from geostore
    area_ha = GeostoreService.make_gadm_request(iso_code, admin_id)

    #send query to terra i elastic database through analysis service
    data = AnalysisService.make_terrai_request(sql)

    #standardize response
    datasetID = '{}'.format(os.getenv('TERRAI_DATASET_ID'))
    standard_format = ResponseService.standardize_response('Terrai', data, "COUNT(day)", datasetID, download_sql, area_ha)

    return jsonify({'data': standard_format}), 200

@endpoints.route('/terrai-alerts/admin/<iso_code>/<admin_id>/<dist_id>', methods=['GET'])
@validate_terrai_period
@validate_admin

def terrai_dist(iso_code, admin_id, dist_id):
    logging.info('Running Terra I Analysis on District')

    period = request.args.get('period', None)

    #format period request to julian dates
    from_year, from_date, to_year, to_date = DateService.date_to_julian_day(period)

    #get query and download sql from sql format service
    sql, download_sql = SqlService.format_terrai_sql(from_year, from_date, to_year, to_date, iso_code, admin_id, dist_id)

    #get area in hectares of request from geostore
    area_ha = GeostoreService.make_gadm_request(iso_code, admin_id, dist_id)

    #send query to terra i elastic database through analysis service
    data = AnalysisService.make_terrai_request(sql)

    #standardize response
    datasetID = '{}'.format(os.getenv('TERRAI_DATASET_ID'))
    standard_format = ResponseService.standardize_response('Terrai', data, "COUNT(day)", datasetID, download_sql, area_ha)

    return jsonify({'data': standard_format}), 200

@endpoints.route('/terrai-alerts/use/<use_type>/<use_id>', methods=['GET'])
@validate_use
@validate_terrai_period

def terrai_use(use_type, use_id):

    logging.info('Intersect Terra I and Land Use data')

    period = request.args.get('period', None)

    #format period request to julian dates
    from_year, from_date, to_year, to_date = DateService.date_to_julian_day(period)

    #get query and download sql from sql format service
    sql, download_sql = SqlService.format_terrai_sql(from_year, from_date, to_year, to_date)

    #get geostore ID and area in hectares of request from geostore
    geostore, area = GeostoreService.make_use_request(use_type, use_id)

    #send query to terra i elastic database through analysis service
    data = AnalysisService.make_terrai_request(sql, geostore)

    #standardize response
    datasetID = '{}'.format(os.getenv('TERRAI_DATASET_ID'))
    standard_format = ResponseService.standardize_response('Terrai', data, "COUNT(day)", datasetID, download_sql, area, geostore)

    return jsonify({'data': standard_format}), 200

@endpoints.route('/terrai-alerts/wdpa/<wdpa_id>', methods=['GET'])
@validate_terrai_period
@validate_wdpa

def terrai_wdpa(wdpa_id):

    logging.info('Intersect Terra I and WDPA')

    period = request.args.get('period', None)

    #format period request to julian dates
    from_year, from_date, to_year, to_date = DateService.date_to_julian_day(period)

    #get query and download sql from sql format service
    sql, download_sql = SqlService.format_terrai_sql(from_year, from_date, to_year, to_date)

    #get geostore id and area in hectares of request from geostore
    geostore, area = GeostoreService.make_wdpa_request(wdpa_id)

    #Send query to Terra I elastic database through analysis service
    data = AnalysisService.make_terrai_request(sql, geostore)

    #standardize response
    datasetID = '{}'.format(os.getenv('TERRAI_DATASET_ID'))
    standard_format = ResponseService.standardize_response('Terrai', data, "COUNT(day)", datasetID, download_sql, area, geostore)

    return jsonify({'data': standard_format}), 200

@endpoints.route('/terrai-alerts/date-range', methods=['GET'])
def terrai_date_range():

    logging.info('Creating Terra I Date Range')

    #set dataset ids
    datasetID = '{}'.format(os.getenv('TERRAI_DATASET_ID'))
    indexID = '{}'.format(os.getenv('TERRAI_INDEX_ID'))

    #get min and max date from sql queries
    min_date, max_date = SqlService.format_date_sql(SqlService.get_min_max_date(datasetID, indexID))

    #standardize response
    response = ResponseService.format_date_range("Terrai", min_date, max_date)

    return jsonify({'data': response}), 200