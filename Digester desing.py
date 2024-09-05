#LIBRARY
import numpy as np

# 1.DESIGN PARAMETER
specific_weight = 1000 #densidad
specific_us = 62.4
m3_ft3 = 35.3147
m2_ft2 =10.7639
m_ft = 3.28084
btu_J = 1055.06

# PRYMARY SLUDGE
Ps_Solid_produced = 3813.54 # kg/d
Ps_Solid_concentration = 0.05 #5%
Ps_specific_gravity = 1.02
Ps_VS = 0.65 #65%

#THICKENED WASTE ACTIVED SLUDGE
Ts_Solid_produced = 1910.54 #kg/d
Ts_Solid_concentration = 0.04 #4%
Ts_specific_gravity = 1.00
Ts_VS = 0.75 #70%

# 2.DAILY SLUDGE VOLUME
Ps_Volume = (Ps_Solid_produced)/(specific_weight*Ps_specific_gravity*Ps_Solid_concentration)
WAS_Volume = (Ts_Solid_produced)/(specific_weight*Ts_specific_gravity*Ts_Solid_concentration)
Total_sludge_volume= Ps_Volume + WAS_Volume
print("Primary sludge volume = ",Ps_Volume, "m3/d")
print("Was volume = ",WAS_Volume, "m3/d")
print("Total sludge volume = ",Total_sludge_volume, "m3/d")

#3. DESIGN VOLUME
sizing_criteria = 15 #day of SRT
digester_volume = Total_sludge_volume*sizing_criteria
print("digester volume = ",digester_volume, "m3")

#4. Solids loading rate: 
Total_VS_loading = Ps_Solid_produced*Ps_VS+Ts_Solid_produced*Ts_VS
print("Total VS loading = ",Total_VS_loading, "kg/d")
VS_loading_rate =Total_VS_loading/digester_volume
print("VS loading rate = ",VS_loading_rate, "kg/m3-d")

#5. Combined feed solids concentration
# Assume that the specific gravity of 
# the combined sludge is 1.01.
sg_combined = 1.01
Total_solids_feed =Ps_Solid_produced+Ts_Solid_produced
print("Total solids feed = ",Total_solids_feed, "kg/d")
Total_solids_concentration = (Total_solids_feed*100)/(sg_combined*specific_weight*Total_sludge_volume)
print("solids concentration ",Total_solids_concentration, "%")
# # 6. Digester sizing: 

number_digester_provided = 4
Activate_volume_digester = digester_volume/number_digester_provided
print("Volumen activo de cada digestor ",Activate_volume_digester, "m3")
# Assume a diameter tank
Diameter_tank_assumed = 10
Diameter_tank_assumed_Us = Diameter_tank_assumed * m_ft
area_of_tank=np.pi*(Diameter_tank_assumed/2)**2
print("Area del tanque ",area_of_tank, "m2")
Active_depth = Activate_volume_digester/area_of_tank
print("Profundidad del tanque ",Active_depth, "m")

#Add additional depths as follows:
grit_deposit = 0.5 #m
scum_blanket = 0.5 #m
space_bellow_cover_at_maximum_level = 0.5 #m
Total_additional_depth = grit_deposit+scum_blanket+space_bellow_cover_at_maximum_level

# Note: Some designers provide an allowance for maximum sludge production conditions. However, in this example, an SRT of 15 days is 
# selected (the minimum SRT should be 10 days) to account for the fluctuations in solids production.

Total_sidewall_height = Active_depth+Total_additional_depth
print("Altura del tanque ",Total_sidewall_height, "m")
print("vamos a redondearlo")
Total_sidewall_height= round(Total_sidewall_height)
print("Altura del tanque ",Total_sidewall_height, "m")

# 7. VS destruction and gas production
#  From Figure 6-1, VS destruction is 
# 56% for an SRT of 15 days.
Vs_destruction = 0.56 #56% for 15 days of srt
Vs_destroyed = Vs_destruction*Total_VS_loading
print("VS destroyed ",Vs_destroyed, "kg/d")

# Assume that the gas produced is 16 ft3/lb (1 m/kg) of VS destroyed
gas_production_rate= 1 # ft3/lb or 1m3/kg of VS destroyed
Total_gas_produced = Vs_destroyed*gas_production_rate
print("Gas produced ",Total_gas_produced, "m3/d")
print("Gas produced ",Total_gas_produced/24, "m3/h")

# Because digester gas is about two-thirds methane
metano_porcentaje = 0.67 # two thirds of the digested gas
total_metano_produced = Total_gas_produced*metano_porcentaje
print("metano produced ",total_metano_produced, "m3/d")
print("metano produced ",total_metano_produced/24, "m3/h")

# # 8. Digested sludge solids
fixed_solids_in_feed = Total_solids_feed-Total_VS_loading
print("solidos fijos en la alimentación ",fixed_solids_in_feed, "kg/d")
VS_remaining_after_digestion =Total_VS_loading-Vs_destroyed
print("VS remanentes depues de la digestion ",VS_remaining_after_digestion, "kg/d")
total_solids_in_digested_lugde=fixed_solids_in_feed+VS_remaining_after_digestion
print("solidos totales digeridos ",total_solids_in_digested_lugde, "kg/d")
# Single-stage digesters operate without supernatant withdrawal. Therefore, the volume of 6170 ft3
# /d fed is the same as the volume withdrawn. 
# Assume that the specific gravity of digested sludge is 1.02.

sg_digested_sludge =1.02
Solids_concentration_in_digested_sludge = (total_solids_in_digested_lugde*100)/(sg_digested_sludge*specific_weight*Total_sludge_volume)
print("Concentración de sólidos en el lodo digerido ",Solids_concentration_in_digested_sludge, "%")

# 9. Digester heating 
# Assume the following temperature conditions
air = 25 #°F (-4°C)
average_for_earth_around_wall = 35 #°F (1.7°C)
earth_bellow_floor= 45 #°F (7.2°C)
raw_sludge_feed = 55#°F (12.8°C)
digester_contents= 95#°F (35°C)


# ## Heat transfer coefficients, U (see Table 6.5):

insulated_wall_exposed_to_air = 0.12 #Btu/ft2-°F-hr
wall_exposed_to_dry_earth = 0.11
moist_earth_bellow_floor = 0.15
insulated_roof = 0.17

sludge_feed_to_each_digester = Total_sludge_volume/number_digester_provided
print("Alimentación para cada digestor ",sludge_feed_to_each_digester, "m3/d")
sludge_feed_to_each_digester_Us=sludge_feed_to_each_digester*m3_ft3
print("Alimentación para cada digestor ",sludge_feed_to_each_digester_Us, "ft3/d")
Specefic_heat_sludge = 1 #Btu/lb-°F
# ## Compute heat required for each digester for raw sludge using equation (5.2)

Q1 = sludge_feed_to_each_digester_Us*specific_us*Specefic_heat_sludge*(digester_contents-raw_sludge_feed)
print("Q1= ",Q1, "Btu/d")
Q1_hora = sludge_feed_to_each_digester_Us*specific_us*Specefic_heat_sludge*(digester_contents-raw_sludge_feed)/24
print("Q1= ",Q1_hora, "Btu/h")
print("Q1= ",Q1_hora*btu_J, "j/h")

# ## Compute the area of each component:

Wall_area = np.pi*Diameter_tank_assumed*Total_sidewall_height
print("Area de las paredes = ",Wall_area, "m2")
Wall_area_Us = Wall_area * m2_ft2
print("Area de las paredes = ",Wall_area_Us, "ft2")

# Assume that one-half of the wall is below grade
areas_exposed_to_dry_Air = Wall_area_Us/2
print("Areas expuestas a la tierra o al aire seco = ",areas_exposed_to_dry_Air, "ft2")

center_depth_conical_tank_floor = 5 #ft 1:5
print("Profundidad central del fondo del tanque cónico en una pendiente 1:5 = ",center_depth_conical_tank_floor, "ft")
floor_area_exposed_earth = np.pi*(Diameter_tank_assumed_Us/2)*((Diameter_tank_assumed_Us/2)**2 + center_depth_conical_tank_floor**2)**(1/2)
print("Area del piso expuesto a la tierra = ",floor_area_exposed_earth, "ft2")
roof_area= np.pi*(Diameter_tank_assumed_Us/2)**2
print("Area del techo = ",roof_area, "ft2")

# ## Compute the heat loss for each component using equation (6.3)
wall_above_grade = insulated_wall_exposed_to_air*areas_exposed_to_dry_Air*(digester_contents-air)
print("Pared por encima del nivel del suelo = ",wall_above_grade, "BTU/h")
wall_below_grade = wall_exposed_to_dry_earth * areas_exposed_to_dry_Air*(digester_contents-average_for_earth_around_wall)
print("Pared por debajo del nivel del suelo = ",wall_below_grade, "BTU/h")
floor=moist_earth_bellow_floor*floor_area_exposed_earth*(digester_contents-earth_bellow_floor)
print("Piso = ",floor, "BTU/h")
roof=insulated_roof*roof_area*(digester_contents-air)
print("techo = ",roof, "BTU/h")
Total_heat_loss = roof+wall_below_grade+floor+wall_above_grade
print("Perdida de calor total = ",Total_heat_loss, "BTU/h")
print("Perdida de calor total = ",Total_heat_loss*btu_J, "J/h")