import math

def main(L: int, max: int = -13, min: int = -20):
    wyniki = []

    for f in fArr:
        wzmocnieniaArr = set([])
        wyniki.append(f"Tłumienie {L}m kabla dla {f} MHz: {tlumienieKabla(100, f, L, 19)} dB")
        l = tlumienie(tlumienieKabla(100, f, L, 19), 3,6,3)
        for i in gArr:
            for j in gArr:
                g = wzmocnienie(i,j)
                for p in pArr:
                    if p - l + g < max and p - l + g > min:
                        wyniki.append((round(p, 2), g, (i, j), round(p - l + g, 2)))


    print(f"\nmoc na wejściu (dBm) \t Łączne Wzmocnienie (dB)\t(G1, G2) (dB) \t moc na wyjściu (dBm)\n")
    for i in wyniki:
        pair = i[2]
        pair == 'u' or wzmocnieniaArr.add(pair)
        print(i)

    print(f"\nZestawy pasujących Wzmocnień: \n")
    for i in wzmocnieniaArr:
        print(i)
        
def dbm_to_mw(dbm: float):
    return 10 ** (dbm / 10)

def mw_to_dbm(mw: float):
    return 10 * math.log10(mw)              #log10 to zwykły log()


def tlumienieKabla(fRef:int, f: int, L: int, A: int):
    wynikRef = A * (L / fRef)  # wynik w dB dla 100mhz np.
    wynikF = wynikRef * math.sqrt(f / fRef)  # wynik w dB dla 400mhz np.
    return wynikF           # wynik w dB

def tlumienie(Tkabla, *Treszty):
    return Tkabla + sum(Treszty)

def wzmocnienie(g1, g2):
    return g1 + g2


fRef = 100  # częstotliwość referencyjna
fArr = [300, 400, 600]  # tablica czestotliwosci dla ktorych liczymy
gArr = [10,15,20,25,30]  # tablica wzmocnien dla ktorych liczymy

A = 19  # współczynnik tłumienia dla 100mhz
L = 38  # długość kabla w metrach
pArr = list(map(lambda x: mw_to_dbm(x * math.pow(10, -5)) ,[x for x in range(1, 6)]))  # tablica mocy w dbm, wczesniej zmieniona na mw
#[-50.0, -46.98970004336019, -45.228787452803374, -43.979400086720375, -43.01029995663981]
main(L)
