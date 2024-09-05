#LIBRARY
import numpy as np

Qdaily = 40000 #m3/d
# Influent Characteristics
BOD = 200 #g/m3
TSS = 250 #g/m3

# Factores de conversion
g_kg_c = 10**(-3)
kg_m3_c = 10**(-3)
g_m3_c = 10**(4)

# Primary Clarifier
BOD_removal = 0.3 #30%
TSS_removal = 0.6 #60%
VSS = 0.65 # %VSS of TSS
slug_concentration = 0.06 #6%

# Effluent
BOD_e = 10 #mg/L
TSS_e =10 #mg/L

# 1.Daily influent mass values 
BOD_1= Qdaily*BOD*g_kg_c
print("a. BOD = ",BOD_1, "kg/d")
TSS_1= Qdaily*TSS*g_kg_c
print("b. TSS = ",TSS_1, "kg/d")

# # 2.Aproach Recicle flows
A_flow = 0.01 # suponemos 1% del flujo total
A_bod = 0.02 # suponemos 2% del BOD total
A_tss = 0.04 # suponemos 4% del TSS total

a2_flow=494.61
#a2_flow = Qdaily*A_flow
print("a. Flow = ",a2_flow, "m3/d")
b2_BOD=230.62
#b2_BOD = BOD_1*A_bod
print("b. BOD = ",b2_BOD, "kg/d")
c3_TSS=584.89
#c3_TSS = TSS_1*A_tss
print("c. TSS = ",c3_TSS, "kg/d")

#3.Primary clarifier
a3_Flow_i = Qdaily + a2_flow
print("a. Influent flow = ",a3_Flow_i, "m3/d")

b3_BOD_i = BOD_1 + b2_BOD
print("b. Influent BOD = ",b3_BOD_i, "kg/d")

c3_TSS_i = TSS_1 + c3_TSS
print("c. Influent TSS = ",c3_TSS_i, "kg/d")

d3_BOD_r = b3_BOD_i*BOD_removal
print("d. BOD removed = ",d3_BOD_r, "kg/d")

e3_TSS_r = c3_TSS_i*TSS_removal
print("e. tss removed = ",e3_TSS_r, "kg/d")

f3_BOD_e = b3_BOD_i - d3_BOD_r
print("f. Efluent BOD = ",f3_BOD_e, "kg/d")

g3_TSS_e = c3_TSS_i - e3_TSS_r
print("g. Efluent TSS = ",g3_TSS_e, "kg/d")

h3_VSS_r = e3_TSS_r * VSS
print("h. VSS removed = ",h3_VSS_r, "kg/d")

i3_VSS_e = e3_TSS_r - h3_VSS_r
print("i. Efluent VSS = ",i3_VSS_e, "kg/d")

j3_sludge_f = (e3_TSS_r*kg_m3_c)/(slug_concentration)#at % of slug_concentration
print("j. Sludge flow = ",j3_sludge_f, "m3/d")

k3_flow_e = a3_Flow_i - j3_sludge_f
print("k. Efluent flow = ",k3_flow_e, "m3/d")

# # 4.Plant Effluent

# Plant effluent: In the first iteration, assume the plant effluent flow to be 
# the same as the plant influent flow, although this may vary depending on 
# the recycle flows and primary sludge and WAS flows discharged to the 
# sludge processing system
a4_BOD_e = Qdaily*BOD_e*g_kg_c
print("a. BOD = ",a4_BOD_e, "kg/d")

b4_TSS_e = Qdaily*TSS_e*g_kg_c
print("b. TSS = ",b4_TSS_e, "kg/d")


# 5. Secondary process:

# a.Operating parameters:

R_W_c = 0.008 #8000 g/m3
MLSS = 0.8 # 80% OF MLSS
SRT = 6 #dias
Yobs =0.56

b5_flow_i = k3_flow_e

c5_BOD_c = (f3_BOD_e)/(g_kg_c*b5_flow_i)
print("c. inffluent BOD concentration = ",c5_BOD_c, "g/m3")

d5_biomass_P = (Yobs*b5_flow_i*(c5_BOD_c-BOD_e))*g_kg_c
print("d. Biomass Produced: Px = ",d5_biomass_P, "kg/d")

# Note: In reality, the substrate in the effluent (influent soluble BOD escaping 
# treatment) should be determined based on the BOD of the biodegradable 
# effl uent TSS. However, the error in using the effluent BOD as the effluent 
# substrate is negligible. In sizing the aeration basin, some designers ignore 
# the effluent BOD altogether, as it is usually a small amount.
#Determine the solids to be wasted based on the fact that the MLVSS is 80% of MLSS:
e5_WAS = (d5_biomass_P/MLSS)-a4_BOD_e 
print("e. WAS = ",e5_WAS, "kg/d")

#Determine the WAS flow at a solids concentration of 0.8%
f5_WAS_f = (e5_WAS*kg_m3_c)/(R_W_c)
print("f. WAS flow = ",f5_WAS_f, "m3/d")

#Return activated sludge: Assuming an MLSS of 3500 g/m3, compute the RAS ratio:
MLSS_asumed = 3500  #g/m3
W_R_asumed = 8000  #g/m3

g5_RAS = MLSS_asumed/(W_R_asumed-MLSS_asumed)
print("g. RAS(retun rate)= ",g5_RAS, "#78%")
g5_RAS_f = b5_flow_i*g5_RAS
print("g. RAS flow= ",g5_RAS_f, "m3/d")

h5_Total_ML = b5_flow_i+g5_RAS_f
print("h. Total mix liquor = ", h5_Total_ML,"m3/d")

i5_TSS_in_RAS = g5_RAS_f*MLSS*g_m3_c*g_kg_c
print("i. TSS in RAS = ", i5_TSS_in_RAS,"kg/d")

j5_TSS_in_ML = g3_TSS_e + i5_TSS_in_RAS #to the aeration tank (3.g + 5.i)
print("j. ML(to the aeration tank) = ", j5_TSS_in_ML,"kg/d")

k5_TSS_in_ML = j5_TSS_in_ML + d5_biomass_P #from the aeration tank 
print("k. ML(from the aeration tank)= ", k5_TSS_in_ML,"kg/d")

l5_TSS_in_ML_c = k5_TSS_in_ML/(g_kg_c*h5_Total_ML)
print("l. TSS concentration in ML ", l5_TSS_in_ML_c,"g/m3")


# Note: If solids are wasted from mixed liquor, the volume to be wasted 
# based on an MLSS concentration of 3368 g/m3 is

vol_a_desechar = e5_WAS/(l5_TSS_in_ML_c*g_kg_c)
print("Volumen a desechar = ",vol_a_desechar,"m3/d")

# 6.Gravity belt tickening:
# a.operating parameters
a6_WAS_f = f5_WAS_f #5.f
a6_WAS_s = e5_WAS   #5.e
a6_WAS_c = 0.008    #0.8%
a6_Solid_capture_eficiency = 0.95 #95%
Thickened_sludge_concentration = 0.05 #5%


# Belt wash water flow and the weight of polymer are not considered in the 
# mass balance calcwulations.

b6_solids_in_tickened_sludge = a6_WAS_s*a6_Solid_capture_eficiency
print("b. Solidos en el lodo espesado  = ",b6_solids_in_tickened_sludge,"kg/d")

c6_Tsludge_f = (b6_solids_in_tickened_sludge*kg_m3_c)/Thickened_sludge_concentration
print("c. flujo de lodo espesado  = ",c6_Tsludge_f,"m3/d")

d6_VSS_in_Tsludge = b6_solids_in_tickened_sludge*MLSS
print("d. VSS in lodo espesado  = ",d6_VSS_in_Tsludge,"kg/d")

e6_filtrate_f = a6_WAS_f - c6_Tsludge_f
print("e. flujo filtrado  = ",e6_filtrate_f,"m3/d")

f6_TSS_filtrate = a6_WAS_s - b6_solids_in_tickened_sludge
print("f. TSS filtrado  = ",f6_TSS_filtrate,"kg/d")

print("g. Assuming that the BOD of the WAS solids is 50%")
bod_inWAS = 0.5
g6_BOD_filtrate = f6_TSS_filtrate * bod_inWAS
print("       BOD filtrado  = ",g6_BOD_filtrate,"kg/d")

h6_BOD_in_Tsludge = b6_solids_in_tickened_sludge * bod_inWAS
print("h. BOD en lodo espesado  = ",h6_BOD_in_Tsludge,"kg/d")

# # 7. Anaerobic sludge digestion 

# ## a. Operating parameters
a7_VSS_destruction_in_digestion = 0.60 #38%
a7_BOD_in_supernatant = 250 #g/m3
TSS_in_supernatant = 2500 #g/m3
Digested_sludge_drawoff_c = 0.05 # 5%

b7_TSS_to_digester = e3_TSS_r + b6_solids_in_tickened_sludge #(3.e + 6.b)
print("b. TSS al digestor  = ",b7_TSS_to_digester,"kg/d")

c7_VSS_to_digester = h3_VSS_r + d6_VSS_in_Tsludge #(3.h + 6.d)
print("c. VSS al digestor  = ",c7_VSS_to_digester,"kg/d")

d7_FLOW_to_digester = j3_sludge_f + c6_Tsludge_f #(3.j + 6.c)
print("d. FLOW al digestor  = ",d7_FLOW_to_digester,"m3/d")

e7_NON_VSS_to_digester = b7_TSS_to_digester - c7_VSS_to_digester
print("e. non-VSS al digestor  = ",e7_NON_VSS_to_digester,"kg/d")

f7_VSS_remaining_afer_digester = c7_VSS_to_digester*(1-a7_VSS_destruction_in_digestion)
print("f. VSS remanente despues de la digestion  = ",f7_VSS_remaining_afer_digester,"kg/d")

g7_TSS_remaining_afer_digester = e7_NON_VSS_to_digester+f7_VSS_remaining_afer_digester
print("g. TSS remanente despues de la digestion  = ",g7_TSS_remaining_afer_digester,"kg/d")

# h. To determine the flow distribution between supernatant at 3000 g/m3
# (0.3%) concentration and digested sludge draw-off at 5% concentration, let Qs be supernatant flow and Qd be the digested sludge drawoff. The

print("(0.003*Qs [m3/d] + 0.05*Qd [m3/d])*10**(3)kg/m3 = ", g7_TSS_remaining_afer_digester, "kg/d")

A = np.array([[3,50], [1,1]])
B = np.array([g7_TSS_remaining_afer_digester,d7_FLOW_to_digester])

solution = np.linalg.solve(A, B)
Qs = solution[0]
Qd = solution[1]
print("La solución es:", "Qs = ",Qs,"Qd = ",Qd)

i7_BOD_in_supernatant = Qs*a7_BOD_in_supernatant*g_kg_c
print("i. BOD in supernatant  = ",i7_BOD_in_supernatant,"kg/d")

j7_TSS_in_supernatant = Qs*TSS_in_supernatant*g_kg_c
print("j. TSS in supernatant  = ",j7_TSS_in_supernatant,"kg/d")

k7_TSS_in_digested_sludge_drawoff = g7_TSS_remaining_afer_digester - j7_TSS_in_supernatant
print("k. TSS in digested sludge draw off  = ",k7_TSS_in_digested_sludge_drawoff,"kg/d")
# Note: If there is no supernatant recycle, flow to and from the digester is 
# the same (63 m3
# /d), and then


TSS_c_in_digested_sludge = (kg_m3_c*g7_TSS_remaining_afer_digester)/d7_FLOW_to_digester
print(" TSS concentration in digested sludge = ",TSS_c_in_digested_sludge, "(",round(100*TSS_c_in_digested_sludge,4),"%)")

# 8. Belt filter press (BFP) dewatering
# a.Operating parameters 
a8_capture_efficiency = 0.95 #95%
Dewatered_cake_solids = 0.20 #20%
Specific_gravity_cake = 0.95 #95%

# Belt wash water flow and the weight of polymer are not considered in the 
# mass balance calculations

b8_sludge_cake_solids = k7_TSS_in_digested_sludge_drawoff*a8_capture_efficiency
print("b. cantidad de solidos en la torta de lodo  = ",b8_sludge_cake_solids,"kg/d")

c8_cake_volume = (b8_sludge_cake_solids*kg_m3_c)/(Dewatered_cake_solids*1.05)
print("c. volumen de la torta  = ",c8_cake_volume,"m3/d")

d8_FiltrateFlow = Qd- c8_cake_volume
print("d. filtrate flow  = ",d8_FiltrateFlow,"m3/d")

e8_FiltrateTSS = k7_TSS_in_digested_sludge_drawoff- b8_sludge_cake_solids
print("e. filtrate TSS  = ",e8_FiltrateTSS,"kg/d")

print("f. Assuming that the BOD of the filtrate is 50% of the filtrate TSS")
bod_inTSS = 0.5
f8_BOD_in_filtrate = bod_inTSS*e8_FiltrateTSS
print("  BOD in filtrate  = ",f8_BOD_in_filtrate,"kg/d")

# 9. Total recycle quantity versus quantity assumed:
print("VALORES NUEVOS ")
RFlow = d8_FiltrateFlow + Qs + e6_filtrate_f
print("recycle Flow = ",RFlow,"m3/d")

RBOD = f8_BOD_in_filtrate + i7_BOD_in_supernatant + g6_BOD_filtrate
print("recycle BOD = ",RBOD,"kg/d")

RTSS = e8_FiltrateTSS + j7_TSS_in_supernatant + f6_TSS_filtrate
print("recycle TSS = ",RTSS,"kg/d")

print("VALORES SUPUESTOS ")
print("recycle Flow = ",a2_flow,"m3/d")
print("recycle BOD = ",b2_BOD,"kg/d")
print("recycle TSS = ",c3_TSS,"kg/d")

# comparatioN
Flow_P = ((RFlow-a2_flow)/a2_flow)*100
BOD_P = ((RBOD-b2_BOD)/b2_BOD)*100
TSS_P = ((RTSS-c3_TSS)/c3_TSS)*100

print("Porcentaje de diferencia ")
print("Flow = ",round(Flow_P,2),"%")
print("BOD = ",round(BOD_P,2),"%")
print("TSS = ",round(TSS_P,2),"%")

