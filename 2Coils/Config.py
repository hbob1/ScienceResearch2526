import math

wireGuage = 16 #Guage
amp = 3 #amps
radius = 0.06 #meters
numCoils = 200
u = 4 * math.pi * pow(10, -7)

if wireGuage == 24:
    # resistance per 1000m
    resistance = 88
elif wireGuage == 22:
    resistance = 52
elif wireGuage == 20:
    resistance = 34
elif wireGuage == 18:
    resistance = 21
elif wireGuage == 16:
    resistance = 13
elif wireGuage == 14:
    resistance = 8.2
elif wireGuage == 12:
    resistance = 5.2
elif wireGuage == 10:
    resistance = 3.3
else:
    print("gauge is not in library")

length = radius * 2 * math.pi * numCoils

resistancePerCoil = resistance * length / 1000

B = u * numCoils * amp / (2 * radius) * 10000
print ("Strength of B in one coil: " + str(B)) # gauss

B2 = pow(0.8, 1.5) * u * numCoils * amp / radius * 10000
print ("Strength of B in between 2 coils: " + str(B2)) #gauss

voltage = amp * resistancePerCoil * 2
print ("Voltage needed for 2 coils: " + str(voltage))

watts = voltage * amp
print ("watts: " + str(watts))


