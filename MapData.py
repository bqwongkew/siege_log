class MapData:
    def __init__(self, name, *points):
        self.name = name
        self.points = points


MapData.bank = MapData("bank", "basement", "ceo", "kitchen", "archives")
MapData.border = MapData("border", "armory", "workshop", "tellers", "customs")
MapData.chalet = MapData("chalet", "basement", "kitchen", "bar", "bedroom")
MapData.club = MapData("club", "cash", "gym", "basement", "bar")
MapData.coastline = MapData("coastline", "kitchen", "penthouse", "hookah", "bar")
MapData.consulate = MapData("consulate", "garage", "2f", "lobby", "visa")
MapData.hereford = MapData("hereford", "basement", "3f", "2f", "1f")
MapData.kafe = MapData("kafe", "bar", "trains", "bakery")
MapData.oregon = MapData("oregon", "kids", "basement", "kitchen", "tower")
MapData.skyscraper = MapData("skyscraper", "tea", "kitchen", "office", "bedroom")
MapData.theme = MapData("theme", "drugs", "kids", "initiation", "haunted")
MapData.maps = [MapData.bank, MapData.border, MapData.chalet, MapData.club, MapData.coastline, MapData.consulate, MapData.hereford,
                MapData.kafe, MapData.oregon, MapData.skyscraper, MapData.theme]