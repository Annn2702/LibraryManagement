class Penalty:
    TYPE_LATE = "LATE"
    TYPE_LOST = "LOST"
    TYPE_DAMAGED = "DAMAGED"

    def __init__(
        self,
        reader_id,
        slip_id,
        book_id,
        penalty_type,
        amount,
        penalty_id=None,
        created_at=None
    ):
        self.penalty_id = penalty_id
        self.reader_id = reader_id
        self.slip_id = slip_id
        self.book_id = book_id
        self.penalty_type = penalty_type
        self.amount = amount
        self.created_at = created_at

    def to_tuple(self):
        return (
            self.reader_id,
            self.slip_id,
            self.book_id,
            self.penalty_type,
            self.amount
        )
