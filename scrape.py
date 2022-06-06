import pandas as pd
import requests, json

# Search by BBL. example: 4013050036

mapPlutoURL = 'https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/ArcGIS/rest/services/MAPPLUTO/FeatureServer/0/query?where=BBL+%3D+4013050036&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=false&returnCentroid=true&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&defaultSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=false&quantizationParameters=&sqlFormat=none&f=pjson&token='
url = requests.get(mapPlutoURL)
text = url.text
data = json.loads(text)
# features of BBL 4013050036
df = pd.DataFrame(data['features'][0]['attributes'], index=[0])
df.to_csv("data")
