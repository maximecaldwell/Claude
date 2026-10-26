"""Small built-in wordlists of common English and French words, used by the
'letters' score when you do not give --wordlist.  They deliberately include
1- and 2-letter words (a, I, is, or, y, à, au...) so short messages count.
Accents do not matter: everything is folded to a-z before matching.
"""
from __future__ import annotations

from typing import List

ENGLISH = """
a i am an as at be by do go he if in is it me my no of oh on or so to up us we
ago all and any are ask big boy but can day did end far few for get got had has
her him his how its key let man may men new nor not now off old one our out own
put red run sat saw say see set she sit six sun ten the too top two use war was
way who why win yes yet you
also away back bank bear been bell best bird blue boat body book both call came
camp city cold come copper dark dawn days door down each east even eyes face fall
farm find fire fish five flag four free from gate gave give glad gold good gray
grey half hall hand have head hear help here hide high hill hold home hope hour
into iron just keep kind king lake land last late left life like line lion long
look lost made mail make many mark mile mill mind mine more most move much must
name near need next nine none north note once only open over page park part pass
past path port read rest ring road rock roof room rose rule said salt same sand
seat seen ship shop show side sign snow some soon star stay step stop such sure
take tell than that them then they this time told town tree true turn unit upon
very view wait walk wall want warm well went west what when wide will wind with
wood word work yard year your
about above after again along among angel begin below black block board bound
brook brown build chain chart clear clock close coast count cross dream earth
eight empty enter every field final first floor found front ghost glass going
grand grass great green guard guide heart horse hotel house image inner island
large later layer least level light lower magic metal might money month mount
mouth music never night ninth north ocean often order other paper peace piece
place plain plant point pound queen quiet right river roman round route royal
scale seven shall shore short sight since small sound south space stand start
state steel still stone story table their there these thing think third those
three tower track trail train trees truth under until upper value voice watch
water where which while white whole world would write young
across always animal answer around autumn before behind beyond border bridge
canada center centre church circle corner county dollar double eleven escape
family famous finger follow forest garden golden ground hidden island letter
little lumber market middle mirror moment mother nature number object palace
people person pirate player prince record riddle search second secret silver
simple single spring square stream street summer system thirty toward travel
twelve twenty valley window winter
between brother captain capital century chapter compass country crystal diamond
eastern emerald evening fifteen forever freedom general harbour harbor history
journey kingdom lantern machine message million morning mystery nothing
outside picture railway shelter station student thought through village
western whisper
mountain northern southern treasure
"""

FRENCH = """
a à y ô de du la le les un une et en est il elle on ou où au aux ce ces se sa son
ses sur par pour qui que dans pas plus nous vous ils mais ni si là or ici me te
ma ta mon ton tes mes nos vos leur lui eux moi toi oui non
ami ans art bas bon cap cou cri dos eau feu fer fil fin roi loi lac lit mer mot
mur nez nom nord sud ouest peu pré rue sel sol son tôt vie vin vue âge île val
mont
aide aller allé alors aube auto avec avez avoir bain beau bien blanc bleu bois
bord bout but cave cent cher chez ciel cinq clef clé coin côte cour dame dans
date deux dieu dire dix doux droit elle ange étoile être fait faim fête feuille
fils fond fort four gare gens gros haut heure hier hiver huit jour jeu joie
juste lent lieu long lune main mais mars mère midi mine mois mort neuf nuit onze
pain papier parc part pays père petit pied pierre place plage pluie pont port
porte poste pour prix quai quand quel rive roche rose rouge route sable sage
sang sans seize sept seul soir sous suis tard tour tout tous train trois trou
très vent vers vert vide vieux ville voie voir vous
argent arbre blanche bureau carte centre chemin cheval chose clair colline
compte coutume croix cuivre dernier dessous dessus église enfant ensemble entre
espace étang femme fenêtre fleuve forêt grand grande guerre histoire homme
hiver jardin lettre lumière maison matin minuit monde montagne mystère nombre
ombre parole passage pensée personne pointe premier prince quatre question
rivière ruelle saison secret sentier soleil source temps terre trésor trente
vallée village voyage
"""


def builtin_wordlist(label: str) -> List[str]:
    lab = label.lower()
    if lab.startswith("en"):
        return ENGLISH.split()
    if lab.startswith("fr"):
        return FRENCH.split()
    return ENGLISH.split() + FRENCH.split()


def builtin_name(label: str) -> str:
    lab = label.lower()
    if lab.startswith("en"):
        return "built-in English list (%d words)" % len(ENGLISH.split())
    if lab.startswith("fr"):
        return "built-in French list (%d words)" % len(FRENCH.split())
    return "built-in English+French list (%d words)" % (len(ENGLISH.split()) + len(FRENCH.split()))
