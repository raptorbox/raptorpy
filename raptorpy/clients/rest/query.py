def create_device_query(
    index=None,
    type=None,
    limit=None,
    offset=None,
    sort=None,
    search=None,
    name=None,
    description=None,
    custom_fields=None):
    '''
    Create a query for searching a device definition
    ================================================

    Query structure:
    ``
    {
        "index": "string",
        "type": "string",
        "limit": 0,
        "offset": 0,
        "sort": {
            "sort": "ASC",
            "field": "string"
        },
        "search": "string",
        "name": "string",
        "description": "string",
        "customFields": {
            "additionalProp1": {},
            "additionalProp2": {},
            "additionalProp3": {}
        }
    }
    ``
    '''
    args = locals()
    query = {}

    for arg, val in args.iteritems():
        if val:
            query[arg] = val #TODO check if the values are valid

    return query

def create_stream_query(
    index=None,
    type=None,
    limit=None,
    offset=None,
    sort=None,
    queryList=None,
    numericrange=False,
    geodistance=False,
    geoboundingbox=False,
    match=False,
    numericrangefrom =None,
    numericrangeto= None,
    timerangefrom=None,
    timerangeto=None,
    numericrangefield=None,
    limitcount=None,
    pointlat=None,
    pointlon=None,
    geodistancevalue=None,
    geodistanceunit=None,
    geoboxupperleftlat=None,
    geoboxupperleftlon=None,
    geoboxbottomrightlat=None,
    geoboxbottomrightlon=None,
    match=None,
    matchfield=None,
    matchstring=None):
    '''
    Create a query for searching into a stream for a record
    =======================================================

    Query structure:
    ``
    {
        "index": "string",
        "type": "string",
        "limit": 0,
        "offset": 0,
        "sort": {
            "sort": "ASC",
            "field": "string"
        },
        "queryList": [
            null
        ],
        "numericrange": true,
        "numericrangefrom": 0,
        "numericrangeto": 0,
        "timerange": true,
        "timerangefrom": 0,
        "timerangeto": 0,
        "numericrangefield": "string",
        "limitcount": 0,
        "geodistance": true,
        "pointlat": 0,
        "pointlon": 0,
        "geodistancevalue": 0,
        "geodistanceunit": "inches",
        "geoboundingbox": true,
        "geoboxupperleftlat": 0,
        "geoboxupperleftlon": 0,
        "geoboxbottomrightlat": 0,
        "geoboxbottomrightlon": 0,
        "match": true,
        "matchfield": "string",
        "matchstring": "string"
    }
    ``
    '''
    args = locals()
    query = {}

    for arg, val in args.iteritems():
        if val:
            query[arg] = val #TODO check if the values are valid

    return query
