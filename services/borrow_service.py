from config.database import db
from models.BorrowSlip import BorrowSlip
from models.BorrowDetail import BorrowDetail
from models.reader import Reader
from models.book import Book
from datetime import datetime, timedelta

class BorrowService:

    BORROW_DAYS = 14

    def create_borrow(self, reader_name: str, book_name: str):
        # Lấy reader theo tên
        sql_reader = "SELECT * FROM readers WHERE full_name=%s"
        reader_data = db.fetchone(sql_reader, (reader_name,))
        if not reader_data:
            return False, "Bạn đọc không tồn tại"
        reader = Reader.from_dict(reader_data)
        if not reader.is_active():
            return False, "Thẻ bạn đọc không hợp lệ"

        # Lấy book theo tên
        sql_book = "SELECT * FROM books WHERE title=%s"
        book_data = db.fetchone(sql_book, (book_name,))
        if not book_data:
            return False, f"Sách '{book_name}' không tồn tại"
        book = Book.from_dict(book_data)

        if book.available_quantity < 1:
            return False, f"Sách '{book_name}' không đủ số lượng"

        # Tạo borrow slip
        borrow_date = datetime.now().date()
        return_due = borrow_date + timedelta(days=self.BORROW_DAYS)
        slip = BorrowSlip(
            reader_id=reader.reader_id,
            staff_id=1,  # demo
            borrow_date=borrow_date,
            return_due=return_due
        )
        slip_id = self._insert_borrow_slip(slip)

        # Tạo borrow detail
        detail = BorrowDetail(
            slip_id=slip_id,
            book_id=book.book_id,
            quantity=1
        )
        self._insert_borrow_detail(detail)
        self._decrease_stock(book.book_id, 1)

        return True, "Tạo phiếu mượn thành công"

    def update_borrow(self, slip_id, borrow_date, return_date, status):
        sql = """
        UPDATE borrow_slips
        SET borrow_date=%s, return_date=%s, status=%s
        WHERE slip_id=%s
        """
        db.execute_query(sql, (borrow_date, return_date, status, slip_id), commit=True)
        return True, "Cập nhật phiếu thành công"

    def return_books(self, slip_id):
        sql_slip = "SELECT * FROM borrow_slips WHERE slip_id=%s"
        slip = db.fetchone(sql_slip, (slip_id,))
        if not slip:
            return False, "Phiếu mượn không tồn tại"

        # Tăng lại số lượng sách
        sql_details = "SELECT * FROM borrow_details WHERE slip_id=%s"
        details = db.fetchall(sql_details, (slip_id,))
        for d in details:
            sql_inc = "UPDATE books SET available_quantity = available_quantity + %s WHERE book_id=%s"
            db.execute_query(sql_inc, (d["quantity"], d["book_id"]), commit=True)

        sql_update = "UPDATE borrow_slips SET status='RETURNED', return_date=CURDATE() WHERE slip_id=%s"
        db.execute_query(sql_update, (slip_id,), commit=True)
        return True, "Trả sách thành công"

    def get_all_borrows(self):
        sql = """
        SELECT b.slip_id, r.full_name, bk.title AS book_name,
               b.borrow_date, b.return_due, b.return_date, b.status
        FROM borrow_slips b
        JOIN readers r ON b.reader_id=r.reader_id
        JOIN borrow_details bd ON b.slip_id=bd.slip_id
        JOIN books bk ON bd.book_id=bk.book_id
        ORDER BY b.borrow_date DESC
        """
        return db.execute_query(sql, fetch=True)

    # -----------------------
    # Các hàm nội bộ
    # -----------------------
    def _insert_borrow_slip(self, slip: BorrowSlip):
        sql = """
        INSERT INTO borrow_slips (reader_id, staff_id, borrow_date, return_due, status)
        VALUES (%s, %s, %s, %s, %s)
        """
        return db.execute_query(sql, slip.to_tuple(), commit=True)

    def _insert_borrow_detail(self, detail: BorrowDetail):
        sql = """
        INSERT INTO borrow_details (slip_id, book_id, quantity, fine_amount)
        VALUES (%s, %s, %s, %s)
        """
        db.execute_query(sql, detail.to_tuple(), commit=True)

    def _decrease_stock(self, book_id, qty):
        sql = "UPDATE books SET available_quantity = available_quantity - %s WHERE book_id=%s"
        db.execute_query(sql, (qty, book_id), commit=True)
