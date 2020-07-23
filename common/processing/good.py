
def get_good_processing(good):
    good.status = "P"
    good.save(update_fields=['status'])
    return good

def get_good_offer_processing(good):
    good.status = "D"
    good.save(update_fields=['status'])
    return good
