class BorrowDetail:
    def __init__(
        self,
        slip_id,
        book_id,
        quantity=1,
        fine_amount=0,
        detail_id=None
    ):
        self.detail_id = detail_id
        self.slip_id = slip_id
        self.book_id = book_id
        self.quantity = quantity
        self.fine_amount = fine_amount

    def to_tuple(self):
        return (
            self.slip_id,
            self.book_id,
            self.quantity,
            self.fine_amount
        )
