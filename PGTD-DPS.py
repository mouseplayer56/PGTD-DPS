def appendDPS_1s(Tower):  # this shows the DPS done in the first second of firing
    DPS = 0
    empty = False
    exRnds = 0

    Tower[1] += Tower[4]
    if Tower[1] == 0:  # just so it doesn't divide by 0 (throws ERROR)
        SPS = 0
    else:
        SPS = 1/Tower[1]
        if SPS == 1:
            exRnds -= 1
    exRnds += (SPS//1) + 1

    # this format is pretty much the same for appendDPS_sustained(), so i'll explain both here.
    # this pretty much simulates the gun being fired over "n" amount of time.
    # "exRnds" is the amount of shots that can be fired within n time.
    # once exRnds reaches 0, that indicates there is no more time to shoot.

    while (exRnds // 1) > 0:  # repeats until there's no more exRnds (shots to shoot).
        if exRnds >= Tower[5]:  # if an entire magazine can be shot, it'll do so.
            # this also means the gun is empty and has to be reloaded, costing exRnds.
            DPS += Tower[5] * Tower[0]
            exRnds -= Tower[5]
            empty = True  # gun is now empty, empty state is "True"
        else:  # if an entire magazine CANNOT be shot, it'll use as much exRnds as are in the magazine
            DPS += exRnds * Tower[0]
            exRnds = 0
            empty = False
        if empty:  # once the gun is empty, it will reload. this costs exRnds because it takes up time
            # depending on how long the reload time is, depends on how much exRnds are taken up
            # abstracted calculation of the below:
            # Rounds I can fire = Rounds I can fire - Rounds I could've fired during reload time
            exRnds = exRnds - (SPS * Tower[3])/1
            empty = False
    
    print("1s DPS =", DPS)
    Tower.append(round(DPS, 3))
    return Tower

def appendDPS_sustained(Tower, seconds):  # this shows the DPS over "seconds" seconds of firing
    DPS = 0
    empty = False
    exRnds = 0

    Tower[1] += Tower[4]
    if Tower[1] == 0:  # just so it doesn't divide by 0 (throws ERROR)
        SPS = 0
    else:
        SPS = seconds/Tower[1]
    if SPS == 1:
        exRnds -= 1
    exRnds += (SPS//1) + 1
##    print(exRnds)

    while (exRnds // 1) > 0:
##        print("exRnds =", exRnds)
        if exRnds >= Tower[5]:
            DPS += Tower[5] * Tower[0]
            exRnds -= Tower[5]
            empty = True
##            print("magdump, DPS=", DPS)
        else:
            DPS += exRnds * Tower[0]
            exRnds = 0
            empty = False
##            print("partial, DPS=", DPS)

        if empty:
##            print("pre-reload, exRnds=",exRnds)
            exRnds = exRnds - (SPS * Tower[3])/seconds
            empty = False
##            print("reload, exRnds=", exRnds)

    DPS = DPS/seconds
    print("sustained DPS =", DPS)
    Tower.append(round(DPS, 3))
    return Tower


def append_gList(gList):  # this runs all the append DPS cmds
    print()
    gList = appendDPS_1s(gList)
    gList = appendDPS_sustained(gList, 60)
    print(gList, "\n")
    return gList

userInp = None
gTowers = []
#gTowers format:
#[damage0, fire_rate1, range2, reload_time3, reload_firerate4, magazine_size5]

while userInp != "exit":
    gWeapons = []
    gTowers = []
    gCombos = []
    userInp = str(input("'place' tower or 'exit'?\n")).lower()
    if userInp == "place":

        # this is purely for weapon stats
        name = str(input("weapon_name = "))
        fit = float(input("magazine_size = "))
        zt = float(input("damage = "))
        tt = float(input("range = "))
        ot = float(input("fire_rate = "))
        trt = float(input("reload_speed = "))
        ft = float(input("reload_fire_rate = "))

# this code can be uncommented for debugging
##        name = "tactical rifle"
##        fit = float(30)
##        zt = 7.9
##        tt = float(83)
##        ot = 0.11
##        trt = 1.5
##        ft = 0.045

        print(name)
        gWeapons = [zt, ot, tt, trt, ft, fit, name]
        print(gWeapons)
        gWeapons = append_gList(gWeapons)
        typeoutW = str(gWeapons[6])+":"+" 1s_DPS = "+str(gWeapons[7])+" / "+"sustained_DPS = "+str(gWeapons[8])+"\n"

        # optional, allows the user to check specific combos
        userInp = input("'tower' or 'no'?\n").lower()
        if userInp == "tower":
            tname = str(input("tower_name = "))
            tfit = float(input("ammo = "))
            ttrt = float(input("reload_time = "))
            tzt = float(input("damage = "))
            tot = 1/(float(input("fire_rate = ")))
            ttt = float(input("range = "))

# this code can be uncommented for debugging
##            tname = "Pro"
##            tfit = float(1)
##            ttrt = 1.15
##            tzt = 1.15
##            tot = 0.95
##            ttt = 1.1
            
            cfit = round((fit * tfit), 3)
            czt = round((zt * tzt), 3)
            ctt = round((tt * ttt), 3)
            cot = round((ot * tot), 3)
            ctrt = round((trt * ttrt), 3)
            cft = round((ft / ttrt), 3)
            cname = name+" & "+tname

            gTowers = [tzt, tot, ttt, ttrt, 0, tfit, tname]
            print(cname)
            gCombos = [czt, cot, ctt, ctrt, cft, cfit, cname]
            gCombos = append_gList(gCombos)
            typeoutC = str(gCombos[6])+":"+" 1s_DPS = "+str(gCombos[7])+" / "+"sustained_DPS = "+str(gCombos[8])+"\n"
            # this writes into a "combos" txt file.
            with open("PGTD-DPSc_records.txt", "a") as f:
                f.write(typeoutC)

        # this (default) writes into a "weapons" txt file.
        with open("PGTD-DPSw_records.txt", "a") as f:
            f.write(typeoutW)
    else:
        print("fuck you")
exit(0)
