class BorrowSlip:
    STATUS_BORROWING = "BORROWING"
    STATUS_RETURNED = "RETURNED"
    STATUS_LATE = "LATE"
    STATUS_LOST = "LOST"

    def __init__(
        self,
        reader_id,
        staff_id,
        borrow_date,
        return_due,
        return_date=None,
        status=STATUS_BORROWING,
        slip_id=None
    ):
        self.slip_id = slip_id
        self.reader_id = reader_id
        self.staff_id = staff_id
        self.borrow_date = borrow_date
        self.return_due = return_due
        self.return_date = return_date
        self.status = status

    def to_tuple(self):
        # Chỉ trả về các giá trị cần thiết để insert
        return (
            self.reader_id,
            self.staff_id,
            self.borrow_date,
            self.return_due,
            self.status  # bỏ return_date
        )

    @staticmethod
    def from_dict(data: dict):
        return BorrowSlip(**data)
