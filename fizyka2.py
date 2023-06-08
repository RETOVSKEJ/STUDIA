import math

S = 0.24  # nachylenie amplitudy [mw/mA]  (wzrost na mw)
I = 45 # amplituda prądu w impulsie "1" [mA]  M
Iprog = 10 # amplituda prądu w stanie spoczynku [mA]
Fmod = 34 # częstotliwość modulacji impulsów przez zegar modulacji [GHz]  (zegar modulacji określa liczbę bitów w jednej sekundzie)
Rf = 0.88 # czułość fotodiody [mA/mW]

L = 42 # dlugość światłowodu [km]
MaxL = 5 # maxymalna dlugosc jednego odcinka swiatlowodu [km]
LLoss = 0.5 # strata na każdym łączeniu światłowodu [dB]
A = 0.28 # tłumienie światłowodu [dB/km]
N = math.ceil((L / MaxL) + 1) # liczba połączeń światłowodu

def main():
    #### zadanie 1 ####
    Pnad = S * (I-Iprog)  # [mW] moc na wyjsciu nadajnika

    #### zadanie 2 ####
    T = N * LLoss + L * A   # TŁUMIENIE [dB] = całkowita strata na łączeniach w światłowodzie + Tłumienie kabla 
    Tmw = round(dbm_to_mw(T), 4)  # Tłumienie w mW

    #### zadanie 3 ####
    Podb = mw_to_dbm(Pnad) - T  # moc na wejsciu odbiornika [dBm]
    Podb = round(dbm_to_mw(Podb), 3)  # moc na wejsciu odbiornika [mW]

    #### zadanie 4 ####
    Imo = round(Podb * Rf, 3)  # wartosc prądu w impulsie w prądzie fotodiody [mA]

    #### zadanie 5 ####
    h = 6.626 * math.pow(10, -34)  # stała plancka [J*s]
    λ = 1320 # długość fali [nm]
    c = 300_000_000 # predkosc swiatla [m/s]
    f_opt = round(c / (λ * math.pow(10, -9)), -11) # częstotliwość światła, zaokraglona do pierwszych 4 cyfr [Hz]
    Ef = round(h * f_opt, 21)  # energia fotonu [J]
    N_fotonow_nad = policzFotony(Pnad, Ef)  # BŁĄD W PREZENTACJI
    N_fotonow_odb = policzFotony(Pnad, Ef, dbm_to_mw(T))  # BŁĄD W PREZENTACJI

    ####### ODPOWIEDZI #########
    print(Pnad, "mW = Moc na wyjsciu nadajnika")
    print(T, "dB / ", Tmw, "mW = Całkowite tłumienie światłowodu")
    print(Podb, "mW = Moc na wejsciu odbiornika")
    print(Imo, "mA = Natężenie w impulsie w prądzie fotodiody")
    print(N_fotonow_nad, " = Liczba fotonów w jednym impulsie nadajnika")
    print(N_fotonow_odb, " = Liczba fotonów docierajacych do odbiornika")


def policzFotony(Pnad: float, Ef: float, T: float = ""):
    F_mod = Fmod * math.pow(10, 9) # zamiana z Ghz na Hz
    N = mw_to_js(Pnad) / Ef     # ILOSC FOTONOW NA SEKUNDE
    N_nad = N / F_mod           # ILOSC FOTONOW NA JEDEN IMPULS
    if T != "":   # Jesli podamy tłumienie
        N_odb = N_nad / T
        return round(N_odb)
    return round(N_nad)

def dbm_to_mw(dbm: float):
    return 10 ** (dbm / 10)

def mw_to_dbm(mw: float):
    return 10 * math.log10(mw)              #log10 to zwykły log()

def mw_to_js(mw: float):
    return round(mw * math.pow(10, -3), 6)            #miliwaty na dżule/s

main()