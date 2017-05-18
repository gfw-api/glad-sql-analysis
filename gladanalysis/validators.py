"""VALIDATORS"""

from functools import wraps
from flask import request

from gladanalysis.routes.api.v1 import error

def validate_geostore(func):
    """validate geostore argument"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.method == 'GET':
            geostore = request.args.get('geostore')
            if not geostore:
                return error(status=400, detail="Geostore must be set")
        return func(*args, **kwargs)
    return wrapper

def validate_period(func):
    """validate period argument"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.method == 'GET':
            period = request.args.get('period')
            if not period:
                return error(status=400, detail="Time period must be set")
            elif len(period.split(',')) < 2:
                return error(status=400, detail="Period needs 2 arguments")
        return func(*args, **kwargs)
    return wrapper

def validate_use(func):
    """Use Validation"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        names = ['mining', 'oilpalm', 'fiber', 'logging']
        name = request.view_args.get('use_type')
        if name not in names:
            return error(status=400, detail='Name not valid')
        return func(*args, **kwargs)
    return wrapper

def validate_admin(func):
    """validate admin arguments"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.method == 'GET':
        iso_code = request.view_args.get('iso_code')
            if not iso_code:
                return error(status=400, detail="Must specify a ISO code, and optionally a /state_id and /ditrict_id")
        return func(*args, **kwargs)
    return wrapper
