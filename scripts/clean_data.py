import pandas as pd
from zipfile import ZipFile
import os
os.environ['USE_PYGEOS'] = '0'
import fiona
fiona.drvsupport.supported_drivers['libkml'] = 'rw' # enable KML support which is disabled by default
fiona.drvsupport.supported_drivers['LIBKML'] = 'rw' # enable KML support which is disabled 
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon, shape, Point, LineString
from glob import glob

def convert_3D_2D(geometry):
    '''
    Takes a GeoSeries of 3D Multi/Polygons (has_z) and returns a list of 2D Multi/Polygons
    '''
    if geometry.has_z:
        if geometry.geom_type == 'Polygon':
            lines = [xy[:2] for xy in list(geometry.exterior.coords)]
            return Polygon(lines)
        elif geometry.geom_type == 'MultiPolygon':
            new_multi_p = []
            for ap in geometry:
                lines = [xy[:2] for xy in list(ap.exterior.coords)]
                new_p = Polygon(lines)
                new_multi_p.append(new_p)
            return MultiPolygon(new_multi_p)
        elif geometry.geom_type == 'Point':
            return Point(geometry.coords[0][:2])
        elif geometry.geom_type == 'LineString':
            geo = LineString([xy[:2] for xy in list(geometry.coords)])
            return geo
        else:
            return geometry
    else:
        return geometry

demography_cols = {
 'Workers 16 Years and Over:':'Workers 16 and over:',
 'Workers 16 Years and Over: Car, Truck, or Van':'Car, Truck, or Van workers',
 'Workers 16 Years and Over: Drove Alone':'Drove Alone workers',
 'Workers 16 Years and Over: Carpooled':'Carpooled workers',
 'Workers 16 Years and Over: Public Transportation (Includes Taxicab)':'Public Transportation (Includes Taxicab) workers',
 'Workers 16 Years and Over: Motorcycle':'Motorcycle workers',
 'Workers 16 Years and Over: Bicycle':'Bicycle workers',
 'Workers 16 Years and Over: Walked':'Walked workers',
 'Workers 16 Years and Over: Other Means':'Other Means workers',
 'Workers 16 Years and Over: Worked At Home':'Worked At Home workers',
 'Total Population:':'Total Population',
 'Total Population: More than 5 Years':'Pop over 5 Years',
 'Total Population: More than 10 Years':'Pop over 10 Years',
 'Total Population: More than 15 Years':'Pop over 15 Years',
 'Total Population: More than 18 Years':'Pop over 18 Years',
 'Total Population: More than 25 Years':'Pop over 25 Years',
 'Total Population: More than 35 Years':'Pop over 35 Years',
 'Total Population: More than 45 Years':'Pop over 45 Years',
 'Total Population: More than 55 Years':'Pop over 55 Years',
 'Total Population: More than 65 Years':'Pop over 65 Years',
 'Total Population: More than 75 Years':'Pop over 75 Years',
 'Total Population: More than 85 Years':'Pop over 85 Years',
 'Median Household Income (In 2021 Inflation Adjusted Dollars)':'Median Household Income',
 'Total Population: Not Hispanic or Latino: White Alone': 'NH White Alone',
 'Total Population: Not Hispanic or Latino: Black or African American Alone': 'NH Black or African American Alone',
 'Total Population: Not Hispanic or Latino: American Indian and Alaska Native Alone': 'NH American Indian and Alaska Native Alone',
 'Total Population: Not Hispanic or Latino: Asian Alone': 'NH Asian Alone',
 'Total Population: Not Hispanic or Latino: Native Hawaiian and Other Pacific Islander Alone': 'NH Native Hawaiian and Other Pacific Islander Alone',
 'Total Population: Not Hispanic or Latino: Some Other Race Alone': 'NH Some Other Race Alone',
 'Total Population: Not Hispanic or Latino: Two or More Races': 'NH Two or More Races',
 'Total Population: Hispanic or Latino':'Hispanic or Latino',
}

def clean_df(df: pd.DataFrame, cols: dict = demography_cols):
    df = df.rename(columns=cols)
    for col in cols.values():
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass
    return df

def clean_community_vars():
    zipcode_data = pd.read_csv("./data/community vars/zipcode-SDdata.csv")
    zipcode_data["zipcode"] = zipcode_data["Qualifying Name"].str.slice(6)
    zipcode_data = zipcode_data[["zipcode"]+list(demography_cols.keys())]
    zipcode_data = clean_df(zipcode_data)
    tracts_data = pd.read_csv("./data/community vars/tract-SDdata.csv")[["FIPS"]+list(demography_cols.keys())]
    tracts_data = clean_df(tracts_data)
    tracts_data['FIPS'] = tracts_data['FIPS'].apply(lambda x: f"{x:0>11}")
    # # geo
    tracts = gpd.read_file("./data/geo/cb_2021_06_tract_500k/cb_2021_06_tract_500k.shp")
    tracts = tracts.to_crs("EPSG:4326")
    tracts = tracts[tracts["COUNTYFP"] == "073"]
    zip_geo= gpd.read_file("./data/geo/cb_2020_us_zcta520_500k/cb_2020_us_zcta520_500k.shp")
    zip_geo = zip_geo.to_crs("EPSG:4326")
    # take only zips intersecting with tracts
    zip_geo = gpd.sjoin(zip_geo, tracts, how="inner", predicate="intersects")
    zip_geo = zip_geo[["ZCTA5CE20", 'ALAND20', 'AWATER20', "geometry"]]
    # filter tracts data start with 06073
    tracts_data = tracts_data[tracts_data["FIPS"].str.startswith("06073")]
    zipcode_data = zipcode_data[zipcode_data["zipcode"].isin(zip_geo["ZCTA5CE20"])]
    tracts_data.to_parquet("./data/community vars/tracts_data.parquet")
    zipcode_data.to_parquet("./data/community vars/zipcode_data.parquet")

def get_geo():
    tracts = gpd.read_file("./data/geo/cb_2021_06_tract_500k/cb_2021_06_tract_500k.shp")
    tracts = tracts.to_crs("EPSG:4326")
    tracts = tracts[tracts["COUNTYFP"] == "073"]
    zip_geo= gpd.read_file("./data/geo/cb_2020_us_zcta520_500k/cb_2020_us_zcta520_500k.shp")
    zip_geo = zip_geo.to_crs("EPSG:4326")
    # take only zips intersecting with tracts
    zip_geo = gpd.sjoin(zip_geo, tracts, how="inner", predicate="intersects")
    zip_geo = zip_geo[["ZCTA5CE20", 'ALAND20', 'AWATER20', "geometry"]]
    community_planning_districts = gpd.read_file("./data/geo/cmty_plan_datasd.geojson")
    community_planning_districts = community_planning_districts.to_crs("EPSG:4326")
    council_districts = gpd.read_file("./data/geo/council_districts_datasd.geojson")
    council_districts = council_districts.to_crs("EPSG:4326")

    sjoin_zip = zip_geo[['ZCTA5CE20','geometry']]
    sjoin_cdp = community_planning_districts[['cpcode','geometry']]
    sjoin_council = council_districts[['district','geometry']]
    sjoin_tracts = tracts[['GEOID','geometry']]

    tracts.to_parquet("./data/geo/tracts_geo.parquet")
    zip_geo.to_parquet("./data/geo/zip_geo.parquet")

    return {
        "sjoin_zip": sjoin_zip,
        "sjoin_cdp": sjoin_cdp,
        "sjoin_council": sjoin_council,
        "sjoin_tracts": sjoin_tracts,
    }

def handle_311_data(geodata):
    sjoin_zip = geodata["sjoin_zip"]
    sjoin_cdp = geodata["sjoin_cdp"]
    sjoin_council = geodata["sjoin_council"]
    sjoin_tracts = geodata["sjoin_tracts"]

    files311 = glob("./data/get it done 2021-2023/*close*.csv")
    
    data311 = pd.concat([pd.read_csv(f) for f in files311])
    data311 = gpd.GeoDataFrame(data311, geometry=gpd.points_from_xy(data311.lng, data311.lat))
    data311.crs = "EPSG:4326"
    data311 = gpd.sjoin(data311, sjoin_zip, how="left", predicate="within")

    if "index_right" in data311.columns:
        data311 = data311.drop(columns=["index_right"])
    if "index_left" in data311.columns:
        data311 = data311.drop(columns=["index_left"])
    data311 = gpd.sjoin(data311, sjoin_cdp, how="left", predicate="within")
    if "index_right" in data311.columns:
        data311 = data311.drop(columns=["index_right"])
    if "index_left" in data311.columns:
        data311 = data311.drop(columns=["index_left"])
    data311 = gpd.sjoin(data311, sjoin_council, how="left", predicate="within")
    if "index_right" in data311.columns:
        data311 = data311.drop(columns=["index_right"])
    if "index_left" in data311.columns:
        data311 = data311.drop(columns=["index_left"])
    data311 = gpd.sjoin(data311, sjoin_tracts, how="left", predicate="within")
    if "index_right" in data311.columns:
        data311 = data311.drop(columns=["index_right"])
    if "index_left" in data311.columns:
        data311 = data311.drop(columns=["index_left"])
    print('sjoined 311')
    # drop zipcode
    if "zipcode" in data311.columns:
        data311 = data311.drop(columns=["zipcode"])
    print(data311.head())
    # ZIP_CODE as string
    data311["ZIP_CODE"] = data311["ZCTA5CE20"].astype(str)
    print('Exporting to parquet...')
    data311.to_parquet("./data/311_data.parquet")

def read_file(filepath: str):
  filename = filepath.split('/')[-1].split('.kmz')[0]
  kmz = ZipFile(filepath, 'r')
  kmz.extract(f'doc.kml', './data/walk audits')
  # rename doc to filename.kml
  kml_file = f'./data/walk audits/{filename}.kml'
  os.rename(f'./data/walk audits/doc.kml', kml_file)

  gdf_list = []
  for layer in fiona.listlayers(kml_file):    
      gdf = gpd.read_file(kml_file, driver='LIBKML', layer=layer)
      gdf_list.append(gdf)

  gdf = gpd.GeoDataFrame(pd.concat(gdf_list, ignore_index=True))
  gdf['geometry'] = gdf['geometry'].apply(lambda x: convert_3D_2D(x))
  return gdf

def processfile(filepath: str):
    gdf = read_file(filepath)
    site = filepath.split('/')[-1].split('.kmz')[0]
    gdf['site'] = site
    return gdf

def handle_walk_audits(geodata):
    sjoin_zip = geodata["sjoin_zip"]
    sjoin_cdp = geodata["sjoin_cdp"]
    sjoin_council = geodata["sjoin_council"]
    sjoin_tracts = geodata["sjoin_tracts"]
    # walk audits 
    walk_audits = glob("./data/walk audits/*.kmz")
    audit_data = []
    for f in walk_audits:
        audit_data.append(processfile(f))
    full_audit_data = pd.concat(audit_data)
    full_audit_data = gpd.sjoin(full_audit_data, sjoin_zip, how="left", predicate="intersects")
    if "index_right" in full_audit_data.columns:
        full_audit_data = full_audit_data.drop(columns=["index_right"])
    if "index_left" in full_audit_data.columns:
        full_audit_data = full_audit_data.drop(columns=["index_left"])
    full_audit_data = gpd.sjoin(full_audit_data, sjoin_cdp, how="left", predicate="intersects")
    if "index_right" in full_audit_data.columns:
        full_audit_data = full_audit_data.drop(columns=["index_right"])
    if "index_left" in full_audit_data.columns:
        full_audit_data = full_audit_data.drop(columns=["index_left"])
    full_audit_data = gpd.sjoin(full_audit_data, sjoin_council, how="left", predicate="intersects")
    if "index_right" in full_audit_data.columns:
        full_audit_data = full_audit_data.drop(columns=["index_right"])
    if "index_left" in full_audit_data.columns:
        full_audit_data = full_audit_data.drop(columns=["index_left"])
    full_audit_data = gpd.sjoin(full_audit_data, sjoin_tracts, how="left", predicate="intersects")
    if "index_right" in full_audit_data.columns:
        full_audit_data = full_audit_data.drop(columns=["index_right"])
    if "index_left" in full_audit_data.columns:
        full_audit_data = full_audit_data.drop(columns=["index_left"])
    full_audit_data.to_parquet("./data/walk_audits.parquet")

def main():
    geodata = get_geo()
    print("got geo")

    try:
        print("Handing community vars")
        clean_community_vars()
    except Exception as e:
        print("community vars failed")
        print(e)
    
    try: 
        print("Handing 311 data")
        handle_311_data(geodata)
    except Exception as e:
        print("311 data failed")
        print(e)
    
    try:
        print("Handing walk audits")
        handle_walk_audits(geodata)
    except Exception as e:
        print("walk audits failed")
        print(e)

if __name__ == "__main__":
    main()