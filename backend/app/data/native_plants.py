"""Native plant database by ecoregion for REWILD scenario engine."""

# Compact format: (common, scientific, bloom_months, height_ft, sun, soil, value, pollinators)
# sun: F=Full, P=Partial, S=Shade | soil: W=Well-drained, C=Clay, S=Sandy, A=Any
_P = {
"Eastern Temperate Forests": [
("Purple Coneflower","Echinacea purpurea",[6,7,8,9],3,"F","A","high",["monarch","bumblebee","swallowtail"]),
("Black-eyed Susan","Rudbeckia hirta",[6,7,8,9],2,"F","A","high",["sweat bee","bumblebee","painted lady"]),
("Wild Bergamot","Monarda fistulosa",[7,8],3,"F","W","high",["hummingbird","bumblebee","monarch"]),
("New England Aster","Symphyotrichum novae-angliae",[8,9,10],4,"F","A","high",["monarch","bumblebee","skipper"]),
("Joe Pye Weed","Eutrochium purpureum",[7,8,9],6,"P","C","high",["swallowtail","monarch","bumblebee"]),
("Cardinal Flower","Lobelia cardinalis",[7,8,9],3,"P","C","high",["hummingbird","swallowtail"]),
("Butterfly Weed","Asclepias tuberosa",[6,7,8],2,"F","W","critical",["monarch","hairstreak","bumblebee"]),
("Common Milkweed","Asclepias syriaca",[6,7],4,"F","A","critical",["monarch","bumblebee","sweat bee"]),
("Blazing Star","Liatris spicata",[7,8],3,"F","W","high",["monarch","bumblebee","skipper"]),
("Wild Columbine","Aquilegia canadensis",[4,5,6],2,"P","W","medium",["hummingbird","bumblebee"]),
("Virginia Bluebells","Mertensia virginica",[3,4,5],1.5,"P","A","medium",["bumblebee","mason bee"]),
("Swamp Milkweed","Asclepias incarnata",[6,7,8],4,"F","C","critical",["monarch","swallowtail","bumblebee"]),
("Blue Lobelia","Lobelia siphilitica",[8,9],3,"P","C","medium",["bumblebee","hummingbird"]),
("Goldenrod","Solidago speciosa",[8,9,10],4,"F","A","high",["monarch","sweat bee","bumblebee"]),
("Bee Balm","Monarda didyma",[7,8],3,"F","A","high",["hummingbird","bumblebee","monarch"]),
("Wild Geranium","Geranium maculatum",[4,5,6],1.5,"P","W","medium",["bumblebee","mason bee","sweat bee"]),
("Ironweed","Vernonia noveboracensis",[8,9],6,"F","C","high",["swallowtail","monarch","bumblebee"]),
("Spicebush","Lindera benzoin",[3,4],8,"P","A","high",["spicebush swallowtail","mason bee"]),
],
"Southeastern Plains": [
("Blanket Flower","Gaillardia pulchella",[5,6,7,8,9],1.5,"F","S","medium",["painted lady","bumblebee","skipper"]),
("Tickseed","Coreopsis lanceolata",[5,6,7],2,"F","S","medium",["sweat bee","skipper","painted lady"]),
("Purple Coneflower","Echinacea purpurea",[6,7,8,9],3,"F","A","high",["monarch","bumblebee","swallowtail"]),
("Butterfly Weed","Asclepias tuberosa",[5,6,7],2,"F","W","critical",["monarch","hairstreak","bumblebee"]),
("Coral Honeysuckle","Lonicera sempervirens",[4,5,6,7],10,"F","A","high",["hummingbird","clearwing moth"]),
("Blazing Star","Liatris spicata",[7,8],3,"F","W","high",["monarch","swallowtail","skipper"]),
("Swamp Sunflower","Helianthus angustifolius",[9,10,11],6,"F","C","high",["bumblebee","sweat bee","monarch"]),
("Partridge Pea","Chamaecrista fasciculata",[7,8,9],2,"F","S","medium",["bumblebee","sulphur butterfly"]),
("Wild Indigo","Baptisia tinctoria",[5,6],3,"F","S","medium",["bumblebee","wild indigo skipper"]),
("Scarlet Sage","Salvia coccinea",[5,6,7,8,9,10],2,"F","W","high",["hummingbird","swallowtail","bumblebee"]),
("Beautyberry","Callicarpa americana",[5,6],5,"P","A","medium",["sweat bee","bluebird food"]),
("Black-eyed Susan","Rudbeckia hirta",[5,6,7,8],2,"F","A","high",["sweat bee","bumblebee","skipper"]),
("Passionflower","Passiflora incarnata",[6,7,8],15,"F","A","critical",["gulf fritillary","bumblebee"]),
("Cardinal Flower","Lobelia cardinalis",[7,8,9],3,"P","C","high",["hummingbird","swallowtail"]),
("Common Milkweed","Asclepias syriaca",[6,7],4,"F","A","critical",["monarch","bumblebee"]),
],
"Great Plains": [
("Purple Coneflower","Echinacea purpurea",[6,7,8],3,"F","A","high",["bumblebee","monarch","skipper"]),
("Pale Coneflower","Echinacea pallida",[5,6,7],3,"F","W","high",["bumblebee","sweat bee"]),
("Black-eyed Susan","Rudbeckia hirta",[6,7,8],2,"F","A","high",["sweat bee","bumblebee"]),
("Butterfly Weed","Asclepias tuberosa",[6,7],2,"F","W","critical",["monarch","hairstreak"]),
("Leadplant","Amorpha canescens",[6,7],3,"F","W","high",["bumblebee","sweat bee"]),
("Prairie Blazing Star","Liatris pycnostachya",[7,8],4,"F","A","high",["monarch","bumblebee"]),
("Wild Bergamot","Monarda fistulosa",[7,8],3,"F","W","high",["bumblebee","hummingbird"]),
("Little Bluestem","Schizachyrium scoparium",[8,9],3,"F","W","medium",[]),
("Big Bluestem","Andropogon gerardii",[8,9],6,"F","A","medium",[]),
("Switchgrass","Panicum virgatum",[7,8,9],5,"F","A","medium",[]),
("Prairie Dropseed","Sporobolus heterolepis",[8,9],2,"F","W","medium",[]),
("Plains Coreopsis","Coreopsis tinctoria",[6,7,8],2,"F","A","medium",["sweat bee","skipper"]),
("Maximilian Sunflower","Helianthus maximiliani",[8,9,10],8,"F","A","high",["bumblebee","monarch"]),
("Prairie Clover","Dalea purpurea",[6,7],2,"F","W","high",["bumblebee","sweat bee"]),
("Goldenrod","Solidago rigida",[8,9,10],4,"F","A","high",["monarch","sweat bee"]),
],
"Mediterranean California": [
("California Poppy","Eschscholzia californica",[2,3,4,5,6],1,"F","S","medium",["sweat bee","syrphid fly"]),
("Seaside Daisy","Erigeron glaucus",[4,5,6,7,8],1,"F","S","medium",["painted lady","bumblebee"]),
("California Fuchsia","Epilobium canum",[8,9,10,11],2,"F","W","high",["hummingbird","hawk moth"]),
("Coyote Mint","Monardella villosa",[6,7,8],1.5,"F","W","high",["bumblebee","painted lady"]),
("Cleveland Sage","Salvia clevelandii",[5,6,7],4,"F","W","high",["hummingbird","bumblebee"]),
("Toyon","Heteromeles arbutifolia",[6,7],10,"F","A","high",["mason bee","bird food"]),
("Manzanita","Arctostaphylos spp.",[1,2,3],6,"F","W","critical",["bumblebee","mason bee"]),
("Buckwheat","Eriogonum fasciculatum",[5,6,7,8,9],3,"F","W","critical",["painted lady","hairstreak","sweat bee"]),
("Milkweed","Asclepias fascicularis",[6,7,8],3,"F","W","critical",["monarch","bumblebee"]),
("Douglas Iris","Iris douglasiana",[3,4,5],1.5,"P","W","medium",["bumblebee"]),
("Ceanothus","Ceanothus thyrsiflorus",[3,4,5],8,"F","W","high",["bumblebee","mason bee","painted lady"]),
("Deer Grass","Muhlenbergia rigens",[7,8,9],4,"F","A","medium",[]),
("Hummingbird Sage","Salvia spathacea",[3,4,5],2,"P","W","high",["hummingbird","bumblebee"]),
("Black Sage","Salvia mellifera",[4,5,6],4,"F","W","critical",["honeybee","bumblebee","mason bee"]),
("Woolly Blue Curls","Trichostema lanatum",[4,5,6,7],4,"F","W","high",["bumblebee","hummingbird"]),
],
"North American Deserts": [
("Desert Marigold","Baileya multiradiata",[3,4,5,6,7,8,9,10],1.5,"F","S","medium",["sweat bee","painted lady"]),
("Penstemon","Penstemon parryi",[3,4,5],3,"F","S","high",["hummingbird","bumblebee"]),
("Chuparosa","Justicia californica",[2,3,4,5],4,"F","S","high",["hummingbird","carpenter bee"]),
("Desert Milkweed","Asclepias subulata",[5,6,7,8],3,"F","S","critical",["monarch","queen butterfly"]),
("Globe Mallow","Sphaeralcea ambigua",[3,4,5],3,"F","S","medium",["globe mallow bee","sweat bee"]),
("Brittlebush","Encelia farinosa",[2,3,4,5],3,"F","S","medium",["sweat bee","painted lady"]),
("Desert Ironwood","Olneya tesota",[5,6],25,"F","S","high",["carpenter bee","bumblebee"]),
("Fairy Duster","Calliandra eriophylla",[2,3,4],3,"F","S","high",["hummingbird","carpenter bee"]),
("Agave","Agave parryi",[6,7],4,"F","S","high",["bat","hummingbird","carpenter bee"]),
("Sacred Datura","Datura wrightii",[5,6,7,8,9],3,"F","S","medium",["hawk moth"]),
("Desert Lavender","Condea emoryi",[1,2,3,4],5,"F","S","high",["bumblebee","mason bee"]),
("Ocotillo","Fouquieria splendens",[3,4,5],15,"F","S","high",["hummingbird","carpenter bee"]),
("Palo Verde","Parkinsonia florida",[4,5],20,"F","S","high",["carpenter bee","sweat bee"]),
("Wolfberry","Lycium spp.",[3,4,5],6,"F","S","medium",["sweat bee","bumblebee"]),
("Apache Plume","Fallugia paradoxa",[5,6,7],5,"F","S","medium",["sweat bee","bumblebee"]),
],
"Northern Forests": [
("Wild Lupine","Lupinus perennis",[5,6],2,"F","S","critical",["karner blue","bumblebee"]),
("Wild Columbine","Aquilegia canadensis",[4,5,6],2,"P","W","medium",["hummingbird","bumblebee"]),
("Black-eyed Susan","Rudbeckia hirta",[6,7,8],2,"F","A","high",["sweat bee","bumblebee"]),
("Bergamot","Monarda fistulosa",[7,8],3,"F","W","high",["bumblebee","hummingbird"]),
("Joe Pye Weed","Eutrochium maculatum",[7,8,9],5,"F","C","high",["monarch","swallowtail"]),
("New England Aster","Symphyotrichum novae-angliae",[8,9,10],4,"F","A","high",["monarch","bumblebee"]),
("Fireweed","Chamerion angustifolium",[7,8],5,"F","A","medium",["bumblebee","hummingbird"]),
("Large-leaved Aster","Eurybia macrophylla",[8,9],2,"S","A","medium",["bumblebee","sweat bee"]),
("Canada Goldenrod","Solidago canadensis",[8,9,10],4,"F","A","high",["monarch","sweat bee"]),
("Common Milkweed","Asclepias syriaca",[6,7],4,"F","A","critical",["monarch","bumblebee"]),
("Blue Flag Iris","Iris versicolor",[5,6],3,"F","C","medium",["bumblebee"]),
("Solomon's Seal","Polygonatum biflorum",[5,6],2,"S","W","medium",["bumblebee"]),
("Wild Strawberry","Fragaria virginiana",[4,5,6],0.5,"F","A","medium",["sweat bee","mason bee"]),
("Meadowsweet","Spiraea alba",[6,7,8],4,"F","C","medium",["sweat bee","bumblebee"]),
("Red Osier Dogwood","Cornus sericea",[5,6],8,"P","C","high",["mason bee","bird food"]),
],
"Central USA Plains": [
("Purple Coneflower","Echinacea purpurea",[6,7,8],3,"F","A","high",["bumblebee","monarch"]),
("Black-eyed Susan","Rudbeckia hirta",[6,7,8],2,"F","A","high",["sweat bee","bumblebee"]),
("Butterfly Weed","Asclepias tuberosa",[6,7],2,"F","W","critical",["monarch","hairstreak"]),
("Prairie Dock","Silphium terebinthinaceum",[7,8,9],8,"F","A","medium",["bumblebee"]),
("Compass Plant","Silphium laciniatum",[7,8],8,"F","A","medium",["bumblebee","sweat bee"]),
("Cup Plant","Silphium perfoliatum",[7,8,9],7,"F","C","high",["bumblebee","goldfinch"]),
("Wild Bergamot","Monarda fistulosa",[7,8],3,"F","W","high",["bumblebee","hummingbird"]),
("New England Aster","Symphyotrichum novae-angliae",[8,9,10],4,"F","A","high",["monarch","bumblebee"]),
("Prairie Blazing Star","Liatris pycnostachya",[7,8],4,"F","A","high",["monarch","bumblebee"]),
("Rattlesnake Master","Eryngium yuccifolium",[7,8],4,"F","W","high",["great black wasp","sweat bee"]),
("Pale Indian Plantain","Arnoglossum atriplicifolium",[6,7],5,"P","A","medium",["sweat bee"]),
("Wild Quinine","Parthenium integrifolium",[6,7,8],3,"F","W","medium",["sweat bee","bumblebee"]),
("Prairie Dropseed","Sporobolus heterolepis",[8,9],2,"F","W","medium",[]),
("Little Bluestem","Schizachyrium scoparium",[8,9],3,"F","W","medium",[]),
("Culver's Root","Veronicastrum virginicum",[7,8],5,"F","A","high",["bumblebee","swallowtail"]),
],
"Pacific Northwest Forests": [
("Oregon Grape","Mahonia aquifolium",[3,4,5],5,"P","W","high",["mason bee","bumblebee"]),
("Red Flowering Currant","Ribes sanguineum",[3,4],8,"P","W","high",["hummingbird","bumblebee"]),
("Douglas Aster","Symphyotrichum subspicatum",[7,8,9],3,"F","A","high",["bumblebee","sweat bee"]),
("Fireweed","Chamerion angustifolium",[7,8],5,"F","A","medium",["bumblebee","hummingbird"]),
("Red Columbine","Aquilegia formosa",[5,6,7],2,"P","W","medium",["hummingbird","bumblebee"]),
("Salal","Gaultheria shallon",[5,6],4,"S","A","medium",["bumblebee","mason bee"]),
("Nootka Rose","Rosa nutkana",[5,6],6,"F","A","medium",["sweat bee","mason bee"]),
("Nodding Onion","Allium cernuum",[6,7],1.5,"F","W","medium",["sweat bee","bumblebee"]),
("Western Sword Fern","Polystichum munitum",[0],3,"S","A","medium",[]),
("Showy Milkweed","Asclepias speciosa",[6,7],3,"F","A","critical",["monarch","bumblebee"]),
("Oceanspray","Holodiscus discolor",[6,7],10,"P","W","medium",["sweat bee","painted lady"]),
("Blue Elderberry","Sambucus cerulea",[5,6],15,"F","A","high",["mason bee","bird food"]),
("Camas","Camassia quamash",[4,5],2,"F","C","high",["bumblebee","mason bee"]),
("Pacific Bleeding Heart","Dicentra formosa",[3,4,5,6],1.5,"S","W","medium",["hummingbird","bumblebee"]),
("Lupine","Lupinus polyphyllus",[5,6,7],4,"F","A","high",["bumblebee"]),
],
"Ozark/Ouachita Highlands": [
("Purple Coneflower","Echinacea purpurea",[6,7,8],3,"F","A","high",["bumblebee","monarch"]),
("Butterfly Weed","Asclepias tuberosa",[6,7],2,"F","W","critical",["monarch","hairstreak"]),
("Wild Hyacinth","Camassia scilloides",[4,5],1.5,"P","A","medium",["bumblebee","mason bee"]),
("Aromatic Aster","Symphyotrichum oblongifolium",[9,10],2,"F","W","high",["monarch","bumblebee"]),
("Royal Catchfly","Silene regia",[7,8],3,"F","W","high",["hummingbird","swallowtail"]),
("Indian Pink","Spigelia marilandica",[5,6],1.5,"P","W","high",["hummingbird"]),
("Coreopsis","Coreopsis lanceolata",[5,6,7],2,"F","W","medium",["sweat bee","skipper"]),
("Black-eyed Susan","Rudbeckia hirta",[6,7,8],2,"F","A","high",["sweat bee","bumblebee"]),
("Wild Bergamot","Monarda fistulosa",[7,8],3,"F","W","high",["bumblebee","hummingbird"]),
("Blue Star","Amsonia hubrichtii",[4,5],3,"F","W","medium",["bumblebee"]),
("Blazing Star","Liatris aspera",[8,9],3,"F","W","high",["monarch","bumblebee"]),
("Ozark Sunflower","Helianthus silphioides",[8,9],4,"F","W","medium",["bumblebee","sweat bee"]),
("Green Milkweed","Asclepias viridis",[5,6,7],2,"F","A","critical",["monarch","bumblebee"]),
("Dwarf Crested Iris","Iris cristata",[4,5],0.5,"P","W","medium",["bumblebee"]),
("Prairie Dock","Silphium terebinthinaceum",[7,8],8,"F","A","medium",["bumblebee"]),
],
"Western Mountains": [
("Showy Milkweed","Asclepias speciosa",[6,7],3,"F","A","critical",["monarch","bumblebee"]),
("Rocky Mountain Penstemon","Penstemon strictus",[6,7],2,"F","W","high",["bumblebee","hummingbird"]),
("Blanket Flower","Gaillardia aristata",[6,7,8],2,"F","W","medium",["painted lady","bumblebee"]),
("Blue Flax","Linum lewisii",[5,6,7],2,"F","W","medium",["sweat bee","bumblebee"]),
("Aspen Daisy","Erigeron speciosus",[6,7,8],2,"F","W","medium",["bumblebee","syrphid fly"]),
("Wild Geranium","Geranium viscosissimum",[6,7],2,"P","W","medium",["bumblebee","sweat bee"]),
("Lupine","Lupinus argenteus",[6,7],2,"F","W","high",["bumblebee"]),
("Indian Paintbrush","Castilleja miniata",[6,7,8],2,"F","W","high",["hummingbird","bumblebee"]),
("Yarrow","Achillea millefolium",[6,7,8],2,"F","A","medium",["sweat bee","painted lady","skipper"]),
("Wild Rose","Rosa woodsii",[5,6],5,"F","A","medium",["sweat bee","bumblebee"]),
("Rabbitbrush","Ericameria nauseosa",[8,9,10],4,"F","W","high",["monarch","painted lady","sweat bee"]),
("Blue Columbine","Aquilegia coerulea",[6,7],2,"P","W","high",["hummingbird","bumblebee"]),
("Black-eyed Susan","Rudbeckia hirta",[6,7,8],2,"F","A","high",["sweat bee","bumblebee"]),
("Bee Plant","Cleome serrulata",[6,7,8],4,"F","A","high",["bumblebee","hummingbird"]),
("Goldenrod","Solidago missouriensis",[7,8,9],2,"F","W","high",["sweat bee","monarch"]),
],
"Tropical/Subtropical Florida": [
("Firebush","Hamelia patens",[1,2,3,4,5,6,7,8,9,10,11,12],8,"F","A","high",["hummingbird","swallowtail","monarch"]),
("Coontie","Zamia integrifolia",[3,4],3,"P","S","critical",["atala butterfly"]),
("Beach Sunflower","Helianthus debilis",[1,2,3,4,5,6,7,8,9,10,11,12],2,"F","S","medium",["sweat bee","painted lady"]),
("Muhly Grass","Muhlenbergia capillaris",[10,11],3,"F","S","medium",[]),
("Blanket Flower","Gaillardia pulchella",[3,4,5,6,7,8,9],1.5,"F","S","medium",["painted lady","skipper"]),
("Coral Honeysuckle","Lonicera sempervirens",[3,4,5,6,7,8,9,10],10,"F","A","high",["hummingbird","clearwing moth"]),
("Passionflower","Passiflora incarnata",[5,6,7,8,9],15,"F","A","critical",["gulf fritillary","zebra longwing"]),
("Walter's Viburnum","Viburnum obovatum",[2,3],12,"P","A","high",["mason bee","bird food"]),
("Scarlet Sage","Salvia coccinea",[3,4,5,6,7,8,9,10,11],2,"F","W","high",["hummingbird","swallowtail"]),
("Sea Oats","Uniola paniculata",[6,7,8],4,"F","S","medium",[]),
("Beautyberry","Callicarpa americana",[5,6],5,"P","A","medium",["sweat bee","bird food"]),
("Milkweed","Asclepias tuberosa",[5,6,7,8],2,"F","W","critical",["monarch","queen butterfly"]),
("Sunshine Mimosa","Mimosa strigillosa",[4,5,6,7,8,9],0.5,"F","A","medium",["sweat bee","skipper"]),
("Scorpion Tail","Heliotropium angiospermum",[1,2,3,4,5,6,7,8,9,10,11,12],2,"F","A","high",["miami blue","skipper"]),
("Simpson's Stopper","Myrcianthes fragrans",[4,5,6,7],15,"P","S","high",["mason bee","bird food"]),
],
"Gulf Coast Plains": [
("Cardinal Flower","Lobelia cardinalis",[7,8,9],3,"P","C","high",["hummingbird","swallowtail"]),
("Swamp Milkweed","Asclepias incarnata",[6,7,8],4,"F","C","critical",["monarch","swallowtail"]),
("Blue Flag Iris","Iris virginica",[4,5],3,"F","C","medium",["bumblebee"]),
("Swamp Sunflower","Helianthus angustifolius",[9,10,11],6,"F","C","high",["bumblebee","monarch"]),
("Inland Sea Oats","Chasmanthium latifolium",[7,8],3,"P","A","medium",[]),
("Coral Honeysuckle","Lonicera sempervirens",[3,4,5,6,7],10,"F","A","high",["hummingbird","clearwing moth"]),
("Black-eyed Susan","Rudbeckia hirta",[5,6,7,8],2,"F","A","high",["sweat bee","bumblebee"]),
("Turk's Cap","Malvaviscus arboreus",[5,6,7,8,9,10],4,"P","A","high",["hummingbird","swallowtail"]),
("Scarlet Sage","Salvia coccinea",[5,6,7,8,9,10],2,"F","W","high",["hummingbird","swallowtail"]),
("Spider Lily","Hymenocallis liriosme",[4,5],2,"P","C","medium",["hawk moth"]),
("Switchgrass","Panicum virgatum",[7,8,9],5,"F","A","medium",[]),
("Gulf Muhly","Muhlenbergia capillaris",[10,11],3,"F","A","medium",[]),
("Purple Coneflower","Echinacea purpurea",[6,7,8],3,"F","A","high",["bumblebee","monarch"]),
("Passionflower","Passiflora incarnata",[6,7,8,9],15,"F","A","critical",["gulf fritillary","zebra longwing"]),
("Wax Myrtle","Morella cerifera",[3,4],12,"F","A","medium",["sweat bee","bird food"]),
],
}

_SUN_MAP = {"F": "Full sun (6+ hrs)", "P": "Partial shade (3-6 hrs)", "S": "Full shade (<3 hrs)"}
_SOIL_MAP = {"W": "Well-drained", "C": "Clay-heavy", "S": "Sandy", "A": "Any"}
_MONTHS = ["","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]


def _normalize_sun_filter(sun: str) -> str | None:
    key = sun.strip().lower().replace("-", "_").replace(" ", "_")
    mapping = {
        "full": "F",
        "full_sun": "F",
        "partial": "P",
        "partial_shade": "P",
        "shade": "S",
        "full_shade": "S",
    }
    if key in mapping:
        return mapping[key]

    first = sun[:1].upper()
    return first if first in {"F", "P", "S"} else None


def _normalize_soil_filter(soil: str) -> str | None:
    key = soil.strip().lower().replace("-", "_").replace(" ", "_")
    mapping = {
        "well_drained": "W",
        "welldrained": "W",
        "clay": "C",
        "clay_heavy": "C",
        "sandy": "S",
        "any": "A",
        "unknown": None,
    }
    if key in mapping:
        return mapping[key]

    first = soil[:1].upper()
    return first if first in {"W", "C", "S", "A"} else None


def _expand(entry: tuple) -> dict:
    common, sci, blooms, ht, sun, soil, val, polls = entry
    return {
        "common_name": common,
        "scientific_name": sci,
        "bloom_months": [_MONTHS[m] for m in blooms if m > 0],
        "bloom_month_nums": blooms,
        "height_ft": ht,
        "sun_requirement": _SUN_MAP.get(sun, sun),
        "soil_preference": _SOIL_MAP.get(soil, soil),
        "ecological_value": val,
        "pollinator_associations": polls,
    }


def get_native_plants(
    ecoregion: str,
    sun: str | None = None,
    soil: str | None = None,
) -> list[dict]:
    """Get native plants for an ecoregion, optionally filtered."""
    raw = _P.get(ecoregion, [])

    if sun:
        sun_key = _normalize_sun_filter(sun)
        if sun_key:
            raw = [p for p in raw if p[4] == sun_key]

    if soil:
        soil_key = _normalize_soil_filter(soil)
        if soil_key:
            raw = [p for p in raw if p[5] in {soil_key, "A"}]

    return [_expand(p) for p in raw]


def list_supported_ecoregions() -> list[str]:
    return list(_P.keys())
