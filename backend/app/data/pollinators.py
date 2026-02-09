"""Pollinator database by ecoregion for REWILD scenario engine."""

# Format: (name, type, flight_months, nesting, plants_visited, conservation)
_POLL = {
"Eastern Temperate Forests": [
("Eastern Bumble Bee","bee",[4,5,6,7,8,9],"ground",["coneflower","bergamot","goldenrod","aster","milkweed"],"stable"),
("Common Eastern Bumble Bee","bee",[3,4,5,6,7,8,9,10],"ground",["coneflower","bee balm","clover","goldenrod"],"stable"),
("Monarch Butterfly","butterfly",[5,6,7,8,9],"milkweed",["milkweed","coneflower","blazing star","aster","goldenrod"],"vulnerable"),
("Eastern Tiger Swallowtail","butterfly",[4,5,6,7,8],"tree",["bergamot","joe pye weed","coneflower","lobelia"],"stable"),
("Spicebush Swallowtail","butterfly",[4,5,6,7,8,9],"tree",["joe pye weed","bergamot","cardinal flower"],"stable"),
("Ruby-throated Hummingbird","hummingbird",[4,5,6,7,8,9],"tree",["cardinal flower","bee balm","columbine","lobelia"],"stable"),
("Mason Bee","bee",[3,4,5,6],"cavity",["columbine","bluebells","geranium","spicebush"],"stable"),
("Sweat Bee","bee",[4,5,6,7,8,9],"ground",["black-eyed susan","goldenrod","coneflower","geranium"],"stable"),
("Painted Lady","butterfly",[5,6,7,8,9],"none",["black-eyed susan","aster","coneflower"],"stable"),
("Silver-spotted Skipper","butterfly",[5,6,7,8],"none",["blazing star","bergamot","coneflower"],"stable"),
("Carpenter Bee","bee",[4,5,6,7,8],"wood",["bergamot","wisteria","lobelia"],"stable"),
("Great Spangled Fritillary","butterfly",[6,7,8],"ground",["bergamot","coneflower","milkweed"],"stable"),
],
"Southeastern Plains": [
("Eastern Bumble Bee","bee",[3,4,5,6,7,8,9,10],"ground",["coneflower","sage","coreopsis"],"stable"),
("Monarch Butterfly","butterfly",[3,4,5,6,7,8,9,10],"milkweed",["milkweed","blazing star","coneflower"],"vulnerable"),
("Gulf Fritillary","butterfly",[3,4,5,6,7,8,9,10,11],"none",["passionflower","sage","blanket flower"],"stable"),
("Eastern Tiger Swallowtail","butterfly",[3,4,5,6,7,8,9],"tree",["honeysuckle","sage","joe pye weed"],"stable"),
("Ruby-throated Hummingbird","hummingbird",[3,4,5,6,7,8,9,10],"tree",["coral honeysuckle","sage","cardinal flower"],"stable"),
("Cloudless Sulphur","butterfly",[4,5,6,7,8,9,10],"none",["partridge pea","sage","coneflower"],"stable"),
("Sweat Bee","bee",[3,4,5,6,7,8,9,10],"ground",["coreopsis","black-eyed susan","sunflower"],"stable"),
("Painted Lady","butterfly",[4,5,6,7,8,9],"none",["blanket flower","black-eyed susan"],"stable"),
("Mason Bee","bee",[3,4,5,6],"cavity",["beautyberry","wild indigo","coreopsis"],"stable"),
("Carpenter Bee","bee",[3,4,5,6,7,8],"wood",["passionflower","sage","honeysuckle"],"stable"),
("Zebra Swallowtail","butterfly",[3,4,5,6,7,8],"tree",["milkweed","coneflower","blazing star"],"stable"),
("Wild Indigo Duskywing","butterfly",[4,5,6,7,8],"none",["wild indigo","baptisia"],"stable"),
],
"Great Plains": [
("Bumble Bee","bee",[4,5,6,7,8,9],"ground",["coneflower","blazing star","bergamot","clover"],"stable"),
("Monarch Butterfly","butterfly",[5,6,7,8,9],"milkweed",["milkweed","blazing star","coneflower","sunflower"],"vulnerable"),
("Painted Lady","butterfly",[5,6,7,8,9],"none",["coreopsis","sunflower","coneflower"],"stable"),
("Sweat Bee","bee",[4,5,6,7,8,9],"ground",["coreopsis","sunflower","goldenrod","leadplant"],"stable"),
("Regal Fritillary","butterfly",[6,7,8],"ground",["milkweed","coneflower","blazing star"],"vulnerable"),
("Two-tailed Swallowtail","butterfly",[5,6,7,8],"tree",["bergamot","coneflower"],"stable"),
("Mining Bee","bee",[4,5,6,7],"ground",["prairie clover","leadplant","coreopsis"],"stable"),
("Hummingbird Clearwing Moth","moth",[5,6,7,8],"ground",["bergamot","coneflower","blazing star"],"stable"),
("Long-horned Bee","bee",[6,7,8],"ground",["sunflower","coneflower"],"stable"),
("Skipper","butterfly",[5,6,7,8,9],"none",["blazing star","coneflower","coreopsis"],"stable"),
("Great Spangled Fritillary","butterfly",[6,7,8],"ground",["milkweed","coneflower","bergamot"],"stable"),
],
"Mediterranean California": [
("Yellow-faced Bumble Bee","bee",[2,3,4,5,6,7,8,9],"ground",["sage","buckwheat","ceanothus","manzanita"],"declining"),
("Monarch Butterfly","butterfly",[2,3,4,5,6,7,8,9,10,11],"milkweed",["milkweed","buckwheat","sage"],"vulnerable"),
("Anna's Hummingbird","hummingbird",[1,2,3,4,5,6,7,8,9,10,11,12],"tree",["sage","fuchsia","manzanita","ceanothus"],"stable"),
("Painted Lady","butterfly",[3,4,5,6,7,8,9],"none",["buckwheat","coyote mint","seaside daisy"],"stable"),
("Mason Bee","bee",[2,3,4,5,6],"cavity",["manzanita","ceanothus","sage","poppy"],"stable"),
("Hairstreak Butterfly","butterfly",[3,4,5,6,7],"tree",["buckwheat","ceanothus"],"stable"),
("Carpenter Bee","bee",[3,4,5,6,7,8],"wood",["sage","ceanothus","buckwheat"],"stable"),
("Hawk Moth","moth",[5,6,7,8,9],"ground",["fuchsia","sacred datura"],"stable"),
("Sweat Bee","bee",[3,4,5,6,7,8,9],"ground",["poppy","buckwheat","sage","manzanita"],"stable"),
("Western Tiger Swallowtail","butterfly",[4,5,6,7,8],"tree",["sage","buckwheat","coyote mint"],"stable"),
("Syrphid Fly","fly",[3,4,5,6,7,8],"ground",["poppy","daisy","yarrow"],"stable"),
],
"North American Deserts": [
("Sonoran Bumble Bee","bee",[2,3,4,5,6],"ground",["penstemon","globe mallow","fairy duster"],"declining"),
("Queen Butterfly","butterfly",[3,4,5,6,7,8,9,10],"milkweed",["desert milkweed","globe mallow"],"stable"),
("Monarch Butterfly","butterfly",[3,4,5,6,7,8,9],"milkweed",["desert milkweed","marigold"],"vulnerable"),
("Costa's Hummingbird","hummingbird",[1,2,3,4,5,6,7],"tree",["chuparosa","ocotillo","penstemon","fairy duster"],"stable"),
("Carpenter Bee","bee",[3,4,5,6,7,8],"wood",["palo verde","ironwood","chuparosa"],"stable"),
("Globe Mallow Bee","bee",[3,4,5],"ground",["globe mallow"],"stable"),
("Hawk Moth","moth",[5,6,7,8,9],"ground",["sacred datura","agave"],"stable"),
("Painted Lady","butterfly",[3,4,5,6,7,8,9],"none",["desert marigold","brittlebush"],"stable"),
("Sweat Bee","bee",[3,4,5,6,7,8],"ground",["brittlebush","marigold","lavender"],"stable"),
("Greater Long-nosed Bat","bat",[6,7,8],"cave",["agave","saguaro","ocotillo"],"endangered"),
("Pipevine Swallowtail","butterfly",[3,4,5,6,7,8],"none",["penstemon","globe mallow"],"stable"),
],
"Northern Forests": [
("Common Eastern Bumble Bee","bee",[4,5,6,7,8,9],"ground",["bergamot","aster","goldenrod","milkweed"],"stable"),
("Monarch Butterfly","butterfly",[6,7,8,9],"milkweed",["milkweed","aster","goldenrod"],"vulnerable"),
("Canadian Tiger Swallowtail","butterfly",[5,6,7],"tree",["bergamot","joe pye weed","lupine"],"stable"),
("Karner Blue","butterfly",[5,6,7],"ground",["wild lupine"],"endangered"),
("Ruby-throated Hummingbird","hummingbird",[5,6,7,8,9],"tree",["columbine","cardinal flower","bergamot"],"stable"),
("Sweat Bee","bee",[5,6,7,8],"ground",["black-eyed susan","goldenrod","strawberry"],"stable"),
("Mason Bee","bee",[4,5,6],"cavity",["columbine","bluebells","iris"],"stable"),
("Painted Lady","butterfly",[6,7,8],"none",["aster","black-eyed susan","goldenrod"],"stable"),
("Mining Bee","bee",[4,5,6],"ground",["strawberry","columbine","lupine"],"stable"),
("Fritillary","butterfly",[6,7,8],"ground",["bergamot","joe pye weed","milkweed"],"stable"),
],
"Central USA Plains": [
("Bumble Bee","bee",[4,5,6,7,8,9],"ground",["coneflower","bergamot","blazing star","cup plant"],"stable"),
("Monarch Butterfly","butterfly",[5,6,7,8,9],"milkweed",["milkweed","blazing star","coneflower","aster"],"vulnerable"),
("Great Black Wasp","wasp",[6,7,8],"ground",["rattlesnake master","bergamot"],"stable"),
("Sweat Bee","bee",[4,5,6,7,8,9],"ground",["black-eyed susan","coreopsis","goldenrod","quinine"],"stable"),
("Eastern Tiger Swallowtail","butterfly",[5,6,7,8],"tree",["bergamot","coneflower","culver's root"],"stable"),
("Ruby-throated Hummingbird","hummingbird",[5,6,7,8,9],"tree",["bergamot","cardinal flower","bee balm"],"stable"),
("Painted Lady","butterfly",[5,6,7,8,9],"none",["coneflower","black-eyed susan","aster"],"stable"),
("Mason Bee","bee",[4,5,6],"cavity",["columbine","geranium"],"stable"),
("Skipper","butterfly",[5,6,7,8],"none",["blazing star","coneflower"],"stable"),
("Carpenter Bee","bee",[4,5,6,7,8],"wood",["bergamot","cup plant"],"stable"),
("Fritillary","butterfly",[6,7,8],"ground",["milkweed","coneflower","bergamot"],"stable"),
],
"Pacific Northwest Forests": [
("Yellow-faced Bumble Bee","bee",[3,4,5,6,7,8,9],"ground",["oregon grape","currant","aster","camas"],"declining"),
("Monarch Butterfly","butterfly",[6,7,8,9],"milkweed",["milkweed","aster","goldenrod"],"vulnerable"),
("Rufous Hummingbird","hummingbird",[3,4,5,6,7,8],"tree",["currant","columbine","bleeding heart","fuchsia"],"declining"),
("Painted Lady","butterfly",[5,6,7,8,9],"none",["aster","oceanspray"],"stable"),
("Mason Bee","bee",[3,4,5,6],"cavity",["oregon grape","camas","currant"],"stable"),
("Sweat Bee","bee",[4,5,6,7,8],"ground",["nodding onion","aster","oceanspray"],"stable"),
("Western Tiger Swallowtail","butterfly",[5,6,7,8],"tree",["elderberry","columbine","lupine"],"stable"),
("Anise Swallowtail","butterfly",[4,5,6,7],"none",["lupine","columbine"],"stable"),
("Mining Bee","bee",[3,4,5,6],"ground",["camas","oregon grape","currant"],"stable"),
("Clearwing Moth","moth",[6,7,8],"ground",["honeysuckle","columbine"],"stable"),
],
"Ozark/Ouachita Highlands": [
("Eastern Bumble Bee","bee",[4,5,6,7,8,9],"ground",["coneflower","bergamot","blazing star"],"stable"),
("Monarch Butterfly","butterfly",[5,6,7,8,9],"milkweed",["milkweed","blazing star","coneflower","aster"],"vulnerable"),
("Ruby-throated Hummingbird","hummingbird",[4,5,6,7,8,9],"tree",["royal catchfly","indian pink","bergamot"],"stable"),
("Sweat Bee","bee",[4,5,6,7,8,9],"ground",["coreopsis","black-eyed susan","sunflower"],"stable"),
("Eastern Tiger Swallowtail","butterfly",[4,5,6,7,8],"tree",["bergamot","coneflower"],"stable"),
("Painted Lady","butterfly",[5,6,7,8,9],"none",["coreopsis","black-eyed susan"],"stable"),
("Great Spangled Fritillary","butterfly",[6,7,8],"ground",["bergamot","milkweed","coneflower"],"stable"),
("Mason Bee","bee",[3,4,5,6],"cavity",["wild hyacinth","iris","columbine"],"stable"),
("Carpenter Bee","bee",[4,5,6,7,8],"wood",["bergamot","coneflower"],"stable"),
("Hairstreak","butterfly",[4,5,6,7],"tree",["blue star","coreopsis"],"stable"),
],
"Western Mountains": [
("Western Bumble Bee","bee",[5,6,7,8],"ground",["penstemon","lupine","blanket flower"],"declining"),
("Monarch Butterfly","butterfly",[6,7,8,9],"milkweed",["milkweed","rabbitbrush","goldenrod"],"vulnerable"),
("Broad-tailed Hummingbird","hummingbird",[5,6,7,8,9],"tree",["paintbrush","penstemon","columbine"],"stable"),
("Painted Lady","butterfly",[5,6,7,8,9],"none",["blanket flower","yarrow","rabbitbrush"],"stable"),
("Sweat Bee","bee",[5,6,7,8],"ground",["flax","yarrow","goldenrod","blanket flower"],"stable"),
("Mason Bee","bee",[4,5,6,7],"cavity",["penstemon","columbine","flax"],"stable"),
("Skipper","butterfly",[6,7,8],"none",["yarrow","blanket flower","penstemon"],"stable"),
("Syrphid Fly","fly",[5,6,7,8],"ground",["yarrow","daisy","blanket flower"],"stable"),
("Western Tiger Swallowtail","butterfly",[6,7,8],"tree",["penstemon","columbine","bee plant"],"stable"),
("Mining Bee","bee",[5,6,7],"ground",["flax","lupine","penstemon"],"stable"),
],
"Tropical/Subtropical Florida": [
("Atala Butterfly","butterfly",[1,2,3,4,5,6,7,8,9,10,11,12],"none",["coontie"],"recovering"),
("Gulf Fritillary","butterfly",[1,2,3,4,5,6,7,8,9,10,11,12],"none",["passionflower","firebush"],"stable"),
("Zebra Longwing","butterfly",[1,2,3,4,5,6,7,8,9,10,11,12],"none",["passionflower","firebush","sage"],"stable"),
("Monarch Butterfly","butterfly",[10,11,12,1,2,3],"milkweed",["milkweed","scorpion tail","firebush"],"vulnerable"),
("Ruby-throated Hummingbird","hummingbird",[10,11,12,1,2,3,4],"tree",["firebush","coral honeysuckle","sage"],"stable"),
("Miami Blue","butterfly",[1,2,3,4,5,6,7,8,9,10,11,12],"none",["scorpion tail","balloon vine"],"critically endangered"),
("Sweat Bee","bee",[1,2,3,4,5,6,7,8,9,10,11,12],"ground",["sunflower","blanket flower","sage"],"stable"),
("Carpenter Bee","bee",[2,3,4,5,6,7,8,9],"wood",["passionflower","honeysuckle"],"stable"),
("Mason Bee","bee",[2,3,4,5,6],"cavity",["viburnum","stopper"],"stable"),
("Clearwing Moth","moth",[4,5,6,7,8,9],"ground",["honeysuckle","firebush"],"stable"),
("Painted Lady","butterfly",[3,4,5,6,7,8,9,10],"none",["sunflower","blanket flower"],"stable"),
],
"Gulf Coast Plains": [
("Eastern Bumble Bee","bee",[3,4,5,6,7,8,9,10],"ground",["coneflower","sage","sunflower"],"stable"),
("Monarch Butterfly","butterfly",[3,4,5,6,7,8,9,10],"milkweed",["milkweed","coneflower","sage"],"vulnerable"),
("Gulf Fritillary","butterfly",[3,4,5,6,7,8,9,10,11],"none",["passionflower","sage","turk's cap"],"stable"),
("Ruby-throated Hummingbird","hummingbird",[3,4,5,6,7,8,9,10],"tree",["turk's cap","coral honeysuckle","sage","cardinal flower"],"stable"),
("Zebra Longwing","butterfly",[4,5,6,7,8,9,10],"none",["passionflower","sage"],"stable"),
("Sweat Bee","bee",[3,4,5,6,7,8,9,10],"ground",["black-eyed susan","sunflower","coreopsis"],"stable"),
("Cloudless Sulphur","butterfly",[4,5,6,7,8,9,10],"none",["partridge pea","sage"],"stable"),
("Carpenter Bee","bee",[3,4,5,6,7,8],"wood",["passionflower","honeysuckle","turk's cap"],"stable"),
("Hawk Moth","moth",[5,6,7,8,9],"ground",["spider lily","honeysuckle"],"stable"),
("Painted Lady","butterfly",[4,5,6,7,8,9],"none",["black-eyed susan","sunflower"],"stable"),
("Mason Bee","bee",[3,4,5,6],"cavity",["wax myrtle","viburnum"],"stable"),
],
}

_MONTHS = ["","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]


def _expand(entry: tuple) -> dict:
    name, ptype, months, nesting, plants, status = entry
    return {
        "name": name,
        "type": ptype,
        "flight_months": [_MONTHS[m] for m in months if 1 <= m <= 12],
        "flight_month_nums": months,
        "nesting_type": nesting,
        "plants_visited": plants,
        "conservation_status": status,
    }


def get_pollinators(ecoregion: str) -> list[dict]:
    """Get pollinators for an ecoregion."""
    return [_expand(p) for p in _POLL.get(ecoregion, [])]


def get_plant_pollinator_matrix(ecoregion: str) -> dict[str, list[str]]:
    """Build plant → pollinator mapping for an ecoregion."""
    matrix: dict[str, list[str]] = {}
    for entry in _POLL.get(ecoregion, []):
        name, _, _, _, plants, _ = entry
        for plant in plants:
            matrix.setdefault(plant, []).append(name)
    return matrix
