import pandas as pd

# zap list api
projects = pd.DataFrame()
boroughs = ['Manhattan','Bronx','Brooklyn','Queens','Staten%20Island']

for borough in boroughs: 
  url = 'https://zap-api-production.herokuapp.com/projects.csv?page=1&block=&boroughs%5B0%5D='+borough+'&dcp_publicstatus%5B0%5D=In%20Public%20Review&dcp_publicstatus%5B1%5D=Noticed'
  projects = projects.append(pd.read_csv(url))
projects = projects.reset_index(drop=True)

projects = projects[["id", "applicants", "dcp-borough", "dcp-femafloodzonea", "dcp-projectname", "dcp-projectbrief", "dcp-ceqrnumber", "dcp-publicstatus", "dcp-noticeddate"]]

# zap single file api
import requests, json
zapURL = list('https://zap-api-production.herokuapp.com/projects/'+projects['id'])
bbls = []
ulurps = []
polygons = []
for i in zapURL:
    #print(i)
    url = requests.get(i)
    text = url.text

    data = json.loads(text)
    # read bbl
    bbls.append(data['data']['attributes']['bbls'])

    # read ulurp number
    ulurp = []
    for i in range(len(data['included'])):
        try:
            ulurp.append(data['included'][i]['attributes']['dcp-ulurpnumber'])

        except KeyError:
            continue
    ulurps.append(ulurp)

    # read polygon
    try:
        polygons.append(data['data']['attributes']['bbl-featurecollection']['features'][0]['geometry']['coordinates'][0][0])
    except KeyError:
        #print(i)
        #print('error')
        polygons.append('')
        continue

# add to make dataframe
projects['bbls'] = bbls
projects['ulurpnumbers'] = ulurps
projects['polygon'] = polygons

# save zap alone
projects.to_csv("zap_projects_data.csv")

# combine zap and pluto
# transform dataframe, list by BBL
df_new = pd.merge(projects,
        (projects['bbls'].apply(lambda x: pd.Series(x)).T
             .unstack().reset_index(level=-1, drop=True)
             .dropna().to_frame()),
        left_index = True,
        right_index = True).drop('bbls', axis=1)

df_new = df_new.rename(columns={0:'BBL'})

# read in pluto
df = df1 = pd.DataFrame()
bbl_list = df_new['BBL']
for i in bbl_list:
    try:
        mapPlutoURL = 'https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/ArcGIS/rest/services/MAPPLUTO/FeatureServer/0/query?where=BBL+%3D+'+i+'&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=false&returnCentroid=true&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&defaultSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=false&quantizationParameters=&sqlFormat=none&f=pjson&token='

        url = requests.get(mapPlutoURL)
        text = url.text

        data = json.loads(text)
        df1 = pd.DataFrame(data['features'][0]['attributes'], index=[0])
        df = pd.concat([df, df1])
    except:
        blank_df = pd.DataFrame(None, index=[0], columns=df.columns)
        blank_df['BBL'][0] = i
        df = pd.concat([df, blank_df])
        continue

# select features
df = df[['BBL', 'BuiltFAR', 'ResidFAR', 'CommFAR', 'FacilFAR', 'ZoneMap', 'OwnerName', 'ZipCode', 'Block', 'LotArea', 'BldgArea', 'LandUse']]
df['BBL'] = df['BBL'].astype(str)
result = pd.merge(df_new, df, how="left", on=['BBL'])
combined = result.drop_duplicates(subset=['id', 'dcp-ceqrnumber', 'BBL'])
result = result.drop_duplicates(subset=['id', 'BBL'])

# save combined
result.to_csv("consolidated_data.csv")