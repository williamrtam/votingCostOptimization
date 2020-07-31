import math

def deg2rad(deg):
  return deg * (math.pi/180)

# Using the Haversine formula, compute the distance between two lat,long points
def getDist(lat1,lon1,lat2,lon2):
  radius_earth_km = 6371
  dLat = deg2rad(lat2-lat1)
  dLon = deg2rad(lon2-lon1)
  a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) \
      * math.sin(dLon/2) * math.sin(dLon/2)
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
  d = radius_earth_km * c
  d_km_to_m = d * 0.621371
  return d_km_to_m

# Add unique polling locations to set based on lat,long
districts = set()

districts.add((39.9541435, -75.2085688))
districts.add((39.9489292, -75.2114126))
districts.add((39.9522485, -75.1952141))
districts.add((39.9401631, -75.2163654))
districts.add((39.9524577, -75.2014366))
districts.add((39.956883, -75.2061845))
districts.add((39.9465441, -75.208133))
districts.add((39.9539892, -75.2015048))
districts.add((39.9539892, -75.2015048))
districts.add((39.9533386, -75.2118169))
districts.add((39.9545686, -75.1968938))
districts.add((39.9401631, -75.2163654))
districts.add((39.956883, -75.2061845))
districts.add((39.9533386, -75.2118169))
districts.add((39.9420582, -75.2117197))
districts.add((39.9420582, -75.2117197))
districts.add((39.9387613, -75.2134922))
districts.add((39.9512686, -75.1978861))
districts.add((39.9522485, -75.1952141))
districts.add((39.9518512, -75.2011037))
districts.add((39.9522831, -75.2001674))
districts.add((39.9509138, -75.1938738))
districts.add((39.9541435, -75.2085688))

# Manually boxed out corner points for square encompassing ward 27
UL = (39.958266,-75.211050)
UR = (39.954609,-75.181369)
LL = (39.937289,-75.215156)
LR = (39.932712,-75.186098)

# Constants and Assumptions
num_registered_voters = 22860
participation_rate = 0.6
num_actual_voters = num_registered_voters*participation_rate
num_poll_stations = len(districts)
poll_station_capacity = round(num_actual_voters / num_poll_stations)
side_length = getDist(UL[0],UL[1],UR[0],UR[1]) # length in miles of one side of ward based on UL and UR
num_rows_cols = round(math.sqrt(num_actual_voters)) # length of array to be constructed in GAMS
unit_length = side_length / num_rows_cols # unit length in miles of distance between voter
rounded_num_actual_voters = num_rows_cols * num_rows_cols # actual number of voters to make calculations easy

for poll in districts:
    # get distance between Upper Left corner (origin) and polling station
    a = getDist(UL[0],UL[1],poll[0],poll[1])

    #get distance between Lower Left corner and polling station
    b = getDist(LL[0],LL[1],poll[0],poll[1])

    #get distance between Upper Left corner and Lower Left corner
    c = getDist(UL[0],UL[1],LL[0],LL[1])

    #Use Law of Cosines to figure out angle b
    angle_b_radians = math.acos((c**2 + a**2 - b**2)/(2*a*c))

    # get x distance in miles (this will be your column coordinate for GAMS matrix, so set it equal to y)
    y = math.sin(angle_b_radians) * a

    # get y distance in miles (this will be your row coordinate for GAMS matrix, so set it equal to x)
    x = math.cos(angle_b_radians) * a

    # distance out of bounds check
    if x > c:
        x = c
    if y > side_length:
        y = side_length

    #Display location of each poll in ward 27
    print(x,y)


