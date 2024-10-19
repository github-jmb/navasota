import pandas as pd
import os

directory = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(directory, 'swqmispublicdata.txt')

df = pd.read_csv(filepath, delimiter='|')

exclude = [
    "TEMPERATURE, WATER (DEGREES CENTIGRADE)", 
    "SPECIFIC CONDUCTANCE,FIELD (US/CM @ 25C)",
    "OXYGEN, DISSOLVED (MG/L)", "PH (STANDARD UNITS)", 
    "SPECIFIC CONDUCTANCE,LAB (UMHOS/CM @ 25C)",
    "CARBBIOCHEM OXY DEM,INHIB, DISS(MG/L,5DAY-20C, C", 
    "CARBBIOCHEM OX DM,NIT INHB,TOT (MG/L,20 DAY-20C",
    "CARBBIOCHEM OXY DM,NIT INHB DISS(MG/L,20 DAY-20C", 
    "CARBONACEOUS BIOCHEMICAL OXYGEN DEMAND NITRIFICATION INHIBITOR, TOTAL, 5 DAY-20 DEGREE C",
    "PH (STANDARD UNITS) LAB", "ALKALINITY, TOTAL (MG/L AS CACO3)", 
    "RESIDUE, TOTAL NONFILTRABLE (MG/L)",
    "RESIDUE, VOLATILE NONFILTRABLE (MG/L)", 
    "RESIDUE,TOTAL FILTRABLE (DRIED AT 180C) (MG/L)",
    "FLOW SEVERITY:1=No Flow,2=Low,3=Normal,4=Flood,5=High,6=Dry", 
    "FECAL COLIFORM,MEMBR FILTER,M-FC BROTH, #/100ML",
    "FLOW  STREAM, INSTANTANEOUS (CUBIC FEET PER SEC)", 
    "TRANSPARENCY, SECCHI DISC (INCHES)",
    "CALCIUM, DISSOLVED (MG/L AS CA)", 
    "MAGNESIUM, DISSOLVED (MG/L AS MG)", 
    "DAYS SINCE PRECIPITATION EVENT (DAYS)",
    "TRANSPARENCY, SECCHI DISC (METERS)", 
    "HARDNESS, TOTAL (MG/L AS CACO3)", 
    "SOLIDS, DISSOLVED-SUM OF CONSTITUENTS (MG/L)",
    "SODIUM ADSORPTION RATIO", 
    "STREAM FLOW ESTIMATE (CFS)", 
    "SALINITY - PARTS PER THOUSAND",
    "OXYGEN, DISSOLVED (PERCENT OF SATURATION)", 
    "STREAM VELOCITY (FEET PER SECOND)",
    "COLOR, BORGER SYSTEM (USE BORGER CODE)", 
    "AVERAGE STREAM WIDTH (METERS)", 
    "MACROPHYTE BED AT COLLECTION POINT (%)",
    "WIND INTENSITY (1=CALM,2=SLIGHT,3=MOD.,4=STRONG)", 
    "PRESENT WEATHER (1=CLEAR,2=PTCLDY,3=CLDY,4=RAIN,5=OTHER)",
    "WATER SURFACE(1=CALM,2=RIPPLE,3=WAVE,4=WHITECAP)", 
    "AVERAGE STREAM DEPTH (METERS)",
    "FLOW, STREAM, MEAN DAILY (CUBIC FEET PER SEC)", 
    "E. COLI, COLILERT, IDEXX METHOD, MPN/100ML",
    "FLOW MTH 1=GAGE 2=ELEC 3=MECH 4=WEIR/FLU 5=DOPPLER", 
    "DEPTH OF BOTTOM OF WATER BODY AT SAMPLE SITE",
    "BARIUM, DISSOLVED (UG/L AS BA)", 
    "CADMIUM, DISSOLVED (UG/L AS CD)", 
    "COBALT, DISSOLVED (UG/L AS CO)",
    "COPPER, DISSOLVED (UG/L AS CU)", 
    "ALUMINUM, DISSOLVED (UG/L AS AL)", 
    "IRON, DISSOLVED (UG/L)",
    "MANGANESE, DISSOLVED (UG/L AS MN)", 
    "NICKEL, DISSOLVED (UG/L AS NI)", 
    "SILVER, DISSOLVED (UG/L AS AG)",
    "VANADIUM, DISSOLVED (UG/L AS V)", 
    "CHROMIUM, DISSOLVED (UG/L AS CR)", 
    "LEAD, DISSOLVED (UG/L AS PB)",
    "THALLIUM, DISSOLVED (UG/L AS TL)", 
    "ZINC, DISSOLVED (UG/L AS ZN)", 
    "ANTIMONY, DISSOLVED (UG/L AS SB)",
    "SELENIUM, DISSOLVED (UG/L AS SE)", 
    "ARSENIC, DISSOLVED  (UG/L AS AS)", 
    "BERYLLIUM, DISSOLVED (UG/L AS BE)",
    "CARBARYL, WATER, DISSOLVED, UG/L", 
    "TURBIDITY,LAB NEPHELOMETRIC TURBIDITY UNITS, NTU",
    "PRIMARY CONTACT, OBSERVED ACTIVITY (# OF PEOPLE OBSERVED)", 
    "EVIDENCE OF PRIMARY CONTACT RECREATION (1 = OBSERVED, 0 = NOT OBSERVED)",
    "TEMPERATURE, AIR (DEGREES CENTIGRADE)", 
    "TURBIDITY,FIELD NEPHELOMETRIC TURBIDITY UNITS, N", 
    "RAINFALL IN 7 DAYS INCLUSIVE PRIOR TO SAMP. (IN)",
    "E. COLI, MTEC, MF, #/100 ML", "RAINFALL IN 1 DAY INCLUSIVE PRIOR TO SAMPLE (IN)", 
    "E.COLI, COLILERT, IDEXX, HOLDING TIME"
]

remaining_df = df[~df['Parameter Name'].isin(exclude)].copy()
remaining_df['End Date'] = pd.to_datetime(remaining_df['End Date'], errors='coerce')
remaining_df['Year'] = remaining_df['End Date'].dt.year

stations = remaining_df['Station ID'].unique()

params_per_station = {}
for station in stations:
    station_data = remaining_df[remaining_df['Station ID'] == station]
    param_counts = station_data['Parameter Name'].value_counts()
    valid_params = param_counts[param_counts >= 15].index.tolist()
    params_per_station[station] = valid_params

final_params = set(params_per_station[stations[0]])
for station in stations[1:]:
    final_params.intersection_update(params_per_station[station])

grouped = remaining_df[remaining_df['Parameter Name'].isin(final_params)].groupby('Station ID')

for segment_id, group in grouped:
    filename = f'segment_{segment_id}.xlsx'
    full_path = os.path.join(directory, filename)

    group.to_excel(full_path, index=False)

    print(f'Saved: {full_path}')
