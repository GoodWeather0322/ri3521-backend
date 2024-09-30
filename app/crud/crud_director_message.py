from app.models import DirectorMessage
from app.crud.crud_base_document import CRUDBaseDocument


class CRUDDirectorMessage(CRUDBaseDocument):
    model = DirectorMessage


crud_director_message = CRUDDirectorMessage()
