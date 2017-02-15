import os
import json
import csv
import StringIO
import logging

from flask import jsonify, request, Response, stream_with_context
import requests

from . import endpoints
from landcoverloss.responders import ErrorResponder
from landcoverloss.utils.http import request_to_microservice


@endpoints.route('/landcoverloss', methods=['GET'])
def make_request():
    """Make request to image service"""
    logging.info('pinging image service')

    shape = 'esriGeometryPolygon'

    geometry = '{"type":"Polygon","rings":[[[-52.108154296875,-8.537565350804018],[-52.437744140625,-9.156332560046778],[-52.020263671875,-9.329831355689176],[-51.690673828125,-8.733077421211563],[-52.108154296875,-8.537565350804018]]]}'

    mosaic_rule = '{"mosaicMethod":"esriMosaicLockRaster","lockRasterIds":[1],"ascending":true,"mosaicOperation":"MT_FIRST"}'

    rendering_rule = '{"rasterFunction":"Arithmetic","rasterFunctionArguments":{"Raster":{"rasterFunction":"Remap","rasterFunctionArguments":{"InputRanges":[0,30,30,101],"OutputValues":[0,1],"Raster":"$2","AllowUnmatched":false}},"Raster2":{"rasterFunction":"Arithmetic","rasterFunctionArguments":{"Raster":{"rasterFunction":"Arithmetic","rasterFunctionArguments":{"Raster":{"rasterFunction":"Remap","rasterFunctionArguments":{"InputRanges":[1,16],"OutputValues":[16],"Raster":"$1","AllowUnmatched":false}},"Raster2":"$1","Operation":3}},"Raster2":"$3","Operation":1},"outputPixelType":"U8"},"Operation":3}}'

    #how does vizz grab the geoetry?
    #need to send the geostore id to the microservice and get back the geojson
    #/geostore/id
    #example: https://github.com/resource-watch/adapter-earth-engine/blob/master/adapterearthengine/utils/http.py

    url = 'http://gis-gfw.wri.org/arcgis/rest/services/image_services/tree_cover_loss_year_wgs84/ImageServer/computeHistograms?geometry={0}&geometryType={1}&renderingRule={2}&f=json'.format(geometry, shape, mosaic_rule)

    resp = requests.get(url=url)
    data = resp.json()

    return jsonify({'data': data}), 200
