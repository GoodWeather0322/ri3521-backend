from app.models import PresidentAnnouncement
from app.crud.crud_base_document import CRUDBaseDocument


class CRUDPresidentAnnouncement(CRUDBaseDocument):
    model = PresidentAnnouncement


crud_president_announcement = CRUDPresidentAnnouncement()
