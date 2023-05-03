import cianparser
i = 0
while i < 100:
    cianparser.parse(
        deal_type="sale", # "rent_long", "rent_short", "sale"
        accommodation_type="flat", # "flat", "room", "house", "house-part", "townhouse"
        location="Москва",
        rooms="studio", # "studio", 1, 2, 3, 4, 5
        start_page=1,
        end_page=100,
        is_saving_csv=True,
        is_latin=True,
        is_express_mode=False,
        is_by_homeowner=False)
    i+=1
    