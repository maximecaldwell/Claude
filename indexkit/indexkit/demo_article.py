"""A made-up article (English + French) used by `demo` and `selftest`.
Every place and person in it is invented.  Nothing is downloaded.
"""
from __future__ import annotations

import textwrap

EN_PARAGRAPHS = [
    "The Lanterns of Lac-des-Lanternes: a village that keeps its lights on",
    "Every autumn, when the first frost settles on the shore, the people of "
    "Lac-des-Lanternes hang a paper lantern in every window. Nobody remembers "
    "exactly when the custom began. Some say it was 1887; others insist it is "
    "older than the church.",
    "The village sits at the end of a gravel road, forty minutes north of "
    "Val-du-Cuivre. In summer, canoes drift past the old copper mill; in winter, "
    "the lake freezes so thick that trucks cross it to reach Pointe-aux-Hérons.",
    "“We don’t do it for tourists,” says Madeleine Arsenault, who has run "
    "the general store for thirty-one years. “We do it so the fishermen can "
    "find their way home – that’s all.”",
    "Her store sells bait, coffee, and maps of the islands. The most popular map "
    "shows a hiking trail that climbs Mont Sureau, the rounded hill behind the "
    "school. From the summit, on a clear night, you can count more than two "
    "hundred lanterns.",
    "Not everyone is pleased. A councillor from the regional office complained "
    "last year that the lanterns are a fire hazard: paper, candles, and old "
    "wooden houses. The village answered with battery lights, which glow a "
    "little bluer than before.",
    "The tradition has its own vocabulary. A lantern that goes out before "
    "midnight is called a “sleeper”; one that lasts until dawn is a "
    "“keeper”. Children compete to light the most keepers, and the winner "
    "rings the bell at the Rivière-Noire bridge.",
    "Historians at the provincial archives have found only one written mention "
    "of the custom before 1950: a letter from a schoolteacher describing “a "
    "necklace of small suns” around the bay. The letter is unsigned. It also "
    "mentions the gold rush.",
    "This year the festival begins on the second Saturday of October. Visitors "
    "are welcome, says Arsenault, as long as they leave their own lantern lit "
    "for one night. “It is a promise,” she adds, “not a decoration.”",
]

FR_PARAGRAPHS = [
    "Les lanternes de Lac-des-Lanternes : un village qui garde ses lumières allumées",
    "Chaque automne, quand le premier gel se pose sur la rive, les gens de "
    "Lac-des-Lanternes accrochent une lanterne de papier à chaque fenêtre. "
    "Personne ne se souvient exactement du début de la coutume. Certains disent "
    "que c’était en 1887 ; d’autres affirment qu’elle est plus vieille "
    "que l’église.",
    "Le village se trouve au bout d’un chemin de gravier, à quarante minutes "
    "au nord de Val-du-Cuivre. L’été, les canots glissent devant le vieux "
    "moulin de cuivre ; l’hiver, le lac gèle si épais que les camions le "
    "traversent pour rejoindre Pointe-aux-Hérons.",
    "« On ne le fait pas pour les touristes », dit Madeleine Arsenault, "
    "qui tient le magasin général depuis trente et un ans. « On le fait "
    "pour que les pêcheurs retrouvent le chemin de la maison – c’est "
    "tout. »",
    "Son magasin vend des appâts, du café et des cartes des îles. La carte "
    "la plus populaire montre un sentier qui grimpe le mont Sureau, la colline "
    "arrondie derrière l'école. Du sommet, par une nuit claire, on peut "
    "compter plus de deux cents lanternes.",
    "Tout le monde n’est pas content. Un conseiller du bureau régional s’est "
    "plaint l’an dernier : les lanternes seraient un risque d’incendie "
    "(papier, chandelles et vieilles maisons de bois). Le village a répondu "
    "avec des lumières à piles, un peu plus bleues qu’avant.",
    "La tradition a son propre vocabulaire. Une lanterne qui s’éteint avant "
    "minuit est une « dormeuse » ; celle qui dure jusqu’à l’aube "
    "est une « gardienne ». Les enfants rivalisent pour allumer le plus "
    "de gardiennes, et le gagnant sonne la cloche du pont de la Rivière-Noire.",
    "Aux archives provinciales, les historiens n’ont trouvé qu’une seule "
    "mention écrite de la coutume avant 1950 : la lettre d’une "
    "institutrice décrivant « un collier de petits soleils » autour "
    "de la baie. La lettre n’est pas signée. Elle évoque aussi la ruée "
    "vers l'Or.",
    "Cette année, la fête commence le deuxième samedi d’octobre. Les "
    "visiteurs sont les bienvenus, dit Arsenault, pourvu qu’ils laissent leur "
    "propre lanterne allumée une nuit. « C’est une promesse, "
    "ajoute-t-elle, pas une décoration. »",
]

# Place names in the article: what a "hit" means in the demo.
TARGETS = [
    "Lac-des-Lanternes", "Val-du-Cuivre", "Pointe-aux-Hérons", "Mont Sureau",
    "Rivière-Noire", "Sureau", "Cuivre", "Hérons",
]


def as_file_text(paragraphs) -> str:
    """Hard-wrapped at 72 characters, blank line between paragraphs, like a
    typical .txt file."""
    out = [paragraphs[0]]
    for p in paragraphs[1:]:
        out.append(textwrap.fill(p, width=72, break_long_words=False, break_on_hyphens=False))
    return "\n\n".join(out) + "\n"
