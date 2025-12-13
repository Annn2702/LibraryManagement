from services.borrow_service import BorrowService

class BorrowController:
    def __init__(self):
        self.service = BorrowService()

    def create_borrow_by_name(self, reader_name, book_name):
        return self.service.create_borrow(reader_name, book_name)

    def update_borrow(self, slip_id, borrow_date, return_date, status):
        return self.service.update_borrow(slip_id, borrow_date, return_date, status)

    def return_books(self, slip_id):
        return self.service.return_books(slip_id)

    def get_all_borrows(self):
        return self.service.get_all_borrows()
