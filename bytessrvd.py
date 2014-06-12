from urllib2 import urlopen
import json
import datetime
from flask import Flask
app = Flask(__name__)

@app.route("/<int:respcode>")
def bytes_median(respcode):
  "returns the median value for bytes sent for given respcode over the most recent available 24 hours."
  try:
    #find most recent time the given respcode occured, and 1 hours before that.
    enddate_query = {"query": {  "bool": {
          "must": [
             { "match": { "response": "%s" % respcode }}
             ]
          }},
          "size": 1,
          "sort": [
             { "@timestamp": { "order": "desc" }}
             ]
          }
    enddate_resp = urlopen('http://127.0.0.1:9200/_all/_search', json.dumps(enddate_query).encode()) 
    enddate_respo = json.load(enddate_resp)
    enddate = enddate_respo['hits']['hits'][0]['_source']['@timestamp']
    enddate_date = datetime.datetime.strptime(enddate,"%Y-%m-%dT%H:%M:%S.%fZ")
    startdate_date = enddate_date - datetime.timedelta(hours=1)
    
    #query for given response code and date range. Aggregate and return 50th percentile (median)
    query = {"query": {  "bool": {
          "must": [
             { "match": { "response": "%s" % respcode }},
             { "range": {
                "@timestamp": {
                 "from": "%s" % startdate_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                 "to"  : "%s" % enddate_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ") }}}
             ]
          }},
          "aggs" : {
           "bytes_percentiles" : {
            "percentiles" : {
                "field" : "bytes"     
            }
          }}}

    qresp = urlopen('http://127.0.0.1:9200/_all/_search', json.dumps(query).encode()) 
    qrespo = json.load(qresp)
    median = int(qrespo['aggregations']['bytes_percentiles']['50.0'])
    return "{\"median_size\": %s}" % median
  except ValueError:
    return '{"error": "true"}'

if __name__ == "__main__":
    app.run(port=8888)
