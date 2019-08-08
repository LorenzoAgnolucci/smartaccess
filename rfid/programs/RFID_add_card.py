from ..models import RFIDCard


cards_list = RFIDCard.objects.all()
print(cards_list)