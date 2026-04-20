"""Acari species data from the Fauna of India checklist."""

from __future__ import annotations

import csv
from pathlib import Path


ACARI_SPECIES = [
    {
        "species_name": "Gehypochthonius rhadamanthus",
        "date": "1936",
        "discoverer": "Jacot"
    },
    {
        "species_name": "Brachychthonius pacificus",
        "date": "1973",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Eobrachychthonius latior",
        "date": "1910",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Sellnickochthonius cricoides",
        "date": "1948",
        "discoverer": "Weis-Fogh"
    },
    {
        "species_name": "Cosmochthonius (Cosmochthonius) agartalaensis",
        "date": "1983",
        "discoverer": "Sarkar"
    },
    {
        "species_name": "Cosmochthonius (Cosmochthonius) assamensis",
        "date": "1984",
        "discoverer": "Roy Talukdar and Chakrabarti"
    },
    {
        "species_name": "Cosmochthonius (Cosmochthonius) bengalensis",
        "date": "1972",
        "discoverer": "Chakrabarti et al."
    },
    {
        "species_name": "Cosmochthonius (Cosmochthonius) lanatus diversiseta",
        "date": "1982",
        "discoverer": "Sarkar and Subias"
    },
    {
        "species_name": "Cosmochthonius (Cosmochthonius) lanatus lanatus",
        "date": "1885",
        "discoverer": "Michael"
    },
    {
        "species_name": "Cosmochthonius (Cosmochthonius) plumatus suramericanus",
        "date": "1958",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Phyllozetes emmae",
        "date": "1910",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Phyllozetes longifolius",
        "date": "1986",
        "discoverer": "Balakrishnan"
    },
    {
        "species_name": "Phyllozetes nilamburicus",
        "date": "1986",
        "discoverer": "Balakrishnan"
    },
    {
        "species_name": "Haplochthonius (Haplochthonius) arcuata",
        "date": "1998",
        "discoverer": "Bose et al."
    },
    {
        "species_name": "Haplochthonius (Haplochthonius) clavatus",
        "date": "1958",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Haplochthonius (Haplochthonius) intermedius",
        "date": "1977",
        "discoverer": "Chakrabarti et al."
    },
    {
        "species_name": "Haplochthonius (Haplochthonius) simplex",
        "date": "1930",
        "discoverer": "Willmann"
    },
    {
        "species_name": "Similochthonius decoratus",
        "date": "1985",
        "discoverer": "Mahunka"
    },
    {
        "species_name": "Sphaerochthonius bengalensis",
        "date": "1990",
        "discoverer": "Sanyal and Sengupta"
    },
    {
        "species_name": "Sphaerochthonius transversus",
        "date": "1960",
        "discoverer": "Wallwork"
    },
    {
        "species_name": "Pterochthonius angelus",
        "date": "1910",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Eohypochthonius (Eohypochthonius) gracilis",
        "date": "1936",
        "discoverer": "Jacot"
    },
    {
        "species_name": "Eohypochthonius (Eohypochthonius) vilhenarum",
        "date": "1958",
        "discoverer": "Balogh"
    },
    {
        "species_name": "Hypochthonius rufulus",
        "date": "1835",
        "discoverer": "Koch"
    },
    {
        "species_name": "Malacoangelia assamica",
        "date": "1984",
        "discoverer": "Roy Talukder and Chakrabarti"
    },
    {
        "species_name": "Malacoangelia remigera remigera",
        "date": "1913",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Malacoangelia remigera indica",
        "date": "1972",
        "discoverer": "Chakrabarti et al."
    },
    {
        "species_name": "Malacoangelia similis",
        "date": "1982",
        "discoverer": "Sarkar and Subias"
    },
    {
        "species_name": "Hypochthoniella minutissimus",
        "date": "1904",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Annectacarus aokii",
        "date": "1994",
        "discoverer": "Jaikumar et al."
    },
    {
        "species_name": "Annectacarus hammerae",
        "date": "2007",
        "discoverer": "Shiji et al."
    },
    {
        "species_name": "Annectacarus longisetosus",
        "date": "1974",
        "discoverer": "Bhattacharya et al."
    },
    {
        "species_name": "Annectacarus mahabaeus",
        "date": "1979",
        "discoverer": "Corpuz–Raros"
    },
    {
        "species_name": "Annectacarus mucronatus",
        "date": "1950",
        "discoverer": "Grandjean"
    },
    {
        "species_name": "Annectacarus trivandricus",
        "date": "1978",
        "discoverer": "Haq"
    },
    {
        "species_name": "Annectacarus wallworki",
        "date": "1991",
        "discoverer": "Adolph and Haq"
    },
    {
        "species_name": "Cryptacarus dendrisetosus",
        "date": "1974",
        "discoverer": "Bhattacharya et al."
    },
    {
        "species_name": "Cryptacarus grandjeani",
        "date": "1991",
        "discoverer": "Adolph and Haq"
    },
    {
        "species_name": "Cryptacarus keralensis",
        "date": "2007",
        "discoverer": "Shiji et al."
    },
    {
        "species_name": "Cryptacarus schauenbergi",
        "date": "1977",
        "discoverer": "Mahunka"
    },
    {
        "species_name": "Cryptacarus tuberculatus",
        "date": "1961",
        "discoverer": "Csiszar"
    },
    {
        "species_name": "Haplacarus bhadurii",
        "date": "1984",
        "discoverer": "Sanyal"
    },
    {
        "species_name": "Haplacarus davisi",
        "date": "2005",
        "discoverer": "Xavier et al."
    },
    {
        "species_name": "Haplacarus foliatus foliatus",
        "date": "1962",
        "discoverer": "Wallwork"
    },
    {
        "species_name": "Haplacarus foliatus bengalensis",
        "date": "1974",
        "discoverer": "Bhattacharya et al."
    },
    {
        "species_name": "Haplacarus keralensis",
        "date": "1983",
        "discoverer": "Haq et al."
    },
    {
        "species_name": "Haplacarus maharashtraensis",
        "date": "1984",
        "discoverer": "Sanyal"
    },
    {
        "species_name": "Haplacarus porosus",
        "date": "1995",
        "discoverer": "Haq and Adolph"
    },
    {
        "species_name": "Haplacarus xavieri",
        "date": "2005",
        "discoverer": "Xavier et al."
    },
    {
        "species_name": "Haplacarus hirsutus",
        "date": "1964",
        "discoverer": "Wallwork"
    },
    {
        "species_name": "Haplacarus neotropicus",
        "date": "1985",
        "discoverer": "Mahunka"
    },
    {
        "species_name": "Javacarus (Javacarus) foliatus",
        "date": "1972",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Javacarus (Javacarus) foveolatus",
        "date": "1992",
        "discoverer": "Kardar"
    },
    {
        "species_name": "Javacarus (Javacarus) indicus",
        "date": "1992",
        "discoverer": "Kardar"
    },
    {
        "species_name": "Javacarus (Javacarus) kuehnelti",
        "date": "1961",
        "discoverer": "Balogh"
    },
    {
        "species_name": "Javacarus (Javacarus) longisetosus",
        "date": "1992",
        "discoverer": "Kardar"
    },
    {
        "species_name": "Javacarus (Javacarus) reticulatus",
        "date": "1982",
        "discoverer": "Senbusch"
    },
    {
        "species_name": "Lepidacarus ennarpi",
        "date": "1997",
        "discoverer": "Haq and Ramani"
    },
    {
        "species_name": "Lepidacarus ornatissimus ornatissimus",
        "date": "1961",
        "discoverer": "Csiszar"
    },
    {
        "species_name": "Lepidacarus ornatissimus rehmabia",
        "date": "1983",
        "discoverer": "Haq et al."
    },
    {
        "species_name": "Licneremaeus indicus",
        "date": "2020",
        "discoverer": "Arun & Ramani"
    },
    {
        "species_name": "Lohmannia (Lohmannia) indica",
        "date": "1972",
        "discoverer": "Kardar"
    },
    {
        "species_name": "Lohmannia (Lohmannia) javana javana",
        "date": "1961",
        "discoverer": "Balogh"
    },
    {
        "species_name": "Meristacarus degradatus",
        "date": "1993",
        "discoverer": "Haq and Jaikumar"
    },
    {
        "species_name": "Meristacarus wynadensis",
        "date": "1995",
        "discoverer": "Haq and Adolph"
    },
    {
        "species_name": "Mixacarus (Mixacarus) quadrifasciatus",
        "date": "1986",
        "discoverer": "Balakrishnan"
    },
    {
        "species_name": "Papillacarus (Vepracarus) acaciensis",
        "date": "2020",
        "discoverer": "Arun & Ramani"
    },
    {
        "species_name": "Papillacarus angulatus",
        "date": "1962",
        "discoverer": "Wallwork"
    },
    {
        "species_name": "Papillacarus cornutus",
        "date": "1984",
        "discoverer": "Sarkar and Subias"
    },
    {
        "species_name": "Papillacarus hirsutus",
        "date": "1961",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Papillacarus simplirostratus",
        "date": "1974",
        "discoverer": "Bhattacharya et al."
    },
    {
        "species_name": "Paulianacarus (Paulianacarus) simplisetosus",
        "date": "1985",
        "discoverer": "Mahunka"
    },
    {
        "species_name": "Paulianacarus (Millotacarus) foliatus",
        "date": "1982",
        "discoverer": "Mondal and Chakrabarti"
    },
    {
        "species_name": "Paulianacarus (M.) granulatus",
        "date": "1961",
        "discoverer": "Balogh"
    },
    {
        "species_name": "Paulianacarus (M.) indicus",
        "date": "1992",
        "discoverer": "Sanyal"
    },
    {
        "species_name": "Paulianacarus (M.) sarbias",
        "date": "2001",
        "discoverer": "Coetzee"
    },
    {
        "species_name": "Apoplophora aokii",
        "date": "1999",
        "discoverer": "Mondal et al."
    },
    {
        "species_name": "Apoplophora pantotrema",
        "date": "1913",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Mesoplophora (Mesoplophora) crassisetosa",
        "date": "1984",
        "discoverer": "Subias and Sarkar"
    },
    {
        "species_name": "Mesoplophora (Mesoplophora) gaveae",
        "date": "1962",
        "discoverer": "Schuster"
    },
    {
        "species_name": "Mesoplophora (Mesoplophora) invisitata",
        "date": "1983",
        "discoverer": "Niedbala"
    },
    {
        "species_name": "Mesoplophora (Mesoplophora) michaeliana",
        "date": "1904",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Epilohmannia cylindrica",
        "date": "1904",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Epilohmannia minuta areolata",
        "date": "1982",
        "discoverer": "Sarkar and Subias"
    },
    {
        "species_name": "Epilohmannia minuta indica",
        "date": "1979",
        "discoverer": "Bhattacharya and Banerjee"
    },
    {
        "species_name": "Epilohmannia minuta minuta",
        "date": "1962",
        "discoverer": "Wallwork"
    },
    {
        "species_name": "Epilohmannia minuta pacifica",
        "date": "1965",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Epilohmannia pallida areolata",
        "date": "1982",
        "discoverer": "Sarkar and Subias"
    },
    {
        "species_name": "Epilohmannia pallida indica",
        "date": "1979",
        "discoverer": "Bhattacharya and Banerjee"
    },
    {
        "species_name": "Epilohmannia pallida pallida",
        "date": "1962",
        "discoverer": "Wallwork"
    },
    {
        "species_name": "Epilohmannia pallida rugosa",
        "date": "1982",
        "discoverer": "Sarkar and Subias"
    },
    {
        "species_name": "Austrotritia gibba",
        "date": "1979",
        "discoverer": "Bayoumi and Mahunka"
    },
    {
        "species_name": "Austrotritia saraburiensis",
        "date": "1965",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Indotritia (Indotritia) lakshadweepensis",
        "date": "2014",
        "discoverer": "Sanyal and Basu"
    },
    {
        "species_name": "Indotritia (Indotritia) propinqua",
        "date": "1991",
        "discoverer": "Niedbala"
    },
    {
        "species_name": "Indotritia (Indotritia) undulata",
        "date": "1979",
        "discoverer": "Bayoumi and Mahunka"
    },
    {
        "species_name": "Mesotritia (Mesotritia) indica",
        "date": "1988",
        "discoverer": "Sanyal"
    },
    {
        "species_name": "Mesotritia (Mesotritia) maerkeli",
        "date": "1965",
        "discoverer": "Sheals"
    },
    {
        "species_name": "Mesotritia (Mesotritia) similis",
        "date": "2000",
        "discoverer": "Niedbala"
    },
    {
        "species_name": "Oribotritia gigas",
        "date": "1979",
        "discoverer": "Bayoumi and Mahunka"
    },
    {
        "species_name": "Oribotritia submolesta",
        "date": "2000",
        "discoverer": "Niedbala"
    },
    {
        "species_name": "Acrotritia ardua ardua",
        "date": "1841",
        "discoverer": "Koch"
    },
    {
        "species_name": "Acrotritia brasiliana",
        "date": "1983",
        "discoverer": "Mahunka"
    },
    {
        "species_name": "Acrotritia clavata",
        "date": "1964",
        "discoverer": "Markel"
    },
    {
        "species_name": "Acrotritia furcata",
        "date": "1979",
        "discoverer": "Bayoumi and Mahunka"
    },
    {
        "species_name": "Acrotritia gracile",
        "date": "2000",
        "discoverer": "Niedbala"
    },
    {
        "species_name": "Acrotritia hyeroglyphica",
        "date": "1916",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Acrotritia koreensis",
        "date": "1997",
        "discoverer": "Mahunka"
    },
    {
        "species_name": "Acrotritia otaheitensis",
        "date": "1972",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Acrotritia peruensis",
        "date": "1961",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Acrotritia sinensis",
        "date": "1923",
        "discoverer": "Jacot"
    },
    {
        "species_name": "Euphthiracarus (Euphthiracarus) pakistanensis",
        "date": "1977",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Euphthiracarus (Euphthiracarus) monodactylus",
        "date": "1919",
        "discoverer": "Willmann"
    },
    {
        "species_name": "Atropacarus striculus",
        "date": "1836",
        "discoverer": "Koch"
    },
    {
        "species_name": "Hoplophorella (Hoplophorella) calotropicus",
        "date": "2005",
        "discoverer": "Haq and Xavier"
    },
    {
        "species_name": "Hoplophorella (Hoplophorella) chaliyamensis",
        "date": "2005",
        "discoverer": "Haq and Xavier"
    },
    {
        "species_name": "Hoplophorella (Hoplophorella) crenulus",
        "date": "2005",
        "discoverer": "Haq and Xavier"
    },
    {
        "species_name": "Hoplophorella (Hoplophorella) cucullata",
        "date": "1909",
        "discoverer": "Ewing"
    },
    {
        "species_name": "Hoplophorella (Hoplophorella) hamata",
        "date": "1909",
        "discoverer": "Ewing"
    },
    {
        "species_name": "Hoplophorella (Hoplophorella) manipurensis",
        "date": "1982",
        "discoverer": "Misra et al."
    },
    {
        "species_name": "Hoplophorella (Hoplophorella) perisi",
        "date": "1984",
        "discoverer": "Subias and Sarkar"
    },
    {
        "species_name": "Hoplophorella (Hoplophorella) reticulatus",
        "date": "2005",
        "discoverer": "Haq & Xavier"
    },
    {
        "species_name": "Hoplophorella (Hoplophorella) singularis",
        "date": "1959",
        "discoverer": "Sellnick"
    },
    {
        "species_name": "Hoplophorella (Hoplophorella) stilifera",
        "date": "1961",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Hoplophorella (Hoplophorella) vitrina",
        "date": "1913",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Hoplophthiracarus bengalensis",
        "date": "1992",
        "discoverer": "Sanyal"
    },
    {
        "species_name": "Hoplophthiracarus concinuus",
        "date": "1982",
        "discoverer": "Niedbala"
    },
    {
        "species_name": "Hoplophthiracarus clavellatus",
        "date": "1998",
        "discoverer": "Niedbala and Corpuz-Raros"
    },
    {
        "species_name": "Hoplophthiracarus foveolatus",
        "date": "1980",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Hoplophthiracarus illinoisensis",
        "date": "1909",
        "discoverer": "Ewing"
    },
    {
        "species_name": "Hoplophthiracarus kugohi",
        "date": "1959",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Hoplophthiracarus nepalensis",
        "date": "1965",
        "discoverer": "Sheals"
    },
    {
        "species_name": "Hoplophthiracarus pakistanensis",
        "date": "1977",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Hoplophthiracarus punctatus",
        "date": "1988",
        "discoverer": "Mondal and Kundu"
    },
    {
        "species_name": "Hoplophthiracarus regalis",
        "date": "1978",
        "discoverer": "Mahunka"
    },
    {
        "species_name": "Hoplophthiracarus repetitus",
        "date": "1990",
        "discoverer": "Sanyal"
    },
    {
        "species_name": "Hoplophthiracarus similis",
        "date": "2000",
        "discoverer": "Niedbala"
    },
    {
        "species_name": "Notophthiracarus (Notophthiracarus) indicus",
        "date": "1979",
        "discoverer": "Bayoumi and Mahunka"
    },
    {
        "species_name": "Notophthiracarus (Notophthiracarus) inenarrabilis",
        "date": "1982",
        "discoverer": "Niedbala"
    },
    {
        "species_name": "Notophthiracarus (Notophthiracarus) latior",
        "date": "1982",
        "discoverer": "Niedbala"
    },
    {
        "species_name": "Notophthiracarus (Notophthiracarus) pullus",
        "date": "1989",
        "discoverer": "Niedbala"
    },
    {
        "species_name": "Notophthiracarus (Besuchetacarus) orientalis",
        "date": "1985",
        "discoverer": "Mahunka"
    },
    {
        "species_name": "Notophthiracarus (Calyptophthiracarus) costai",
        "date": "1965",
        "discoverer": "Macfarlane and Sheals"
    },
    {
        "species_name": "Notophthiracarus (C.) pavidus",
        "date": "1913",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Notophthiracarus (Protophthiracarus) ventosus",
        "date": "1961",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Notophthiracarus (P.) villosus",
        "date": "1982",
        "discoverer": "Niedbala"
    },
    {
        "species_name": "Phthiracarus (Phthiracarus) boresetosus",
        "date": "1930",
        "discoverer": "Jacot"
    },
    {
        "species_name": "Phthiracarus (Phthiracarus) claviger",
        "date": "1906",
        "discoverer": "Pearce"
    },
    {
        "species_name": "Phthiracarus (Phthiracarus) planus",
        "date": "1985",
        "discoverer": "Mahunka"
    },
    {
        "species_name": "Phthiracarus (Archiphthiracarus) paraglobosus",
        "date": "1982",
        "discoverer": "Niedbala"
    },
    {
        "species_name": "Phthiracarus (A.) robertsi",
        "date": "1965",
        "discoverer": "Sheals"
    },
    {
        "species_name": "Rhacaplacarus (Rhacaplacarus) ineptus",
        "date": "1984",
        "discoverer": "Niedbala"
    },
    {
        "species_name": "Rhacaplacarus (Rhacaplacarus) loebli",
        "date": "1985",
        "discoverer": "Mahunka"
    },
    {
        "species_name": "Rhacaplacarus (Rhacaplacarus) rafalskii",
        "date": "1997",
        "discoverer": "Niedbala"
    },
    {
        "species_name": "Afronothrus arboreus",
        "date": "1992",
        "discoverer": "Ramani and Haq"
    },
    {
        "species_name": "Afronothrus incisivus",
        "date": "1961",
        "discoverer": "Wallwork"
    },
    {
        "species_name": "Allonothrus (Allonothrus) dhananjayi",
        "date": "1991",
        "discoverer": "Sarkar"
    },
    {
        "species_name": "Allonothrus (Allonothrus) giganticus",
        "date": "1978",
        "discoverer": "Haq"
    },
    {
        "species_name": "Allonothrus (Allonothrus) indicus",
        "date": "1968",
        "discoverer": "Bhaduri and Raychaudhuri"
    },
    {
        "species_name": "Allonothrus (Allonothrus) monensis",
        "date": "1978",
        "discoverer": "Ghosh and Bhaduri"
    },
    {
        "species_name": "Allonothrus (Allonothrus) monodactylus",
        "date": "1960",
        "discoverer": "Wallwork"
    },
    {
        "species_name": "Allonothrus (Allonothrus) pararusseolus",
        "date": "1982",
        "discoverer": "Subias and Sarkar"
    },
    {
        "species_name": "Allonothrus (Allonothrus) russeolus russeolus",
        "date": "1960",
        "discoverer": "Wallwork"
    },
    {
        "species_name": "Archegozetes longisetosus",
        "date": "1965",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Archegozetes magnus magnus",
        "date": "1925",
        "discoverer": "Sellnick"
    },
    {
        "species_name": "Trhypochthonius tectorum tectorum",
        "date": "1896",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Malaconothrus (Malaconothrus) crassisetosus",
        "date": "1982",
        "discoverer": "Subias and Sarkar"
    },
    {
        "species_name": "Malaconothrus (Malaconothrus) dipankari",
        "date": "1996",
        "discoverer": "Saha and Sanyal"
    },
    {
        "species_name": "Malaconothrus (Malaconothrus) pseudolamellatus",
        "date": "1931",
        "discoverer": "Willmann"
    },
    {
        "species_name": "Malaconothrus macrofoveolatus",
        "date": "2013",
        "discoverer": "Ermilov, Kalúz et Wu"
    },
    {
        "species_name": "Malaconothrus (Cristonothrus) asiaticus",
        "date": "1967",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Malaconothrus (C.) assamensis",
        "date": "1979",
        "discoverer": "Chakrabarti and Roy Talukdar"
    },
    {
        "species_name": "Malaconothrus (C.) geminus",
        "date": "1972",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Malaconothrus (C.) pauciareolatus",
        "date": "1982",
        "discoverer": "Subias and Sarkar"
    },
    {
        "species_name": "Malaconothrus (C.) peruensis",
        "date": "1961",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Malaconothrus (C.) ramensis",
        "date": "1966",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Malaconothrus (C.) robustus",
        "date": "1958",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Malaconothrus (C.) rostropilosus",
        "date": "1996",
        "discoverer": "Saha and Sanyal"
    },
    {
        "species_name": "Trimalaconothrus (Trimalaconothrus) crispus",
        "date": "1962",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Trimalaconothrus (Trimalaconothrus) heterotrichus",
        "date": "1973",
        "discoverer": "Wallwork"
    },
    {
        "species_name": "Trimalaconothrus (Trimalaconothrus) platyrhinus",
        "date": "1962",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Trimalaconothrus (Trimalaconothrus) tripurensis",
        "date": "1983",
        "discoverer": "Sarkar"
    },
    {
        "species_name": "Trimalaconothrus (Tyrphonothrus) cajamarcensis",
        "date": "1961",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Trimalaconothrus crassisetosus",
        "date": "1931",
        "discoverer": "Willmann"
    },
    {
        "species_name": "Nothrus biciliatus",
        "date": "1841",
        "discoverer": "Koch"
    },
    {
        "species_name": "Nothrus brevirostris",
        "date": "1910",
        "discoverer": "Ewing"
    },
    {
        "species_name": "Nothrus discifer",
        "date": "1961",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Nothrus gracilis",
        "date": "1961",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Nothrus monticola",
        "date": "1961",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Nothrus oblongus",
        "date": "1961",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Nothrus phylliformis",
        "date": "2013",
        "discoverer": "Ermilov, Kalúz et Wu"
    },
    {
        "species_name": "Nothrus palustris palustris",
        "date": "1839",
        "discoverer": "Koch"
    },
    {
        "species_name": "Camisia segnis",
        "date": "1804",
        "discoverer": "Hermann"
    },
    {
        "species_name": "Camisia (Camisia) horrida",
        "date": "1804",
        "discoverer": "Hermann"
    },
    {
        "species_name": "Heminothrus (Capillonothrus) numatai",
        "date": "1965",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Heminothrus (C.) thori",
        "date": "1904",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Heminothrus (C.) bistriatus",
        "date": "1978",
        "discoverer": "Chakrabarti and Mandal"
    },
    {
        "species_name": "Heminothrus (Platynothrus) peltifer",
        "date": "1839",
        "discoverer": "Koch"
    },
    {
        "species_name": "Heminothrus (P.) praeoccupatus",
        "date": "1978",
        "discoverer": "Chakrabarti and Kundu"
    },
    {
        "species_name": "Heminothrus (P.) ovatus",
        "date": "1978",
        "discoverer": "Kundu and Mondal"
    },
    {
        "species_name": "Bicyrthermannia bicornuta",
        "date": "1978",
        "discoverer": "Haq"
    },
    {
        "species_name": "Bicyrthermannia duodentata",
        "date": "1979",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Cyrthermanniac quadricornuta",
        "date": "1977",
        "discoverer": "Chakracarti et al."
    },
    {
        "species_name": "Cyrthermanniac vicinicornuta",
        "date": "1965",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Masthermannia mamillaris",
        "date": "1904",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Nanhermannia gorodkovi",
        "date": "1975",
        "discoverer": "Sitnikova"
    },
    {
        "species_name": "Nanhermannia himalayensis",
        "date": "1977",
        "discoverer": "Chakrabarti et al."
    },
    {
        "species_name": "Nanhermannia thaiensis",
        "date": "1965",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Hermannia (Hermannia) convexa",
        "date": "1839",
        "discoverer": "Koch"
    },
    {
        "species_name": "Hermannia (Phyllhermannia) berlesei",
        "date": "1984",
        "discoverer": "Mondal"
    },
    {
        "species_name": "Hermannia (P.) foveolata",
        "date": "1990",
        "discoverer": "Sanyal"
    },
    {
        "species_name": "Hermannia (P.) punctata",
        "date": "1990",
        "discoverer": "Sanyal"
    },
    {
        "species_name": "Hermannia (P.) setiformis",
        "date": "1993",
        "discoverer": "De Wet"
    },
    {
        "species_name": "Hermanniella aliverdievae",
        "date": "2012",
        "discoverer": "Shtanchaeva et Subías"
    },
    {
        "species_name": "Hermanniella aristosa",
        "date": "1965",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Sacculobates indicus",
        "date": "2013",
        "discoverer": "Ermilov, Kalúz et Tolstikov"
    },
    {
        "species_name": "Plasmobates javensis",
        "date": "1979",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Plasmobates pagoda",
        "date": "1929",
        "discoverer": "Grandjean"
    },
    {
        "species_name": "Neoliodes ocellatus",
        "date": "1906",
        "discoverer": "Pearce"
    },
    {
        "species_name": "Neoliodes terrestris",
        "date": "1963",
        "discoverer": "Wallwork"
    },
    {
        "species_name": "Teleioliodes ghanensis",
        "date": "1963",
        "discoverer": "Wallwork"
    },
    {
        "species_name": "Pheroliodes rotundatus",
        "date": "1913",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Gymnodamaeus adpressus",
        "date": "1971",
        "discoverer": "Aoki and Fujikawa"
    },
    {
        "species_name": "Gymnodamaeus glaber",
        "date": "1992",
        "discoverer": "Woas"
    },
    {
        "species_name": "Jacotella ornata",
        "date": "1963",
        "discoverer": "Balogh and Ciszar"
    },
    {
        "species_name": "Belbodamaeus indicus",
        "date": "2013",
        "discoverer": "Ermilov, Kalúz et Wu"
    },
    {
        "species_name": "Damaeus (Damaeus) angustipes",
        "date": "1905",
        "discoverer": "Banks"
    },
    {
        "species_name": "Damaeus (Epidamaeus) parayunnanensis",
        "date": "2013",
        "discoverer": "Ermilov et Kalúz"
    },
    {
        "species_name": "Metabelba (Metabelba) obtusus",
        "date": "1966",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Tectodamaeus armatus",
        "date": "1984",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Tritegeus tridactylus",
        "date": "1963",
        "discoverer": "Woolley et Higgins"
    },
    {
        "species_name": "Niphocepheus neotrichus",
        "date": "2014",
        "discoverer": "Ermilov, Sergey G., Stanislav Kalúz & Jochen Martens"
    },
    {
        "species_name": "Austroceratoppia japonica",
        "date": "1984",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Ceratoppia bipilis",
        "date": "1804",
        "discoverer": "Hermann"
    },
    {
        "species_name": "Podopterotegaeus tectus",
        "date": "1969",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Ommatocepheus ocellatus",
        "date": "1882",
        "discoverer": "Michael"
    },
    {
        "species_name": "Microtegeus globifer",
        "date": "1985",
        "discoverer": "Mahunka"
    },
    {
        "species_name": "Microtegeus reticulatus",
        "date": "1965",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Microtegeus sabahnus",
        "date": "1987",
        "discoverer": "Mahunka"
    },
    {
        "species_name": "Berlesezetes baloghi",
        "date": "1998",
        "discoverer": "Bose et al."
    },
    {
        "species_name": "Berlesezetes brazilozetoides",
        "date": "1981",
        "discoverer": "Balogh and Mahunka"
    },
    {
        "species_name": "Berlesezetes longisetosus",
        "date": "1992",
        "discoverer": "Sarkar"
    },
    {
        "species_name": "Berlesezetes monoramai",
        "date": "1992",
        "discoverer": "Sarkar"
    },
    {
        "species_name": "Berlesezetes ornatissimus appalachicola",
        "date": "1938",
        "discoverer": "Jacot"
    },
    {
        "species_name": "Berlesezetes ornatissimus ornatissimus",
        "date": "1913",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Berlesezetes peruensis",
        "date": "1961",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Berlesezetes rudrasagarensis",
        "date": "1992",
        "discoverer": "Sarkar"
    },
    {
        "species_name": "Orthozetes dispar",
        "date": "1962",
        "discoverer": "Balogh"
    },
    {
        "species_name": "Schizozetes quadrilineatus",
        "date": "1962",
        "discoverer": "Balogh"
    },
    {
        "species_name": "Litholestes altitudinis",
        "date": "1951",
        "discoverer": "Grandjean"
    },
    {
        "species_name": "Zetorchestes saltator",
        "date": "1915",
        "discoverer": "Oudemans"
    },
    {
        "species_name": "Zetorchestes schusteri",
        "date": "1984",
        "discoverer": "Krisper"
    },
    {
        "species_name": "Cultroribula lata",
        "date": "1961",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Furcoppia (Furcoppia) cornuta",
        "date": "1972",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Maorizetes ferox",
        "date": "1966",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Ceratoppia bipilis",
        "date": "1804",
        "discoverer": "Hermann"
    },
    {
        "species_name": "Gustavia oceania",
        "date": "1987",
        "discoverer": "Perez-Inigo"
    },
    {
        "species_name": "Gustavia palmicinctus",
        "date": "1906",
        "discoverer": "Pearce"
    },
    {
        "species_name": "Gustavia microcephala",
        "date": "1855",
        "discoverer": "Nicolet"
    },
    {
        "species_name": "Liacarus (Liacarus) cidarus",
        "date": "1968",
        "discoverer": "Woolley"
    },
    {
        "species_name": "Liacarus (Liacarus) nigrescens",
        "date": "1906",
        "discoverer": "Pearce"
    },
    {
        "species_name": "Liacarus (Dorycranosus) acutidens",
        "date": "1965",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Carinabella tuberculata",
        "date": "1979",
        "discoverer": "Bayoumi and Mahunka"
    },
    {
        "species_name": "Eremulus avenifer",
        "date": "1913",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Eremulus flagellifer",
        "date": "1908",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Eremulus heterotrichus",
        "date": "1996",
        "discoverer": "Chakrabarti and Dasgupta"
    },
    {
        "species_name": "Eremulus indicus",
        "date": "2008",
        "discoverer": "Sanyal et al."
    },
    {
        "species_name": "Eremulus jyotsnai",
        "date": "1991",
        "discoverer": "Sarkar"
    },
    {
        "species_name": "Eremulus nigrisetosus",
        "date": "1958",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Eremulus punctatus",
        "date": "1996",
        "discoverer": "Chakrabarti and Dasgupta"
    },
    {
        "species_name": "Eremulus renukae",
        "date": "1992",
        "discoverer": "Sanyal"
    },
    {
        "species_name": "Eremulus sigmolamellatus",
        "date": "1996",
        "discoverer": "Chakrabarti and Dasgupta"
    },
    {
        "species_name": "Eremulus truncatus",
        "date": "1971",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Fosseremus laciniatus",
        "date": "1905",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Eremobelba himalayensis",
        "date": "1984",
        "discoverer": "Mondal and Kundu"
    },
    {
        "species_name": "Eremobelba indica",
        "date": "1978",
        "discoverer": "Ghosh and Bhaduri"
    },
    {
        "species_name": "Eremobelba miliae",
        "date": "1992",
        "discoverer": "Sanyal"
    },
    {
        "species_name": "Eremobelba nagaroorica",
        "date": "1978",
        "discoverer": "Haq"
    },
    {
        "species_name": "Eremobelba shillongensis",
        "date": "1988",
        "discoverer": "Sanyal"
    },
    {
        "species_name": "Eremobelba bellicosa",
        "date": "1967",
        "discoverer": "Balogh et Mahunka"
    },
    {
        "species_name": "Heterobelba rostrata",
        "date": "1984",
        "discoverer": "Mondal and Kundu"
    },
    {
        "species_name": "Heterobelba galerulata",
        "date": "1913",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Basilobelba barbata",
        "date": "1984",
        "discoverer": "Mondal and Kundu"
    },
    {
        "species_name": "Basilobelba indica",
        "date": "1974",
        "discoverer": "Bhaduri et al."
    },
    {
        "species_name": "Basilobelba papillata",
        "date": "2007",
        "discoverer": "Sanyal et al."
    },
    {
        "species_name": "Basilobelba retiaria symmetrica",
        "date": "1962",
        "discoverer": "Wallwork"
    },
    {
        "species_name": "Xiphobelba barbata",
        "date": "1984",
        "discoverer": "Roy Talukdar and Chakrabarti"
    },
    {
        "species_name": "Xiphobelba ismalia",
        "date": "1979",
        "discoverer": "Haq"
    },
    {
        "species_name": "Xiphobelba hamanni",
        "date": "1961",
        "discoverer": "Csiszár"
    },
    {
        "species_name": "Hymenobelba ypsilon",
        "date": "1962",
        "discoverer": "Balogh"
    },
    {
        "species_name": "Caenosamerus spatiosus",
        "date": "1977",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Eremella induta",
        "date": "1913",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Machadobelba baloghi",
        "date": "1999",
        "discoverer": "Mondal and Kundu"
    },
    {
        "species_name": "Machadobelba barbata",
        "date": "2005",
        "discoverer": "Sanyal et al."
    },
    {
        "species_name": "Machadobelba symmetrica",
        "date": "1958",
        "discoverer": "Balogh"
    },
    {
        "species_name": "Aeroppia (Paraeroppia) indiana",
        "date": "2009",
        "discoverer": "Sanyal et al."
    },
    {
        "species_name": "Arcoppia arcualis arcualis",
        "date": "1913",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Arcoppia arcualis novaeguineae",
        "date": "1986",
        "discoverer": "J. and P. Balogh"
    },
    {
        "species_name": "Arcoppia bidentata bidentata",
        "date": "1979",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Arcoppia cryptomeriae",
        "date": "1985",
        "discoverer": "Mondal and Kundu"
    },
    {
        "species_name": "Arcoppia fenestralis orientalis",
        "date": "1986",
        "discoverer": "J. and P. Balogh"
    },
    {
        "species_name": "Arcoppia indica",
        "date": "2000",
        "discoverer": "Sanyal et al."
    },
    {
        "species_name": "Arcoppia mcadami",
        "date": "1986",
        "discoverer": "J. and P. Balogh"
    },
    {
        "species_name": "Arcoppia meghalayensis",
        "date": "2000",
        "discoverer": "Sanyal et al."
    },
    {
        "species_name": "Arcoppia undulata",
        "date": "2000",
        "discoverer": "Sanyal et al."
    },
    {
        "species_name": "Arcoppia rotunda",
        "date": "1979",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Arcoppia sambhui",
        "date": "2000",
        "discoverer": "Sanyal et al."
    },
    {
        "species_name": "Arcoppia tripuraensis",
        "date": "2000",
        "discoverer": "Sanyal et al."
    },
    {
        "species_name": "Arcoppia hammerae",
        "date": "1984",
        "discoverer": "Rodríguez et Subías"
    },
    {
        "species_name": "Brachioppia cajamarcensis",
        "date": "1961",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Brachioppia cuscensis",
        "date": "1961",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Brachioppiella (Brachioppiella) periculosa",
        "date": "1962",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Brachioppiella (Brachioppiella) variosensilata",
        "date": "1986",
        "discoverer": "Joy and Ray"
    },
    {
        "species_name": "Congoppia ramisetosa",
        "date": "1985",
        "discoverer": "Sanyal and Bhaduri"
    },
    {
        "species_name": "Cycloppia asetosa",
        "date": "2013",
        "discoverer": "Ermilov et Kalúz"
    },
    {
        "species_name": "Cycloppia spindleformis",
        "date": "2013",
        "discoverer": "Ermilov et Kalúz"
    },
    {
        "species_name": "Graptoppia (Graptoppia) sundensis",
        "date": "1979",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Graptoppia (Graptoppia) jyotikanai",
        "date": "2006",
        "discoverer": "Sanyal et al."
    },
    {
        "species_name": "Karenella (Stakarenoppia) granulosa",
        "date": "1983",
        "discoverer": "Subias and Sarkar"
    },
    {
        "species_name": "Kokoppia pectinata",
        "date": "1967",
        "discoverer": "Kok"
    },
    {
        "species_name": "Lanceoppia (Lanceoppia) confusaria",
        "date": "1997",
        "discoverer": "Joy and Chakravorty"
    },
    {
        "species_name": "Lanceoppia (Lancelalmoppia) nodosa",
        "date": "1958",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Lanceoppia (Lasiobelba) arcidiaconoae",
        "date": "1973",
        "discoverer": "Bernini"
    },
    {
        "species_name": "Lanceoppia (Lanceoppia) kuehnelti",
        "date": "1961",
        "discoverer": "Csiszar"
    },
    {
        "species_name": "Lanceoppia (Lanceoppia) remota",
        "date": "1959",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Lanceoppia (Lanceoppia) suchetae",
        "date": "1992",
        "discoverer": "Sanyal"
    },
    {
        "species_name": "Lauroppia fallax",
        "date": "1908",
        "discoverer": "Paoli"
    },
    {
        "species_name": "Membranoppia (Membranoppia) tuxeni",
        "date": "1968",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Moritzoppia (Moritzoppia) hamata",
        "date": "1906",
        "discoverer": "Pearce"
    },
    {
        "species_name": "Multioppia (Furculoppia) himachalensis",
        "date": "1999",
        "discoverer": "Kardar and Mattu"
    },
    {
        "species_name": "Multioppia (Multioppia) gracilis",
        "date": "1972",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Multioppia (Multioppia) indica",
        "date": "1978",
        "discoverer": "Haq"
    },
    {
        "species_name": "Multioppia (Multioppia) radiata",
        "date": "1961",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Multioppia (Multioppia) simplitricha",
        "date": "1985",
        "discoverer": "Sanyal and Bhaduri"
    },
    {
        "species_name": "Multioppia (Multioppia) stellifera",
        "date": "1961",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Multioppia (Multioppia) wilsoni wilsoni",
        "date": "1964",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Mystroppia sellinicki",
        "date": "1959",
        "discoverer": "Balogh"
    },
    {
        "species_name": "Neoamerioppia (Neoamerioppia) asiatica",
        "date": "1977",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Neoamerioppia (Neoamerioppia) chavinensis",
        "date": "1961",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Neoppia minuta",
        "date": "1981",
        "discoverer": "Bhattacharya and Banerjee"
    },
    {
        "species_name": "Oppia cryptomeriae",
        "date": "1985",
        "discoverer": "Mondal and Kundu"
    },
    {
        "species_name": "Oppia himalayensis",
        "date": "1999",
        "discoverer": "Karder and Mattu"
    },
    {
        "species_name": "Oppia microseta",
        "date": "1989",
        "discoverer": "Kardar"
    },
    {
        "species_name": "Oppia orientalis",
        "date": "1985",
        "discoverer": "Sanyal and Bhaduri"
    },
    {
        "species_name": "Oppia samadi",
        "date": "1976",
        "discoverer": "Kardar"
    },
    {
        "species_name": "Oppiella (Oppiella) nova",
        "date": "1902",
        "discoverer": "Oudemans"
    },
    {
        "species_name": "Oxyoppia (Oxyoppiella) polynesia",
        "date": "1972",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Oxyoppia (Oxyoppia) spiculifera",
        "date": "1985",
        "discoverer": "Mahunka"
    },
    {
        "species_name": "Paroppia lebruni",
        "date": "1968",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Ramusella (Ramusella) chulumaniensis",
        "date": "1958",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Ramusella (Ramusella) clavipectinata",
        "date": "1885",
        "discoverer": "Michael"
    },
    {
        "species_name": "Ramusella (Ramusella) puertomonttensis",
        "date": "1962",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Ramusella (Insculptoppia) ananthakrishni",
        "date": "1985",
        "discoverer": "Sanyal and Bhaduri"
    },
    {
        "species_name": "Ramusella (I.) sensiclavata",
        "date": "1976",
        "discoverer": "Kardar"
    },
    {
        "species_name": "Ramusella (Rectoppia) fasciata fasciata",
        "date": "1908",
        "discoverer": "Paoli"
    },
    {
        "species_name": "Striatoppia asiaticus",
        "date": "2009",
        "discoverer": "Sanyal et al."
    },
    {
        "species_name": "Striatoppia lanceolata",
        "date": "1972",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Striatoppia machadoi",
        "date": "1958",
        "discoverer": "Balogh"
    },
    {
        "species_name": "Striatoppia milii",
        "date": "2014",
        "discoverer": "Sanyal and Basu"
    },
    {
        "species_name": "Striatoppia niliaca",
        "date": "1960",
        "discoverer": "Popp"
    },
    {
        "species_name": "Striatoppia opuntiseta",
        "date": "1968",
        "discoverer": "Balogh and Mahunka"
    },
    {
        "species_name": "Striatoppia similis similis",
        "date": "1983",
        "discoverer": "Subias and Sarkar"
    },
    {
        "species_name": "Striatoppia tripurensis",
        "date": "1983",
        "discoverer": "Subias and Sarkar"
    },
    {
        "species_name": "Taiwanoppia (Taiwanoppia) paraflagellifera",
        "date": "2013",
        "discoverer": "Ermilov et Kalúz"
    },
    {
        "species_name": "Granuloppia mirabilis",
        "date": "1987",
        "discoverer": "Mahunka"
    },
    {
        "species_name": "Hammerella (Hammerella) excisa",
        "date": "2013",
        "discoverer": "Ermilov et Kalúz"
    },
    {
        "species_name": "Papillonotus tricarinatus",
        "date": "1983",
        "discoverer": "Sarkar and Subias"
    },
    {
        "species_name": "Hexoppia heterotricha",
        "date": "1958",
        "discoverer": "Balogh"
    },
    {
        "species_name": "Fenestrobelba (Fenestrobelba) nondivisa",
        "date": "1966",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Novosuctobelba (Novosuctobelba) dentissima",
        "date": "1977",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Suctobelbella (Suctobelbella) amurica",
        "date": "1966",
        "discoverer": "Krivolutsky"
    },
    {
        "species_name": "Suctobelbella (Suctobelbella) carchardon",
        "date": "1966",
        "discoverer": "Moritz"
    },
    {
        "species_name": "Suctobelbella (Suctobelbella) subcornigera",
        "date": "1941",
        "discoverer": "Forsslund"
    },
    {
        "species_name": "Suctobelbella (Flagrosuctobelba) elegantula",
        "date": "1958",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Suctobelbella (F.) flabella",
        "date": "1984",
        "discoverer": "Mondal"
    },
    {
        "species_name": "Suctobelbella (F.) insulana",
        "date": "1972",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Suctobelbella (F.) ponticula",
        "date": "1971",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Suctobelbella (F.) semiplumosa indica",
        "date": "1978",
        "discoverer": "Haq."
    },
    {
        "species_name": "Suctobelbella (Ussuribata) variosetosa",
        "date": "1961",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Suctobelbila dentata",
        "date": "1961",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Rhynchoppia sedlaceki",
        "date": "1968",
        "discoverer": "Balogh"
    },
    {
        "species_name": "Oxyamerus himalayensis",
        "date": "1999",
        "discoverer": "Mondal and Kundu"
    },
    {
        "species_name": "Dolicheremaeus auritus",
        "date": "1965",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Dolicheremaeus bengalensis",
        "date": "1992",
        "discoverer": "Sanyal"
    },
    {
        "species_name": "Dolicheremaeus bruneiensis",
        "date": "1967",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Dolicheremaeus coronarius",
        "date": "1981",
        "discoverer": "Chakrabarti et al."
    },
    {
        "species_name": "Dolicheremaeus cuspidatus",
        "date": "1962",
        "discoverer": "Wallwork"
    },
    {
        "species_name": "Dolicheremaeus geminus",
        "date": "1986",
        "discoverer": "Mondal and Kundu"
    },
    {
        "species_name": "Dolicheremaeus himalayensis",
        "date": "1981",
        "discoverer": "Chakrabarti et al."
    },
    {
        "species_name": "Dolicheremaeus indicus",
        "date": "1978",
        "discoverer": "Haq"
    },
    {
        "species_name": "Dolicheremaeus keralensis",
        "date": "1990",
        "discoverer": "Sanyal"
    },
    {
        "species_name": "Dolicheremaeus nepalensis",
        "date": "1967",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Dolicheremaeus obsessus",
        "date": "1981",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Dolicheremaeus papuensis",
        "date": "1967",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Dolicheremaeus renukae",
        "date": "1990",
        "discoverer": "Sanyal"
    },
    {
        "species_name": "Dolicheremaeus russiae",
        "date": "1999",
        "discoverer": "Mondal et al."
    },
    {
        "species_name": "Dolicheremaeus sabahnus",
        "date": "1988",
        "discoverer": "Mahunka"
    },
    {
        "species_name": "Dolicheremaeus specious",
        "date": "1906",
        "discoverer": "Pearce"
    },
    {
        "species_name": "Dolicheremaeus junichiaokii",
        "date": "2010",
        "discoverer": "Subías"
    },
    {
        "species_name": "Dolicheremaeus distinctus",
        "date": "1982",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Pseudotocepheus (Constrictocepheus) orientalis",
        "date": "1999",
        "discoverer": "Mondal et Kundu"
    },
    {
        "species_name": "Fissicepheus (Fissicepheus) coronarius coronarius",
        "date": "1967",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Lophotocepheus simplex",
        "date": "1983",
        "discoverer": "J. and P. Balogh"
    },
    {
        "species_name": "Plenotocepheus (Plenotocepheus) verrucosus",
        "date": "1995",
        "discoverer": "Grobler"
    },
    {
        "species_name": "Pseudotocepheus (Pseudotocepheus) contractus",
        "date": "1997",
        "discoverer": "Grobler"
    },
    {
        "species_name": "Pseudotocepheus (Pseudotocepheus) hammerae",
        "date": "1978",
        "discoverer": "Chakrabarti and Kundu"
    },
    {
        "species_name": "Pseudotocepheus (Pseudotocepheus) gobletus",
        "date": "1978",
        "discoverer": "Chakrabarti and Mondal"
    },
    {
        "species_name": "Pseudotocepheus (Pseudotocepheus) orientalis",
        "date": "1983",
        "discoverer": "Mondal and Kundu"
    },
    {
        "species_name": "Spinotocepheus foveolatus",
        "date": "1981",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Acrotocepheus (Acrotocepheus) philippinensis",
        "date": "1965",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Acrotocepheus (Acrotocepheus) punctatus",
        "date": "2006",
        "discoverer": "Sanyal et al."
    },
    {
        "species_name": "Eurostocepheus mahunkai",
        "date": "1999",
        "discoverer": "Mondal and Kundu"
    },
    {
        "species_name": "Megalotocepheus aokii",
        "date": "1987",
        "discoverer": "Mondal and Kundu"
    },
    {
        "species_name": "Megalotocepheus bengalensis",
        "date": "1987",
        "discoverer": "Mondal and Kundu"
    },
    {
        "species_name": "Megalotocepheus darjeelingensis",
        "date": "1987",
        "discoverer": "Mondal and Kundu"
    },
    {
        "species_name": "Megalotocepheus robustus",
        "date": "2006",
        "discoverer": "Sanyal et al."
    },
    {
        "species_name": "Megalotocepheus undulates",
        "date": "1981",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Carabodes (Carabodes) palmifer",
        "date": "1905",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Carabodes (Phyllocarabodes) insolitus",
        "date": "1984",
        "discoverer": "Balogh, P."
    },
    {
        "species_name": "Diplobodes (Neocarabodes) sexpilosus",
        "date": "1969",
        "discoverer": "Balogh and Mahunka"
    },
    {
        "species_name": "Gibbicepheus (Gibbicepheus) sisiri",
        "date": "1990",
        "discoverer": "Sanyal"
    },
    {
        "species_name": "Odontocepheus (Indotocepheus) himalayensis",
        "date": "1999",
        "discoverer": "Mondal and Kundu"
    },
    {
        "species_name": "Leobodes mirabilis",
        "date": "1965",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Tectocepheus latimellaris",
        "date": "1974",
        "discoverer": "Kardar"
    },
    {
        "species_name": "Tectocepheus minor",
        "date": "1904",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Tectocepheus minutes",
        "date": "1999",
        "discoverer": "Kardar and Mattu"
    },
    {
        "species_name": "Tectocepheus velatus sarekensis",
        "date": "1910",
        "discoverer": "Tragardh"
    },
    {
        "species_name": "Tectocepheus translamellaris",
        "date": "1974",
        "discoverer": "Kardar"
    },
    {
        "species_name": "Tectocepheus velatus velatus",
        "date": "1880",
        "discoverer": "Michael"
    },
    {
        "species_name": "Tegeocranellus punctatus",
        "date": "2004",
        "discoverer": "Saha et al."
    },
    {
        "species_name": "Hydrozetes (Hydrozetes) confervae",
        "date": "1781",
        "discoverer": "Schrank"
    },
    {
        "species_name": "Cymbaeremaeus cymba",
        "date": "1855",
        "discoverer": "Nicolet"
    },
    {
        "species_name": "Scapheremaeus balazsi",
        "date": "1983",
        "discoverer": "Mahunka"
    },
    {
        "species_name": "Scapheremaeus bicornutus",
        "date": "1971",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Scapheremaeus fisheri",
        "date": "1966",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Scapheremaeus nuciferosa",
        "date": "1991",
        "discoverer": "Ramani and Haq"
    },
    {
        "species_name": "Exochocepheus erimitus",
        "date": "1968",
        "discoverer": "Wooley and Higgins"
    },
    {
        "species_name": "Hypovertex transversalis",
        "date": "1963",
        "discoverer": "Balogh and Csiszar"
    },
    {
        "species_name": "S. laminipes",
        "date": "1961",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Eupelops acromios",
        "date": "1804",
        "discoverer": "Hermann"
    },
    {
        "species_name": "Eupelops acromios minor",
        "date": "1973",
        "discoverer": "Chakrabarti et al."
    },
    {
        "species_name": "Eupelops foveolatus",
        "date": "1975",
        "discoverer": "Engelbrecht"
    },
    {
        "species_name": "Eupelops longisetosus",
        "date": "1981",
        "discoverer": "Chakrabarti and Mondal"
    },
    {
        "species_name": "Peloptulus foveolatus",
        "date": "1961",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Unduloribates hebes",
        "date": "1965",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Eremaeozetes himalayensis",
        "date": "1992",
        "discoverer": "Sanyal"
    },
    {
        "species_name": "Eremaeozetes lineatus",
        "date": "1985",
        "discoverer": "Mahunka"
    },
    {
        "species_name": "Allozetes africanus",
        "date": "1958",
        "discoverer": "Balogh"
    },
    {
        "species_name": "Allozetes translamellatus",
        "date": "1973",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Austrachipteria grandis",
        "date": "1967",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Austrachipteria orientalis",
        "date": "1999",
        "discoverer": "Mondal and Kundu"
    },
    {
        "species_name": "Hypozetes bulgaricus",
        "date": "1962",
        "discoverer": "Csiszar and Jeleva"
    },
    {
        "species_name": "Hypozetes imitator",
        "date": "1959",
        "discoverer": "Balogh"
    },
    {
        "species_name": "Hypozetes laysanensis",
        "date": "1964",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Lamellobates (Lamellobates) molecula molecula",
        "date": "1916",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Lamellobates (Lamellobates) reticulatus",
        "date": "1998",
        "discoverer": "Behan-Pelletier"
    },
    {
        "species_name": "Lamellobates (Paralamellobates) bengalensis",
        "date": "1968",
        "discoverer": "Bhaduri and Raychaudhuri"
    },
    {
        "species_name": "Lamellobates (P.) misella",
        "date": "1910",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Lamellobates (P.) striatus",
        "date": "1998",
        "discoverer": "Behan-Pelletier"
    },
    {
        "species_name": "Parachipteria ovalis",
        "date": "1855",
        "discoverer": "Koch"
    },
    {
        "species_name": "Plakoribates scutatus",
        "date": "1979",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Oribatella (Oribatella) alami",
        "date": "1975",
        "discoverer": "Kardar"
    },
    {
        "species_name": "Oribatella (Oribatella) kashmiriensis",
        "date": "1975",
        "discoverer": "Kardar"
    },
    {
        "species_name": "Oribatella (Oribatella) microfoveolata",
        "date": "1977",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Oribatella (Oribatella) superbula superbula",
        "date": "1904",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Oribatella (Oribatella) unispinata",
        "date": "1958",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Ceratozetes (Ceratozetes) gracilis",
        "date": "1884",
        "discoverer": "Michael"
    },
    {
        "species_name": "Murcia rausensis",
        "date": "1982",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Murcia striata",
        "date": "1952",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Sphaerozetes (Porozetes) polygonalis",
        "date": "1962",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Zetomimus (Zetomimus) cristatus",
        "date": "1962",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Pedunculozetes andinus",
        "date": "1962",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Ramsayellus fallax",
        "date": "1906",
        "discoverer": "Pearce"
    },
    {
        "species_name": "Minguezetes insignis",
        "date": "1910",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Minguezetes longiporosus",
        "date": "1963",
        "discoverer": "Balogh"
    },
    {
        "species_name": "Mycobates (Calyptozetes) tridactylus",
        "date": "1929",
        "discoverer": "Willmann"
    },
    {
        "species_name": "Demisalto (Demisalto) engelbrechti",
        "date": "1993",
        "discoverer": "Coetzee"
    },
    {
        "species_name": "Zetomotrichus (Keralotrichus) plumosus",
        "date": "1985",
        "discoverer": "Mahunka"
    },
    {
        "species_name": "Drymobatoides malabarica",
        "date": "1982",
        "discoverer": "Adolph and Haq"
    },
    {
        "species_name": "Rykella asiatica",
        "date": "2000",
        "discoverer": "Yamamoto et Aoki"
    },
    {
        "species_name": "Unguizetes clavatus",
        "date": "1967",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Unguizetes granulatus",
        "date": "2006",
        "discoverer": "Sanyal et al."
    },
    {
        "species_name": "Unguizetes keralensis",
        "date": "1985",
        "discoverer": "Balakrishnan"
    },
    {
        "species_name": "Unguizetes mauritius",
        "date": "1936",
        "discoverer": "Jacot"
    },
    {
        "species_name": "Uracrobates indicus",
        "date": "1990",
        "discoverer": "Ramani and Haq"
    },
    {
        "species_name": "Uracrobates magniporosus",
        "date": "1967",
        "discoverer": "Balogh and Mahunka"
    },
    {
        "species_name": "Oribatula (Oribatula) tibialis",
        "date": "1855",
        "discoverer": "Nicolet"
    },
    {
        "species_name": "Oribatula (Zygoribatula) beloniensis",
        "date": "2004",
        "discoverer": "Sanyal et al."
    },
    {
        "species_name": "Oribatula (Z.) gracilata",
        "date": "1993",
        "discoverer": "Grobler and Kok"
    },
    {
        "species_name": "Oribatula (Z.) keralaensis",
        "date": "1999",
        "discoverer": "Ramani and Haq"
    },
    {
        "species_name": "Oribatula (Z.) tortilis",
        "date": "1977",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Oribatula (Z.) tenuiseta",
        "date": "1977",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Oribatula (Z.) undulata",
        "date": "1916",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Paraphauloppia (Paraphauloppia) altimontana",
        "date": "1958",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Rekharibatula diverseta",
        "date": "1996",
        "discoverer": "Bose et al."
    },
    {
        "species_name": "Sellnickia caudata",
        "date": "1898",
        "discoverer": "Michael"
    },
    {
        "species_name": "Brassiella arboricola",
        "date": "1983",
        "discoverer": "Balogh et P. Balogh"
    },
    {
        "species_name": "Zetorchella abalai",
        "date": "1975",
        "discoverer": "Bhaduri et al."
    },
    {
        "species_name": "Zetorchella amarpurensis",
        "date": "2003",
        "discoverer": "Sanyal et al."
    },
    {
        "species_name": "Zetorchella asperulus",
        "date": "1906",
        "discoverer": "Pearce"
    },
    {
        "species_name": "Zetorchella cancellatus",
        "date": "1906",
        "discoverer": "Pearce"
    },
    {
        "species_name": "Zetorchella latior",
        "date": "1913",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Zetorchella longisetosus",
        "date": "1980",
        "discoverer": "Dhali and Bhaduri"
    },
    {
        "species_name": "Zetorchella minor",
        "date": "1958",
        "discoverer": "Balogh"
    },
    {
        "species_name": "Zetorchella orientalis",
        "date": "2003",
        "discoverer": "Sanyal et al."
    },
    {
        "species_name": "Zetorchella sejugatus",
        "date": "1997",
        "discoverer": "Ramani and Haq"
    },
    {
        "species_name": "Zetorchella sisiri",
        "date": "2003",
        "discoverer": "Sanyal et al."
    },
    {
        "species_name": "Zetorchella sottoetgarciai",
        "date": "1979",
        "discoverer": "Corpuz-Raros"
    },
    {
        "species_name": "Hemileius (Tuberemaeus) singularis",
        "date": "1930",
        "discoverer": "Sellnick"
    },
    {
        "species_name": "Dometorina (Dometorina) malabarica",
        "date": "1998",
        "discoverer": "Ramani et Haq"
    },
    {
        "species_name": "Dometorina (Siculobata) sicula",
        "date": "1892",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Haloribatula tenareae",
        "date": "1957",
        "discoverer": "Schuster"
    },
    {
        "species_name": "Liebstadia similis",
        "date": "1888",
        "discoverer": "Michael"
    },
    {
        "species_name": "Reductobates latiohumeralis",
        "date": "1972",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Euscheloribates (Euscheloribates) samsinaki",
        "date": "1958",
        "discoverer": "Kunst"
    },
    {
        "species_name": "Fijibates rostropilosus",
        "date": "2006",
        "discoverer": "Sanyal et al."
    },
    {
        "species_name": "Fijibates dlouhyi",
        "date": "1984",
        "discoverer": "Mahunka"
    },
    {
        "species_name": "Hammerabates trisetosus",
        "date": "1970",
        "discoverer": "Balogh"
    },
    {
        "species_name": "Rhabdoribates siamensis",
        "date": "1967",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Scheloribates (Perscheloribates) albialatus",
        "date": "1961",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Scheloribates (P.) benguetensis",
        "date": "1980",
        "discoverer": "Corpuz-Raros"
    },
    {
        "species_name": "Scheloribates (P.) lanceolatus",
        "date": "1984",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Scheloribates (P.) luminosus",
        "date": "1961",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Scheloribates (P.) minutus",
        "date": "1965",
        "discoverer": "Pletzen"
    },
    {
        "species_name": "Scheloribates (Scheloribates) caprai",
        "date": "1973",
        "discoverer": "Bernini"
    },
    {
        "species_name": "Scheloribates (Scheloribates) bhadurii",
        "date": "1992",
        "discoverer": "Sanyal"
    },
    {
        "species_name": "Scheloribates (Scheloribates) bicuspidatus",
        "date": "1977",
        "discoverer": "Kardar"
    },
    {
        "species_name": "Scheloribates (Scheloribates) chauhani",
        "date": "1945",
        "discoverer": "Baker"
    },
    {
        "species_name": "Scheloribates (Scheloribates) curvialatus",
        "date": "1961",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Scheloribates (Scheloribates) decarinatus",
        "date": "1984",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Scheloribates (Scheloribates) diversidactylus",
        "date": "1961",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Scheloribates (Scheloribates) elegans",
        "date": "1958",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Scheloribates (Scheloribates) fijiensis",
        "date": "1971",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Scheloribates (Scheloribates) fimbriatoides",
        "date": "1977",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Scheloribates (Scheloribates) fimbriatus",
        "date": "1930",
        "discoverer": "Thor"
    },
    {
        "species_name": "Scheloribates (Scheloribates) fimbriatus fimbriatus",
        "date": "1930",
        "discoverer": "Thor"
    },
    {
        "species_name": "Scheloribates (Scheloribates) fucifer",
        "date": "1908",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Scheloribates (Scheloribates) huancayensis",
        "date": "",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Scheloribates (Scheloribates) jucundior",
        "date": "1923",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Scheloribates (Scheloribates) laevigatus",
        "date": "1835",
        "discoverer": "Koch"
    },
    {
        "species_name": "Scheloribates (Scheloribates) latoincisus",
        "date": "1973",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Scheloribates (Scheloribates) obsessus",
        "date": "2004",
        "discoverer": "Subías"
    },
    {
        "species_name": "Scheloribates (Scheloribates) pallidulus",
        "date": "1841",
        "discoverer": "Koch"
    },
    {
        "species_name": "Scheloribates (Scheloribates) parvus parvus",
        "date": "1963",
        "discoverer": "Pletzen"
    },
    {
        "species_name": "Scheloribates (Scheloribates) praeincisus",
        "date": "1910",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Scheloribates (Scheloribates) praeincisus praeincisus",
        "date": "1910",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Scheloribates (Scheloribates) praeincisus interruptus",
        "date": "1916",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Scheloribates (Scheloribates) praeincisus tenuiseta",
        "date": "1971",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Scheloribates (Scheloribates) praeincisus rectus",
        "date": "1958",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Scheloribates (Scheloribates) praeincisus sandvicensis",
        "date": "1934",
        "discoverer": "Jacot"
    },
    {
        "species_name": "Scheloribates (Scheloribates) praelineatus",
        "date": "1977",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Scheloribates (Scheloribates) rakhali",
        "date": "1992",
        "discoverer": "Sanyal"
    },
    {
        "species_name": "Scheloribates (Scheloribates) sacsahuamanensis",
        "date": "1961",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Scheloribates (Scheloribates) samirani",
        "date": "2006",
        "discoverer": "Sanyal, Saha et Chakraborty"
    },
    {
        "species_name": "Scheloribates (Scheloribates) saswatii",
        "date": "1981",
        "discoverer": "Dhali et Bhaduri"
    },
    {
        "species_name": "Scheloribates (Scheloribates) sikkimensis",
        "date": "1981",
        "discoverer": "Dhali et Bhaduri"
    },
    {
        "species_name": "Scheloribates (Scheloribates) striatus",
        "date": "1958",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Scheloribates (Scheloribates) thermophilus thermophilus",
        "date": "1961",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Scheloribates (Scheloribates) zealandicus",
        "date": "1967",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Scheloribates (Scheloribates) madrasensis",
        "date": "1951",
        "discoverer": "Anantharaman"
    },
    {
        "species_name": "Scheloribates (Scheloribates) pallidulus latipes",
        "date": "1844",
        "discoverer": "Koch"
    },
    {
        "species_name": "Scheloribates (Grandjeanobates) giganteus",
        "date": "1961",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Scheloribates (Bischeloribates) mahunkai",
        "date": "2010",
        "discoverer": "Subías"
    },
    {
        "species_name": "Topobates multiplisetus",
        "date": "1977",
        "discoverer": "Mahunka"
    },
    {
        "species_name": "Euscheloribates (Birobates) reductus",
        "date": "1970",
        "discoverer": "Balogh"
    },
    {
        "species_name": "Protoribates (Protoribates) capucinus",
        "date": "1908",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Protoribates (Protoribates) natalensis",
        "date": "1963",
        "discoverer": "Pletzen"
    },
    {
        "species_name": "Protoribates (Protoribates) paracapucinus",
        "date": "1988",
        "discoverer": "Mahunka"
    },
    {
        "species_name": "Protoribates (Protoribates) rufafulvus",
        "date": "1977",
        "discoverer": "Kardar"
    },
    {
        "species_name": "Protoribates (Protoribates) triangularis",
        "date": "1971",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Protoribates (Triaunguis) maximus",
        "date": "1988",
        "discoverer": "Mahunka"
    },
    {
        "species_name": "Protoribates (T.) magnus",
        "date": "1982",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Protoribates (T.) punctatus",
        "date": "1991",
        "discoverer": "Grobler"
    },
    {
        "species_name": "Protoribates (T.) seminudus",
        "date": "1971",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Protoribates (Lignobates) mollicoma",
        "date": "1973",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Setoxylobates (Plenoxylobates) curtiseta",
        "date": "1979",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Setoxylobates (Setoxylobates) foveolatus",
        "date": "1967",
        "discoverer": "Balogh et Mahunka"
    },
    {
        "species_name": "Vilhenabates (Phalacrozetes) sinatus",
        "date": "1965",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Protoripoda (Protoripoda) insularis",
        "date": "1970",
        "discoverer": "Balogh"
    },
    {
        "species_name": "Truncopes optatus",
        "date": "1956",
        "discoverer": "Grandjean"
    },
    {
        "species_name": "Truncopes moderatus variabilis",
        "date": "2007",
        "discoverer": "Aoki et Yamamoto"
    },
    {
        "species_name": "Lauritzenia (Lauritzenia) longipluma",
        "date": "1958",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Lauritzenia (Lauritzenia) minimicoma",
        "date": "1964",
        "discoverer": "Beck"
    },
    {
        "species_name": "Lauritzenia (Incabates) nuda",
        "date": "1961",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Magyaria cancellata",
        "date": "1964",
        "discoverer": "Beck"
    },
    {
        "species_name": "Paraxylobates imitans",
        "date": "1969",
        "discoverer": "Balogh and Mahunka"
    },
    {
        "species_name": "Peloribates (Peloribates) asejugalis",
        "date": "1999",
        "discoverer": "Pandit and Bhattacharya"
    },
    {
        "species_name": "Peloribates (Peloribates) intermedius",
        "date": "1984",
        "discoverer": "Mondal"
    },
    {
        "species_name": "Peloribates (Peloribates) kaszabi",
        "date": "1988",
        "discoverer": "Mahunka"
    },
    {
        "species_name": "Peloribates (Peloribates) levipunctatus",
        "date": "1984",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Peloribates (Peloribates) longisetosus",
        "date": "1930",
        "discoverer": "Willmann"
    },
    {
        "species_name": "Peloribates (Peloribates) pakistanensis",
        "date": "1977",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Peloribates (Peloribates) paraguayensis",
        "date": "1981",
        "discoverer": "Balogh et Mahunka"
    },
    {
        "species_name": "Peloribates (Peloribates) ryukyuensis",
        "date": "1974",
        "discoverer": "Aoki et Nakatamari"
    },
    {
        "species_name": "Peloribates (Peloribates) tripuraensis",
        "date": "1996",
        "discoverer": "Sanyal et Saha"
    },
    {
        "species_name": "Pilobatella (Pilobatella) berlesei",
        "date": "1980",
        "discoverer": "Bhattacharya et Banerjee"
    },
    {
        "species_name": "Pilobatella (Pilobatella) punctulata",
        "date": "1967",
        "discoverer": "Balogh et Mahunka"
    },
    {
        "species_name": "Pilobates (Pilobates) pilosellus",
        "date": "1958",
        "discoverer": "Balogh"
    },
    {
        "species_name": "Rostrozetes komodensis",
        "date": "1977",
        "discoverer": "Mahunka"
    },
    {
        "species_name": "Rostrozetes ovulum ovulum",
        "date": "1908",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Rostrozetes punctatus",
        "date": "1966",
        "discoverer": "Karppinen"
    },
    {
        "species_name": "Neoribates (Neoribates) aurantiacus",
        "date": "1914",
        "discoverer": "Oudemans"
    },
    {
        "species_name": "Neoribates (Neoribates) erectus",
        "date": "1969",
        "discoverer": "Balogh and Mahunka"
    },
    {
        "species_name": "Neoribates (Neoribates) ornamentus",
        "date": "2013",
        "discoverer": "Ermilov et Kalúz"
    },
    {
        "species_name": "Neoribates (Neoribates) parabarbatus",
        "date": "2013",
        "discoverer": "Ermilov et Kalúz"
    },
    {
        "species_name": "Acrogalumna longipluma longipluma",
        "date": "1904",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Acrogalumna machadoi",
        "date": "1960",
        "discoverer": "Balogh"
    },
    {
        "species_name": "Allogalumna (Acrogalumna) bipartita",
        "date": "1993",
        "discoverer": "Aoki et Hu"
    },
    {
        "species_name": "Cryptogalumna cryptodonta",
        "date": "1957",
        "discoverer": "Grandjean"
    },
    {
        "species_name": "Cryptogalumna grandjeani",
        "date": "1985",
        "discoverer": "Balakrishnan and Haq"
    },
    {
        "species_name": "Flagellozetes porosus indicus",
        "date": "1985",
        "discoverer": "Balakrishnan and Haq"
    },
    {
        "species_name": "Galumna (Galumna) chujoi",
        "date": "1966",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Galumna (Galumna) comparabilis",
        "date": "1972",
        "discoverer": "Engelbrecht"
    },
    {
        "species_name": "Galumna (Galumna) crenata",
        "date": "1975",
        "discoverer": "Deb and Raychaudhuri"
    },
    {
        "species_name": "Galumna (Galumna) crenata indica",
        "date": "2013",
        "discoverer": "Sarkar et al."
    },
    {
        "species_name": "Galumna (Galumna) crenata uttarkashi",
        "date": "2007",
        "discoverer": "Sarkar et al."
    },
    {
        "species_name": "Galumna (Galumna) cuneata",
        "date": "1961",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Galumna (Galumna) discifera",
        "date": "1960",
        "discoverer": "Balogh"
    },
    {
        "species_name": "Galumna (Galumna) flabellifera flabellifera",
        "date": "1958",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Galumna (Galumna) flabellifera orientalis",
        "date": "1965",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Galumna (Galumna) indica",
        "date": "1989",
        "discoverer": "Kardar"
    },
    {
        "species_name": "Galumna (Galumna) levisensilla",
        "date": "2010",
        "discoverer": "Ermilov et Anichkin"
    },
    {
        "species_name": "Galumna (Galumna) longipluma",
        "date": "1980",
        "discoverer": "Haq and Adolph"
    },
    {
        "species_name": "Galumna (Galumna) longiporosa",
        "date": "1972",
        "discoverer": "Fujikawa"
    },
    {
        "species_name": "Galumna (Galumna) major",
        "date": "1906",
        "discoverer": "Pearce"
    },
    {
        "species_name": "Galumna (Galumna) nilgiria",
        "date": "1910",
        "discoverer": "Ewing"
    },
    {
        "species_name": "Galumna (Galumna) parascaber",
        "date": "1975",
        "discoverer": "Deb and Raychaudhuri"
    },
    {
        "species_name": "Galumna (Galumna) parviporosa",
        "date": "1983",
        "discoverer": "Balogh and Balogh"
    },
    {
        "species_name": "Galumna (Galumna) striata",
        "date": "1989",
        "discoverer": "Kardar"
    },
    {
        "species_name": "Galumna (Galumna) tessellata",
        "date": "1910",
        "discoverer": "Ewing"
    },
    {
        "species_name": "Galumna (Galumna) triquetra",
        "date": "1965",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Galumna (Indogalumna) microsulcata",
        "date": "1985",
        "discoverer": "Balakrishnan"
    },
    {
        "species_name": "Galumna (I.) monticola",
        "date": "1985",
        "discoverer": "Balakrishnan"
    },
    {
        "species_name": "Galumna (I.) undulata",
        "date": "1985",
        "discoverer": "Balakrishnan"
    },
    {
        "species_name": "Neogalumna curviporosa",
        "date": "1986",
        "discoverer": "Balakrishnan"
    },
    {
        "species_name": "Notogalumna foveolata",
        "date": "1985",
        "discoverer": "Balakrishnan"
    },
    {
        "species_name": "Notogalumna nortoni",
        "date": "1990",
        "discoverer": "Ramani and Haq"
    },
    {
        "species_name": "Orthogalumna saeva",
        "date": "1960",
        "discoverer": "Balogh"
    },
    {
        "species_name": "Pergalumna aegra",
        "date": "1986",
        "discoverer": "Perez-Inigo and Baggio"
    },
    {
        "species_name": "Pergalumna andhraensis",
        "date": "1981",
        "discoverer": "Raju, Appalanaidu and Rao"
    },
    {
        "species_name": "Pergalumna andicola",
        "date": "1961",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Pergalumna granulata",
        "date": "1967",
        "discoverer": "Balogh and Mahunka"
    },
    {
        "species_name": "Pergalumna hastata",
        "date": "1987",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Pergalumna incomperta",
        "date": "1972",
        "discoverer": "Engelbrecht"
    },
    {
        "species_name": "Pergalumna intermedia",
        "date": "1963",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Pergalumna longiporosa",
        "date": "1987",
        "discoverer": "Fujita and Fujikawa"
    },
    {
        "species_name": "Pergalumna longisetosa",
        "date": "1960",
        "discoverer": "Balogh"
    },
    {
        "species_name": "Pergalumna magnipora capensis",
        "date": "1972",
        "discoverer": "Engelbrecht"
    },
    {
        "species_name": "Pergalumna margaritata",
        "date": "1989",
        "discoverer": "Mahunka"
    },
    {
        "species_name": "Pergalumna petrichosa",
        "date": "1995",
        "discoverer": "Mahunka"
    },
    {
        "species_name": "Pergalumna remota",
        "date": "1968",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Pergalumna sabitai",
        "date": "2012",
        "discoverer": "Sarkar et al."
    },
    {
        "species_name": "Pergalumna tahitensis",
        "date": "2002",
        "discoverer": "Balogh and Balogh"
    },
    {
        "species_name": "Pergalumna taprobanica",
        "date": "1988",
        "discoverer": "Balogh, P."
    },
    {
        "species_name": "Pergalumna (Pergalumna) altera",
        "date": "1915",
        "discoverer": "Oudemans"
    },
    {
        "species_name": "Pergalumna (Pergalumna) asetosa",
        "date": "2013",
        "discoverer": "Ermilov, Shtanchaeva, Kalúz et Subías"
    },
    {
        "species_name": "Pergalumna (Pergalumna) bhaskari",
        "date": "2012",
        "discoverer": "Sh. Sarkar, Sanyal et Chakrabarti"
    },
    {
        "species_name": "Pergalumna (Pergalumna) corolevuensis",
        "date": "1971",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Pergalumna (Pergalumna) foveolata",
        "date": "1973",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Pergalumna (Pergalumna) intermedia retroversa",
        "date": "1993",
        "discoverer": "Aoki and Hu"
    },
    {
        "species_name": "Pergalumna (Pergalumna) paratsurusakii",
        "date": "2013",
        "discoverer": "Ermilov, Shtanchaeva, Kalúz et Subías"
    },
    {
        "species_name": "Pilogalumna variabilis",
        "date": "1972",
        "discoverer": "Engelbrecht"
    },
    {
        "species_name": "Trichogalumna chitralensis",
        "date": "1977",
        "discoverer": "Hammer"
    },
    {
        "species_name": "Trichogalumna nipponica",
        "date": "1966",
        "discoverer": "Aoki"
    },
    {
        "species_name": "Trichogalumna seminuda",
        "date": "1960",
        "discoverer": "Balogh"
    },
    {
        "species_name": "Vaghia blascoi",
        "date": "1981",
        "discoverer": "Trave"
    },
    {
        "species_name": "Galumnella (Galumnella) indica",
        "date": "1985",
        "discoverer": "Balakrishnan"
    },
    {
        "species_name": "Galumnella (Galumnella) nipponica",
        "date": "1970",
        "discoverer": "Suzuki and Aoki"
    },
    {
        "species_name": "Galumnella (Galumnella) parageographica",
        "date": "2013",
        "discoverer": "Ermilov et Kalúz"
    },
    {
        "species_name": "Galumnopsis (Porogalumnella) microsetosa",
        "date": "2013",
        "discoverer": "Ermilov et Kalúz"
    },
    {
        "species_name": "Galumnopsis (P.) setosa",
        "date": "1982",
        "discoverer": "Balakrishnan and Haq"
    },
    {
        "species_name": "Amblyomma clypeolatum",
        "date": "1899",
        "discoverer": "Neumann"
    },
    {
        "species_name": "Amblyomma hebraeum",
        "date": "1844",
        "discoverer": "Koch"
    },
    {
        "species_name": "Amblyomma helvolum",
        "date": "1844",
        "discoverer": "Koch"
    },
    {
        "species_name": "Amblyomma integrum",
        "date": "1879",
        "discoverer": "Karsch"
    },
    {
        "species_name": "Amblyomma javanense",
        "date": "1897",
        "discoverer": "Supino"
    },
    {
        "species_name": "Amblyomma nitidum",
        "date": "1910",
        "discoverer": "Hirst and Hirst"
    },
    {
        "species_name": "Amblyomma supinoi",
        "date": "1905",
        "discoverer": "Neumann"
    },
    {
        "species_name": "Amblyomma testudinarium",
        "date": "1844",
        "discoverer": "Koch"
    },
    {
        "species_name": "Aponomma gervaisi",
        "date": "1847",
        "discoverer": "Lucas"
    },
    {
        "species_name": "Aponomma laeve",
        "date": "1899",
        "discoverer": "Neumann"
    },
    {
        "species_name": "Aponomma lucasi",
        "date": "1910",
        "discoverer": "Warburton"
    },
    {
        "species_name": "Aponomma pattoni",
        "date": "1910",
        "discoverer": "Neumann"
    },
    {
        "species_name": "Boophilus annulatus",
        "date": "1821",
        "discoverer": "Say"
    },
    {
        "species_name": "Boophilus decoloratus",
        "date": "1844",
        "discoverer": "Koch"
    },
    {
        "species_name": "Boophilus microplus",
        "date": "1887",
        "discoverer": "Canestrini"
    },
    {
        "species_name": "Dermacentor atrosignatus",
        "date": "1906",
        "discoverer": "Neumann"
    },
    {
        "species_name": "Dermacentor auratus",
        "date": "1897",
        "discoverer": "Supino"
    },
    {
        "species_name": "Dermacentor raskemensis",
        "date": "1946",
        "discoverer": "Pomerantzev"
    },
    {
        "species_name": "Haemaphysalis choprai",
        "date": "1928",
        "discoverer": "Sharif"
    },
    {
        "species_name": "Haemaphysalis doenitzi",
        "date": "1909",
        "discoverer": "Warburton and Nuttall"
    },
    {
        "species_name": "Haemaphysalis fusca",
        "date": "1907",
        "discoverer": "Christophers"
    },
    {
        "species_name": "Haemaphysalis howletti",
        "date": "1913",
        "discoverer": "Warburton"
    },
    {
        "species_name": "Haemaphysalis intermedia",
        "date": "1909",
        "discoverer": "Warburton and Nuttall"
    },
    {
        "species_name": "Haemaphysalis kutchensis",
        "date": "1963",
        "discoverer": "Hoogstraal & Trapido"
    },
    {
        "species_name": "Haemaphysalis megalaimae",
        "date": "1963",
        "discoverer": "Rajagopalan"
    },
    {
        "species_name": "Haemaphysalis minuta",
        "date": "1950",
        "discoverer": "Kohls"
    },
    {
        "species_name": "Haemaphysalis montgomeryi",
        "date": "1912",
        "discoverer": "Nuttall"
    },
    {
        "species_name": "Haemaphysalis ornithophila",
        "date": "1959",
        "discoverer": "Hoogstraal and Kohls"
    },
    {
        "species_name": "Haemaphysalis paraturturis",
        "date": "1963",
        "discoverer": "Hoogstraal & Trapido and Rebello"
    },
    {
        "species_name": "Haemaphysalis sambar",
        "date": "1971",
        "discoverer": "Hoogstraal"
    },
    {
        "species_name": "Haemaphysalis silvafelis",
        "date": "1963",
        "discoverer": "Hoogstraal and Trapido"
    },
    {
        "species_name": "Haemaphysalis turturis",
        "date": "1915",
        "discoverer": "Nuttall and Warburton"
    },
    {
        "species_name": "Haemaphysalis wellingtoni",
        "date": "1907",
        "discoverer": "Nuttall and Warburton"
    },
    {
        "species_name": "Haemaphysalis (Aboimisalls) cornupunctata",
        "date": "1962",
        "discoverer": "Hoogstraal and Varma"
    },
    {
        "species_name": "Haemaphysalis (Aborphysalis) aborensis",
        "date": "1913",
        "discoverer": "Warburton"
    },
    {
        "species_name": "Haemaphysalis (A.) kyasanurensis",
        "date": "1964",
        "discoverer": "Trapido, Hoogstraal and Rajagopalan"
    },
    {
        "species_name": "Haemaphysalis (Alloceraea) aponommoides",
        "date": "1913",
        "discoverer": "Warburton"
    },
    {
        "species_name": "Haemaphysalis (Allophysalis) garhwalensis",
        "date": "1968",
        "discoverer": "Dhanda and Bhat"
    },
    {
        "species_name": "Haemaphysalis (A.) warburtoni",
        "date": "1912",
        "discoverer": "Nuttall"
    },
    {
        "species_name": "Haemaphysalis (Haemaphysalis) birmaniae",
        "date": "1897",
        "discoverer": "Supino"
    },
    {
        "species_name": "Haemaphysalis (Haemaphysalis) campanulata",
        "date": "1908",
        "discoverer": "Warburton"
    },
    {
        "species_name": "Haemaphysalis (Haemaphysalis) darjeeling",
        "date": "1970",
        "discoverer": "Hoogstraal & Dhanda"
    },
    {
        "species_name": "Haemaphysalis (Haemaphysalis) himalaya",
        "date": "1966",
        "discoverer": "Hoogstraal"
    },
    {
        "species_name": "Haemaphysalis (Haemaphysalis) indoflava",
        "date": "1968",
        "discoverer": "Dhanda and Bhat"
    },
    {
        "species_name": "Haemaphysalis (Haemaphysalis) kashmirensis",
        "date": "1962",
        "discoverer": "Hoogstraal and Varma"
    },
    {
        "species_name": "Haemaphysalis (Haemaphysalis) nepalensis",
        "date": "1962",
        "discoverer": "Hoogstraal"
    },
    {
        "species_name": "Haemaphysalis (Haemaphysalis) obesa",
        "date": "1925",
        "discoverer": "Larrousse"
    },
    {
        "species_name": "Haemaphysalis (Herpetobia) cholodkovskyi",
        "date": "1928",
        "discoverer": "Olenev"
    },
    {
        "species_name": "Haemaphysalis (Haemaphysalis) sulcata",
        "date": "1878",
        "discoverer": "Canestrini and Fanzago"
    },
    {
        "species_name": "Haemaphysalis (Haemaphysalis) sundrai",
        "date": "1928",
        "discoverer": "Sharif"
    },
    {
        "species_name": "Haemaphysalis (Kaiseriana) aculeate",
        "date": "1904",
        "discoverer": "Lavarra"
    },
    {
        "species_name": "Haemaphysalis (K.) anomala",
        "date": "1913",
        "discoverer": "Warburton"
    },
    {
        "species_name": "Haemaphysalis (K.) bispinosa",
        "date": "1897",
        "discoverer": "Neumann"
    },
    {
        "species_name": "Haemaphysalis (K.) cuspidata",
        "date": "1910",
        "discoverer": "Warburton"
    },
    {
        "species_name": "Haemaphysalis (K.) davisi",
        "date": "1970",
        "discoverer": "HoogstraaI, Dhanda and Bhat"
    },
    {
        "species_name": "Haemaphysalis (K.) hystricis",
        "date": "1897",
        "discoverer": "Supino"
    },
    {
        "species_name": "Haemaphysalis (K.) kinneari",
        "date": "1913",
        "discoverer": "Warburton"
    },
    {
        "species_name": "Haemaphysalis (K.) ramachandrai",
        "date": "1970",
        "discoverer": "Dhanda, HoogstraaI and Bhat"
    },
    {
        "species_name": "Haemaphysalis (K.) shimoga",
        "date": "1964",
        "discoverer": "Trapido and Hoogstraal"
    },
    {
        "species_name": "Haemaphysalis (K.) spinigera",
        "date": "1897",
        "discoverer": "Neumann"
    },
    {
        "species_name": "Haemaphysalis (Rhipistoma) canestrinii",
        "date": "1897",
        "discoverer": "Supino"
    },
    {
        "species_name": "Haemaphysalis (R.) indica",
        "date": "1910",
        "discoverer": "Warburton"
    },
    {
        "species_name": "Hyalomma (Hyalomma) anatolicum anatolicum",
        "date": "1844",
        "discoverer": "Koch"
    },
    {
        "species_name": "Hyalomma (Hyalomma) detritum",
        "date": "1919",
        "discoverer": "Schulz"
    },
    {
        "species_name": "Hyalomma (Hyalomma) dromedarii",
        "date": "1844",
        "discoverer": "Koch"
    },
    {
        "species_name": "Hyalomma (Hyalomma) marginatum isaaci",
        "date": "1928",
        "discoverer": "Sharif"
    },
    {
        "species_name": "Hyalomma (Hyalomma) turanicum",
        "date": "1946",
        "discoverer": "Pomerantzev"
    },
    {
        "species_name": "Hyalomma (Delpyiella) brevipunctata",
        "date": "1928",
        "discoverer": "Sharif"
    },
    {
        "species_name": "Hyalomma (D.) kumari",
        "date": "1928",
        "discoverer": "Sharif"
    },
    {
        "species_name": "Hyalomma (D.) hussaini",
        "date": "1928",
        "discoverer": "Sharif"
    },
    {
        "species_name": "Hyalomma (Hyalommina) hystricis",
        "date": "1974",
        "discoverer": "Dhanda and Raja"
    },
    {
        "species_name": "Ixodes (Afrixodes) ceylonensis",
        "date": "1950",
        "discoverer": "Kohls"
    },
    {
        "species_name": "Ixodes (A.) radfordi",
        "date": "1947",
        "discoverer": "Kohls"
    },
    {
        "species_name": "Ixodes (Eschatocephalus) vespertilionis",
        "date": "1844",
        "discoverer": "Koch"
    },
    {
        "species_name": "Ixodes (Ixodes) acutitarsus",
        "date": "1880",
        "discoverer": "Karsch"
    },
    {
        "species_name": "Ixodes (Ixodes) granulatus",
        "date": "1897",
        "discoverer": "Supino"
    },
    {
        "species_name": "Ixodes (Ixodes) himalayensis",
        "date": "1969",
        "discoverer": "Dhanda and Kulkarni"
    },
    {
        "species_name": "Ixodes (Ixodes) kashmiricus",
        "date": "1948",
        "discoverer": "Pomerantzev"
    },
    {
        "species_name": "Ixodes (Ixodes) petauristae",
        "date": "1933",
        "discoverer": "Warburton"
    },
    {
        "species_name": "Ixodes (Ixodes)) turdus",
        "date": "1942",
        "discoverer": "Nakatsuji"
    },
    {
        "species_name": "Ixodes (Partipalpiger) ovatus",
        "date": "1899",
        "discoverer": "Neumann"
    },
    {
        "species_name": "Ixodes (Sternalixodes) holocyclus",
        "date": "1899",
        "discoverer": "Neumann"
    },
    {
        "species_name": "Nosomma monstrosum",
        "date": "1908",
        "discoverer": "Nuttall and Warburton"
    },
    {
        "species_name": "Rhipicephalus haemaphysaloides",
        "date": "1897",
        "discoverer": "Supino"
    },
    {
        "species_name": "Rhipicephalus ramachandrai",
        "date": "1966",
        "discoverer": "Dhanda"
    },
    {
        "species_name": "Rhipicephalus sanguineus",
        "date": "1806",
        "discoverer": "Latrielle"
    },
    {
        "species_name": "Rhipicephalus scalpturatus",
        "date": "1959",
        "discoverer": "Santos Dias"
    },
    {
        "species_name": "Rhipicephalus turanicus",
        "date": "1940",
        "discoverer": "Pomerantzev, Matikashvili and Lotozki"
    },
    {
        "species_name": "Argas (Argas) hermanni",
        "date": "1827",
        "discoverer": "Audouin"
    },
    {
        "species_name": "Argas (Persicargas) abdussalami",
        "date": "1965",
        "discoverer": "Hoogstraal and McCarthy"
    },
    {
        "species_name": "Argas (P.) persicus",
        "date": "1818",
        "discoverer": "Oken"
    },
    {
        "species_name": "Argas (P.) robertsi",
        "date": "1968",
        "discoverer": "Hoogstraal, Kaiser and Kohls"
    },
    {
        "species_name": "Argas (Carios) gujaratensis",
        "date": "1981",
        "discoverer": "Advani and Vazirani"
    },
    {
        "species_name": "Argas (C.) hoogstraali",
        "date": "1981",
        "discoverer": "Advani and Vazirani"
    },
    {
        "species_name": "Argas (C.) indicus",
        "date": "1981",
        "discoverer": "Advani and Vazirani"
    },
    {
        "species_name": "Argas (C.) soneshinei",
        "date": "1981",
        "discoverer": "Advani and Vazirani"
    },
    {
        "species_name": "Argas (C.) vespertilionis",
        "date": "1796",
        "discoverer": "Latrielle"
    },
    {
        "species_name": "Argas (Chiropterargas) wilsoni",
        "date": "1981",
        "discoverer": "Advani and Vazirani"
    },
    {
        "species_name": "Ornithodoros crossi",
        "date": "1922",
        "discoverer": "Brumpt"
    },
    {
        "species_name": "Ornithodoros savignyi",
        "date": "1827",
        "discoverer": "Audouin"
    },
    {
        "species_name": "Ornithodoros (Alveonasus) lahorensis",
        "date": "1908",
        "discoverer": "Neumann"
    },
    {
        "species_name": "Ornithodoros (Alectorbius) coniceps",
        "date": "1890",
        "discoverer": "Canestrini"
    },
    {
        "species_name": "Ornithodoros (Reticulinasus) chiropterphila",
        "date": "1971",
        "discoverer": "Dhanda and Rajagopalan"
    },
    {
        "species_name": "Ornithodoros (R.) faini",
        "date": "1960",
        "discoverer": "Hoogstraal"
    },
    {
        "species_name": "Ornithodoros (R.) piriformis",
        "date": "1918",
        "discoverer": "Warburton"
    },
    {
        "species_name": "Otobius megnini",
        "date": "1844",
        "discoverer": "Duges"
    },
    {
        "species_name": "Bryobia eharai",
        "date": "1958",
        "discoverer": "Pritchard and Keifer"
    },
    {
        "species_name": "Bryobia praetiosa",
        "date": "1836",
        "discoverer": "Koch"
    },
    {
        "species_name": "Bryobiella punjabensis",
        "date": "1975",
        "discoverer": "Prasad"
    },
    {
        "species_name": "Aplonobia sphaeralceae",
        "date": "1968",
        "discoverer": "Tuttle & Baker"
    },
    {
        "species_name": "Mesobryobia jobneri",
        "date": "1975",
        "discoverer": "Prasad"
    },
    {
        "species_name": "Monoceronychus terpoghossiani",
        "date": "1959",
        "discoverer": "Bagdasarian"
    },
    {
        "species_name": "Neopetrobia simlaensis",
        "date": "1975",
        "discoverer": "Prasad"
    },
    {
        "species_name": "Porcupinychus abutiloni",
        "date": "1966",
        "discoverer": "Anwarullah"
    },
    {
        "species_name": "Petrobia (Tetranychina) harti",
        "date": "1909",
        "discoverer": "Ewing"
    },
    {
        "species_name": "Petrobia (Petrobia) latens",
        "date": "1776",
        "discoverer": "Muller"
    },
    {
        "species_name": "Aponychus corpuzae",
        "date": "1966",
        "discoverer": "Rimando"
    },
    {
        "species_name": "Aponychus sarjui",
        "date": "1980",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Aponychus sulcatus",
        "date": "1972",
        "discoverer": "Chaudhri"
    },
    {
        "species_name": "Aponychus (Stylophoronychus) baghensis",
        "date": "1975",
        "discoverer": "Prasad"
    },
    {
        "species_name": "Aponychus (Stylophoronychus) lalii",
        "date": "1975",
        "discoverer": "Prasad"
    },
    {
        "species_name": "Eutetranychus africanus",
        "date": "1926",
        "discoverer": "Tucker"
    },
    {
        "species_name": "Eutetranychus anneckei",
        "date": "1974",
        "discoverer": "Meyer"
    },
    {
        "species_name": "Eutetranychus bilobatus",
        "date": "1981",
        "discoverer": "Nassar & Ghai"
    },
    {
        "species_name": "Eutetranychus bredini",
        "date": "1960",
        "discoverer": "Baker & Pritchard"
    },
    {
        "species_name": "Eutetranychus caricae",
        "date": "1981",
        "discoverer": "Nassar & Ghai"
    },
    {
        "species_name": "Eutetranychus citri",
        "date": "1967",
        "discoverer": "Attiah"
    },
    {
        "species_name": "Eutetranychus maximae",
        "date": "1981",
        "discoverer": "Nassar & Ghai"
    },
    {
        "species_name": "Eutetranychus nagai",
        "date": "1981",
        "discoverer": "Nassar & Ghai"
    },
    {
        "species_name": "Eutetranychus orientalis",
        "date": "1936",
        "discoverer": "Klein"
    },
    {
        "species_name": "Eutetranychus phaseoli",
        "date": "1981",
        "discoverer": "Nassar & Ghai"
    },
    {
        "species_name": "Tenuipalponychus citri",
        "date": "1977",
        "discoverer": "ChannaBasavanna & Lakkundi"
    },
    {
        "species_name": "Mixonychus aculus",
        "date": "1971",
        "discoverer": "Chaudhri"
    },
    {
        "species_name": "Mixonychus orissaensis",
        "date": "1975",
        "discoverer": "Prasad"
    },
    {
        "species_name": "Eotetranychus broodryki",
        "date": "1974",
        "discoverer": "Meyer"
    },
    {
        "species_name": "Eotetranychus frosti",
        "date": "1952",
        "discoverer": "McGregor"
    },
    {
        "species_name": "Eotetranychus fremonti",
        "date": "1964",
        "discoverer": "Tuttle & Baker"
    },
    {
        "species_name": "Eotetranychus hirsti",
        "date": "1926",
        "discoverer": "Pritchard & Baker"
    },
    {
        "species_name": "Eotetranychus irregulaensis",
        "date": "1981",
        "discoverer": "Nassar & Ghai"
    },
    {
        "species_name": "Eotetranychus kankitus",
        "date": "1955",
        "discoverer": "Ehara"
    },
    {
        "species_name": "Eotetranychus ladakhensis",
        "date": "1981",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Eotetranychus mandensis",
        "date": "1963",
        "discoverer": "Manson"
    },
    {
        "species_name": "Eotetranychus neoperplexus",
        "date": "1950",
        "discoverer": "Estebanes & Baker"
    },
    {
        "species_name": "Eotetranychus pamelae",
        "date": "1963",
        "discoverer": "Manson"
    },
    {
        "species_name": "Eotetranychus rohiiae",
        "date": "1981",
        "discoverer": "Nassar & Ghai"
    },
    {
        "species_name": "Eotetranychus rajouriensis",
        "date": "1981",
        "discoverer": "Nassar & Ghai"
    },
    {
        "species_name": "Eotetranychus sexmaculatus",
        "date": "1890",
        "discoverer": "Riley"
    },
    {
        "species_name": "Eotetranychus suginamensis",
        "date": "1922",
        "discoverer": "Yokoyama"
    },
    {
        "species_name": "Eotetranychus syzygii",
        "date": "1979",
        "discoverer": "Gupta & Gupta"
    },
    {
        "species_name": "Eotetranychus truncatus",
        "date": "1966",
        "discoverer": "Estebanes & Baker"
    },
    {
        "species_name": "Eotetranychus uncatus",
        "date": "1952",
        "discoverer": "Garman"
    },
    {
        "species_name": "Oligonychus biharensis",
        "date": "1925",
        "discoverer": "Hirst"
    },
    {
        "species_name": "Oligonychus coffeae",
        "date": "1861",
        "discoverer": "Nietner"
    },
    {
        "species_name": "Oligonychus indicus",
        "date": "1923",
        "discoverer": "Hirst"
    },
    {
        "species_name": "Oligonychus iseilemae",
        "date": "1924",
        "discoverer": "Hirst"
    },
    {
        "species_name": "Oligonychus mangiferus",
        "date": "1940",
        "discoverer": "Rahman & Sapra"
    },
    {
        "species_name": "Oligonychus manishi",
        "date": "1979",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Oligonychus oryzae",
        "date": "1926",
        "discoverer": "Hirst"
    },
    {
        "species_name": "Oligonychus punicae",
        "date": "1926",
        "discoverer": "Hirst"
    },
    {
        "species_name": "Oligonychus sacchari",
        "date": "1942",
        "discoverer": "McGregor"
    },
    {
        "species_name": "Oligonychus sapienticolus",
        "date": "1976",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Oligonychus vitis",
        "date": "1965",
        "discoverer": "Zaher & Shehata"
    },
    {
        "species_name": "Panonychus citri",
        "date": "1916",
        "discoverer": "McGregor"
    },
    {
        "species_name": "Panonychus ulmi",
        "date": "1836",
        "discoverer": "Koch"
    },
    {
        "species_name": "Platytetranychus multidigituli",
        "date": "1917",
        "discoverer": "Ewing"
    },
    {
        "species_name": "Schizotetranychus andropogoni",
        "date": "1926",
        "discoverer": "Hirst"
    },
    {
        "species_name": "Schizotetranychus baltazari",
        "date": "1962",
        "discoverer": "Rimando"
    },
    {
        "species_name": "Schizotetranychus cajani",
        "date": "1976",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Schizotetranychus fluvialis",
        "date": "1928",
        "discoverer": "McGregor"
    },
    {
        "species_name": "Schizotetranychus hindustanicus",
        "date": "1924",
        "discoverer": "Hirst"
    },
    {
        "species_name": "Schizotetranychus mansoni",
        "date": "1980",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Schizotetranychus spireafolia",
        "date": "1940",
        "discoverer": "Garman"
    },
    {
        "species_name": "Schizotetranychus tephrosiae",
        "date": "1968",
        "discoverer": "Gutierrez"
    },
    {
        "species_name": "Schizotetranychus undulatus",
        "date": "1958",
        "discoverer": "Beer & Lang"
    },
    {
        "species_name": "Tetranychus afrindicus",
        "date": "1981",
        "discoverer": "Nassar & Ghai"
    },
    {
        "species_name": "Tetranychus angloensis",
        "date": "1974",
        "discoverer": "Meyer"
    },
    {
        "species_name": "Tetranychus cinnabarinus",
        "date": "1867",
        "discoverer": "Boisd."
    },
    {
        "species_name": "Tetranychus fijiensis",
        "date": "1924",
        "discoverer": "Hirst"
    },
    {
        "species_name": "Tetranychus hypogeae",
        "date": "1976",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Tetranychus kanzawai",
        "date": "1927",
        "discoverer": "Kishida"
    },
    {
        "species_name": "Tetranychus lombardinii",
        "date": "1960",
        "discoverer": "Baker & Pritchard"
    },
    {
        "species_name": "Tetranychus ludeni",
        "date": "1913",
        "discoverer": "Zacher"
    },
    {
        "species_name": "Tetranychus macfarlanei",
        "date": "1960",
        "discoverer": "Baker & Pritchard"
    },
    {
        "species_name": "Tetranychus neocaledonicus",
        "date": "1933",
        "discoverer": "Andre"
    },
    {
        "species_name": "Tetranychus papayae",
        "date": "1981",
        "discoverer": "Nassar & Ghai"
    },
    {
        "species_name": "Tetranychus sayedi",
        "date": "1960",
        "discoverer": "Baker & Pritchard"
    },
    {
        "species_name": "Tetranychus taiwanicus",
        "date": "1969",
        "discoverer": "Ehara"
    },
    {
        "species_name": "Tetranychus urticae",
        "date": "1836",
        "discoverer": "Koch"
    },
    {
        "species_name": "Tetranychus zaheri",
        "date": "1981",
        "discoverer": "Nassar & Ghai"
    },
    {
        "species_name": "Tuckerella delhiensis",
        "date": "1976",
        "discoverer": "Ghai & Maninder"
    },
    {
        "species_name": "Tuckerella indica",
        "date": "1973",
        "discoverer": "Prasad"
    },
    {
        "species_name": "Tuckerella kumaonensis",
        "date": "1979",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Aegyptobia mumulus",
        "date": "1972",
        "discoverer": "Chaudhri"
    },
    {
        "species_name": "Brevipalpus californicus",
        "date": "1904",
        "discoverer": "Banks"
    },
    {
        "species_name": "Brevipalpus chilensis",
        "date": "1949",
        "discoverer": "Baker"
    },
    {
        "species_name": "Brevipalpus cucurbitae",
        "date": "1982",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Brevipalpus deleoni",
        "date": "1958",
        "discoverer": "Pritchard & Baker"
    },
    {
        "species_name": "Brevipalpus euphorbiae",
        "date": "1982",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Brevipalpus essigi",
        "date": "1949",
        "discoverer": "Baker"
    },
    {
        "species_name": "Brevipalpus karachiensis",
        "date": "1974",
        "discoverer": "Chaudhri, Akbar & Rasool"
    },
    {
        "species_name": "Brevipalpus lewisi",
        "date": "1949",
        "discoverer": "McGregor"
    },
    {
        "species_name": "Brevipalpus melichrus",
        "date": "1952",
        "discoverer": "Pritchard & Baker"
    },
    {
        "species_name": "Brevipalpus mitrofanovi",
        "date": "1975",
        "discoverer": "Pegazzano"
    },
    {
        "species_name": "Brevipalpus obovatus",
        "date": "1875",
        "discoverer": "Donnadieu"
    },
    {
        "species_name": "Brevipalpus phoenicis",
        "date": "1939",
        "discoverer": "Geijskes"
    },
    {
        "species_name": "Brevipalpus pulchur",
        "date": "1876",
        "discoverer": "C. & F."
    },
    {
        "species_name": "Brevipalpus rica",
        "date": "1972",
        "discoverer": "Chaudhri"
    },
    {
        "species_name": "Brevipalpus rugulosus",
        "date": "1974",
        "discoverer": "Chaudhri, Akbar & Rasool"
    },
    {
        "species_name": "Brevipalpus turrialbensis",
        "date": "1963",
        "discoverer": "Manson"
    },
    {
        "species_name": "Cenopalpus picitilis",
        "date": "1971",
        "discoverer": "Chaudhri"
    },
    {
        "species_name": "Dolichotetranychus floridamus",
        "date": "1900",
        "discoverer": "Banks"
    },
    {
        "species_name": "Larvacarus transtitans",
        "date": "1922",
        "discoverer": "Ewing"
    },
    {
        "species_name": "Obuloides rajamohani",
        "date": "1975",
        "discoverer": "Baker & Tuttle"
    },
    {
        "species_name": "Pentamerismus oregonensis",
        "date": "1949",
        "discoverer": "McGregor"
    },
    {
        "species_name": "Phytoptipalpus albizziae",
        "date": "1958",
        "discoverer": "Pritchard & Baker"
    },
    {
        "species_name": "Raoiella indica",
        "date": "1924",
        "discoverer": "Hirst"
    },
    {
        "species_name": "Raoiella macfarlanei",
        "date": "1958",
        "discoverer": "Pritchard & Baker"
    },
    {
        "species_name": "Tenuipalpus aboharensis",
        "date": "1980",
        "discoverer": "Sadana & Chhabra"
    },
    {
        "species_name": "Tenuipalpus acacii",
        "date": "1978",
        "discoverer": "Maninder & Ghai"
    },
    {
        "species_name": "Tenuipalpus amygdalusae",
        "date": "1978",
        "discoverer": "Maninder & Ghai"
    },
    {
        "species_name": "Tenuipalpus bassaie",
        "date": "1988",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Tenuipalpus caudatus",
        "date": "1834",
        "discoverer": "Duges"
    },
    {
        "species_name": "Tenuipalpus cissampelosa",
        "date": "1978",
        "discoverer": "Maninder & Ghai"
    },
    {
        "species_name": "Tenuipalpus coimbatorensis",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Tenuipalpus crassulus",
        "date": "1972",
        "discoverer": "Baker and Tuttle"
    },
    {
        "species_name": "Tenuipalpus crassus",
        "date": "1953",
        "discoverer": "Andre"
    },
    {
        "species_name": "Tenuipalpus dimensus",
        "date": "1971",
        "discoverer": "Chaudhri"
    },
    {
        "species_name": "Tenuipalpus faresianus",
        "date": "1978",
        "discoverer": "Maninder & Ghai"
    },
    {
        "species_name": "Tenuipalpus fici",
        "date": "1978",
        "discoverer": "Maninder &. Ghai"
    },
    {
        "species_name": "Tenuipalpus granati",
        "date": "1942",
        "discoverer": "Sayed"
    },
    {
        "species_name": "Tenuipalpus ghaii",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Tenuipalpus hastaligni",
        "date": "1956",
        "discoverer": "DeLeon"
    },
    {
        "species_name": "Tenuipalpus indicus",
        "date": "1978",
        "discoverer": "Maninder & Ghai"
    },
    {
        "species_name": "Tenuipalpus ixorae",
        "date": "1978",
        "discoverer": "Maninder & Ghai"
    },
    {
        "species_name": "Tenuipalpus lalbaghensis",
        "date": "1977",
        "discoverer": "ChannaBasavanna & Lakkundi"
    },
    {
        "species_name": "Tenuipalpus laminasetae",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Tenuipalpus leipoldti",
        "date": "1993",
        "discoverer": "Meyer"
    },
    {
        "species_name": "Tenuipalpus leptadeniaei",
        "date": "1995",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Tenuipalpus ludhianaensis",
        "date": "1980",
        "discoverer": "Sadana & Chhabra"
    },
    {
        "species_name": "Tenuipalpus malligai",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Tenuipalpus micheli",
        "date": "1940",
        "discoverer": "Lawrence"
    },
    {
        "species_name": "Tenuipalpus mustus",
        "date": "1972",
        "discoverer": "Chaudhri"
    },
    {
        "species_name": "Tenuipalpus pernicis",
        "date": "1974",
        "discoverer": "Chaudhri, Akbar & Rasool"
    },
    {
        "species_name": "Tenuipalpus pruni",
        "date": "1978",
        "discoverer": "Maninder & Ghai"
    },
    {
        "species_name": "Tenuipalpus punicae",
        "date": "1958",
        "discoverer": "Pritchard & Baker"
    },
    {
        "species_name": "Tenuipalpus punjabensis",
        "date": "1978",
        "discoverer": "Maninder & Ghai"
    },
    {
        "species_name": "Tenuipalpus pyrusae",
        "date": "1978",
        "discoverer": "Maninder & Ghai"
    },
    {
        "species_name": "Tenuipalpus quadrisetosus",
        "date": "1940",
        "discoverer": "Lawrence"
    },
    {
        "species_name": "Tenuipalpus tectonae",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Tenuipalpus tetrazygae",
        "date": "1956",
        "discoverer": "DeLeon"
    },
    {
        "species_name": "Tenuipalpus yousefi",
        "date": "1981",
        "discoverer": "Nassar & Ghai"
    },
    {
        "species_name": "Terminalichus delhiensis",
        "date": "1978",
        "discoverer": "Maninder & Ghai"
    },
    {
        "species_name": "Terminalichus karachiensis",
        "date": "1973",
        "discoverer": "Anwarullah & Khan"
    },
    {
        "species_name": "Terminalichus panajiensis",
        "date": "1978",
        "discoverer": "Maninder & Ghai"
    },
    {
        "species_name": "Terminalichus serratus",
        "date": "1981",
        "discoverer": "Nassar & Ghai"
    },
    {
        "species_name": "Neophantacrus mallotus",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Mackiella borasis",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Anchiphytoptus giganticus",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Anothopoda deviarensis",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Anothopoda fici",
        "date": "1982",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Anothopoda micheliae",
        "date": "2007",
        "discoverer": "Chakrabarti, Das and Pandit"
    },
    {
        "species_name": "Anothopoda wightianae",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Colopodacus bengalensis",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Colopodacus cinnamomae",
        "date": "1980",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Colopodacus combretus",
        "date": "1982",
        "discoverer": "Ghosh & Chakrabarti"
    },
    {
        "species_name": "Colopodacus eugeniae",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Colopodacus gynalaxtae",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Colopodacus kallari",
        "date": "1986",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Colopodacus walayarensis",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Cosella cissi",
        "date": "1978",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Cosella fleschneri",
        "date": "1959",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Cosella ichnocarpasia",
        "date": "1981",
        "discoverer": "Mondal & Chakrabarti"
    },
    {
        "species_name": "Cosella meghalayensis",
        "date": "2007",
        "discoverer": "Chakrabarti, Das and Pandit"
    },
    {
        "species_name": "Disella cuminis",
        "date": "2007",
        "discoverer": "Chakrabarti, Das and Pandit"
    },
    {
        "species_name": "Disella granulacoxae",
        "date": "1986",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Disella oblongifoliae",
        "date": "1986",
        "discoverer": "Ghosh, Mondal and Chakrabarti"
    },
    {
        "species_name": "Disella tectona",
        "date": "1982",
        "discoverer": "Das & Chakrabarti"
    },
    {
        "species_name": "Disella vagrans",
        "date": "1986",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Floracarus biharensis",
        "date": "1985",
        "discoverer": "Das and Chakrabarti"
    },
    {
        "species_name": "Floracarus eugenifoliae",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Floracarus pollachiensis",
        "date": "1980",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Floracarus salvifoliae",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Floracarus siruvaniensis",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Floracarus sivakumarii",
        "date": "1981",
        "discoverer": "Mohansudaram"
    },
    {
        "species_name": "Neocosella ichnocarpae",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Nothopoda kallarensis",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Ashieldophyes pennadamensis",
        "date": "1985",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Brevishieldophyes glochidionae",
        "date": "2019",
        "discoverer": "Chakrabarti, Pandit and Sur"
    },
    {
        "species_name": "Mesoshieldophyes varecae",
        "date": "2019",
        "discoverer": "Chakrabarti, Pandit and Sur"
    },
    {
        "species_name": "Circaces chakrabartii",
        "date": "1978",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Circaces icacinae",
        "date": "1999",
        "discoverer": "Umapathy"
    },
    {
        "species_name": "Colomerus alangii",
        "date": "1971",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Colomerus neopiperis",
        "date": "1970",
        "discoverer": "Wilson"
    },
    {
        "species_name": "Colomerus trichodesmae",
        "date": "1997",
        "discoverer": "Chakrabarti and Pandit"
    },
    {
        "species_name": "Colomerus vitis",
        "date": "1857",
        "discoverer": "Pgst."
    },
    {
        "species_name": "Colomerus woodfordis",
        "date": "1989",
        "discoverer": "Ghosh and Chakrabarti"
    },
    {
        "species_name": "Cosetacus citrifolis",
        "date": "1985",
        "discoverer": "Das and Chakrabarti"
    },
    {
        "species_name": "Cosetacus eupatori",
        "date": "1997",
        "discoverer": "Chakrabarti and Pandit"
    },
    {
        "species_name": "Cosetacus prosteti",
        "date": "2007",
        "discoverer": "Pandit and Chakrabarti"
    },
    {
        "species_name": "Cosetacus sharadi",
        "date": "2009",
        "discoverer": "Menon, Joshi and Ramamurthy"
    },
    {
        "species_name": "Ectomerus chebulae",
        "date": "1980",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Epicecidophyes clerodendris",
        "date": "1981",
        "discoverer": "Mondal & Chakrabarti"
    },
    {
        "species_name": "Epicecidophyes indica",
        "date": "1982",
        "discoverer": "Mondal, Ghosh & Chakrabarti"
    },
    {
        "species_name": "Gammapbytoptus bengalensis",
        "date": "1985",
        "discoverer": "Das and Chakrabarti"
    },
    {
        "species_name": "Gammapbytoptus litseasis",
        "date": "1982",
        "discoverer": "Mondal, Ghosh & Chakrabarti"
    },
    {
        "species_name": "Indosetacus cleistanthusi",
        "date": "2008",
        "discoverer": "Chakrabarti, Pandit and Mondal"
    },
    {
        "species_name": "Indosetacus rhinacanthi",
        "date": "1987",
        "discoverer": "Ghosh and Chakrabarti"
    },
    {
        "species_name": "Isoannulus bengalensis",
        "date": "2009",
        "discoverer": "Chakrabarti and Pandit"
    },
    {
        "species_name": "Tergamplam calicarpi",
        "date": "2009",
        "discoverer": "Chakrabarti and Pandit"
    },
    {
        "species_name": "Neocecidophyes mallotivagrans",
        "date": "1980",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Acalitus delhiensis",
        "date": "2009",
        "discoverer": "Menon, Joshi and Ramamurthy"
    },
    {
        "species_name": "Acalitus epiphytivagrans",
        "date": "1983",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Acalitus gossypii",
        "date": "1904",
        "discoverer": "Banks"
    },
    {
        "species_name": "Acalitus hibisci",
        "date": "1982",
        "discoverer": "Mondal & Chakrabarti"
    },
    {
        "species_name": "Acalitus meliosmae",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Acalitus reticulatae",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Acalitus ruelliae",
        "date": "1966",
        "discoverer": "Channabasavanna"
    },
    {
        "species_name": "Acalitus schefflerae",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Aceria abutilonae",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria acalyphae",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria acanthae",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria achyranthi",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria aervae",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria agallochae",
        "date": "1983",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria ailanthae",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria alangiae",
        "date": "1986",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria allophylae",
        "date": "2000",
        "discoverer": "Umapathy and Mohanasundaram"
    },
    {
        "species_name": "Aceria amrini",
        "date": "2013",
        "discoverer": "Joshi, Menon and Ramamurthy"
    },
    {
        "species_name": "Aceria anisomelae",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria anonae",
        "date": "1973",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Aceria antidotalae",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Aceria apodytae",
        "date": "2000",
        "discoverer": "Umapathy and Mohanasundaram"
    },
    {
        "species_name": "Aceria ariyankavensis",
        "date": "2000",
        "discoverer": "Umapathy and Mohanasundaram"
    },
    {
        "species_name": "Aceria articulate",
        "date": "2000",
        "discoverer": "Umapathy and Mohanasundaram"
    },
    {
        "species_name": "Aceria asperae",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria asystasiae",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria attakattiensis",
        "date": "2000",
        "discoverer": "Umapathy and Mohanasundaram"
    },
    {
        "species_name": "Aceria bambusae",
        "date": "1966",
        "discoverer": "Channabasavanna"
    },
    {
        "species_name": "Aceria banyani",
        "date": "1983",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria balanties",
        "date": "1927",
        "discoverer": "Massee"
    },
    {
        "species_name": "Aceria barleriae",
        "date": "1966",
        "discoverer": "Channabasavanna"
    },
    {
        "species_name": "Aceria bassiae",
        "date": "1988",
        "discoverer": "Ghosh and Chakrabarti"
    },
    {
        "species_name": "Aceria berberae",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria boraginae",
        "date": "1982",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Aceria borreriae",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria bueitneriae",
        "date": "1985",
        "discoverer": "Mohanasundaram and Sharma"
    },
    {
        "species_name": "Aceria cajani",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Aceria cernuas",
        "date": "1927",
        "discoverer": "Massee"
    },
    {
        "species_name": "Aceria clerodendronis",
        "date": "1960",
        "discoverer": "Farkas"
    },
    {
        "species_name": "Aceria crotalariae",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Aceria commiphorae",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria corchorae",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria cordiae",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Aceria channabasavannai",
        "date": "",
        "discoverer": "Amrine and Stasny"
    },
    {
        "species_name": "Aceria cymbopogonis",
        "date": "1978",
        "discoverer": "Mohanasundaram and Subramaniam"
    },
    {
        "species_name": "Aceria delhiensis",
        "date": "1982",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Aceria dichotomae",
        "date": "1982",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Aceria dactylonae",
        "date": "1983",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Aceria donacis",
        "date": "1983",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Aceria dasi",
        "date": "1988",
        "discoverer": "Ghosh and Chakrabarti"
    },
    {
        "species_name": "Aceria dalbergiae",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Aceria debregeasiae",
        "date": "2001",
        "discoverer": "Umapathy"
    },
    {
        "species_name": "Aceria dhanikhariensis",
        "date": "1985",
        "discoverer": "Mohanasundaram and Sharma"
    },
    {
        "species_name": "Aceria eragrostae",
        "date": "1983",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Aceria erythrinae",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Aceria eugeniae",
        "date": "1999",
        "discoverer": "Umapathy and Mohanasundaram"
    },
    {
        "species_name": "Aceria feroniae",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria ficus",
        "date": "1920",
        "discoverer": "Cotte"
    },
    {
        "species_name": "Aceria fissistigmae",
        "date": "2000",
        "discoverer": "Pandit and Chakrabarti"
    },
    {
        "species_name": "Aceria gastrotrichus",
        "date": "1918",
        "discoverer": "Nalepa"
    },
    {
        "species_name": "Aceria granati",
        "date": "1894",
        "discoverer": "Canestrini & Masalongo"
    },
    {
        "species_name": "Aceria guerreronis",
        "date": "1965",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Aceria hirsutivagrans",
        "date": "1984",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria holopteleae",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Aceria indiensis",
        "date": "1980",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria infectoriae",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Aceria jacobii",
        "date": "1980",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria jasmini",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Aceria jogimatiensis",
        "date": "1985",
        "discoverer": "Mohanasundaram and Jagadish"
    },
    {
        "species_name": "Aceria justiciae",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Aceria kenyae",
        "date": "1966",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Aceria kigeliae",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria lalbaghi",
        "date": "1994",
        "discoverer": "Amrine and Stasny"
    },
    {
        "species_name": "Aceria leucophloeae",
        "date": "1983",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria leucopyrae",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria linnae",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria litchii",
        "date": "1943",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Aceria litseae",
        "date": "1972",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Aceria longisetae",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria lycopersici",
        "date": "1879",
        "discoverer": "Wolff."
    },
    {
        "species_name": "Aceria madhucae",
        "date": "2011",
        "discoverer": "Joshi, Menon and Ramamurthy"
    },
    {
        "species_name": "Aceria madukkaraiensis",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria malloticola",
        "date": "1980",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Aceria mangiferae",
        "date": "1946",
        "discoverer": "Sayed"
    },
    {
        "species_name": "Aceria marudamalaiensis",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria mauritianae",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria mimusopae",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria medicaginis",
        "date": "1941",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Aceria mitragynae",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria mori",
        "date": "1939",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Aceria nandiensis",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Aceria negundi",
        "date": "1913",
        "discoverer": "Hodgkiss"
    },
    {
        "species_name": "Aceria nerii",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Aceria noxia",
        "date": "2020",
        "discoverer": "Flechtmann and Tassi"
    },
    {
        "species_name": "Aceria obliquae",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria phyllanthae",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria poae",
        "date": "1994",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria polygalae",
        "date": "1982",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Aceria pustulatas",
        "date": "1983",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria pongamiae",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Aceria puttarudriahi",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Aceria randi",
        "date": "1988",
        "discoverer": "Ghosh and Chakrabarti"
    },
    {
        "species_name": "Aceria sacchari",
        "date": "1966",
        "discoverer": "Channabasavanna"
    },
    {
        "species_name": "Aceria saccharini",
        "date": "1964",
        "discoverer": "Wang"
    },
    {
        "species_name": "Aceria sapindi",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Aceria securinegae",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria serndanurensis",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria sheldoni",
        "date": "1937",
        "discoverer": "Ewing"
    },
    {
        "species_name": "Aceria setacea",
        "date": "1983",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Aceria siruvaniensis",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria sorghi",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Aceria subramani",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria terminaliphagus",
        "date": "1994",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria trianthemae",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria trichocnemam",
        "date": "1914",
        "discoverer": "Nalepa"
    },
    {
        "species_name": "Aceria tripuraensis",
        "date": "2014",
        "discoverer": "Menon, Joshi and Ramamurthy"
    },
    {
        "species_name": "Aceria tulipae",
        "date": "1938",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Aceria vadalurensis",
        "date": "1983",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria vitifoliae",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria vriddhagiriensis",
        "date": "1981",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria walayri",
        "date": "1994",
        "discoverer": "Amrine and Stasny"
    },
    {
        "species_name": "Aceria wallichianae",
        "date": "1975",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Aceria waltheriae",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aceria wandoorensis",
        "date": "1985",
        "discoverer": "Mohanasundaram and Sharma"
    },
    {
        "species_name": "Aceria xeromphisi",
        "date": "1990",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Acerimina tiliaceae",
        "date": "1985",
        "discoverer": "Mohanasundaram and Sharma"
    },
    {
        "species_name": "Baileyna indica",
        "date": "1989",
        "discoverer": "Chakrabarti and Das"
    },
    {
        "species_name": "Brachendus grewiae",
        "date": "1999",
        "discoverer": "Umapathy"
    },
    {
        "species_name": "Cymoptus bengalensis",
        "date": "1984",
        "discoverer": "Ghosh, Mondal and Chakrabarti"
    },
    {
        "species_name": "Eriophyes acaciae",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Eriophyes antiquorum",
        "date": "1983",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Eriophyes breyniae",
        "date": "1981",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Eriophyes carissae",
        "date": "1981",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Eriophyes casuarinae",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Eriophyes canthii",
        "date": "1966",
        "discoverer": "Channabasavanna"
    },
    {
        "species_name": "Eriophyes cheriani",
        "date": "1933",
        "discoverer": "Massee"
    },
    {
        "species_name": "Eriophyes coimbatoriensis",
        "date": "1981",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Eriophyes cyperi",
        "date": "1966",
        "discoverer": "Channabasavanna"
    },
    {
        "species_name": "Eriophyes eletariae",
        "date": "1981",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Eriophyes ensifoliae",
        "date": "1989",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Eriophyes erineus",
        "date": "1891",
        "discoverer": "Nalepa"
    },
    {
        "species_name": "Eriophyes erythrensis",
        "date": "1981",
        "discoverer": "Chakrabarti and Ghosh"
    },
    {
        "species_name": "Eriophyes ficivorus",
        "date": "1966",
        "discoverer": "Channabasavanna"
    },
    {
        "species_name": "Eriophyes glycosmisae",
        "date": "1981",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Eriophyes hexandrae",
        "date": "1999",
        "discoverer": "Umapathy and Mohanasundaram"
    },
    {
        "species_name": "Eriophyes karnatakaensis",
        "date": "1981",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Eriophyes lantanae",
        "date": "1981",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Eriophyes laurae",
        "date": "1981",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Eriophyes morindae",
        "date": "1981",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Eriophyes plectroniae",
        "date": "1983",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Eriophyes prosopidis",
        "date": "1942",
        "discoverer": "Saxena"
    },
    {
        "species_name": "Eriophyes pyri",
        "date": "1857",
        "discoverer": "Pagt."
    },
    {
        "species_name": "Eriophyes rosae",
        "date": "1981",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Eriophyes rotundae",
        "date": "1983",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Eriophyes saccharini",
        "date": "1981",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Eriophyes subbaroi",
        "date": "1981",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Eriophyes rubifolii",
        "date": "1966",
        "discoverer": "Channabasavanna"
    },
    {
        "species_name": "Eriophyes terminaliae",
        "date": "1966",
        "discoverer": "Channabasavanna"
    },
    {
        "species_name": "Eriophyes tristiatas",
        "date": "1960",
        "discoverer": "Nalepa"
    },
    {
        "species_name": "Proartacris pinnivagrans",
        "date": "1984",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Keiferophyes avicenniae",
        "date": "1983",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Mangalaus bkapus",
        "date": "2011",
        "discoverer": "Menon Ochoa and Bauchan"
    },
    {
        "species_name": "Paraphytoptus alangiae",
        "date": "1984",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Paraphytoptus champacae",
        "date": "1984",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Paraphytoptus chrysanthemi",
        "date": "1940",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Paraphytoptus cristatae",
        "date": "1984",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Paraphytoptus crotalariphagus",
        "date": "1984",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Paraphytoptus elaeocarpae",
        "date": "1984",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Paraphytoptus erinevagrans",
        "date": "1984",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Paraphytoptus jujubae",
        "date": "1989",
        "discoverer": "Mohanasundaran"
    },
    {
        "species_name": "Paraphytoptus serenus",
        "date": "2016",
        "discoverer": "Duarte, Chetverikov, Silva and Navia"
    },
    {
        "species_name": "Ramaculus karnatakaensis",
        "date": "1999",
        "discoverer": "Umapathy"
    },
    {
        "species_name": "Acaphylla indiae",
        "date": "1954",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Acaphylla steinwedeni",
        "date": "1982",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Acaphylla syzygii",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Acaphylla theae",
        "date": "1898",
        "discoverer": "Watt"
    },
    {
        "species_name": "Acaphyllisa araucuriae",
        "date": "2000",
        "discoverer": "Flechtmann"
    },
    {
        "species_name": "Acaphyllisa parindiae",
        "date": "1978",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Acaphyllisa pipera",
        "date": "1987",
        "discoverer": "Ghosh and Chakrabarti"
    },
    {
        "species_name": "Acaricalus artocarpae",
        "date": "1997",
        "discoverer": "Chakrabarti and Pandit"
    },
    {
        "species_name": "Acaricalus darjeelingensis",
        "date": "1989",
        "discoverer": "Ghosh and Chakrabarti"
    },
    {
        "species_name": "Acaricalus indicus",
        "date": "2017",
        "discoverer": "Sur, Roy and Chakrabarti"
    },
    {
        "species_name": "Brionesa semecarpae",
        "date": "1999",
        "discoverer": "Umapathy"
    },
    {
        "species_name": "Cymeda indica",
        "date": "2020",
        "discoverer": "Roy and Chakrabarti"
    },
    {
        "species_name": "Dichopelmus puncti",
        "date": "2016",
        "discoverer": "Debnath and Karmakar"
    },
    {
        "species_name": "Neodichopelmus cordiae",
        "date": "1997",
        "discoverer": "Chakrabarti and Pandit"
    },
    {
        "species_name": "Notacaphylla chinensiae",
        "date": "1988",
        "discoverer": "Mohanasundaram and Singh"
    },
    {
        "species_name": "Neoacaphyllisa alangia",
        "date": "2020",
        "discoverer": "Roy and Chakrabarti"
    },
    {
        "species_name": "Paracaphylla streblae",
        "date": "1982",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Protumescoptes antedesmae",
        "date": "2001",
        "discoverer": "Pandit and Chakrabarti"
    },
    {
        "species_name": "Pseudocalepitrimerus dharmapuriensis",
        "date": "1999",
        "discoverer": "Umapathy"
    },
    {
        "species_name": "Tumescoptes trachycarpi",
        "date": "1939",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Calacarus araliae",
        "date": "1980",
        "discoverer": "Chakrabarti & Mondal"
    },
    {
        "species_name": "Calacarus carinatus",
        "date": "1890",
        "discoverer": "Green"
    },
    {
        "species_name": "Calacarus brionesae",
        "date": "1980",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Calacarus capsica",
        "date": "1980",
        "discoverer": "Chakrabarti & Mondal"
    },
    {
        "species_name": "Calacarus channabasavannae",
        "date": "1974",
        "discoverer": "Lakkundi"
    },
    {
        "species_name": "Calacarus citrifolii",
        "date": "1982",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Calacarus jasmini",
        "date": "1979",
        "discoverer": "Chakrabarti & Mondal"
    },
    {
        "species_name": "Calacarus kalyaniensis",
        "date": "2016",
        "discoverer": "Debnath and Karmakar"
    },
    {
        "species_name": "Calacarus keiferi",
        "date": "1980",
        "discoverer": "Chakrabarti & Mondal"
    },
    {
        "species_name": "Calacarus malvae",
        "date": "1983",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Calacarus malvavagrans",
        "date": "1986",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Calacarus microrostrus",
        "date": "1981",
        "discoverer": "Chakrabarti & Mondal"
    },
    {
        "species_name": "Calacarus millingtoniae",
        "date": "1982",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Calacarus palmae",
        "date": "1994",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Calacarus polyalthiae",
        "date": "1980",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Calacarus quisqualis",
        "date": "",
        "discoverer": "Chakrabarti & Mondal"
    },
    {
        "species_name": "Calacarus swietensis",
        "date": "1980",
        "discoverer": "Chakrabarti & Mondal"
    },
    {
        "species_name": "Calacarus vasicae",
        "date": "2008",
        "discoverer": "Chakrabarti, Sarkar and Pandit"
    },
    {
        "species_name": "Hornophyes andamanensis",
        "date": "1994",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Procalacarus aliyarensis",
        "date": "1983",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Hemiscolocenus rares",
        "date": "1986",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Neotegonotus indicus",
        "date": "1982",
        "discoverer": "Mondal and Chakrabarti"
    },
    {
        "species_name": "Neotegonotus fastigatus",
        "date": "1961",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Oxycenus diospyrosis",
        "date": "1986",
        "discoverer": "Ghosh, Mondal and Chakrabarti"
    },
    {
        "species_name": "Phyllocoptacus barringtoniae",
        "date": "1985",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Propeaciota genusetosis",
        "date": "2017",
        "discoverer": "Chakrabarti, Sur, Roy and Sarkar"
    },
    {
        "species_name": "Scolocenus spiniferus",
        "date": "1962",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Shevtchenkella birbhumensis",
        "date": "1985",
        "discoverer": "Das and Chakrabarti"
    },
    {
        "species_name": "Shevtchenkella brideliae",
        "date": "1989",
        "discoverer": "Ghosh and Chakrabarti"
    },
    {
        "species_name": "Shevtchenkella cardiavagrans",
        "date": "1982",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Shevtchenkella coimbatorensis",
        "date": "1983",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Shevtchenkella parviflorae",
        "date": "1981",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Spinacus pagonis",
        "date": "1979",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Spinaephyes alnus",
        "date": "2017",
        "discoverer": "Chakrabarti, Sur, Roy and Sarkar"
    },
    {
        "species_name": "Tegonotus bassius",
        "date": "1982",
        "discoverer": "Das & Chakrabarti"
    },
    {
        "species_name": "Tegonotus bengalensis",
        "date": "1980",
        "discoverer": "MandaI & Chakrabarti"
    },
    {
        "species_name": "Tegonotus bhutani",
        "date": "2007",
        "discoverer": "Chakrabarti and Chakrabarti"
    },
    {
        "species_name": "Tegonotus convolvuli",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Tegonotus dubrakoni",
        "date": "1983",
        "discoverer": "Ghosh and Chakrabarti"
    },
    {
        "species_name": "Tegonotus ferrugeniae",
        "date": "1985",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Tegonotus fisus",
        "date": "2011",
        "discoverer": "Chakrabarti and Sarkar"
    },
    {
        "species_name": "Tegonotus jambolensis",
        "date": "1982",
        "discoverer": "Mondal, Ghosh & Chakrabarti"
    },
    {
        "species_name": "Tegonotus litseasis",
        "date": "1983",
        "discoverer": "Ghosh and Chakrabarti"
    },
    {
        "species_name": "Tegonotus mangiferae",
        "date": "1946",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Tegonotus schleicherae",
        "date": "1989",
        "discoverer": "Ghosh and Chakrabarti"
    },
    {
        "species_name": "Tegonotus parviflorae",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Calepitrimerus adinus",
        "date": "1985",
        "discoverer": "Das and Chakrabarti"
    },
    {
        "species_name": "Calepitrimerus antedesmae",
        "date": "1982",
        "discoverer": "Chakrabarti & Das"
    },
    {
        "species_name": "Calepitrimerus asperrimae",
        "date": "1982",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Calepitrimerus azadirachtae",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Calepitrimerus cordiae",
        "date": "1982",
        "discoverer": "Chakrabarti & Das"
    },
    {
        "species_name": "Calepitrimerus hispidus",
        "date": "1983",
        "discoverer": "Mondal and Chakrabarti"
    },
    {
        "species_name": "Calepitrimerus leucadis",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Calepitrimerus massanjoris",
        "date": "1982",
        "discoverer": "Das & Chakrabarti"
    },
    {
        "species_name": "Calepitrimerus mysorensis",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Calepitrimerus sagarensis",
        "date": "1983",
        "discoverer": "Mondal and Chakrabarti"
    },
    {
        "species_name": "Calepitrimerus tabernaemontanis",
        "date": "1983",
        "discoverer": "Mondal and Chakrabarti"
    },
    {
        "species_name": "Calepitrimerus terminalis",
        "date": "1985",
        "discoverer": "Das and Chakrabarti"
    },
    {
        "species_name": "Calepitrimerus woodfordis",
        "date": "1985",
        "discoverer": "Das and Chakrabarti"
    },
    {
        "species_name": "Caliphytoptus buchnaniae",
        "date": "",
        "discoverer": "Umapathy and Mohanasundaram"
    },
    {
        "species_name": "Caliphytoptus ulmifoliae",
        "date": "1998",
        "discoverer": "Umapathy and Mohanasundaram"
    },
    {
        "species_name": "Epitrimerus azimae",
        "date": "1982",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Epitrimerus buchneriae",
        "date": "1985",
        "discoverer": "Mohanasundaram and Venkatesh"
    },
    {
        "species_name": "Epitrimerus chandramohani",
        "date": "1980",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Epitrimerus morindae",
        "date": "1983",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Epitrimerus parasakthi",
        "date": "1983",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Indonotalox sudarsani",
        "date": "1982",
        "discoverer": "Ghosh & Chakrabarti"
    },
    {
        "species_name": "Laterotuberculus sterculia",
        "date": "2001",
        "discoverer": "Umapathy"
    },
    {
        "species_name": "Monotrimacus quadrangulari",
        "date": "1982",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Neocupacarus flabelliferis",
        "date": "1985",
        "discoverer": "Das and Chakrabarti"
    },
    {
        "species_name": "Neodicrothrix celloshieldae",
        "date": "1999",
        "discoverer": "Umapathy"
    },
    {
        "species_name": "Neodicrothrix piprae",
        "date": "1989",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Neodicrothrix rutacevagrans",
        "date": "1999",
        "discoverer": "Umapathy"
    },
    {
        "species_name": "Neodicrothrix tiliacorae",
        "date": "1984",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Neometaculus bauhiniae",
        "date": "1983",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Neophytoptus ocimae",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Notostrix attenuata",
        "date": "1963",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Notostrix flabelliferae",
        "date": "1982",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Obesophyes linocierae",
        "date": "1999",
        "discoverer": "Umapathy"
    },
    {
        "species_name": "Phyllocoptes acaciae",
        "date": "1983",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Phyllocoptes anisomeliasis",
        "date": "2008",
        "discoverer": "Chakrabarti, Sarkar and Pandit"
    },
    {
        "species_name": "Phyllocoptes aliyamagarensis",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Phyllocoptes asperaevagrans",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Phyllocoptes epimeredi",
        "date": "1981",
        "discoverer": "Amrine and Stasny"
    },
    {
        "species_name": "Phyllocoptes ficivagrans",
        "date": "1982",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Phyllocoptes immigrans",
        "date": "1940",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Phyllocoptes salmaliae",
        "date": "1979",
        "discoverer": "Chakrabarti & Mondal"
    },
    {
        "species_name": "Phyllocoptes simplicifoliae",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Phyllocoptes shoreum",
        "date": "1986",
        "discoverer": "Ghosh, Mondal and Chakrabarti"
    },
    {
        "species_name": "P tomentosae",
        "date": "1985",
        "discoverer": "Das and Chakrabarti"
    },
    {
        "species_name": "Phyllocoptruta citricola",
        "date": "2011",
        "discoverer": "Chakrabarti and Sarkar"
    },
    {
        "species_name": "Phyllocoptruta daturae",
        "date": "1985",
        "discoverer": "Mohanasundaram and Ranganath"
    },
    {
        "species_name": "Phyllocoptruta himalayana",
        "date": "1980",
        "discoverer": "Chakrabarti and Roy"
    },
    {
        "species_name": "Phyllocoptruta malligai",
        "date": "1980",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Phyllocoptruta neemae",
        "date": "2015",
        "discoverer": "Debnath and Karmakar"
    },
    {
        "species_name": "Phyllocoptruta oleivorus",
        "date": "1879",
        "discoverer": "Ashmead"
    },
    {
        "species_name": "Proneotegonotus antiquorae",
        "date": "1983",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Prophyllocoptes riveae",
        "date": "1984",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Rhombacus eucalypti",
        "date": "1987",
        "discoverer": "Ghosh and Chakrabarti"
    },
    {
        "species_name": "Rhombacus morrisii",
        "date": "1965",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Subductophyes digitariae",
        "date": "2017",
        "discoverer": "Sur and Chakrabarti"
    },
    {
        "species_name": "Vasates cassiae",
        "date": "1982",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Vasates lakoochae",
        "date": "",
        "discoverer": "Pandit and Chakrabarti"
    },
    {
        "species_name": "Vasates odinae",
        "date": "1983",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Vasates pavetis",
        "date": "",
        "discoverer": "Ghosh, Mondal and Chakrabarti"
    },
    {
        "species_name": "Abacarus arjunalis",
        "date": "1982",
        "discoverer": "Mondal, Ghosh & Chakrabarti"
    },
    {
        "species_name": "Abacarus asiaticae",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Abacarus delhiensis",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Abacarus foliavagrans",
        "date": "1986",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Abacarus goaensis",
        "date": "1980",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Abacarus gossypii",
        "date": "1982",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Abacarus oryzae",
        "date": "1963",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Abacarus pseudostriae",
        "date": "1984",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Abacarus sacchari",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Abacarus sundarbanensis",
        "date": "",
        "discoverer": "Sur, Roy and Chakrabarti"
    },
    {
        "species_name": "Aculops abutiloni",
        "date": "1981",
        "discoverer": "Mondal & Chakrabarti"
    },
    {
        "species_name": "Aculops anacardiae",
        "date": "1982",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aculops boerhaeviae",
        "date": "1982",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Aculops dilleniae",
        "date": "",
        "discoverer": "Ghosh and Chakrabarati"
    },
    {
        "species_name": "Aculops extensae",
        "date": "1980",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Aculops jalpaiguriensis",
        "date": "2001",
        "discoverer": "Pandit and Chakrabarti"
    },
    {
        "species_name": "Aculops leguminae",
        "date": "1982",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Aculops morindae",
        "date": "1989",
        "discoverer": "Ghosh and Chakrabarati"
    },
    {
        "species_name": "Aculops spondiasis",
        "date": "2011",
        "discoverer": "Chakrabarti and Sarkar"
    },
    {
        "species_name": "Aculops privae",
        "date": "1980",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Aculops pretoriensis",
        "date": "1990",
        "discoverer": "Smith Meyer and Uckermann"
    },
    {
        "species_name": "Aculops webpenetrans",
        "date": "1985",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aculops xanthocarpi",
        "date": "1982",
        "discoverer": "Mondal & Chakrabarti"
    },
    {
        "species_name": "Aculus acanthae",
        "date": "1982",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Aculus acutangulae",
        "date": "1984",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aculus atturensis",
        "date": "1980",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Aculus asperus",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Aculus bangalorensis",
        "date": "1984",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aculus colei",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Aculus cassiae",
        "date": "1981",
        "discoverer": "Mondal & Chakrabarti"
    },
    {
        "species_name": "Aculus excoecaria",
        "date": "1982",
        "discoverer": "Mondal and Chakrabarti"
    },
    {
        "species_name": "Aculus ficivagrans",
        "date": "1984",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aculus indicus",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Aculus ichnocarpi",
        "date": "1989",
        "discoverer": "Ghosh and Chakrabarati"
    },
    {
        "species_name": "Aculus kolengii",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Aculus kumari",
        "date": "1982",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aculus leguminae",
        "date": "1982",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aculus leptadeniae",
        "date": "1984",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aculus mackenziei",
        "date": "1944",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Aculus menoni",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Aculus montanae",
        "date": "1984",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aculus moringeae",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Aculus niphlocladae",
        "date": "1966",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Aculus ocimumae",
        "date": "1991",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aculus pittosporae",
        "date": "1982",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aculus pterygospermae",
        "date": "1984",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aculus sarcococcae",
        "date": "1984",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Aculus shoreum",
        "date": "1986",
        "discoverer": "Ghosh, Mondal and Chakrabarti"
    },
    {
        "species_name": "Aculus yelagiriensis",
        "date": "1980",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Anthocoptes adhatodae",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Anthocoptes ayyanari",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Anthocoptes bamboovagrans",
        "date": "1991",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Anthocoptes glycosmis",
        "date": "1981",
        "discoverer": "Mondal & Chakrabarti"
    },
    {
        "species_name": "Anthocoptes pavoniae",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Anthocoptes rutacevagrans",
        "date": "1983",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Anthocoptes tectonae",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Anthocoptes vitexae",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Anthocoptes walayarensis",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Bakeriella ocimis",
        "date": "1982",
        "discoverer": "Chakrabarti & Mondal"
    },
    {
        "species_name": "Neoacaphyllisa alangia",
        "date": "2020",
        "discoverer": "Roy & Chakrabarti"
    },
    {
        "species_name": "Ditrymacus keiferi",
        "date": "1982",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Ditrymacus integrifoliae",
        "date": "1982",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Epiphytimerus palampurensis",
        "date": "1984",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Indotegolophus darjeelingensis",
        "date": "1980",
        "discoverer": "Mondal & Chakrabarti"
    },
    {
        "species_name": "Keiferana neolitseae",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Mesalox odayarae",
        "date": "1980",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Mesalox mutica",
        "date": "2017",
        "discoverer": "Sur and Chakrabarti"
    },
    {
        "species_name": "Metaculus londaensis",
        "date": "1980",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Metaculus foveolatae",
        "date": "1983",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Metaculus mangiferae",
        "date": "1955",
        "discoverer": "Attiah"
    },
    {
        "species_name": "Metaculus sapindiphagus",
        "date": "1982",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Monotrimacus quadrangulari",
        "date": "1982",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Neocalacarus mangiferae",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Neocolopodacus mitragynae",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Neocolopodacus muruganii",
        "date": "1986",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Neodactylus mohanasundarami",
        "date": "1999",
        "discoverer": "Umapathy"
    },
    {
        "species_name": "Neooxycenus dilleniae",
        "date": "2017",
        "discoverer": "Sur, Roy and Chakrabarti"
    },
    {
        "species_name": "Neophantacrus mallotus",
        "date": "1981",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Neomesalox kallarensis",
        "date": "1983",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Neotegonotus fastigatus",
        "date": "1890",
        "discoverer": "Nalepa"
    },
    {
        "species_name": "Neotegonotus indicus",
        "date": "1982",
        "discoverer": "Mondal & Chakrabarti"
    },
    {
        "species_name": "Paraciota tetracanthae",
        "date": "1984",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Paratetra albizziae",
        "date": "1983",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Paratetra elephantae",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Paratetra integrifoliavagrans",
        "date": "1983",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Paratetra murrayae",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Porcupinotus acaciae",
        "date": "1984",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Porcupinotus humpae",
        "date": "1984",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Tegolophus bambusae",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Tegolophus betonicae",
        "date": "1981",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Tegolophus birbhumensis",
        "date": "1989",
        "discoverer": "Chakrabarti and Das"
    },
    {
        "species_name": "Tegolophus calotropi",
        "date": "1979",
        "discoverer": "Chakrabarti & Mondal"
    },
    {
        "species_name": "Tegolophus cordis",
        "date": "1982",
        "discoverer": "Das & Chakrabarti"
    },
    {
        "species_name": "Tegolophus dhodabettaensis",
        "date": "1983",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Tegolophus ficusi",
        "date": "1979",
        "discoverer": "Mondal & Chakrabarti"
    },
    {
        "species_name": "Tegolophus gelonis",
        "date": "1982",
        "discoverer": "Mondal & Chakrabarti"
    },
    {
        "species_name": "Tegolophus gmelinus",
        "date": "1982",
        "discoverer": "Das & Chakrabarti"
    },
    {
        "species_name": "Tegolophus indica",
        "date": "1979",
        "discoverer": "Chakrabarti & Mondal"
    },
    {
        "species_name": "Tegolophus kalyanii",
        "date": "1981",
        "discoverer": "Chakrabarti, Ghosh & MondaI"
    },
    {
        "species_name": "Tegolophus mohanasundarami",
        "date": "1983",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Tegolophus monospermasis",
        "date": "1985",
        "discoverer": "Das and Chakrabarti"
    },
    {
        "species_name": "Tegolophus nerii",
        "date": "1979",
        "discoverer": "Mondal & Chakrabarti"
    },
    {
        "species_name": "Tegolophus perviflorii",
        "date": "2007",
        "discoverer": "Pandit and Chakrabarti"
    },
    {
        "species_name": "Tegolophus spondiallus",
        "date": "1981",
        "discoverer": "Mondal & Chakrabarti"
    },
    {
        "species_name": "Tegolophus securinegavagrans",
        "date": "1985",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Tegolophus vitexis",
        "date": "1981",
        "discoverer": "Mondal & Chakrabarti"
    },
    {
        "species_name": "Tetra aegleis",
        "date": "1984",
        "discoverer": "Ghosh Mondal and Chakrabarti"
    },
    {
        "species_name": "Tetra anisomelae",
        "date": "1984",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Tetra ardesiae",
        "date": "1999",
        "discoverer": "Umapathy"
    },
    {
        "species_name": "Tetra asperae",
        "date": "1999",
        "discoverer": "Umapathy"
    },
    {
        "species_name": "Tetra bauhinae",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Tetra brideliae",
        "date": "",
        "discoverer": "Das and Chakrabarti"
    },
    {
        "species_name": "Tetra buteae",
        "date": "2001",
        "discoverer": "Umapathy"
    },
    {
        "species_name": "Tetra cassiae",
        "date": "1994",
        "discoverer": "Das and Chakrabarti"
    },
    {
        "species_name": "Tetra coimbatorensis",
        "date": "1994",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Tetra lanneansis",
        "date": "1981",
        "discoverer": "Chakrabarti, Ghosh & Mondal"
    },
    {
        "species_name": "Tetra limonis",
        "date": "1984",
        "discoverer": "Ghosh, Mondal and Chakrabarti"
    },
    {
        "species_name": "Tetra petuniae",
        "date": "1988",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Tetra shoreacola",
        "date": "1994",
        "discoverer": "Das and Chakrabarti"
    },
    {
        "species_name": "Tetra sissoae",
        "date": "1988",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Tetra tephrosiae",
        "date": "1983",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Tetra triflorae",
        "date": "1994",
        "discoverer": "Das and Chakrabarti"
    },
    {
        "species_name": "Tetra tyrohylae",
        "date": "1992",
        "discoverer": "Smith Meyer"
    },
    {
        "species_name": "Tetra visci",
        "date": "1992",
        "discoverer": "Smith Meyer"
    },
    {
        "species_name": "Thamnacus acanthae",
        "date": "1999",
        "discoverer": "Umapathy"
    },
    {
        "species_name": "Thamnacus elaegnae",
        "date": "2001",
        "discoverer": "Umapathy"
    },
    {
        "species_name": "Thamnacus euphorbiae",
        "date": "1966",
        "discoverer": "ChannaBasavanna"
    },
    {
        "species_name": "Acarhynchus bamboovagrans",
        "date": "1989",
        "discoverer": "Mohanasundram"
    },
    {
        "species_name": "Amrinella dendrocalami",
        "date": "1993",
        "discoverer": "Chakrabarti"
    },
    {
        "species_name": "Asetadiptacus carmonae",
        "date": "2002",
        "discoverer": "Umapathy and Mohanasundaram"
    },
    {
        "species_name": "Diptacus cephalanthi",
        "date": "1993",
        "discoverer": "Das and Chakrabarti"
    },
    {
        "species_name": "Diptacus duabangiphagus",
        "date": "1993",
        "discoverer": "Das and Chakrabarti"
    },
    {
        "species_name": "Diptilomiopus alagarmalaiensis",
        "date": "1986",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Diptilomiopus alangii",
        "date": "1982",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Diptilomiopus anthocephali",
        "date": "2008",
        "discoverer": "Chakrabarti, Sarkar and Pandit"
    },
    {
        "species_name": "Diptilomiopus artocarpae",
        "date": "1981",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Diptilomiopus assamica",
        "date": "1959",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Diptilomiopus asperis",
        "date": "1989",
        "discoverer": "Ghosh and Chakrabarti"
    },
    {
        "species_name": "Diptilomiopus augustifoliae",
        "date": "2018",
        "discoverer": "Sur, Roy and Chakrabarti"
    },
    {
        "species_name": "Diptilomiopus bengalensis",
        "date": "1979",
        "discoverer": "Chakrabarti and Mondal"
    },
    {
        "species_name": "Diptilomiopus camerae",
        "date": "1981",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Diptilomiopus cocculae",
        "date": "1981",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Diptilomiopus cuminis",
        "date": "1992",
        "discoverer": "Chakrabarti, Ghosh and Das"
    },
    {
        "species_name": "Diptilomiopus ficusis",
        "date": "1983",
        "discoverer": "Chakrabarti and Mondal"
    },
    {
        "species_name": "Diptilomiopus guajavae",
        "date": "1985",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Diptilomiopus holoptelus",
        "date": "1983",
        "discoverer": "Chakrabarti and Mondal"
    },
    {
        "species_name": "Diptilomiopus indicus",
        "date": "1996",
        "discoverer": "Chakrabarti and Pandit"
    },
    {
        "species_name": "Diptilomiopus indogangeticus",
        "date": "2019",
        "discoverer": "Chakrabarti, Sur and Sarkar"
    },
    {
        "species_name": "Diptilomiopus integrifoliae",
        "date": "1981",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Diptilomiopus jevremovici",
        "date": "1960",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Diptilomiopus leeasis",
        "date": "1992",
        "discoverer": "Chakrabarti, Ghosh and Das"
    },
    {
        "species_name": "Diptilomiopus lagerstroemae",
        "date": "2008",
        "discoverer": "Chakrabarti, Pandit and Mondal"
    },
    {
        "species_name": "Diptilomiopus maduraiensis",
        "date": "1986",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Diptilomiopus mohanasundarami",
        "date": "2019",
        "discoverer": "Chakrabarti, Sur and Sarkar"
    },
    {
        "species_name": "Diptilomiopus knorri",
        "date": "1974",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Diptilomiopus thangaveli",
        "date": "1983",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Diptilomiopus trewier",
        "date": "1983",
        "discoverer": "Chakrabarti and Mondal"
    },
    {
        "species_name": "Diptilomiopus ulmivagrans",
        "date": "1984",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Diptilorhynacus sinusetus",
        "date": "1981",
        "discoverer": "Mondal, Ghosh and Chakrabarti"
    },
    {
        "species_name": "Levonga attakattiensis",
        "date": "2002",
        "discoverer": "Umapathy and Mohanasundaram"
    },
    {
        "species_name": "Levonga caseariasis",
        "date": "1996",
        "discoverer": "Chakrabarti and Pandit"
    },
    {
        "species_name": "Levonga combretis",
        "date": "1992",
        "discoverer": "Ghosh and Chakrabarti"
    },
    {
        "species_name": "Neodialox palmyrae",
        "date": "1983",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Neodiptilomiopus vishakantai",
        "date": "1982",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Neorhynacus rajendrani",
        "date": "1981",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Neorhynacus lakoochii",
        "date": "2007",
        "discoverer": "Pandit and Chakrabarti"
    },
    {
        "species_name": "Prodiptilomiopus auriculatae",
        "date": "1999",
        "discoverer": "Umapathy and Mohanasundaram"
    },
    {
        "species_name": "Pseudodiptacus litseae",
        "date": "1992",
        "discoverer": "Chakrabarti, Ghosh and Das"
    },
    {
        "species_name": "Unilox lataguriensis",
        "date": "2019",
        "discoverer": "Roy and Chakrabarti"
    },
    {
        "species_name": "Catarhinus munnarensis",
        "date": "1991",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Catarhinus raii",
        "date": "1984",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Catarhinus spontaneae",
        "date": "1984",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Chakrabartiella ficusis",
        "date": "1992",
        "discoverer": "Chakrabarti, Ghosh and Das"
    },
    {
        "species_name": "Cheiracus sulcatus",
        "date": "1977",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Hyboderus globosus",
        "date": "1981",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Hyborhinus kallarensis",
        "date": "1986",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Neorhynacus bidhanae",
        "date": "2016",
        "discoverer": "Debnath and Karmakar"
    },
    {
        "species_name": "Rhyncaphytoptus ficifoliae",
        "date": "1939",
        "discoverer": "Keifer"
    },
    {
        "species_name": "Rhyncaphytoptus shoreacola",
        "date": "1982",
        "discoverer": "Mondal, Ghosh and Chakrabarti"
    },
    {
        "species_name": "Sakthirhynchus canariae",
        "date": "1999",
        "discoverer": "Umapathy and Mohanasundaram"
    },
    {
        "species_name": "Stenarhynchus aristidus",
        "date": "1983",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Vimola guajavae",
        "date": "2009",
        "discoverer": "Chakrabarti and Pandit"
    },
    {
        "species_name": "Anchiphytoptus gianticus",
        "date": "1981",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Mackiella borasis",
        "date": "1981",
        "discoverer": "Mohanasundaram"
    },
    {
        "species_name": "Hyboderus globulus",
        "date": "1981",
        "discoverer": "Mohansundaram"
    },
    {
        "species_name": "Polyphagotarsonemus latus",
        "date": "1904",
        "discoverer": "Banks"
    },
    {
        "species_name": "Steneotarsonemus bancrofti",
        "date": "1890",
        "discoverer": "Michael"
    },
    {
        "species_name": "Lupotarsonemus randsi",
        "date": "1939",
        "discoverer": "Ewing"
    },
    {
        "species_name": "Tarsonemus krichneri",
        "date": "1876",
        "discoverer": "Kramer"
    },
    {
        "species_name": "Chelacaropsis moorei",
        "date": "1949",
        "discoverer": "Baker"
    },
    {
        "species_name": "Cheletogenes ornatus",
        "date": "1879",
        "discoverer": "Canestrini & Fanzago"
    },
    {
        "species_name": "Cheyletus fortis",
        "date": "1904",
        "discoverer": "Oudemans"
    },
    {
        "species_name": "Cheyletus malaccensis",
        "date": "1903",
        "discoverer": "Oudemans"
    },
    {
        "species_name": "Cheletophyes indiacus",
        "date": "1981",
        "discoverer": "Smiley and Whitaker"
    },
    {
        "species_name": "Cheletophyes deodikari",
        "date": "1989",
        "discoverer": "Putatunda & Kapil"
    },
    {
        "species_name": "Cheletophyes newtoni",
        "date": "1989",
        "discoverer": "Putatunda & Kapil"
    },
    {
        "species_name": "Cheletophyes orientalis",
        "date": "1989",
        "discoverer": "Putatunda & Kapil"
    },
    {
        "species_name": "Cheletophyes ruttneri",
        "date": "1989",
        "discoverer": "Putatunda & Kapil"
    },
    {
        "species_name": "Cheletophyes shendei",
        "date": "1989",
        "discoverer": "Putatunda & Kapil"
    },
    {
        "species_name": "Cheletophyes harnaji",
        "date": "1989",
        "discoverer": "Putatunda&Kapil"
    },
    {
        "species_name": "Cheletophyes haryanaensis",
        "date": "1989",
        "discoverer": "Putatunda & Kapil"
    },
    {
        "species_name": "Cheletophyes eckerti",
        "date": "1970",
        "discoverer": "Summers & Price"
    },
    {
        "species_name": "Agistemus industani",
        "date": "1965",
        "discoverer": "Gonzalez-Rodriguez"
    },
    {
        "species_name": "Agistemus fleschneri",
        "date": "1960",
        "discoverer": "Summers"
    },
    {
        "species_name": "Indostigmaeus rangatensis",
        "date": "1980",
        "discoverer": "Gupta & Ghosh"
    },
    {
        "species_name": "Pronematus elongatus",
        "date": "1968",
        "discoverer": "Baker"
    },
    {
        "species_name": "Pronematus fleschneri",
        "date": "1968",
        "discoverer": "Baker"
    },
    {
        "species_name": "Pronematus sextoni",
        "date": "1968",
        "discoverer": "Baker"
    },
    {
        "species_name": "Parapronematos acaciae",
        "date": "1965",
        "discoverer": "Baker"
    },
    {
        "species_name": "Lorryia africana",
        "date": "1965",
        "discoverer": "Baker"
    },
    {
        "species_name": "Bdellodes (Hoploscirus) affinis",
        "date": "1963",
        "discoverer": "Atyeo"
    },
    {
        "species_name": "Cunaxa anacardae",
        "date": "1992",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Cunaxa bambusae",
        "date": "1980",
        "discoverer": "Gupta & Ghosh"
    },
    {
        "species_name": "Cunaxa capreolus",
        "date": "1889",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Cunaxa cynodonae",
        "date": "1980",
        "discoverer": "Gupta & Ghosh"
    },
    {
        "species_name": "Cunaxa evansi",
        "date": "1992",
        "discoverer": "Smiley"
    },
    {
        "species_name": "Cunaxa mangiferae",
        "date": "1992",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Cunaxa myabunderensis",
        "date": "1980",
        "discoverer": "Gupta & Ghosh"
    },
    {
        "species_name": "Cunaxa setirostris",
        "date": "1804",
        "discoverer": "Hermann"
    },
    {
        "species_name": "Cunaxoides nicobarensis",
        "date": "1980",
        "discoverer": "Gupta & Ghosh"
    },
    {
        "species_name": "Dactyloscirus bengalensis",
        "date": "1992",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Dactyloscirus fuscus",
        "date": "1977",
        "discoverer": "Chaudhri"
    },
    {
        "species_name": "Dactyloscirus machairodus",
        "date": "1922",
        "discoverer": "Oudemans"
    },
    {
        "species_name": "Indocunaxa smileyi",
        "date": "1980",
        "discoverer": "Gupta & Ghosh"
    },
    {
        "species_name": "Neocunaxoides pradhani",
        "date": "1980",
        "discoverer": "Gupta & Ghosh"
    },
    {
        "species_name": "Abrolophus delhiensis",
        "date": "1965",
        "discoverer": "Khot"
    },
    {
        "species_name": "Abrolophus ripicola",
        "date": "1934",
        "discoverer": "Womersley"
    },
    {
        "species_name": "Erythraeus plumosus",
        "date": "1963",
        "discoverer": "Khot"
    },
    {
        "species_name": "Leptus giganticus",
        "date": "1965",
        "discoverer": "Khot"
    },
    {
        "species_name": "Leptus poonaensis",
        "date": "1964",
        "discoverer": "Khot"
    },
    {
        "species_name": "Paraerythraeus serratociliatus",
        "date": "1963",
        "discoverer": "Khot"
    },
    {
        "species_name": "Sphaerolophus delhiensis",
        "date": "1965",
        "discoverer": "Khot"
    },
    {
        "species_name": "Sphaerolophus gigas",
        "date": "1965",
        "discoverer": "Khot"
    },
    {
        "species_name": "Ornithocheyletia hallae",
        "date": "1970",
        "discoverer": "Smiley"
    },
    {
        "species_name": "Syringophilus bipectinatus",
        "date": "1880",
        "discoverer": "Heller"
    },
    {
        "species_name": "Kleemannia bengalensis",
        "date": "1972",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Neocypholaelaps indica",
        "date": "1963",
        "discoverer": "Evans"
    },
    {
        "species_name": "Neocypholaelaps pradhani",
        "date": "1969",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Neocypholaelaps stridulans",
        "date": "1955",
        "discoverer": "Evans"
    },
    {
        "species_name": "Asca pseudospicata",
        "date": "1965",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Arctoseius himalayensis",
        "date": "2001",
        "discoverer": "Bhattacharyya,sanyal & Bhattcharyya"
    },
    {
        "species_name": "Gamasellodes jodhpurensis",
        "date": "2004",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Hoploseius sitalaensis",
        "date": "1977",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Melichares (Melichares) fici",
        "date": "1964",
        "discoverer": "Narayanan & Ghai"
    },
    {
        "species_name": "Proctolaelaps orientalis",
        "date": "1968",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Proctolaelaps sternalis",
        "date": "1972",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Blattisocius incisus",
        "date": "1977",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Lasioseius parberlesei",
        "date": "1968",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Lasioseius prakashii",
        "date": "2004",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Lasioseius reticulatus",
        "date": "1968",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Lasioseius terrestris",
        "date": "1968",
        "discoverer": "Menon & Ghai"
    },
    {
        "species_name": "Lasioseius quadrisetosus",
        "date": "1960",
        "discoverer": "Chant"
    },
    {
        "species_name": "Platyseius indicus",
        "date": "1968",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Schizodiplogynium indicum",
        "date": "1977",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Eviphis convergens",
        "date": "1913",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Eviphis cultratellus",
        "date": "1910",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Eviphis indicus",
        "date": "1971",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Eviphis mullani",
        "date": "1915",
        "discoverer": "Oudemans"
    },
    {
        "species_name": "Eviphis rufus",
        "date": "1915",
        "discoverer": "Oudemans"
    },
    {
        "species_name": "Holostaspella parornata",
        "date": "1972",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Macrocheles hyatti",
        "date": "1964",
        "discoverer": "Krantz & Filipponi"
    },
    {
        "species_name": "Macrocheles indicus",
        "date": "1972",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Macrocheles merdarius",
        "date": "1889",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Macrocheles orientalis",
        "date": "1972",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Gamasiphis arcuatus",
        "date": "1952",
        "discoverer": "Tragardh"
    },
    {
        "species_name": "Gamasiphis bengalensis",
        "date": "1966",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Gamasiphis indicus",
        "date": "1978",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Sessiluncus abalaae",
        "date": "1991",
        "discoverer": "Datta & Bhattacharjee"
    },
    {
        "species_name": "Sessiluncus bengalensis",
        "date": "1977",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Sessiluncus calcuttaensis",
        "date": "1977",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Sessiluncus femoralis",
        "date": "1977",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Sessiluncus indicus",
        "date": "1977",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Sessiluncus leei",
        "date": "1991",
        "discoverer": "Datta & Bhattacharjee"
    },
    {
        "species_name": "Sessiluncus oculatus",
        "date": "1935",
        "discoverer": "Vitzthum"
    },
    {
        "species_name": "Pachylaelaps dorsalis",
        "date": "1970",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Pachylaelaps femoralis",
        "date": "1970",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Pachylaelaps setosus",
        "date": "1970",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Gamasholaspis browningi",
        "date": "1960",
        "discoverer": "Bregetova & Koroleva"
    },
    {
        "species_name": "Gamasodes assamensis",
        "date": "1971",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Parasitus consanguineus",
        "date": "1905",
        "discoverer": "Oudemans and Voigts"
    },
    {
        "species_name": "Pergamasus longicornis",
        "date": "1906",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Pergamasus (Pergamasus) ranikhetensis",
        "date": "2001",
        "discoverer": "Bhattachayya"
    },
    {
        "species_name": "Podocinum bengalensis",
        "date": "1968",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Amblyseiulella cancellatus",
        "date": "2022",
        "discoverer": "Kar & Karmakar"
    },
    {
        "species_name": "Amblyseiulella gangtokiensis",
        "date": "2022",
        "discoverer": "Kar & Karmakar"
    },
    {
        "species_name": "Amblyseius azaliae",
        "date": "2021",
        "discoverer": "Kar & Karmakar"
    },
    {
        "species_name": "Amblyseius bengalensis",
        "date": "2017",
        "discoverer": "Karmakar, Bhowmik and Sherpa"
    },
    {
        "species_name": "Amblyseius brachycalyx",
        "date": "2017",
        "discoverer": "Karmakar, Bhowmik and Sherpa"
    },
    {
        "species_name": "Amblyseius conulus",
        "date": "2017",
        "discoverer": "Karmakar, Bhowmik and Sherpa"
    },
    {
        "species_name": "Amblyseius cucurbitae",
        "date": "1985",
        "discoverer": "Rather"
    },
    {
        "species_name": "Amblyseius dahliae",
        "date": "2017",
        "discoverer": "Karmakar, Bhowmik and Sherpa"
    },
    {
        "species_name": "Amblyseius herbicolus",
        "date": "1959",
        "discoverer": "Chant"
    },
    {
        "species_name": "Amblyseius impressus",
        "date": "1973",
        "discoverer": "Denmark & Muma"
    },
    {
        "species_name": "Amblyseius indirae",
        "date": "1985",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius lanceae",
        "date": "2022",
        "discoverer": "Kar & Karmakar"
    },
    {
        "species_name": "Amblyseius meghalayensis",
        "date": "2021",
        "discoverer": "Kar & Karmakar"
    },
    {
        "species_name": "Amblyseius parbatabasii",
        "date": "2017",
        "discoverer": "Karmakar, Bhowmik and Sherpa"
    },
    {
        "species_name": "Amblyseius rishyapensis",
        "date": "2021",
        "discoverer": "Molla & Karmakar"
    },
    {
        "species_name": "Amblyseius tibouchina",
        "date": "2021",
        "discoverer": "Molla & Karmakar"
    },
    {
        "species_name": "Amblyseius (Amblyseius) aerialis",
        "date": "1955",
        "discoverer": "Muma"
    },
    {
        "species_name": "Amblyseius (Amblyseius) adhatodae",
        "date": "1967",
        "discoverer": "Muma"
    },
    {
        "species_name": "Amblyseius (Amblyseius) channabasavanni",
        "date": "1978",
        "discoverer": "Gupta & Daniel"
    },
    {
        "species_name": "Amblyseius (Amblyseius) deleoni",
        "date": "1961",
        "discoverer": "Muma & Denmark"
    },
    {
        "species_name": "Amblyseius (Amblyseius) excelsus",
        "date": "1979",
        "discoverer": "Chaudhri"
    },
    {
        "species_name": "Amblyseius (Amblyseius) hapoliensis",
        "date": "1986",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (Amblyseius) ipomoeae",
        "date": "1967",
        "discoverer": "Ghai & Menon"
    },
    {
        "species_name": "Amblyseius (Amblyseius) kulini",
        "date": "1978",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (Amblyseius) largoensis",
        "date": "1955",
        "discoverer": "Muma"
    },
    {
        "species_name": "Amblyseius (Amblyseius) mcmurtryi",
        "date": "1967",
        "discoverer": "Muma"
    },
    {
        "species_name": "Amblyseius (Amblyseius) muraleedharani",
        "date": "1986",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (Amblyseius) neorykei",
        "date": "1977",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (Amblyseius) orientalis",
        "date": "1959",
        "discoverer": "Ehara"
    },
    {
        "species_name": "Amblyseius (Amblyseius) paraaerialis",
        "date": "1967",
        "discoverer": "Muma"
    },
    {
        "species_name": "Amblyseius (Amblyseius) raoiellus",
        "date": "1989",
        "discoverer": "Denmark & Muma"
    },
    {
        "species_name": "Amblyseius (Amblyseius) rhabdus",
        "date": "1965",
        "discoverer": "Denmark"
    },
    {
        "species_name": "Amblyseius (Amblyseius) shoreae",
        "date": "1977",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (Asperoseius) hyauliangensis",
        "date": "1986",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (Amblyseius) heveae",
        "date": "1930",
        "discoverer": "Oudemans"
    },
    {
        "species_name": "Amblyseius (Amblyseius) nucifera",
        "date": "1979",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (Euseius) ahaioensis",
        "date": "1992",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (E.) alstoniae",
        "date": "1975",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (E.) bambusae",
        "date": "1967",
        "discoverer": "Ghai & Menon"
    },
    {
        "species_name": "Amblyseius (E.) coccineae",
        "date": "1975",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (E.) coccosocius",
        "date": "1967",
        "discoverer": "Ghai & Menon"
    },
    {
        "species_name": "Amblyseius (E.) concordis",
        "date": "1959",
        "discoverer": "Chant"
    },
    {
        "species_name": "Amblyseius (E.) delhiensis",
        "date": "1960",
        "discoverer": "Narayanan & Kaur"
    },
    {
        "species_name": "Amblyseius (E.) eucalypti",
        "date": "1967",
        "discoverer": "Ghai & Menon"
    },
    {
        "species_name": "Amblyseius (E.) finlandicus",
        "date": "1915",
        "discoverer": "Oudemans"
    },
    {
        "species_name": "Amblyseius (E.) insanus",
        "date": "1969",
        "discoverer": "Khan & Chaudhri"
    },
    {
        "species_name": "Amblyseius (E.) kodaikanalensis",
        "date": "1978",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (E.) neococcineae",
        "date": "1978",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (E.) ovalis",
        "date": "1953",
        "discoverer": "Evans"
    },
    {
        "species_name": "Amblyseius (E.) pruni",
        "date": "1975",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (E.) rhododendronis",
        "date": "1970",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (E.) sacchari",
        "date": "1967",
        "discoverer": "Ghai & Menon"
    },
    {
        "species_name": "Amblyseius (E.) scutalis",
        "date": "1958",
        "discoverer": "Athias-Henriot"
    },
    {
        "species_name": "Amblyseius (E.) vignus",
        "date": "1983",
        "discoverer": "Rishi & Rather"
    },
    {
        "species_name": "Amblyseius (Neoseiulus) aceriae",
        "date": "1975",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (N.) assamensis",
        "date": "1960",
        "discoverer": "Chant"
    },
    {
        "species_name": "Amblyseius (N.) baraki",
        "date": "1966",
        "discoverer": "Athias-Henriot"
    },
    {
        "species_name": "Amblyseius (N.) cucumeris",
        "date": "1930",
        "discoverer": "Oudemans"
    },
    {
        "species_name": "Amblyseius (N.) cynodonae",
        "date": "1977",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (N.) dhooriai",
        "date": "1977",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (N.) fallacis",
        "date": "1948",
        "discoverer": "Garman"
    },
    {
        "species_name": "Amblyseius (N.) fraterculus",
        "date": "1917",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Amblyseius (N.) imbricatus",
        "date": "1966",
        "discoverer": "Corpuz & Rimando"
    },
    {
        "species_name": "Amblyseius (N.) indicus",
        "date": "1960",
        "discoverer": "Narayanan & Kaur"
    },
    {
        "species_name": "Amblyseius (N.) longispinosus",
        "date": "1952",
        "discoverer": "Evans"
    },
    {
        "species_name": "Amblyseius (N.) oahuensis",
        "date": "1968",
        "discoverer": "Prasad"
    },
    {
        "species_name": "Amblyseius (N.) paspalivorus",
        "date": "1957",
        "discoverer": "Deleon"
    },
    {
        "species_name": "Amblyseius (N.) rangatensis",
        "date": "1977",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (N.) reticulatus",
        "date": "1930",
        "discoverer": "Oudemans"
    },
    {
        "species_name": "Amblyseius (Paraphytoseius) multidentatus",
        "date": "1961",
        "discoverer": "Swirski & Shechter"
    },
    {
        "species_name": "Amblyseius (P.) scleroticus",
        "date": "1981",
        "discoverer": "Gupta & Ray"
    },
    {
        "species_name": "Amblyseius (Phytoscutella) salebrosus",
        "date": "1960",
        "discoverer": "Chant"
    },
    {
        "species_name": "Amblyseius (Proprioseius) kumaonensis",
        "date": "1982",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (Proprioseiopsis) arunachalensis",
        "date": "1992",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (P.) peltatus",
        "date": "1968",
        "discoverer": "Van der Merwe"
    },
    {
        "species_name": "Amblyseius (P.) synachattiensis",
        "date": "1985",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (Typhlodromalus) chikmagalurensis",
        "date": "1986",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (T.) chitradurgae",
        "date": "1986",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (T.) eucalypticus",
        "date": "1978",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (T.) ficusi",
        "date": "1986",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (T.) havu",
        "date": "1962",
        "discoverer": "Pritchard & Baker"
    },
    {
        "species_name": "Amblyseius (T.) jarooa",
        "date": "1977",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (T.) kalimpongensis",
        "date": "1970",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (T.) lablabi",
        "date": "1967",
        "discoverer": "Ghai & Menon"
    },
    {
        "species_name": "Amblyseius (T.) manipurensis",
        "date": "1978",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (T.) rosica",
        "date": "1992",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (T.) sorghumae",
        "date": "1977",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (T.) swaga",
        "date": "1962",
        "discoverer": "Pritchard & Baker"
    },
    {
        "species_name": "Amblyseius (Typhlodromips) arecae",
        "date": "1977",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (T.) bangalorensis",
        "date": "1983",
        "discoverer": "Karg"
    },
    {
        "species_name": "Amblyseius (T.) crotalariae",
        "date": "1977",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (T.) eujeniae",
        "date": "1977",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (T.) guajavae",
        "date": "1978",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (T.) mangiferae",
        "date": "1967",
        "discoverer": "Ghai & Menon"
    },
    {
        "species_name": "Amblyseius (T.) meghalayensis",
        "date": "1978",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (T.) neocrotalariae",
        "date": "1978",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (T.) neoghanii",
        "date": "1986",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (T.) officinaria",
        "date": "1957",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (T.) polyantheae",
        "date": "1975",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (T.) potentillae",
        "date": "1958",
        "discoverer": "Garman"
    },
    {
        "species_name": "Amblyseius (T.) sapienticola",
        "date": "1977",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (T.) sijiensis",
        "date": "1986",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (T.) suknaensis",
        "date": "1970",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (T.) syzygii",
        "date": "1975",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Amblyseius (T.) tetranychivoros",
        "date": "1978",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Asperoseius jujubae",
        "date": "2018",
        "discoverer": "Karmakar and Bhowmik"
    },
    {
        "species_name": "Asperoseius latericulus",
        "date": "2018",
        "discoverer": "Karmakar and Bhowmik"
    },
    {
        "species_name": "Euseius astrics",
        "date": "2018",
        "discoverer": "Karmakar and Bhowmik"
    },
    {
        "species_name": "Euseius chittooriensis",
        "date": "2022",
        "discoverer": "Kumar, Molla, Karmakar & Demite"
    },
    {
        "species_name": "Euseius curcasae",
        "date": "2018",
        "discoverer": "Santhosh, Sadanandan and Rahul"
    },
    {
        "species_name": "Euseius dwakiensis",
        "date": "2021",
        "discoverer": "Kar & Karmakar"
    },
    {
        "species_name": "Euseius fascae",
        "date": "2021",
        "discoverer": "Kar & Karmakar"
    },
    {
        "species_name": "Euseius karpasae",
        "date": "2022",
        "discoverer": "Kumar, Molla, Karmakar & Demite"
    },
    {
        "species_name": "Euseius neoalstoniae",
        "date": "2022",
        "discoverer": "Kumar, Molla, Karmakar & Demite"
    },
    {
        "species_name": "Euseius pariyarensis",
        "date": "2018",
        "discoverer": "Santhosh, Sadanandan and Rahul"
    },
    {
        "species_name": "Euseius spontaneum",
        "date": "2022",
        "discoverer": "Kar & Karmakar"
    },
    {
        "species_name": "Euseius sundarbanensis",
        "date": "2018",
        "discoverer": "Karmakar and Bhowmik"
    },
    {
        "species_name": "Euseius tripuraensis",
        "date": "2022",
        "discoverer": "Kar & Karmakar"
    },
    {
        "species_name": "Euseius tripurii",
        "date": "2022",
        "discoverer": "Kar & Karmakar"
    },
    {
        "species_name": "Euseius tubuliferus",
        "date": "2022",
        "discoverer": "Kar & Karmakar"
    },
    {
        "species_name": "Garhwalicus himalayensis",
        "date": "1981",
        "discoverer": "Gupta & Ray"
    },
    {
        "species_name": "Indoseiulus eharai",
        "date": "1986",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Indoseiulus ghaiae",
        "date": "1993",
        "discoverer": "Denmark & Kolodochka"
    },
    {
        "species_name": "Indoseiulus ricini",
        "date": "1969",
        "discoverer": "Ghai & Menon"
    },
    {
        "species_name": "Iphiseius andamanicus",
        "date": "1980",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Iphiseius bakeri",
        "date": "1980",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Iphiseius hapoli",
        "date": "1986",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Okiseius himalayana",
        "date": "1986",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Okiseius jainticus",
        "date": "2021",
        "discoverer": "Kar & Karmakar"
    },
    {
        "species_name": "Okiseius pahari",
        "date": "2022",
        "discoverer": "Kar & Karmakar"
    },
    {
        "species_name": "Okiseius ramdhuracus",
        "date": "2021",
        "discoverer": "Molla & Karmakar"
    },
    {
        "species_name": "Okiseius roseus",
        "date": "2021",
        "discoverer": "Molla & Karmakar"
    },
    {
        "species_name": "Okiseius sikkimensis",
        "date": "1986",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Okiseius unisetatus",
        "date": "2021",
        "discoverer": "Kar & Karmakar"
    },
    {
        "species_name": "Okiseius yazuliensis",
        "date": "1986",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Paraamblyseius formosanus",
        "date": "1970",
        "discoverer": "Ehara"
    },
    {
        "species_name": "Paraamblyseius fragariae",
        "date": "1980",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Paraamblyseius mumai",
        "date": "1980",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Paraamblyseius ranipoolensis",
        "date": "2022",
        "discoverer": "Kar & Karmakar"
    },
    {
        "species_name": "Paraphytoseius bhadrakaliensis",
        "date": "1969",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Paraphytoseius orientalis",
        "date": "1960",
        "discoverer": "Narayanan, Kaur & Ghai"
    },
    {
        "species_name": "Platyseiella mumai",
        "date": "1981",
        "discoverer": "Ray & Gupta"
    },
    {
        "species_name": "Phytoseiulus persimilis",
        "date": "1957",
        "discoverer": "Athias-Henriot"
    },
    {
        "species_name": "Phytoseius aonlae",
        "date": "2021",
        "discoverer": "Kar & Karmakar"
    },
    {
        "species_name": "Phytoseius baramuracus",
        "date": "2022",
        "discoverer": "Kar & Karmakar"
    },
    {
        "species_name": "Phytoseius birbikrami",
        "date": "2022",
        "discoverer": "Kar & Karmakar"
    },
    {
        "species_name": "Phytoseius brevicrinis",
        "date": "1961",
        "discoverer": "Swirski & Shechter"
    },
    {
        "species_name": "Phytoseius coheni",
        "date": "1961",
        "discoverer": "Swirski & Shechter"
    },
    {
        "species_name": "Phytoseius clavus",
        "date": "2021",
        "discoverer": "Kar &Karmakar"
    },
    {
        "species_name": "Phytoseius domesticus",
        "date": "1985",
        "discoverer": "Rather"
    },
    {
        "species_name": "Phytoseius dumurae",
        "date": "2022",
        "discoverer": "Karmakar & Molla"
    },
    {
        "species_name": "Phytoseius ferrum",
        "date": "2022",
        "discoverer": "Kar & Karmakar"
    },
    {
        "species_name": "Phytoseius indicus",
        "date": "1968",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Phytoseius khowaiensis",
        "date": "2022",
        "discoverer": "Kar & Karmakar"
    },
    {
        "species_name": "Phytoseius maldahaensis",
        "date": "1992",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Phytoseius mauritiana",
        "date": "2021",
        "discoverer": "Bhowmik & Karmakar"
    },
    {
        "species_name": "Phytoseius namdaphaensis",
        "date": "1986",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Phytoseius namkhanaensis",
        "date": "2018",
        "discoverer": "Karmakar and Bhowmik"
    },
    {
        "species_name": "Phytoseius neoferox",
        "date": "1977",
        "discoverer": "Ehara & Bhandhufalck"
    },
    {
        "species_name": "Phytoseius nipponicus",
        "date": "1962",
        "discoverer": "Ehara"
    },
    {
        "species_name": "Phytoseius (Pennaseius) kapuri",
        "date": "1969",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Phytoseius (Phytoseius) minutus",
        "date": "1960",
        "discoverer": "Narayanan, Kaur & Ghai"
    },
    {
        "species_name": "Phytoseius (Phytoseius) bandipurensis",
        "date": "1980",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Phytoseius (Phytoseius) corniger",
        "date": "1959",
        "discoverer": "Wainstein"
    },
    {
        "species_name": "Phytoseius (Phytoseius) crinitus",
        "date": "1961",
        "discoverer": "Swirski &. Shechter"
    },
    {
        "species_name": "Phytoseius (Phytoseius) intermedius",
        "date": "1962",
        "discoverer": "Evans & Macfarlane"
    },
    {
        "species_name": "Phytoseius (Phytoseius) jaunpurensis",
        "date": "1982",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Phytoseius (Phytoseius) jujuba",
        "date": "1977",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Phytoseius (Phytoseius) macropilis",
        "date": "1909",
        "discoverer": "Banks"
    },
    {
        "species_name": "Phytoseius (Phytoseius) macrosetosus",
        "date": "1977",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Phytoseius (Phytoseius) meyerae",
        "date": "1977",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Phytoseius (Phytoseius) mixtus",
        "date": "1973",
        "discoverer": "Chaudhri"
    },
    {
        "species_name": "Phytoseius (Phytoseius) mizoramensis",
        "date": "2003",
        "discoverer": "Gupta & Chatterjee"
    },
    {
        "species_name": "Phytoseius (Phytoseius) neglecta",
        "date": "1969",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Phytoseius (Phytoseius) neocorniger",
        "date": "1977",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Phytoseius (Phytoseius) punjabensis",
        "date": "1977",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Phytoseius (Phytoseius) rachelae",
        "date": "1961",
        "discoverer": "Swirski & Shechter"
    },
    {
        "species_name": "Phytoseius (Phytoseius) rugosus",
        "date": "1966",
        "discoverer": "Denmark"
    },
    {
        "species_name": "Phytoseius (Phytoseius) roseus",
        "date": "1969",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Phytoseius (Phytoseius) swirskii",
        "date": "1980",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Phytoseius (Phytoseius) wainsteini",
        "date": "1981",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Phytoseius (Phytoseius) woodburyi",
        "date": "1965",
        "discoverer": "DeLeon"
    },
    {
        "species_name": "Proprioseiopsis amari",
        "date": "2021",
        "discoverer": "Bhowmik & Karmakar"
    },
    {
        "species_name": "Scapulaseius moraesi",
        "date": "2018",
        "discoverer": "Karmakar and Bhowmik"
    },
    {
        "species_name": "Typhlodromus arunachalensis",
        "date": "1986",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Typhlodromus dalii",
        "date": "1984",
        "discoverer": "Rather"
    },
    {
        "species_name": "Typhlodromus meerutensis",
        "date": "1969",
        "discoverer": "Ghai & Menon"
    },
    {
        "species_name": "Typhlodromus kashmiricus",
        "date": "1981",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Typhlodromus (Amblydromella) bakeri",
        "date": "1948",
        "discoverer": "Garman"
    },
    {
        "species_name": "Typhlodromus (A.) bambusicolus",
        "date": "1977",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Typhlodromus (A.) chrysanthemi",
        "date": "1977",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Typhlodromus (A.) darjeelingensis",
        "date": "1986",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Typhlodromus (A.) denmarki",
        "date": "1984",
        "discoverer": "Rather"
    },
    {
        "species_name": "Typhlodromus (A.) divergentis",
        "date": "1974",
        "discoverer": "Chaudhri, Akbar & Rasaol"
    },
    {
        "species_name": "Typhlodromus (A.) eharai",
        "date": "1980",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Typhlodromus (A.) fleschneri",
        "date": "1960",
        "discoverer": "Chant"
    },
    {
        "species_name": "Typhlodromus (A.) gopali",
        "date": "1969",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Typhlodromus (A.) himalayensis",
        "date": "1981",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Typhlodromus (A.) homalii",
        "date": "1970",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Typhlodromus (A.) kodaikanalensis",
        "date": "1978",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Typhlodromus (A.) mori",
        "date": "1981",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Typhlodromus (A.) nilgiriensis",
        "date": "1986",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Typhlodromus (A.) persicus",
        "date": "1992",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Typhlodromus (A.) rhenanus",
        "date": "1905",
        "discoverer": "Oudemans"
    },
    {
        "species_name": "Typhlodromus (A.) rhododendronis",
        "date": "1978",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Typhlodromus (A.) sonprayagensis",
        "date": "1985",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Typhlodromus (A.) tarbateijamae",
        "date": "1982",
        "discoverer": "Denmark & Daneshvar"
    },
    {
        "species_name": "Typhlodromus (A.) umbratus",
        "date": "1974",
        "discoverer": "Chaudhri, Akbar & Rasool"
    },
    {
        "species_name": "Typhlodromus (A.) vinifera",
        "date": "1987",
        "discoverer": "Rather"
    },
    {
        "species_name": "Typhlodromus (A.) zafari",
        "date": "1965",
        "discoverer": "Chaudhri"
    },
    {
        "species_name": "Typhlodromus (Anthoseius) adhatoda",
        "date": "2021",
        "discoverer": "Karmakar, Molla, Kar & Bala"
    },
    {
        "species_name": "Typhlodromus (A.) barapanicus",
        "date": "2021",
        "discoverer": "Kar & Karmakar"
    },
    {
        "species_name": "Typhlodromus (A.) bengalensis",
        "date": "2021",
        "discoverer": "Karmakar, Molla, Kar & Bala"
    },
    {
        "species_name": "Typhlodromus (A.) bolpurensis",
        "date": "2021",
        "discoverer": "Bhowmik & Karmakar"
    },
    {
        "species_name": "Typhlodromus (A.) bulbosis",
        "date": "2021",
        "discoverer": "Karmakar, Molla, Kar & Bala"
    },
    {
        "species_name": "Typhlodromus (A.) campana",
        "date": "2021",
        "discoverer": "Kar & Karmakar"
    },
    {
        "species_name": "Typhlodromus (A.) carambolae",
        "date": "2018",
        "discoverer": "Karmakar and Bhowmik"
    },
    {
        "species_name": "Typhlodromus (A.) cherrapunjiensis",
        "date": "2021",
        "discoverer": "Kar & Karmakar"
    },
    {
        "species_name": "Typhlodromus (A.) gilbertoi",
        "date": "2022",
        "discoverer": "Kumar, Molla, Karmakar & Demite"
    },
    {
        "species_name": "Typhlodromus (A.) hasnuhanae",
        "date": "2022",
        "discoverer": "Karmakar & Molla"
    },
    {
        "species_name": "Typhlodromus (A.) heliotropium",
        "date": "2018",
        "discoverer": "Karmakar and Bhowmik"
    },
    {
        "species_name": "Typhlodromus (A.) himaliniae",
        "date": "2022",
        "discoverer": "Kar & Karmakar"
    },
    {
        "species_name": "Typhlodromus (A.) kanchanjanghai",
        "date": "2022",
        "discoverer": "Kar & Karmakar"
    },
    {
        "species_name": "Typhlodromus (A.) majumderi",
        "date": "1986",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Typhlodromus (A.) ramdhuraensis",
        "date": "2022",
        "discoverer": "Karmakar & Molla"
    },
    {
        "species_name": "Typhlodromus (A.) sagaricus",
        "date": "2021",
        "discoverer": "Karmakar, Molla, Kar & Bala"
    },
    {
        "species_name": "Typhlodromus (A.) sonajhuriae",
        "date": "2022",
        "discoverer": "Kar & Karmakar"
    },
    {
        "species_name": "Typhlodromus (A.) theae",
        "date": "2022",
        "discoverer": "Karmakar & Molla"
    },
    {
        "species_name": "Typhlodromus (Brethria) confusus",
        "date": "1960",
        "discoverer": "Narayanan, Kaur & Ghai"
    },
    {
        "species_name": "Typhlodromus (B.) roshanlali",
        "date": "1964",
        "discoverer": "Narayanan & Ghai"
    },
    {
        "species_name": "Typhlodromus (Clavidromus) neotransvaalensis",
        "date": "1978",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Typhlodromus (Orientiseius) channabasavanni",
        "date": "1978",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Typhlodromus (O.) hadii",
        "date": "1965",
        "discoverer": "Chaudhri"
    },
    {
        "species_name": "Typhlodromus (O.) manipurensis",
        "date": "1977",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Typhlodromus (O.) orissaensis",
        "date": "1977",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Typhlodromus (O.) pruni",
        "date": "1970",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Typhlodromus (O.) rickeri",
        "date": "1960",
        "discoverer": "Chant"
    },
    {
        "species_name": "Typhlodromus (Paraseiulus) neosoleiger",
        "date": "1981",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Typhlodromus (P.) kuzini",
        "date": "1962",
        "discoverer": "Wainstein"
    },
    {
        "species_name": "Typhlodromus (Typhlodromus) celtis",
        "date": "1996",
        "discoverer": "Denmark & Rather"
    },
    {
        "species_name": "Typhlodromus (Typhlodromus) communis",
        "date": "1982",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Typhlodromus (Typhlodromus) garhwalicus",
        "date": "1982",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Typhlodromus (Typhlodromus) neorhenanus",
        "date": "1977",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Typhlodromus (Typhlodromus) nesbitti",
        "date": "1954",
        "discoverer": "Womersley"
    },
    {
        "species_name": "Typhlodromus (Typhlodromus) sijiensis",
        "date": "1986",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Typhlodromus (Typhlodromus) transitans",
        "date": "1985",
        "discoverer": "Gupta"
    },
    {
        "species_name": "Typhlodromips cinchonai",
        "date": "2021",
        "discoverer": "Molla & Karmakar"
    },
    {
        "species_name": "Typhlodromips jhilimiliensis",
        "date": "2021",
        "discoverer": "Bhowmik & Karmakar"
    },
    {
        "species_name": "Typhlodromips neosyzygii",
        "date": "2021",
        "discoverer": "Bhowmik & Karmakar"
    },
    {
        "species_name": "Uroactinia anchor",
        "date": "1902",
        "discoverer": "Trouessart"
    },
    {
        "species_name": "Uroobovella cylindrica",
        "date": "1913",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Uroobovella villosella",
        "date": "1913",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Euvarroa sinhai",
        "date": "1974",
        "discoverer": "Delfinado and Baker"
    },
    {
        "species_name": "Varroa jacobsoni",
        "date": "1904",
        "discoverer": "Oudemans"
    },
    {
        "species_name": "Dermatophagoides farinae",
        "date": "1961",
        "discoverer": "A.M.Hughes"
    },
    {
        "species_name": "Dermatophagoides pteronyssinus",
        "date": "1897",
        "discoverer": "Trouessart"
    },
    {
        "species_name": "Euroglyphus maynei",
        "date": "1950",
        "discoverer": "Cooreman"
    },
    {
        "species_name": "Hirstia domicola",
        "date": "1974",
        "discoverer": "Fain, Oshima & Bronswijk"
    },
    {
        "species_name": "Malayoglyphus intermedius",
        "date": "1969",
        "discoverer": "Fain, Cunnington & Spieksma"
    },
    {
        "species_name": "Kuzinia evae",
        "date": "1984",
        "discoverer": "Putatunda, Aggarwal & Kapil"
    },
    {
        "species_name": "Rhizoglyphus echinopus",
        "date": "1968",
        "discoverer": "Fumouse & Robin"
    },
    {
        "species_name": "Rhizoglyphus robini",
        "date": "1869",
        "discoverer": "Claparede"
    },
    {
        "species_name": "Tyrophagus brevicrinatus",
        "date": "1959",
        "discoverer": "Robertson"
    },
    {
        "species_name": "Tyrophagus longior",
        "date": "1844",
        "discoverer": "Gervais"
    },
    {
        "species_name": "Tyrophagus putrescentiae",
        "date": "1781",
        "discoverer": "Schrank"
    },
    {
        "species_name": "Tyrophagus tropicus",
        "date": "1959",
        "discoverer": "Robertson"
    },
    {
        "species_name": "Acarus siro",
        "date": "1758",
        "discoverer": "Linnaeus"
    },
    {
        "species_name": "Suidasia nesbitti",
        "date": "1948",
        "discoverer": "Hughes"
    },
    {
        "species_name": "Suidasia medanensis",
        "date": "1924",
        "discoverer": "Oudemans"
    },
    {
        "species_name": "Carpoglyphus lactis",
        "date": "1758",
        "discoverer": "Linnaeus"
    },
    {
        "species_name": "Chortoglyphus arcuatus",
        "date": "1879",
        "discoverer": "Troupeau"
    },
    {
        "species_name": "Glycyphagus bicaudatus",
        "date": "1976",
        "discoverer": "Hughes"
    },
    {
        "species_name": "Glycyphagus domesticus",
        "date": "1778",
        "discoverer": "De Geer"
    },
    {
        "species_name": "Blomia tropicalis",
        "date": "1973",
        "discoverer": "Bronswijk, Cook and Oshima"
    },
    {
        "species_name": "Blomia freemani",
        "date": "1976",
        "discoverer": "Hughes"
    },
    {
        "species_name": "Calvolia summersi",
        "date": "1970",
        "discoverer": "Mostafa"
    },
    {
        "species_name": "Sennertia hipposiderus",
        "date": "1902",
        "discoverer": "Oudemans"
    },
    {
        "species_name": "Sennertia robusta",
        "date": "2001",
        "discoverer": "Delfinado and Baker, 1976 (=Sennertia carpenter Ramaraju and Mohanasundaram"
    },
    {
        "species_name": "Sennertia delfinadoae",
        "date": "2001",
        "discoverer": "Fain, 1981(= Sennertia bakeri Ramaraju and Mohanasundaram"
    },
    {
        "species_name": "Sennertia horrida",
        "date": "1912",
        "discoverer": "Vitzthum"
    },
    {
        "species_name": "Sennertia leucothorae",
        "date": "2001",
        "discoverer": "Ramaraju & Mohanasundaram"
    },
    {
        "species_name": "Sennertia punctatus",
        "date": "2013",
        "discoverer": "Sarangi, Gupta & Saha"
    },
    {
        "species_name": "Sennertia xylocopi",
        "date": "2013",
        "discoverer": "Sarangi, Gupta & Saha"
    },
    {
        "species_name": "Sarcoptes scabiei",
        "date": "1778",
        "discoverer": "De Geer"
    },
    {
        "species_name": "Leptosphyra antarctica",
        "date": "1952",
        "discoverer": "Gaud"
    },
    {
        "species_name": "Leptosphyra tridactyla",
        "date": "1959",
        "discoverer": "Gaud & Mouchet"
    },
    {
        "species_name": "Leptosphyra velata",
        "date": "1877",
        "discoverer": "Mergnin"
    },
    {
        "species_name": "Diplaegidia columbae",
        "date": "1869",
        "discoverer": "Buchholz"
    },
    {
        "species_name": "Megninia cubitalis",
        "date": "1877",
        "discoverer": "Megnin"
    },
    {
        "species_name": "Megninia ginglymura",
        "date": "1877",
        "discoverer": "Megnin"
    },
    {
        "species_name": "Dermoglyphus columbae",
        "date": "1941",
        "discoverer": "Sugimoto"
    },
    {
        "species_name": "Dermoglyphus elongatus",
        "date": "1877",
        "discoverer": "Megnin"
    },
    {
        "species_name": "Pterolichus obtusus",
        "date": "1868",
        "discoverer": "Robin"
    },
    {
        "species_name": "Knemidokoptes mutans",
        "date": "1859",
        "discoverer": "Robin & Linquetin"
    },
    {
        "species_name": "Bongotarsonemus bicornus",
        "date": "2021",
        "discoverer": "Mondal & Karmakar"
    },
    {
        "species_name": "Bongotarsonemus unicornus",
        "date": "2021",
        "discoverer": "Mondal & Karmakar"
    },
    {
        "species_name": "Tarsonemus kanthali",
        "date": "2021",
        "discoverer": "Karmakar & Mondal"
    },
    {
        "species_name": "Tarsonemus kukri",
        "date": "2021",
        "discoverer": "Karmakar & Mondal"
    },
    {
        "species_name": "Tarsonemus mondouriensis",
        "date": "2021",
        "discoverer": "Karmakar & Ganguly"
    },
    {
        "species_name": "Tarsonemus narkelae",
        "date": "2021",
        "discoverer": "Karmakar & Mondal"
    },
    {
        "species_name": "Metatarsonemus badurkani",
        "date": "2021",
        "discoverer": "Karmakar & Mondal"
    },
    {
        "species_name": "Metatarsonemus connexus",
        "date": "2021",
        "discoverer": "Karmakar & Mondal"
    },
    {
        "species_name": "Metatarsonemus diplojuga",
        "date": "2021",
        "discoverer": "Karmakar, Ganguly & Mondal"
    },
    {
        "species_name": "Metatarsonemus infundibulum",
        "date": "2021",
        "discoverer": "Karmakar & Mondal"
    },
    {
        "species_name": "Metatarsonemus shirishi",
        "date": "2021",
        "discoverer": "Karmakar & Mondal"
    },
    {
        "species_name": "Steneotarsonemus amlisoae",
        "date": "2021",
        "discoverer": "Ganguly, Mondal & Karmakar"
    },
    {
        "species_name": "Steneotarsonemus (Steneotarsonemoides) indianensis",
        "date": "2021",
        "discoverer": "Karmakar & Mondal"
    },
    {
        "species_name": "Athyreacarus indicus",
        "date": "2020",
        "discoverer": "Khaustov & Frolov"
    },
    {
        "species_name": "Bharatavolzia musicola",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Bharatavolzia pallida",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Hydrovolzia infringata",
        "date": "1928",
        "discoverer": "Walter"
    },
    {
        "species_name": "Limnochares crinita",
        "date": "1898",
        "discoverer": "Koenike"
    },
    {
        "species_name": "Stygolimnochares elongata",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Eylais degenerata",
        "date": "1897",
        "discoverer": "Koenike"
    },
    {
        "species_name": "Eylais hamata",
        "date": "1897",
        "discoverer": "Koenike"
    },
    {
        "species_name": "Eylais rimosoides",
        "date": "1926",
        "discoverer": "K. Viets"
    },
    {
        "species_name": "Hydrachna conjecta",
        "date": "1895",
        "discoverer": "Koenike"
    },
    {
        "species_name": "Hydrachna multipora",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Hydrachna simulans",
        "date": "1928",
        "discoverer": "Marshall"
    },
    {
        "species_name": "Hydrachna testudinata",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Hydrachna trilobata",
        "date": "1926",
        "discoverer": "K. Viets"
    },
    {
        "species_name": "Diplodontus silvestrii",
        "date": "1898",
        "discoverer": "Daday"
    },
    {
        "species_name": "Hydrodroma despiciens",
        "date": "1776",
        "discoverer": "Müller"
    },
    {
        "species_name": "Hydrodroma monticola",
        "date": "1906",
        "discoverer": "Piersig"
    },
    {
        "species_name": "Hydrodroma rheophila",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Hydrodroma tonapii",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "H (Papilloporus) incertus",
        "date": "1893",
        "discoverer": "Koenike"
    },
    {
        "species_name": "Javathyas cornipes",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Mamersa gennada",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Mamersa indica",
        "date": "1969",
        "discoverer": "Nayar"
    },
    {
        "species_name": "Mamersa petrophila",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Parathyas primitiva",
        "date": "1926",
        "discoverer": "Lundblad"
    },
    {
        "species_name": "Partnunia chenabi",
        "date": "1994",
        "discoverer": "Panesar & Gerecke"
    },
    {
        "species_name": "Protzia flagellum",
        "date": "1934",
        "discoverer": "Lundblad"
    },
    {
        "species_name": "Protzia gata",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Protzia indica",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Protzia montana",
        "date": "1935",
        "discoverer": "Lundblad"
    },
    {
        "species_name": "Protziella hutchinsoni",
        "date": "1934",
        "discoverer": "Lundblad"
    },
    {
        "species_name": "Trichothyas (Kashmirothyas) hutchinsoni",
        "date": "1934",
        "discoverer": "Lundblad"
    },
    {
        "species_name": "Wandesia approximata",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": ". W. vermiformis",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Bandakia curvipalpis",
        "date": "2004",
        "discoverer": "Panesar"
    },
    {
        "species_name": "Bandakia gangetica",
        "date": "2004",
        "discoverer": "Panesar"
    },
    {
        "species_name": "Bandakia himachali",
        "date": "2004",
        "discoverer": "Panesar"
    },
    {
        "species_name": "Bandakia kulluensis",
        "date": "2004",
        "discoverer": "Panesar"
    },
    {
        "species_name": "Bharatonia vietsi",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Mamersella maryellenae",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Navamamersides karekari",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Navamamersides similis",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Nilgiriopsis imamurai",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Nilotonia (Dartiella) navina",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Nilotonia (Dartonia) perplexa",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Nilotonia (Manotonia) shivai",
        "date": "2004",
        "discoverer": "Panesar"
    },
    {
        "species_name": "Nilotonia (Nilotonia) cooki",
        "date": "2004",
        "discoverer": "Panesar"
    },
    {
        "species_name": "Nilotonia (Nilotonia) indica",
        "date": "1928",
        "discoverer": "Walter"
    },
    {
        "species_name": "Nilotonia (Tadjikodartia) emarginata",
        "date": "1948",
        "discoverer": "Sokolow"
    },
    {
        "species_name": "Paddelia eichhorniae",
        "date": "2004",
        "discoverer": "Panesar"
    },
    {
        "species_name": "Platymamersopsis adhika",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Platymamersopsis mysorensis",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Shivatonia acetabulensis",
        "date": "2004",
        "discoverer": "Panesar"
    },
    {
        "species_name": "Sigthoria nilotica",
        "date": "1905",
        "discoverer": "Nordenskiöld"
    },
    {
        "species_name": "Utaxatax brahmeri",
        "date": "2004",
        "discoverer": "Panesar"
    },
    {
        "species_name": "Utaxatax crassipalpis",
        "date": "2004",
        "discoverer": "Panesar"
    },
    {
        "species_name": "Utaxatax gereckei",
        "date": "2004",
        "discoverer": "Panesar"
    },
    {
        "species_name": "Utaxatax parvati",
        "date": "2004",
        "discoverer": "Panesar"
    },
    {
        "species_name": "Bandakiopsis phaluti",
        "date": "2004",
        "discoverer": "Panesar"
    },
    {
        "species_name": "Lebertia (Pilolebertia) carmamaya",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Lebertia (Lebertia) orientalis",
        "date": "1898",
        "discoverer": "Walter"
    },
    {
        "species_name": "Oxus longisetus",
        "date": "1885",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Oxus pictus",
        "date": "1898",
        "discoverer": "Daday"
    },
    {
        "species_name": "Sperchon bakeri",
        "date": "2009",
        "discoverer": "Pešić & Panesar"
    },
    {
        "species_name": "Sperchon garhwalensis",
        "date": "2007",
        "discoverer": "N. Kumar, K. Kumar & Pešić"
    },
    {
        "species_name": "Sperchon hirsutus",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Sperchon indicus",
        "date": "2007",
        "discoverer": "N. Kumar, K. Kumar & Pešić"
    },
    {
        "species_name": "Sperchon ivonae",
        "date": "2008",
        "discoverer": "Pešić & Gerecke"
    },
    {
        "species_name": "Sperchon nilgiris",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Sperchon ootacamundis",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Sperchon schwoerbeli",
        "date": "2009",
        "discoverer": "Pešić & Panesar"
    },
    {
        "species_name": "Sperchonopsis verrucosa",
        "date": "1896",
        "discoverer": "Protz"
    },
    {
        "species_name": "Monatractides angulatus",
        "date": "1928",
        "discoverer": "Walter"
    },
    {
        "species_name": "Monatractides apratima apratima",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Monatractides dadayi",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Monatractides devatta",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Monatractides garhwaliensis",
        "date": "2007",
        "discoverer": "Pešić, Kumar N. & K. Kumar"
    },
    {
        "species_name": "Monatractides kontschani",
        "date": "2020",
        "discoverer": "Pesic, Smit, Negi, Bahuguna & Dobriyal"
    },
    {
        "species_name": "Monatractides nondescripta",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Monatractides oza",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Monatractides parvatiya",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Monatractides parviventris",
        "date": "1935",
        "discoverer": "K. Viets"
    },
    {
        "species_name": "Monatractides pinapalpis",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Monatractides sakina",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Monatractides setivalvata",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Monatractides sucira",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Monatractides tuzovskyi",
        "date": "2006",
        "discoverer": "Pešić, N. Kumar, K. Kumar & S. Kumar"
    },
    {
        "species_name": "Monatractides yosana",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Testudacarus tripeltatus",
        "date": "1928",
        "discoverer": "Walter"
    },
    {
        "species_name": "Torrenticola chatterjeei",
        "date": "2019",
        "discoverer": "Pesic, Smit and Bahuguna"
    },
    {
        "species_name": "Torrenticola (Torrenticola) indica",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Torrenticola kumari",
        "date": "2020",
        "discoverer": "Pesic, Smit, Negi, Bahuguna & Dobriya"
    },
    {
        "species_name": "Torrenticola (Torrenticola) maharashtris",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Torrenticola (Torrenticola) microdentifera",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Torrenticola (Torrenticola) mulherkarae",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Torrenticola muranyii",
        "date": "2020",
        "discoverer": "Pesic, Smit, Negi, Bahuguna & Dobriyal"
    },
    {
        "species_name": "Torrenticola (Torrenticola) semisuta",
        "date": "1930",
        "discoverer": "Halík"
    },
    {
        "species_name": "Torrenticola (Torrenticola) tetrapora",
        "date": "1935",
        "discoverer": "K. Viets"
    },
    {
        "species_name": "Torrenticola (Torrenticola) cf. turkestanica",
        "date": "1926",
        "discoverer": "Sokolow"
    },
    {
        "species_name": "Torrenticola uttarakhandensis",
        "date": "2019",
        "discoverer": "Pesic, Smit and Bahuguna"
    },
    {
        "species_name": "Torrenticola (Torrenticola) vicista",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Neoatractides (Allotorrenticola) suvarna",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Albaxona indica",
        "date": "2009",
        "discoverer": "Pešić & Ranga Reddy"
    },
    {
        "species_name": "Albaxona stoka",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Albia (Anchistalbia) suvarna",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Albia (Dentalbia) dentipalpis",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Albia (Dentalbia) phreatica",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Aturus hiatosomus",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Aturus indicus",
        "date": "2009",
        "discoverer": "Pešić & Panesar"
    },
    {
        "species_name": "Aturus scutelliferus",
        "date": "1928",
        "discoverer": "Walter"
    },
    {
        "species_name": "Axonopsalbia kanyana",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Axonopsalbia indica",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Axonopsis (Axonopsis) indica",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Axonopsis (Axonopsis) keralensis",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Axonopsis (Axonopsis) phreaticola",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Axonopsis (Axonopsis) vayitriensis",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Axonopsis (Brachypodopsis) latifrons",
        "date": "1928",
        "discoverer": "Walter"
    },
    {
        "species_name": "Axonopsis (Hexaxonopsis) alpa",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Axonopsis (H.) bharatensis",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Axonopsis (H.) falcifer",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Axonopsis (H.) niraensis",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Axonopsis (H.) rucira",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Axonopsis (Navinaxonopsis) abnormipes",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Axonopsis (Paraxonopsis) angulata",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Axonopsis (P.) panduvarna",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Axonopsis (P.) projecta",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Axonopsis (P.) vivarna",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Axonopsis (Plesiobrachypoda) periyar",
        "date": "2009",
        "discoverer": "Pešić & Ranga Reddy"
    },
    {
        "species_name": "Bharatalbia (Bharatalbia) sucirapalpis",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Bharatalbia (Bharatalbia) talinapalpis",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Javalbia antama",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Javalbia punya",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Khedacarus platypes",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Kongsbergia crassipalpis crassipalpis",
        "date": "",
        "discoverer": "K. Viets"
    },
    {
        "species_name": "Kongsbergia (Kongsbergia) indica",
        "date": "2019",
        "discoverer": "Pesic, Smit and Bahuguna"
    },
    {
        "species_name": "Kongsbergia parvatiya",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Kongsbergia rucira",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Stokaxonopsis besselingi",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Feltria balneatoris",
        "date": "2008",
        "discoverer": "Pešić & Panesar"
    },
    {
        "species_name": "Feltria gereckei",
        "date": "2008",
        "discoverer": "Pešić & Panesar"
    },
    {
        "species_name": "Feltria himachali",
        "date": "2008",
        "discoverer": "Pešić & Panesar"
    },
    {
        "species_name": "Feltria indica",
        "date": "2008",
        "discoverer": "Pešić & Panesar"
    },
    {
        "species_name": "Feltria kulluis",
        "date": "2008",
        "discoverer": "Pešić & Panesar"
    },
    {
        "species_name": "Feltria longipalpis",
        "date": "1941",
        "discoverer": "Lundblad"
    },
    {
        "species_name": "Feltria rubra",
        "date": "1898",
        "discoverer": "Piersig"
    },
    {
        "species_name": "Feltria sannae",
        "date": "2008",
        "discoverer": "Pešić & Panesar"
    },
    {
        "species_name": "Feltria schwoerbeli",
        "date": "2008",
        "discoverer": "Pešić & Panesar"
    },
    {
        "species_name": "Feltria tuzovskyi",
        "date": "2008",
        "discoverer": "Pešić & Panesar"
    },
    {
        "species_name": "Frontipodopsis reticulatifrons indicus",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Lethaxona kutapalpis",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Lethaxona panduvarna",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Kawamuracarus polyporus",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Kawamuracarus similis",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Kawamuracarus uniscutatus",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Limnesia (Limnesia) lembangensis",
        "date": "1906",
        "discoverer": "Piersig"
    },
    {
        "species_name": "Limnesia (Limnesia) lucifera uniseta",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Limnesia (Tetralimnesia) pinguipalpis",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Nicalimnesia andha",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Atractides (Atractides) acetabulensis",
        "date": "2009",
        "discoverer": "Pešić & Panesar"
    },
    {
        "species_name": "Atractides (Atractides) biscutatus",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Atractides (Atractides) dorsoscutatus",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Atractides (Atractides) garhwali",
        "date": "2007",
        "discoverer": "Pešić, N. Kumar & K. Kumar"
    },
    {
        "species_name": "Atractides (Atractides) himachali",
        "date": "2009",
        "discoverer": "Pešić & Panesar"
    },
    {
        "species_name": "Atractides (Atractides) indicus",
        "date": "2019",
        "discoverer": "Pesic, Smit and Bahuguna"
    },
    {
        "species_name": "Atractides (Atractides) keralensis",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Atractides (Atractides) lahauli",
        "date": "2009",
        "discoverer": "Pešić & Panesar"
    },
    {
        "species_name": "Atractides (Atractides) nilgiris",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Atractides (Atractides) ootacamundis",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Atractides (Atractides) orthoporus",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Atractides (Atractides) panesari",
        "date": "2009",
        "discoverer": "Pešić & Ranga Reddy"
    },
    {
        "species_name": "Atractides (Atractides) sabulonis",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Atractides (Atractides) talinarostris",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Atractides (Atractides) vayitriensis",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Atractides (Atractides) yukii",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Atractides (Megabates) orientalis",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Atractides (Polymegapus) proximalis",
        "date": "1934",
        "discoverer": "Lundblad"
    },
    {
        "species_name": "Atractides (P.) davecooki",
        "date": "2009",
        "discoverer": "Pešić & Panesar"
    },
    {
        "species_name": "Atractides (P.) diversus",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Atractides (P.) minutus",
        "date": "1928",
        "discoverer": "Walter"
    },
    {
        "species_name": "Hygrobates dobriyali",
        "date": "2019",
        "discoverer": "Pesic, Smit and Bahuguna"
    },
    {
        "species_name": "Hygrobates (Hygrobates) dadayi",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Hygrobates (Hygrobates) gangeticus",
        "date": "2007",
        "discoverer": "Pešić, N. Kumar & K. Kumar"
    },
    {
        "species_name": "Hygrobates (Hygrobates) grimshavi",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Hygrobates (Hygrobates) hamatus",
        "date": "1935",
        "discoverer": "K. Viets"
    },
    {
        "species_name": "Hygrobates (Hygrobates) phreaticus",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Hygrobates (Monobates) falcipalpis",
        "date": "1906",
        "discoverer": "Koenike"
    },
    {
        "species_name": "Hygrobates (M.) keralensis",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Maharashtracarus phreaticus",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Piona catatama",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Piona dadayi",
        "date": "1900",
        "discoverer": "Piersig"
    },
    {
        "species_name": "Piona caligifera",
        "date": "1898",
        "discoverer": "Koenike"
    },
    {
        "species_name": "Piona mahisa",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Piona cf. pachydermoidea",
        "date": "1956",
        "discoverer": "K. Viets"
    },
    {
        "species_name": "Piona pseudouncata",
        "date": "1906",
        "discoverer": "Piersig"
    },
    {
        "species_name": "Tiphys (Tiphys) ornatus",
        "date": "",
        "discoverer": "Koch"
    },
    {
        "species_name": "Litarachna denhami",
        "date": "1909",
        "discoverer": "Lohmann"
    },
    {
        "species_name": "Pontarachna australis",
        "date": "2003",
        "discoverer": "Smit"
    },
    {
        "species_name": "Encentridophorus (Encentridophorus) chelatus",
        "date": "1911",
        "discoverer": "Walter"
    },
    {
        "species_name": "Encentridophorus (Encentridophorus) sarasini",
        "date": "1915",
        "discoverer": "Walter"
    },
    {
        "species_name": "Encentridophorus (Encentridophorus) similis",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Neumania (Ecpolopsis) multiscutata multiscutata",
        "date": "1906",
        "discoverer": "Piersig"
    },
    {
        "species_name": "Neumania (E.) multiscutata bharatensis",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Neumania (Lemienia) maharashtris",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Neumania (Neumania) ambigua",
        "date": "1906",
        "discoverer": "Piersig"
    },
    {
        "species_name": "Neumania (Neumania) excavata",
        "date": "1969",
        "discoverer": "Lundblad"
    },
    {
        "species_name": "Neumania (Neumania) indica",
        "date": "1926",
        "discoverer": "K. Viets"
    },
    {
        "species_name": "Neumania (Neumania) longipes",
        "date": "1928",
        "discoverer": "Walter"
    },
    {
        "species_name": "Neumania (Neumania) nodosa",
        "date": "1898",
        "discoverer": "Daday"
    },
    {
        "species_name": "Neumania (Neumania) pilosa",
        "date": "1906",
        "discoverer": "Koenike"
    },
    {
        "species_name": "Neumania (Neumania) vivarna",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Neumania (Soarella) flagellata",
        "date": "1930",
        "discoverer": "Walter"
    },
    {
        "species_name": "Neumania (S.) megulbana",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Neumania (S.) navina",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Neumania (S.) ulbana",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Unionicola (Conroyatax) setifera",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Unionicola (Imamuratax) scutigera",
        "date": "1926",
        "discoverer": "K. Viets"
    },
    {
        "species_name": "Unionicola (Prasadatax) brandti",
        "date": "1985",
        "discoverer": "Vidrine"
    },
    {
        "species_name": "Unionicola (P.) diversipes",
        "date": "1926",
        "discoverer": "K. Viets"
    },
    {
        "species_name": "Unionicola (Pentatax) affinis",
        "date": "1906",
        "discoverer": "Piersig"
    },
    {
        "species_name": "Unionicola (P.) armata",
        "date": "1929",
        "discoverer": "Walter"
    },
    {
        "species_name": "Unionicola (P.) necessaria",
        "date": "1906",
        "discoverer": "Koenike"
    },
    {
        "species_name": "Unionicola (Bakeratax) chappuisi",
        "date": "1935",
        "discoverer": "Walter"
    },
    {
        "species_name": "Unionicola (Heversatax) unguiculata",
        "date": "1929",
        "discoverer": "Walter"
    },
    {
        "species_name": "Unionicola (Unionicola) crassipes",
        "date": "1776",
        "discoverer": "Müller"
    },
    {
        "species_name": "Africasia mahadensis",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Africasia navina",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Africasia pinguipalpis",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Africasia rucira",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Africasia ruksa",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Africasia subterranea",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Arrenurus (Arrenurus) abnormis",
        "date": "1983",
        "discoverer": "Tomar & Raychaudhuri"
    },
    {
        "species_name": "Arrenurus (Arrenurus) bharatensis",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Arrenurus (Arrenurus) congener",
        "date": "1898",
        "discoverer": "Daday"
    },
    {
        "species_name": "Arrenurus (Arrenurus) dadayi",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Arrenurus (Arrenurus) deccanensis",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Arrenurus (Arrenurus) hamatoides",
        "date": "1969",
        "discoverer": "Lundblad"
    },
    {
        "species_name": "Arrenurus (Arrenurus) hamipetiolatus",
        "date": "1941",
        "discoverer": "Lundblad"
    },
    {
        "species_name": "Arrenurus (Arrenurus) kanktakaphorus",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Arrenurus (Arrenurus) kurtvietsi",
        "date": "1969",
        "discoverer": "Lundblad"
    },
    {
        "species_name": "Arrenurus (Arrenurus) liberatus",
        "date": "1929",
        "discoverer": "Walter"
    },
    {
        "species_name": "Arrenurus (Arrenurus) mysorensis",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Arrenurus (Arrenurus) pseudoaffinis",
        "date": "1906",
        "discoverer": "Piersig"
    },
    {
        "species_name": "Arrenurus (Arrenurus) rhopalopetiolatus",
        "date": "1981",
        "discoverer": "Tomar & Raychaudhury"
    },
    {
        "species_name": "Arrenurus (Arrenurus) ritophilus",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Arrenurus (Arrenurus) rouxi",
        "date": "1915",
        "discoverer": "Walter"
    },
    {
        "species_name": "Arrenurus (Arrenurus)) spinosus",
        "date": "1929",
        "discoverer": "Walter"
    },
    {
        "species_name": "Arrenurus (Brevicaudaturus) quadrilobatus",
        "date": "1969",
        "discoverer": "Nayar"
    },
    {
        "species_name": "Arrenurus (B.) laticodulus",
        "date": "1898",
        "discoverer": "Piersig"
    },
    {
        "species_name": "Arrenurus (Megaluracarus) bicornicodulus",
        "date": "1906",
        "discoverer": "Piersig"
    },
    {
        "species_name": "Arrenurus (M.) ceylonicus",
        "date": "1898",
        "discoverer": "Daday"
    },
    {
        "species_name": "Arrenurus (M.) constrictus",
        "date": "1969",
        "discoverer": "Lundblad"
    },
    {
        "species_name": "Arrenurus (M.) dorsusetosus",
        "date": "1981",
        "discoverer": "Tomar & Raychaudhury"
    },
    {
        "species_name": "Arrenurus (M.) poonaensis",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Arrenurus (M.) rostratus",
        "date": "1898",
        "discoverer": "Daday"
    },
    {
        "species_name": "Arrenurus (Micruracarus) bengalensis",
        "date": "1981",
        "discoverer": "Tomar & Raychaudhury"
    },
    {
        "species_name": "Arrenurus (M.) gibberifrons",
        "date": "1906",
        "discoverer": "Piersig"
    },
    {
        "species_name": "Arrenurus (M.) madaraszi",
        "date": "1898",
        "discoverer": "Daday"
    },
    {
        "species_name": "Arrenurus (M.) micropetiolatus",
        "date": "1928",
        "discoverer": "Walter"
    },
    {
        "species_name": "Arrenurus (M.) pulcher",
        "date": "1911",
        "discoverer": "Walter"
    },
    {
        "species_name": "Arrenurus (Rhinophoracarus) gracilipes",
        "date": "1906",
        "discoverer": "Piersig"
    },
    {
        "species_name": "Arrenurus (Truncaturus) alpapetiolatus",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Arrenurus (T.) indicus",
        "date": "2008",
        "discoverer": "Smit & Pešić"
    },
    {
        "species_name": "Wuria cf. sumatrensis",
        "date": "1935",
        "discoverer": "K. Viets"
    },
    {
        "species_name": "Wuria indica",
        "date": "2010",
        "discoverer": "Peši ć, Chatterjee & Bordoloi"
    },
    {
        "species_name": "Harpagopalpus (Harpagopalpus) indicus",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Hungarohydracarus indicus",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Hungarohydracarus szalayi",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Bharatohydracarus elongatus",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Bharatohydracarus imamurai",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Bharatohydracarus orientalis",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Bharatohydracarus phreaticus",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Bharatohydracarus schwoerbeli",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Bharatohydracarus similis",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Tiramideopsis (Tiramideopsis) ovalis",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Tiramideopsis (Tiramideopsis) pallida",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Tiramideopsis (Tiramideopsis) tanasachiae",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Tiramideopsis (Navamideopsis) expansipes",
        "date": "1967",
        "discoverer": "Cook"
    },
    {
        "species_name": "Polyaspis (Polyaspis) bengalensis",
        "date": "1978",
        "discoverer": "Pramanik and Raychaudhuri"
    },
    {
        "species_name": "Polyaspis (Polyaspis) calcuttaensis",
        "date": "1999",
        "discoverer": "Sarkar and Sanyal"
    },
    {
        "species_name": "Hypoaspis bengalensis",
        "date": "1968",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Hypoaspis burdwanensis",
        "date": "1972",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Hypoaspis dubius",
        "date": "1971",
        "discoverer": "Costa"
    },
    {
        "species_name": "Hypoaspis greeni",
        "date": "1902",
        "discoverer": "Oudemans"
    },
    {
        "species_name": "Hypoaspis krameri",
        "date": "1881",
        "discoverer": "G. & R. Canestrini"
    },
    {
        "species_name": "Hypoaspis orientalis",
        "date": "1968",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Hypoaspis tarsalis",
        "date": "1968",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Hypoaspis vacua",
        "date": "1891",
        "discoverer": "Michael"
    },
    {
        "species_name": "Pseudoparasitus indicus",
        "date": "1977",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Androlaelaps aduncus",
        "date": "1969",
        "discoverer": "Allred"
    },
    {
        "species_name": "Androlaelaps casalis",
        "date": "1887",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Androlaelaps fahrenholzi",
        "date": "1911",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Androlaelaps havliki",
        "date": "1973",
        "discoverer": "Mrciak et al."
    },
    {
        "species_name": "Androlaelaps marshalli",
        "date": "1911",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Androlaelaps ovalis",
        "date": "1961",
        "discoverer": "Costa"
    },
    {
        "species_name": "Androlaelaps theseus",
        "date": "1950",
        "discoverer": "Zumpt"
    },
    {
        "species_name": "Androlaelaps zuluensis",
        "date": "1950",
        "discoverer": "Zumpt"
    },
    {
        "species_name": "Coleolaelaps indicus",
        "date": "1967",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Cosmolaelaps acuta",
        "date": "1891",
        "discoverer": "Michael"
    },
    {
        "species_name": "Cosmolaelaps bengalensis",
        "date": "1968",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Cosmolaelaps burdwanensis",
        "date": "1972",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Cosmolaelaps claviger",
        "date": "1882",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Cosmolaelaps indicus",
        "date": "1966",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Cosmolaelaps vacua",
        "date": "1891",
        "discoverer": "Michael"
    },
    {
        "species_name": "Dinogamasus albulus",
        "date": "1999",
        "discoverer": "Lundqvist"
    },
    {
        "species_name": "Dinogamasus alfkeni",
        "date": "1902",
        "discoverer": "Oudemans"
    },
    {
        "species_name": "Dinogamasus perkinsi",
        "date": "1901",
        "discoverer": "Oudemans"
    },
    {
        "species_name": "Dinogamasus piperi",
        "date": "1930",
        "discoverer": "LeVeque"
    },
    {
        "species_name": "Dinogamasus punensis",
        "date": "2020",
        "discoverer": "Andhale, Pai, Pai, Pandit"
    },
    {
        "species_name": "Dinogamasus tonkinensis",
        "date": "1999",
        "discoverer": "Lundqvist"
    },
    {
        "species_name": "Euandrolaelaps pavlovskii",
        "date": "1955",
        "discoverer": "Bregetova"
    },
    {
        "species_name": "Euandrolaelaps sardous",
        "date": "1911",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Eulaelaps indiscretus",
        "date": "1969",
        "discoverer": "Allred"
    },
    {
        "species_name": "Eulaelaps stabularis",
        "date": "1840",
        "discoverer": "Koch"
    },
    {
        "species_name": "Gaeolaelaps aculeifer",
        "date": "1884",
        "discoverer": "Canestrini"
    },
    {
        "species_name": "Gaeolaelaps marksi",
        "date": "1962",
        "discoverer": "Strandtmann & Crossley"
    },
    {
        "species_name": "Gaeolaelaps minor",
        "date": "1968",
        "discoverer": "Costa"
    },
    {
        "species_name": "Gaeolaelaps sitalaensis",
        "date": "1965",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Gaeolaelaps tarsalis",
        "date": "1968",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Gymnolaelaps margopilus",
        "date": "1966",
        "discoverer": "Hunter"
    },
    {
        "species_name": "Gymnolaelaps sitalaensis",
        "date": "1966",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Haemogamasus gyrinoides",
        "date": "1969",
        "discoverer": "Allred"
    },
    {
        "species_name": "Haemogamasus nidiformes",
        "date": "1955",
        "discoverer": "Bregetova"
    },
    {
        "species_name": "Ellsworthia imphalensis",
        "date": "1947",
        "discoverer": "Radford"
    },
    {
        "species_name": "Hypoaspisella lubrica",
        "date": "1904",
        "discoverer": "Oudemans & Voigts"
    },
    {
        "species_name": "Julolaelaps luctator",
        "date": "1916",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Julolaelaps spirostrepti",
        "date": "1914",
        "discoverer": "Oudemans"
    },
    {
        "species_name": "Laelaps agilis",
        "date": "1836",
        "discoverer": "Koch"
    },
    {
        "species_name": "Laelaps algericus",
        "date": "1925",
        "discoverer": "Hirst"
    },
    {
        "species_name": "Laelaps buxtoni",
        "date": "1941",
        "discoverer": "Radford"
    },
    {
        "species_name": "Laelaps echidninus",
        "date": "1887",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Laelaps jugalis",
        "date": "1969",
        "discoverer": "Allred"
    },
    {
        "species_name": "Laelaps manii",
        "date": "1974",
        "discoverer": "Mrciak et al."
    },
    {
        "species_name": "Laelaps manipurensis",
        "date": "1954",
        "discoverer": "Sinha"
    },
    {
        "species_name": "Laelaps nuttalli",
        "date": "1915",
        "discoverer": "Hirst"
    },
    {
        "species_name": "Laelaps myonyssognathus",
        "date": "1961",
        "discoverer": "Grokhovskaya & Nguyen"
    },
    {
        "species_name": "Laelaps ramakrishnani",
        "date": "1974",
        "discoverer": "Mrciak et al."
    },
    {
        "species_name": "Laelaps sinofiensis",
        "date": "1969",
        "discoverer": "Allred"
    },
    {
        "species_name": "Laelaps traubi",
        "date": "1962",
        "discoverer": "Domrow"
    },
    {
        "species_name": "Laelaps turkestanicus",
        "date": "1955",
        "discoverer": "Lange"
    },
    {
        "species_name": "Neolaelaps spinosus",
        "date": "1910",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Ololaelaps burdwanensis",
        "date": "1978",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Ololaelaps holaspis",
        "date": "1902",
        "discoverer": "Oudemans"
    },
    {
        "species_name": "Ololaelaps sellnicki",
        "date": "1964",
        "discoverer": "Bregetova & Koroleva"
    },
    {
        "species_name": "Ololaelaps sitalaensis",
        "date": "1978",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Ololaelaps venetus",
        "date": "1903",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Pneumolaelaps longanalis",
        "date": "1973",
        "discoverer": "Hunter & Husband"
    },
    {
        "species_name": "Pseudoparasitus centralis",
        "date": "1920",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Pseudoparasitus indicus",
        "date": "1977",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Stigmatolaelaps greeni",
        "date": "1902",
        "discoverer": "Oudemans"
    },
    {
        "species_name": "Stigmatolaelaps hunteri",
        "date": "1998",
        "discoverer": "Krantz"
    },
    {
        "species_name": "Stratiolaelaps miles",
        "date": "1892",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Tropilaelaps clareae",
        "date": "1961",
        "discoverer": "Delfinado& Baker"
    },
    {
        "species_name": "Tropilaelaps koenigerum",
        "date": "1982",
        "discoverer": "Delfinado-Baker & Baker"
    },
    {
        "species_name": "Tropilaelaps mercedesae",
        "date": "2007",
        "discoverer": "Anderson & Morgan"
    },
    {
        "species_name": "Dermanyssus gallinae",
        "date": "1778",
        "discoverer": "DeGeer"
    },
    {
        "species_name": "Laelaspisella kabitae",
        "date": "1968",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Liponyssoides sanguineus",
        "date": "1914",
        "discoverer": "Hirst"
    },
    {
        "species_name": "Ornithonyssus sylviarum",
        "date": "1877",
        "discoverer": "G. Canestrini & Fanzago"
    },
    {
        "species_name": "Ornithonyssus bursa",
        "date": "1888",
        "discoverer": "Berlese"
    },
    {
        "species_name": "Epicroseius abinashi",
        "date": "1966",
        "discoverer": "Bhattacharyya"
    },
    {
        "species_name": "Leiodinychus parasiticus",
        "date": "1964",
        "discoverer": "Choudhury & Mukherjee"
    },
    {
        "species_name": "Multisetosa himalayensis",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Odontacarus (Leogonius) audyi",
        "date": "1968",
        "discoverer": "Vercammen-Grandjean"
    },
    {
        "species_name": "Odontacarus (L.) gymnodactyli",
        "date": "1925",
        "discoverer": "Ewing"
    },
    {
        "species_name": "Odontacarus (L.) indica",
        "date": "1966",
        "discoverer": "Nadchatram and loshee"
    },
    {
        "species_name": "Odontacarus (L.) joshii",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Shunsennia wissemani",
        "date": "1966",
        "discoverer": "Traub and Nadchatram"
    },
    {
        "species_name": "Whartonia (Fascutonia) brennani",
        "date": "1955",
        "discoverer": "Hiregaudar and Bal"
    },
    {
        "species_name": "Whartonia (F.) indica",
        "date": "1956",
        "discoverer": "Hiregaudar and Bal"
    },
    {
        "species_name": "Whartonia (F.) kumaonensis",
        "date": "1971",
        "discoverer": "Bhat"
    },
    {
        "species_name": "Trombicula hampii",
        "date": "1955",
        "discoverer": "Hiregaudar and Bal"
    },
    {
        "species_name": "Trombicula (Trombicula) hypodermata",
        "date": "1966",
        "discoverer": "Nadchatram and Traub"
    },
    {
        "species_name": "Trombicula schmitzi",
        "date": "1914",
        "discoverer": "Oudemans"
    },
    {
        "species_name": "Blankaartia (Blankaartia) nilotica",
        "date": "1904",
        "discoverer": "Tragardh"
    },
    {
        "species_name": "Blankaartia (Blankaartia) acuscutellaris",
        "date": "1922",
        "discoverer": "Walch"
    },
    {
        "species_name": "Chiroptella (Chiroptella) bandupi",
        "date": "1956",
        "discoverer": "Hiregaudar and Bal"
    },
    {
        "species_name": "Chiroptella (Chiroptella) hiregaudari",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Eutrombicula hirsti",
        "date": "1927",
        "discoverer": "Sambon"
    },
    {
        "species_name": "Fonsecia (Fonsecia) coluberina",
        "date": "1946",
        "discoverer": "Radford"
    },
    {
        "species_name": "Fonsecia (Fonsecia) ptyasi",
        "date": "1955",
        "discoverer": "Rao and Hiregaudar"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) baltalense",
        "date": "1976",
        "discoverer": "Vercammen-Grandjean and Langston"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) bhimtalense",
        "date": "1952",
        "discoverer": "Womersley"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) burmense",
        "date": "1945",
        "discoverer": "Ewing"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) dehradunense",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) deliense",
        "date": "1922",
        "discoverer": "Walch"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) delimushi",
        "date": "1976",
        "discoverer": "Vercammen-Grandjean and Langston"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) dihumerale",
        "date": "1967",
        "discoverer": "Traub and Nadchatram"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) discrepans",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) dooleyi",
        "date": "1970",
        "discoverer": "Nadchatram"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) dux",
        "date": "1952",
        "discoverer": "Womersley"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) fulleri",
        "date": "1949",
        "discoverer": "Ewing"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) fulmentum",
        "date": "1976",
        "discoverer": "Vercammen-Grandjean and Langston"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) imphalum",
        "date": "1976",
        "discoverer": "Vercammen-Grandjean and Langston"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) insigne",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) irregulare",
        "date": "1967",
        "discoverer": "Traub and Nadchatram"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) jayewickremei",
        "date": "1952",
        "discoverer": "Womersley"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) kalrai",
        "date": "1953",
        "discoverer": "Radford"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) keukenschrijveri",
        "date": "1923",
        "discoverer": "Walch"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) kulkarnii",
        "date": "1976",
        "discoverer": "Vercammen-Grandjean and Langston"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) lagone",
        "date": "1976",
        "discoverer": "Vercammen-Grandjean and Langston"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) longisetum",
        "date": "1952",
        "discoverer": "Womersley"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) macacum",
        "date": "1952",
        "discoverer": "Womersley"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) mirum",
        "date": "1976",
        "discoverer": "Vercammen-Grandjean and Langston"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) mitchelli",
        "date": "1970",
        "discoverer": "Nadchatram"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) multisetosum",
        "date": "1964",
        "discoverer": "Joshee"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) oreophilum",
        "date": "1976",
        "discoverer": "Vercammen-Grandjean and Langston"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) pakistanum",
        "date": "1976",
        "discoverer": "Vercammen-Grandjean and Langston"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) paradux",
        "date": "1976",
        "discoverer": "Vercammen-Grandjean and Langston"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) parapalpale",
        "date": "1952",
        "discoverer": "Womersley"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) parviscutum",
        "date": "1966",
        "discoverer": "Mitchell and Nadchatram"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) peniscutum",
        "date": "1966",
        "discoverer": "Vercammen-Grandjean"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) pseudofulmentum",
        "date": "1976",
        "discoverer": "Vercammen-Grandjean and Langston"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) puta",
        "date": "1952",
        "discoverer": "Womersley"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) radfordi",
        "date": "1954",
        "discoverer": "Sinha"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) rupestre",
        "date": "1967",
        "discoverer": "Traub and Nadchatram"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) russicum",
        "date": "1902",
        "discoverer": "Oudemans"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) siligorense",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) sinhgarhense",
        "date": "1973",
        "discoverer": "Kulkarni"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) solitarium",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) spilletti",
        "date": "1966",
        "discoverer": "Mitchell and Nadchatram"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) subintermedium",
        "date": "1954",
        "discoverer": "Jameson and Toshioka"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) subrussicum",
        "date": "1970",
        "discoverer": "Kolebinova"
    },
    {
        "species_name": "Leptotrombidium (Leptotrombidium) tithwalense",
        "date": "1952",
        "discoverer": "Womersley"
    },
    {
        "species_name": "Leptotrombidium (Erkotrombidium) bhattipadense",
        "date": "1964",
        "discoverer": "Joshee"
    },
    {
        "species_name": "Leptotrombidium (Ericotrombidium) eximium",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Leptotrombidium (E.) gliricoiens",
        "date": "1915",
        "discoverer": "Hirst"
    },
    {
        "species_name": "Leptotrombidium (E.) indicum",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Leptotrombidium (E.) lepidum",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Leptotrombidium (E.) murphyi",
        "date": "1970",
        "discoverer": "Nadchatram"
    },
    {
        "species_name": "Leptotrombidium (E.) pseudogliricolens",
        "date": "1976",
        "discoverer": "Vercammen-Grandjean and Langston"
    },
    {
        "species_name": "Leptotrombidium (E.) rajaniae",
        "date": "1979",
        "discoverer": "Kulkarni"
    },
    {
        "species_name": "Leptotrombidium (E.) rajasthanense",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Leptotrombidium (E.) uriense",
        "date": "1976",
        "discoverer": "Vercammen-Grandjean and Langston"
    },
    {
        "species_name": "Leptotrombidium (E.) vietzi",
        "date": "1952",
        "discoverer": "Womersley"
    },
    {
        "species_name": "Leptotrombidium (E.) wallacei",
        "date": "1966",
        "discoverer": "Mitchell and Nadchatram"
    },
    {
        "species_name": "Microtrombicula (Microtrombicula) alpicula",
        "date": "1966",
        "discoverer": "Traub and Nadchatram"
    },
    {
        "species_name": "Microtrombicula (Microtrombicula) altens",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Microtrombicula (Microtrombicula) buxtoni",
        "date": "1952",
        "discoverer": "Womersley"
    },
    {
        "species_name": "Microtrombicula (Microtrombicula) cotrivensa",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Microtrombicula (Microtrombicula) kajutekrii",
        "date": "1964",
        "discoverer": "Joshee"
    },
    {
        "species_name": "Microtrombicula (Microtrombicula) khurdangencosa",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Microtrombicula (Microtrombicula) khurdangensis",
        "date": "1952",
        "discoverer": "Womersley"
    },
    {
        "species_name": "Microtrombicula (Microtrombicula) latens",
        "date": "1966",
        "discoverer": "Traub and Nadchatram"
    },
    {
        "species_name": "Microtrombicula (Microtrombicula) munda",
        "date": "1932",
        "discoverer": "Gater"
    },
    {
        "species_name": "Microtrombicula (Microtrombicula) palicula",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Microtrombicula (Microtrombicula) perissochaeta",
        "date": "1966",
        "discoverer": "Traub and Nadchatram"
    },
    {
        "species_name": "Microtrombicula (Microtrombicula) pseudoperissochaeta",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Microtrombicula (Microtrombicula) rajoriensis",
        "date": "1952",
        "discoverer": "Womersley"
    },
    {
        "species_name": "Microtrombicula (Microtrombicula) spicea",
        "date": "1932",
        "discoverer": "Gater"
    },
    {
        "species_name": "Microtrombicula (Microtrombicula) talens",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Microtrombicula (Microtrombicula) unigenuala",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Microtrombicula (Microtrombicula) vacillata",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Microtrombicula (Microtrombicula) vencotrisa",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Microtrombicula (Microtrombicula) ventricosa",
        "date": "1966",
        "discoverer": "Traub and Nadchatram"
    },
    {
        "species_name": "Miyatrombicula cooli",
        "date": "1962",
        "discoverer": "Domrow"
    },
    {
        "species_name": "Miyatrombicula najai",
        "date": "1957",
        "discoverer": "Hiregaudar"
    },
    {
        "species_name": "Myotrombicula (Myotrombicula) kauli",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Neotrombicula autumnalis",
        "date": "1790",
        "discoverer": "Shaw"
    },
    {
        "species_name": "Neotrombicula anax",
        "date": "1957",
        "discoverer": "Audy and Womersley"
    },
    {
        "species_name": "Neotrombicula cervulicola",
        "date": "1931",
        "discoverer": "Ewing"
    },
    {
        "species_name": "Neotrombicula fujigmo",
        "date": "1950",
        "discoverer": "Philip and Fuller"
    },
    {
        "species_name": "Neotrombicula gayanoi",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Neotrombicula guptai",
        "date": "1979",
        "discoverer": "Nadchatram"
    },
    {
        "species_name": "Neotrombicula inflata",
        "date": "1966",
        "discoverer": "Mitchell and Nadchatram"
    },
    {
        "species_name": "Neotrombicula kanzalwanensis",
        "date": "1952",
        "discoverer": "Womersley"
    },
    {
        "species_name": "Neotrombicula kashmirensis",
        "date": "1952",
        "discoverer": "Womersley"
    },
    {
        "species_name": "Neotrombicula microti",
        "date": "1928",
        "discoverer": "Ewing"
    },
    {
        "species_name": "Neotrombicula nagayoi",
        "date": "1950",
        "discoverer": "Sasa"
    },
    {
        "species_name": "Neotrombicula nivalis",
        "date": "1977",
        "discoverer": "Kudryashova"
    },
    {
        "species_name": "Trombiculindus squamosus",
        "date": "1948",
        "discoverer": "Radford"
    },
    {
        "species_name": "Trombiculindus aetherius",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Trombiculindus cuneatus",
        "date": "1951",
        "discoverer": "Traub and Evans"
    },
    {
        "species_name": "Trombiculindus deccanensis",
        "date": "1966",
        "discoverer": "Mitchell and Nadchatram"
    },
    {
        "species_name": "Trombiculindus foliaceus",
        "date": "1951",
        "discoverer": "Traub and Evans"
    },
    {
        "species_name": "Trombiculindus fordi",
        "date": "1952",
        "discoverer": "Womersley"
    },
    {
        "species_name": "Trombiculindus mehtai",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Trombiculindus pruthi",
        "date": "1954",
        "discoverer": "Sinha"
    },
    {
        "species_name": "Trombiculindus squamiferus",
        "date": "1952",
        "discoverer": "Womersley"
    },
    {
        "species_name": "Trombiculindus traubi",
        "date": "1952",
        "discoverer": "Womersley"
    },
    {
        "species_name": "Trombiculindus varifolius",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Trombigaslia abdita",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Trombigaslia tristernala",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Schoengastia kanhaensis",
        "date": "1966",
        "discoverer": "Mitchell and Nadchatram"
    },
    {
        "species_name": "Schoengastia propria",
        "date": "1957",
        "discoverer": "Audy and Womersley"
    },
    {
        "species_name": "Schoengastia pseudoschuffneri",
        "date": "1927",
        "discoverer": "Walch"
    },
    {
        "species_name": "Schoengastia tuberculatae",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Ascoschoengastia guptai",
        "date": "1974",
        "discoverer": "Kulkarni"
    },
    {
        "species_name": "Ascoschoengastia indica",
        "date": "1915",
        "discoverer": "Hirst"
    },
    {
        "species_name": "Ascoschoengastia katarmalensis",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Ascoschoengastia leechi",
        "date": "1962",
        "discoverer": "Domrow"
    },
    {
        "species_name": "Ascoschoengastia roluis",
        "date": "1954",
        "discoverer": "Traub and Audy"
    },
    {
        "species_name": "Doloisia (Doloisia) bhati",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Doloisia (Doloisia) manipurensis",
        "date": "1946",
        "discoverer": "Radford"
    },
    {
        "species_name": "Helenicula lanius",
        "date": "1946",
        "discoverer": "Radford"
    },
    {
        "species_name": "Helenicula comata",
        "date": "1952",
        "discoverer": "Womersley"
    },
    {
        "species_name": "Helenicula g lobularis",
        "date": "1927",
        "discoverer": "Walch"
    },
    {
        "species_name": "Helenicula kohlsi",
        "date": "1946",
        "discoverer": "Philip and Woodward"
    },
    {
        "species_name": "Helenicula mattei",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Helenicula miyagawai",
        "date": "1951",
        "discoverer": "Sasa, Kumada and Miura"
    },
    {
        "species_name": "Helenicula nadchatrami",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Herpetacarus (Herpetacarus) longisetosa",
        "date": "1957",
        "discoverer": "Hiregaudar"
    },
    {
        "species_name": "Herpetacarus (Herpetacarus) schlugeri",
        "date": "1953",
        "discoverer": "Radford"
    },
    {
        "species_name": "Neoschoengastia (Neoschoengastia) thomasi",
        "date": "1946",
        "discoverer": "Radford"
    },
    {
        "species_name": "Riedlinia coeca",
        "date": "1914",
        "discoverer": "Oudemans"
    },
    {
        "species_name": "Schoutcdenichia (Schoutedenichia) capillata",
        "date": "1953",
        "discoverer": "Radford"
    },
    {
        "species_name": "Schoutedenichia (Schoutedenichia) gangutriani",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Schoutedenichia (Schoutedenichia) goffi",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Schoutedenichia (Schoutedenichia) jubbulporensis",
        "date": "1952",
        "discoverer": "Womersley"
    },
    {
        "species_name": "Schoutedenichia (Schoutedenichia) nagpurensis",
        "date": "1975",
        "discoverer": "Srivastva and Wattal"
    },
    {
        "species_name": "Schoutedenichia (Schoutedenichia) nausheraensis",
        "date": "1952",
        "discoverer": "Womersley"
    },
    {
        "species_name": "Schoutedenichia (Schoutedenichia) schalleri",
        "date": "1966",
        "discoverer": "Mitchell and Nadchatram"
    },
    {
        "species_name": "Walchiella oudemansi",
        "date": "1922",
        "discoverer": "Walch"
    },
    {
        "species_name": "Walchiella lewthwaitei",
        "date": "1952",
        "discoverer": "Womersley"
    },
    {
        "species_name": "Gahrliepia armata",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Gahrliepia armigera",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Gahrliepia barbigera",
        "date": "1957",
        "discoverer": "Traub and Morrow"
    },
    {
        "species_name": "Gahrliepia crassiscuti",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Gahrliepia crocidura",
        "date": "1946",
        "discoverer": "Radford"
    },
    {
        "species_name": "Gahrliepia darita",
        "date": "1957",
        "discoverer": "Traub and Morrow"
    },
    {
        "species_name": "Gahrliepia dhandai",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Gahrliepia dupliseta",
        "date": "1955",
        "discoverer": "Traub and Morrow"
    },
    {
        "species_name": "Gahrliepia fletcheri",
        "date": "1932",
        "discoverer": "Gater"
    },
    {
        "species_name": "Gahrliepia hirsuta",
        "date": "1946",
        "discoverer": "Radford"
    },
    {
        "species_name": "Gahrliepia inconstans",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Gahrliepia khandalaensis",
        "date": "1974",
        "discoverer": "Kulkarni"
    },
    {
        "species_name": "Gahrliepia longipili",
        "date": "1946",
        "discoverer": "Radford"
    },
    {
        "species_name": "Gahrliepia murini",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Gahrliepia plurisetae",
        "date": "1955",
        "discoverer": "Traub and Morrow"
    },
    {
        "species_name": "Gahrliepia punensis",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Gahrliepia uttaranchalensis",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Gahrliepia usitata",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Schoengastiella bengalensis",
        "date": "1915",
        "discoverer": "Hirst"
    },
    {
        "species_name": "Schoengastiella argalea",
        "date": "1957",
        "discoverer": "Traub and Morrow"
    },
    {
        "species_name": "Schoengastiella brevis",
        "date": "1946",
        "discoverer": "Radford"
    },
    {
        "species_name": "Schoengastiella ceylonica",
        "date": "1952",
        "discoverer": "Womersley"
    },
    {
        "species_name": "Schoengastiella chirhatiensis",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Schoengastiella dalhousiensis",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Schoengastiella darjeelingensis",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Schoengastiella galarea",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Schoengastiella gammonsi",
        "date": "1954",
        "discoverer": "Traub and Evans"
    },
    {
        "species_name": "Schoengastiella helata",
        "date": "1954",
        "discoverer": "Traub and Evans"
    },
    {
        "species_name": "Schoengastiella herulata ernandes and",
        "date": "2003",
        "discoverer": "Kulkarni"
    },
    {
        "species_name": "Schoengastiella homunguis",
        "date": "1939",
        "discoverer": "Abdussalam"
    },
    {
        "species_name": "Schoengastiella kalrata",
        "date": "1954",
        "discoverer": "Traub and Evans"
    },
    {
        "species_name": "Schoengastiella kumaonensis",
        "date": "1952",
        "discoverer": "Womersley"
    },
    {
        "species_name": "Schoengastiella ligula",
        "date": "1946",
        "discoverer": "Radford"
    },
    {
        "species_name": "Schoengastiella liota",
        "date": "1954",
        "discoverer": "Traub and Evans"
    },
    {
        "species_name": "Schoengastiella minuta",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Schoengastiella praecipua",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Schoengastiella punctata",
        "date": "1946",
        "discoverer": "Radford"
    },
    {
        "species_name": "Schoengastiella ralagea",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Schoengastiella ramachandrai",
        "date": "1973",
        "discoverer": "Kulkarni"
    },
    {
        "species_name": "Schoengastiella shrivastavi",
        "date": "1975",
        "discoverer": "Srivastva and Wattal"
    },
    {
        "species_name": "Schoengastiella sicata",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Schoengastiella singularis",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Schoengastiella tarsala",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Schoengastiella uttarkashiensis",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Walchia (Walchia) ewingi",
        "date": "1949",
        "discoverer": "Fuller"
    },
    {
        "species_name": "Walchia (Walchia) enode",
        "date": "1932",
        "discoverer": "Gater"
    },
    {
        "species_name": "Walchia (Walchia) gujaratensis",
        "date": "2003",
        "discoverer": "Fernandes and Kulkarni"
    },
    {
        "species_name": "Walchia (Walchia) lupella",
        "date": "1957",
        "discoverer": "Traub and Evans"
    },
    {
        "species_name": "Walchia (Walchia) manipurensis",
        "date": "1954",
        "discoverer": "Sinha"
    },
    {
        "species_name": "Walchia (Walchia) rustica",
        "date": "1932",
        "discoverer": "Gater"
    },
    {
        "species_name": "Walchia (Walchia) soricicola",
        "date": "1957",
        "discoverer": "Traub and Evans"
    },
    {
        "species_name": "Walchia (Walchia) turmalis",
        "date": "1932",
        "discoverer": "Gater"
    }
]


import csv
from pathlib import Path

# Assuming ACARI_SPECIES looks something like this:
# ACARI_SPECIES = [
#     {"species_name": "Varroa destructor", "date": "1904", "discoverer": "Oudemans"},
#     {"species_name": "Ixodes ricinus", "date": "1758", "discoverer": "Linnaeus"}
# ]

def write_acari_species_csv(path: str | Path = "acari_species.csv") -> Path:
    """Write the Acari species list to a CSV file and return the output path."""
    output_path = Path(path)
    
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        # Define fieldnames for the "long format" structure
        writer = csv.DictWriter(csv_file, fieldnames=("id", "species_name", "attribute", "value"))
        writer.writeheader()
        
        # enumerate(..., start=1) adds our numbering
        for index, species in enumerate(ACARI_SPECIES, start=1):
            name = species.get("species_name", "")
            
            # Write the first row for the Discoverer
            writer.writerow({
                "id": index,
                "species_name": name,
                "attribute": "discoverer",
                "value": species.get("discoverer", "")
            })
            
            # Write the second row for the Date
            writer.writerow({
                "id": index,
                "species_name": name,
                "attribute": "date",
                "value": species.get("date", "")
            })
            
    return output_path


if __name__ == "__main__":
    write_acari_species_csv()
