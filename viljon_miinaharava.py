import datetime as dt
import random as r
import haravasto as h
import ikkunasto as ik

PELINASETUKSET = {
    "leveys": 0,
    "korkeus": 0,
    "miinojen_lkm": 0
}

TILA = {
    "näyttö": "alkunäkymä",
    "kentta_piilossa": [],
    "kentta_näkyvä": [],
    "palaute": " "
}

muuttujia = {
    "pelaajan_nimi_kentta": 0,
    "leveys_kentta": 0,
    "korkeus_kentta": 0,
    "miinojen_lkm_kentta": 0,
    "tekstilaatikko": 0,
}

tilaston_teksti = {
    "sisältö": " "
}

ajantaju = {
    "alkamisaika": dt.datetime.now(),
}

tallennettavat_tiedot = {
    "pelin_alkamisajankohta": " ",
    "pelin_kesto": " ",
    "pelaajan_nimi": "nimeton",
    "lopputulos": "Voitto",
    "kentan_koko": " "
}

koordinaattiparit = {
    "tyhjat_ruudut":[]
}

painikkeet = {
        h.HIIRI_VASEN: "vasen",
        h.HIIRI_KESKI: "keski",
        h.HIIRI_OIKEA: "oikea"
        }

def tutki_ruutu(sisalto, rivin_nro, sarakkeen_nro):
    """
    Funktio tutkii ruudun - jos siellä on eläin, se tulostaa eläimen sijainnin sekä nimen.
    """
    x = sarakkeen_nro
    y = rivin_nro
    if sisalto == " ":
        return True

def tutki_kentta(kentta):
    """
    Funktio tutkii kentän sisällön käymällä sen kokonaan läpi kutsuen tutki_ruutu-funktiota
    jokaiselle kentän sisällä olevalle alkiolle.
    """
    avaamattomat_ruudut = 0
    for i, sisus in enumerate(kentta):
        y = i 
        for j, sisus2 in enumerate(sisus):
            x = j
            sisalto = sisus2
            if tutki_ruutu(sisalto, y, x):
                avaamattomat_ruudut += 1
    return avaamattomat_ruudut


def voitonkulku():
    avaamattomat_ruudut = tutki_kentta(TILA["kentta_näkyvä"])
    if avaamattomat_ruudut == 0:
        #ottaa huomioon ensimmäisen kierroksen, kun listat vielä tyhjiä
        pass
    elif avaamattomat_ruudut == PELINASETUKSET["miinojen_lkm"]:
        TILA["palaute"] = "VOITIT PELIN!!!"
        TILA["näyttö"] = "lopputulos_näkymä"
        tallennettavat_tiedot["lopputulos"] = "Voitto"
        lopetus_aika()
        TILA["kentta_näkyvä"] = []
    else:
        pass

def miinoita(kentta, vapaat_ruudut, aset_miinat_kplm):
    """
    Asettaa kentälle N kpl miinoja satunnaisiin paikkoihin.
    """
    satunnaisuus = []
    random_luku = 0
    while len(satunnaisuus) < aset_miinat_kplm:
        random_luku = r.randrange(len(vapaat_ruudut) - 1)
        if random_luku in satunnaisuus:
            pass
        else:
            satunnaisuus.append(random_luku)
    #selvitetään miinoitettavien ruutujen koordinaatit ja laitetaan ne listaan
    miinoitettavat = []
    for j in satunnaisuus:
        miinoitettavat.append(vapaat_ruudut[j])
    #sijoitetaan miina ("x") selvitettyihin vapaisiin satunnaisiin koordinaatteihin kentälle
    for i in range(aset_miinat_kplm):
        for x_m, y_m in miinoitettavat:
            kentta[y_m][x_m] = "x"

def numeroita(kentta):
    """
    Asettaa näkymättömään listaan jokaisen ruudun kohdalle
    oikeat numeroarvot kuvaamaan ympärillä olevien miinojen lukumäärää.
    Lisäksi selvittää ympärillä olevien ruutujen sisällön
    ja lisää tunetmaatomat koordinattiparilistaan  
    """
    
    kent_korkeus = len(kentta) - 1
    kent_leveys = len(kentta[0]) - 1
    for y in range(len(kentta)):
        for x in range(len(kentta[y])):
            miina_laskuri = 0
            for a, b in [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, 1), (1, 1), (-1, -1), (1, -1)]:
                if 0 <= x + a <= kent_leveys and 0 <= y + b <= kent_korkeus:
                    sisalto = kentta[y + b][x + a]
                    if sisalto == "x":
                        miina_laskuri += 1
            if kentta[y][x] == "x":
                pass
            else:
                TILA["kentta_piilossa"][y][x] = str(miina_laskuri)
             
def selvita_ymparys(x, y, kentta):
    """
    Selvittää ympärillä olevien ruutujen sisällön
    ja lisää tunetmaatomat koordinattiparilistaan
    """
    kent_korkeus = len(kentta) - 1
    kent_leveys = len(kentta[0]) - 1
    for q, r in [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, 1), (1, 1), (-1, -1), (1, -1)]:
        if 0 <= x + q <= kent_leveys and 0 <= y + r <= kent_korkeus:
            sisalto = kentta[y + r][x + q]
            if sisalto == "0":
                koordinaattiparit["tyhjat_ruudut"].append((x + q, y + r))
            if sisalto != "x" and sisalto != "t" and sisalto != "0":
                TILA["kentta_näkyvä"][y + r][x + q] = TILA["kentta_piilossa"][y + r][x + q]          
    
           
def tulvataytto(planeetta, alku_x, alku_y):
    """
    #Merkitsee planeetalla olevat tuntemattomat alueet turvalliseksi siten, että
    #täyttö aloitetaan annetusta x, y -pisteestä.
    """
    koordinaattiparit["tyhjat_ruudut"].append((alku_x, alku_y))
    while koordinaattiparit["tyhjat_ruudut"]:
        x_tutkittava, y_tutkittava = koordinaattiparit["tyhjat_ruudut"][-1]
        koordinaattiparit["tyhjat_ruudut"].pop(-1)
        planeetta[y_tutkittava][x_tutkittava] = "0"
        TILA["kentta_piilossa"][y_tutkittava][x_tutkittava] = "t" #estää ikuisen loopin
        selvita_ymparys(x_tutkittava, y_tutkittava, TILA["kentta_piilossa"])

def luo_kentta():
    """luo kentnän pelaajan asettamien arvojen mukaan"""
    miinojen_lkm = PELINASETUKSET["miinojen_lkm"]
    kentan_leveys = PELINASETUKSET["leveys"]
    kentan_korkeus = PELINASETUKSET["korkeus"]
    tallennettavat_tiedot["kentan_koko"] = "{leveys} X {korkeus}".format(
        leveys=kentan_leveys, korkeus=kentan_korkeus
        )
    kentta = []
    for rivi in range(kentan_korkeus):
        kentta.append([])
        for sarake in range(kentan_leveys):
            kentta[-1].append(" ")
    TILA["kentta_piilossa"] = kentta

    kentta_tyhja = []
    for rivi in range(kentan_korkeus):
        kentta_tyhja.append([])
        for sarake in range(kentan_leveys):
            kentta_tyhja[-1].append(" ")
    TILA["kentta_näkyvä"] = kentta_tyhja
    
    jaljella = []
    for x in range(kentan_leveys):
        for y in range(kentan_korkeus):
            jaljella.append((x, y))

    miinoita(TILA["kentta_piilossa"], jaljella, miinojen_lkm)
    numeroita(TILA["kentta_piilossa"])

def lopetus_aika():
    lopetus_aika = dt.datetime.now()
    kesto = lopetus_aika - ajantaju["alkamisaika"]
    kesto_jaoteluna = str(kesto).split(":")
    minutit = float(kesto_jaoteluna[1])
    sekunnit = float(kesto_jaoteluna[2])
    tallennettavat_tiedot["pelin_kesto"] = \
    "{minutit:.0f} minuuttia ja {sekunnit:.0f} sekunttia".format(
        minutit=minutit, sekunnit=sekunnit
        )

def ajan_seuranta():
    alkamis_ajankohta = dt.datetime.now()
    ajantaju["alkamisaika"] = dt.datetime.now()
    tallennettavat_tiedot["pelin_alkamisajankohta"] = \
    alkamis_ajankohta.strftime("%d.%m.%Y %H:%M")

def kaynnistaa_uuden_pelin():
    luo_kentta()
    ajan_seuranta()
    TILA["näyttö"] = "pelinäkymä"

def gameover():
    TILA["palaute"] = "Hävisit pelin!"
    TILA["näyttö"] = "lopputulos_näkymä"
    tallennettavat_tiedot["lopputulos"] = "Havio"
    lopetus_aika()

def tallenna_syote():
    """
    Tallentaa syötteen ja samalla aloitaa uuden pelin
    TÄHÄN WHILE SILMUKKA VIRHEELLISTEN SYÖTTEIDEN VARALTA"""
    while True:
        try:
            PELINASETUKSET["leveys"] = int(
                ik.lue_kentan_sisalto(muuttujia["leveys_kentta"]).strip().lower())
            PELINASETUKSET["korkeus"] = int(
                ik.lue_kentan_sisalto(muuttujia["korkeus_kentta"]).strip().lower())
            PELINASETUKSET["miinojen_lkm"] = int(
                ik.lue_kentan_sisalto(muuttujia["miinojen_lkm_kentta"]).strip().lower())
            tallennettavat_tiedot["pelaajan_nimi"] = str(
                ik.lue_kentan_sisalto(muuttujia["pelaajan_nimi_kentta"]).strip())
        except ValueError:
            ohje = "Et antanut arvoja kokonaislukuina!"
            ik.kirjoita_tekstilaatikkoon(muuttujia["tekstilaatikko"], ohje)
            return            
        else:
            if PELINASETUKSET["korkeus"] <= 0 \
            or PELINASETUKSET["leveys"] <= 0 \
            or PELINASETUKSET["miinojen_lkm"] <= 0:
                ohje = "Ei hyväksytä nollaa tai negatiivisia lukuja"
                ik.kirjoita_tekstilaatikkoon(muuttujia["tekstilaatikko"], ohje)
                return
            elif PELINASETUKSET["korkeus"] <= 1 or PELINASETUKSET["leveys"] <= 1:
                ohje = "Liian pieni kenttä!"
                ik.kirjoita_tekstilaatikkoon(muuttujia["tekstilaatikko"], ohje)
                return
            elif PELINASETUKSET["korkeus"] >= 30 or PELINASETUKSET["leveys"] >= 20:
                ohje = "Liian iso kenttä!"
                ik.kirjoita_tekstilaatikkoon(muuttujia["tekstilaatikko"], ohje)
                return     
            elif PELINASETUKSET["miinojen_lkm"] >=\
             PELINASETUKSET["korkeus"] * PELINASETUKSET["leveys"]:
                ohje = "Liikaa miinoja"
                ik.kirjoita_tekstilaatikkoon(muuttujia["tekstilaatikko"], ohje)
                return     
            kaynnistaa_uuden_pelin()
            ik.lopeta()
            break

def piilota_tilastolaatikko():
    ik.lopeta()

def kysy_pelikentta_ikkuna():
    """
    Luo graafisen inputin, mihin käyttäjä voi syöttää
    pelin asetuksia.
    """
    kysy_ikkuna = ik.luo_ikkuna("Kentän koko")
    ylakehys = ik.luo_kehys(kysy_ikkuna, ik.YLA)
    alakehys = ik.luo_kehys(kysy_ikkuna, ik.YLA)
    nappikehys = ik.luo_kehys(ylakehys, ik.VASEN)
    syotekehys = ik.luo_kehys(ylakehys, ik.VASEN)
    ik.luo_nappi(nappikehys, "aloita peli!", tallenna_syote)
    ik.luo_tekstirivi(syotekehys, "Pelaajan nimi")
    muuttujia["pelaajan_nimi_kentta"] = ik.luo_tekstikentta(syotekehys)
    ik.luo_tekstirivi(syotekehys, "Määrää kentän leveys")
    muuttujia["leveys_kentta"] = ik.luo_tekstikentta(syotekehys)
    ik.luo_tekstirivi(syotekehys, "Määrää kentän korkeus")
    muuttujia["korkeus_kentta"] = ik.luo_tekstikentta(syotekehys)
    ik.luo_tekstirivi(syotekehys, "Määrää miinojen lukumäärä")
    muuttujia["miinojen_lkm_kentta"] = ik.luo_tekstikentta(syotekehys)
    muuttujia["tekstilaatikko"] = ik.luo_tekstilaatikko(alakehys, 45, 20)
    ik.kirjoita_tekstilaatikkoon(
        muuttujia["tekstilaatikko"], "Valitse kentän koko ruutuina"
        )
    ik.kaynnista()

def nayta_tilastot_ikkuna():
    """
    Luo graafisen näkymän tilastojen näyttämistä varten
    """
    tilastot_ikkuna = ik.luo_ikkuna("Tilastot")
    ylakehys = ik.luo_kehys(tilastot_ikkuna, ik.YLA)
    alakehys = ik.luo_kehys(tilastot_ikkuna, ik.YLA)
    nappikehys = ik.luo_kehys(alakehys, ik.VASEN)
    ik.luo_nappi(nappikehys, "Sulje", piilota_tilastolaatikko)
    tilastolaatikko = ik.luo_tekstilaatikko(ylakehys, 100, 20)
    ik.kirjoita_tekstilaatikkoon(tilastolaatikko,\
         tilaston_teksti["sisältö"])
    ik.kaynnista()

#Itse luotujen nappien toiminnot
#Tehty helpottamaan ohjelman toiminnan hahmottamista

def uusi_peli_nappain():
    kysy_pelikentta_ikkuna()

def palaa_nappain():
    TILA["näyttö"] = "alkunäkymä"

def tilastot_nappi():
    try:
        with open("tilastot.txt") as tilastot:
                tilaston_teksti["sisältö"] = tilastot.read()
    except IOError:
        tilaston_teksti["sisältö"] = "Tiedoston avaaminen ei onnistunut."
    nayta_tilastot_ikkuna()

def lopeta_nappi():
    h.lopeta()

def palaa_paavalikkoon_nappain():
    TILA["näyttö"] = "alkunäkymä"

def tallenna_peli_nappain():
    try:
        #kopioitu materiaalista
        with open("tilastot.txt", "a") as tilastot:
            tilastot.write("{pelaaja}, {alkamisajankohta}, {kesto}, {lopputulos}, {kent_koko}\n".format(
                pelaaja=tallennettavat_tiedot["pelaajan_nimi"],
                alkamisajankohta=tallennettavat_tiedot["pelin_alkamisajankohta"],
                kesto=tallennettavat_tiedot["pelin_kesto"],
                lopputulos=tallennettavat_tiedot["lopputulos"],
                kent_koko=tallennettavat_tiedot["kentan_koko"],
                ))
        TILA["palaute"] = "Peli tallennettu"
    except IOError:
        TILA["palaute"] = "Kohdetiedostoa ei voitu avata. Tallennus epäonnistui"


def main_hiiri_kasittelija(x, y, painike, muok_mappain):
    if TILA["näyttö"] == "alkunäkymä":
        #Hiiren käsitteljiä alkunäkymässä
        if 360 < x < 440 and 360 < y < 400:
            uusi_peli_nappain()
        elif 360 < x < 440 and 300 < y < 340:
            tilastot_nappi()
        elif 360 < x < 440 and 240 < y < 280:
            lopeta_nappi()

    elif TILA["näyttö"] == "pelinäkymä":
        #Hiiren käsittelijä pelinäkymässä
        if painike == h.HIIRI_VASEN:
            hiiri_x = int(x / 40)
            hiiri_y = int(y / 40)
            if x > PELINASETUKSET["leveys"] * 40 and y < 40:
                palaa_nappain()
            elif x > PELINASETUKSET["leveys"] * 40 and y > 40:
                #tyhjä alue
                pass
            else:
                if TILA["kentta_piilossa"][hiiri_y][hiiri_x] == "0":
                    tulvataytto(TILA["kentta_näkyvä"], hiiri_x, hiiri_y)
                elif TILA["kentta_piilossa"][hiiri_y][hiiri_x] == "x":
                    TILA["kentta_näkyvä"][hiiri_y][hiiri_x] =\
                     TILA["kentta_piilossa"][hiiri_y][hiiri_x]
                    gameover()
                elif TILA["kentta_piilossa"][hiiri_y][hiiri_x] == "t":
                    pass
                else:
                    TILA["kentta_näkyvä"][hiiri_y][hiiri_x] =\
                     TILA["kentta_piilossa"][hiiri_y][hiiri_x]
        elif painike == h.HIIRI_KESKI:
            print(
                "Hiiren nappia {painike} painettiin kohdassa {x}, {y}".format(
                    painike=painikkeet[h.HIIRI_KESKI], x=x, y=y))
        elif painike == h.HIIRI_OIKEA:
            #tulossa lipputoiminto tähän
            print(
                "Hiiren nappia {painike} painettiin kohdassa {x}, {y}".format(
                    painike=painikkeet[h.HIIRI_OIKEA], x=x, y=y))

    elif TILA["näyttö"] == "lopputulos_näkymä":
        #Hiiren käsitteljiä alkunäkymässä
        if 320 < x < 480 and 360 < y < 400:
            palaa_paavalikkoon_nappain()
        elif 320 < x < 440 and 300 < y < 340:
            tallenna_peli_nappain()

        
def piirra_kayttoliittyma():
    if TILA["näyttö"] == "alkunäkymä":
        #Piirtää grafiikat alkutilanteessa
        h.tyhjaa_ikkuna()
        h.piirra_tausta()
        h.muuta_ikkunan_koko(800, 600)
        h.aloita_ruutujen_piirto()
        # uusi_peli nappi
        h.lisaa_piirrettava_ruutu("0", 360, 360)
        h.lisaa_piirrettava_ruutu("0", 400, 360)
        h.lisaa_piirrettava_ruutu("0", 440, 360)
        #tilastot napin pohja
        h.lisaa_piirrettava_ruutu("0", 360, 300)
        h.lisaa_piirrettava_ruutu("0", 400, 300)
        h.lisaa_piirrettava_ruutu("0", 440, 300)
        #lopeta napin pohja
        h.lisaa_piirrettava_ruutu("0", 360, 240)
        h.lisaa_piirrettava_ruutu("0", 400, 240)
        h.lisaa_piirrettava_ruutu("0", 440, 240)

        h.piirra_ruudut()

        #tekstien lisaykset
        h.piirra_tekstia(\
            "Viljon miinaharava", 345, 450, vari=(0, 0, 0, 255), fontti="serif", koko=20)
        h.piirra_tekstia("Uusi peli", 368, 362, vari=(0, 0, 0, 255), fontti="serif", koko=20)
        h.piirra_tekstia("Tilastot", 368, 302, vari=(0, 0, 0, 255), fontti="serif", koko=20)
        h.piirra_tekstia("Lopeta", 368, 242, vari=(0, 0, 0, 255), fontti="serif", koko=20)

    elif TILA["näyttö"] == "pelinäkymä":
        #Piirtää grafiikat pelinäkymässä
        h.tyhjaa_ikkuna()
        h.piirra_tausta()
        h.muuta_ikkunan_koko(PELINASETUKSET["leveys"] * 40 + 80, PELINASETUKSET["korkeus"] * 40)
        h.aloita_ruutujen_piirto()
        for y_p, tyhja in enumerate(TILA["kentta_näkyvä"]):
            for x_p, sisalto in enumerate(TILA["kentta_näkyvä"][y_p]):
                h.lisaa_piirrettava_ruutu(sisalto, x_p * 40, y_p * 40)
        #lopeta napin pohja
        h.lisaa_piirrettava_ruutu("0", PELINASETUKSET["leveys"] * 40, 0)
        h.lisaa_piirrettava_ruutu("0", PELINASETUKSET["leveys"] * 40 + 40, 0)
        h.piirra_ruudut()
        #lopeta tekstin lisäys
        h.piirra_tekstia("Lopeta",\
             PELINASETUKSET["leveys"] * 40 + 4, 4, vari=(0, 0, 0, 255), fontti="serif", koko=14)

    elif TILA["näyttö"] == "lopputulos_näkymä":
        #Piirtää grafiikat alkutilanteessa
        h.tyhjaa_ikkuna()
        h.piirra_tausta()
        h.muuta_ikkunan_koko(800, 600)
        h.aloita_ruutujen_piirto()
        #Palaa päävalikkoon nappin pohja
        h.lisaa_piirrettava_ruutu("0", 320, 360)
        h.lisaa_piirrettava_ruutu("0", 360, 360)
        h.lisaa_piirrettava_ruutu("0", 400, 360)
        h.lisaa_piirrettava_ruutu("0", 440, 360)
        h.lisaa_piirrettava_ruutu("0", 480, 360)
        #Tallenna peli napin pohja
        h.lisaa_piirrettava_ruutu("0", 320, 300)
        h.lisaa_piirrettava_ruutu("0", 360, 300)
        h.lisaa_piirrettava_ruutu("0", 400, 300)
        h.lisaa_piirrettava_ruutu("0", 440, 300)

        h.piirra_ruudut()

        #tekstien lisaykset
        h.piirra_tekstia(TILA["palaute"], 320, 450, vari=(0, 0, 0, 255), fontti="serif", koko=20)
        h.piirra_tekstia("Palaa päävalikkoon",\
             328, 362, vari=(0, 0, 0, 255), fontti="serif", koko=16)
        h.piirra_tekstia("Tallenna peli", 328, 302, vari=(0, 0, 0, 255), fontti="serif", koko=16)

def juoksevat_asiat(kulunut_aika):
    """
    toistuva käsittelijä 
    """
    #Päivittää grafiikoita 60 kertaa sekunnissa
    h.aseta_piirto_kasittelija(piirra_kayttoliittyma)
    h.aseta_hiiri_kasittelija(main_hiiri_kasittelija)

    #seuraa milloin pelaaja voittaa pelin 
    voitonkulku()
    
h.lataa_kuvat("spritet")
h.luo_ikkuna()
h.aseta_toistuva_kasittelija(juoksevat_asiat)

h.aloita()
