from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import sessionmaker
from datetime import datetime

import click

# TBD datum přidání do knihovny
# TBD přečtená
# TBD rozečtená
# TBD datum zapůjčení

'''
Aplikace by měla uchovávat tyto údaje:
- název knihy
- autor
- počet stran
- datum přidání do knihovny
- přečtená (ano/ne)
- rozečtená (ano/ne)
- půjčená (půjčená komu/None)
- datum zapůjčení (datum/None)
- další informace, které uznáte za vhodné (např. identifikace knihy, slovní hodnocení)

S aplikací by mělo být možné zacházet zeširoka,
tedy knihy vkládat, vypisovat, zapůjčovat a zápůjčky vracet,
editovat chybné položky, nastavovat příznak přečtení a rozečtení atd.
Výpis ideálně nějak rozumně formátovaný,
řípadně např. celkový + detailní o jedné knize.
'''

db = create_engine("sqlite:///knihy.sqlite")
Base = declarative_base()

def pripoj_se():
    Base.metadata.create_all(db)
    Session = sessionmaker(bind=db)
    return Session()

@click.group()
def knihovna():
    pass


class Kniha(Base):
    # Název tabulky s knihami
    __tablename__ = "knihy"
    # Číselný identifikátor knihy
    id = Column(Integer, primary_key=True)
    # Název knihy
    nazev = Column(String)
    # Autor
    autor = Column(String)
    # Počet stran
    pocet_stran = Column(Integer)
    # Datum přidání do knihovny
    pridano = Column(DateTime)
    # Přečtená (ano/ne)
    precteno = Column(String)
    # Rozečteno (ano/ne)
    rozecteno = Column(Integer)
    # Půjčená (půjčená komu/None)
    pujceno = Column(String)
    # Datum zapůjčení (datum/None)
    datum_zapujceni = Column(DateTime)


    def __repr__(self):
        return f"<Kniha(nazev='{self.nazev}',autor={self.autor}, pocet_stran={self.pocet_stran}, pridano={self.pridano}, precteno={self.precteno}, rozecteno={self.rozecteno}, pujceno={self.pujceno}, datum_zapujceni={self.datum_zapujceni})>"


#Session = sessionmaker(bind=db)
#sezeni = Session()
#Base.metadata.create_all(db)

# Vkládat
@knihovna.command()
@click.option('--zadani',prompt= 'Zadej knihu')
def pridej(zadani):
    sezeni = pripoj_se()
    kniha = Kniha(nazev=zadani, pridano = datetime.now())
    sezeni.add(kniha)
    sezeni.commit()
    print(f'Přidána {kniha.nazev} {kniha.pridano}')

# Vypisovat
@knihovna.command()
def vypis():
    sezeni = pripoj_se()
    dotaz = sezeni.query(Kniha)
    for kniha in dotaz.all():
        print(f'{"[x]" if kniha.pujceno else "[ ]"} {kniha.id} {kniha.nazev} {kniha.autor} {kniha.pocet_stran}p. {kniha.pridano} {kniha.precteno} {kniha.pujceno}')

# Editovat chybné položky
@knihovna.command()
@click.option('--identifikace',prompt='Zadej ID knihy')
@click.option('--pocet_stran',prompt='Zadej počet stran')
@click.option('--autor',prompt='Zadej autora')
#@click.option('--datum',prompt='Zadej datum pridani do knihovny')
def edit(identifikace, pocet_stran, autor):
    sezeni = pripoj_se()
    dotaz = sezeni.query(Kniha)
    kniha = dotaz.filter_by(id=identifikace).one()
    if pocet_stran != None:
        kniha.pocet_stran = pocet_stran
    if autor != None:
        kniha.autor = autor
    sezeni.add(kniha)
    sezeni.commit()
    print(f'Kniha s ID {kniha.id} byla editována')


# Zapůjčovat
@knihovna.command()
@click.option('--identifikace',prompt='Zadej ID knihy')
@click.option('--komu', prompt = 'Zadej komu vypůjčit')
def vypujci(identifikace, komu):
    sezeni = pripoj_se()
    dotaz = sezeni.query(Kniha)
    kniha = dotaz.filter_by(id=identifikace).one()
    kniha.pujceno = komu
    sezeni.add(kniha)
    sezeni.commit()
    print(f'Kniha s ID {kniha.id} je vypůjčena {kniha.pujceno}')

# Výpujčky vracet
@knihovna.command()
@click.option('--identifikace',prompt='Zadej ID knihy')
def vrat(identifikace):
    sezeni = pripoj_se()
    dotaz = sezeni.query(Kniha)
    kniha = dotaz.filter_by(id=identifikace).one()
    kniha.pujceno = None
    sezeni.add(kniha)
    sezeni.commit()
    print(f'Kniha s ID {kniha.id} je vrácena.')


# Nastavovat příznak přečtení
@knihovna.command()
@click.option('--identifikace',prompt='Zadej ID knihy')
@click.option('--precteno/--neprecteno', default=False, prompt="Prečtena?")
def oznac(identifikace, precteno, neprecteno=None):
    sezeni = pripoj_se()
    dotaz = sezeni.query(Kniha)
    kniha = dotaz.filter_by(id=identifikace).one()
    if precteno:
        kniha.precteno = 'prectena'
    else:
        kniha.precteno = 'neprectena'
    sezeni.add(kniha)
    sezeni.commit()
    print(f'Kniha {kniha.id} byla přečtena')


# Nastavovat příznak rozečtení




if __name__ == "__main__":
    knihovna()
