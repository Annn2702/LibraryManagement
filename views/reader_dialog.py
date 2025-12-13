import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from typing import Optional

from models.reader import Reader, get_all_statuses


class ReaderDialog(tk.Toplevel):
    """Dialog thêm/sửa bạn đọc với giao diện cân đối"""

    def __init__(self, parent, title="Bạn đọc", reader: Optional[Reader] = None):
        super().__init__(parent)
        self.title(title)
        self.geometry("700x800")
        self.resizable(False, False)

        self.reader = reader
        self.result: Optional[Reader] = None
        self.is_edit_mode = reader is not None

        # Style configuration
        self.configure(bg='#f5f5f5')

        self._create_widgets()

        if self.is_edit_mode:
            self._fill_data()

        # Center window
        self.transient(parent)
        self.grab_set()
        self._center_window()

    def _center_window(self):
        """Center dialog on parent"""
        self.update_idletasks()
        x = self.winfo_x() + (self.master.winfo_width() // 2) - (self.winfo_width() // 2)
        y = self.winfo_y() + (self.master.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    def _create_widgets(self):
        """Tạo giao diện form"""
        # ========== HEADER ==========
        header_frame = tk.Frame(self, bg='#1976D2', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        icon = "✏️" if self.is_edit_mode else "➕"
        title_text = f"{icon} {'CẬP NHẬT' if self.is_edit_mode else 'THÊM MỚI'} BẠN ĐỌC"

        tk.Label(
            header_frame,
            text=title_text,
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='#1976D2'
        ).pack(expand=True)

        # ========== MAIN CONTENT ==========
        main_frame = ttk.Frame(self, padding=30)
        main_frame.pack(fill='both', expand=True)

        # Scrollable form frame
        canvas = tk.Canvas(main_frame, highlightthickness=0, bg='#f5f5f5')
        scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw', width=640)
        canvas.configure(yscrollcommand=scrollbar.set)

        # ========== SECTION 1: THÔNG TIN CÁ NHÂN ==========
        section1 = self._create_section(scrollable_frame, "👤 Thông tin cá nhân")
        section1.pack(fill='x', pady=(0, 20))

        # Họ tên *
        self._create_field(
            section1,
            "Họ tên:",
            required=True,
            row=0
        )
        self.full_name_var = tk.StringVar()
        self.full_name_entry = ttk.Entry(
            section1,
            textvariable=self.full_name_var,
            font=('Arial', 10),
            width=50
        )
        self.full_name_entry.grid(row=0, column=1, sticky='ew', pady=8, padx=(10, 0))
        self.full_name_entry.focus()

        # Số điện thoại
        self._create_field(section1, "Số điện thoại:", row=1)
        self.phone_var = tk.StringVar()
        phone_entry = ttk.Entry(
            section1,
            textvariable=self.phone_var,
            font=('Arial', 10),
            width=50
        )
        phone_entry.grid(row=1, column=1, sticky='ew', pady=8, padx=(10, 0))

        # Email
        self._create_field(section1, "Email:", row=2)
        self.email_var = tk.StringVar()
        email_entry = ttk.Entry(
            section1,
            textvariable=self.email_var,
            font=('Arial', 10),
            width=50
        )
        email_entry.grid(row=2, column=1, sticky='ew', pady=8, padx=(10, 0))

        # Địa chỉ
        self._create_field(section1, "Địa chỉ:", row=3)
        address_frame = ttk.Frame(section1)
        address_frame.grid(row=3, column=1, sticky='ew', pady=8, padx=(10, 0))

        self.address_text = tk.Text(
            address_frame,
            height=3,
            font=('Arial', 10),
            wrap='word',
            relief='solid',
            borderwidth=1
        )
        self.address_text.pack(fill='x')

        # Configure grid weights
        section1.columnconfigure(1, weight=1)

        # ========== SECTION 2: THÔNG TIN THẺ ==========
        section2 = self._create_section(scrollable_frame, "📇 Thông tin thẻ thư viện")
        section2.pack(fill='x', pady=(0, 20))

        # Ngày cấp thẻ
        self._create_field(section2, "Ngày cấp thẻ:", row=0)
        date_frame1 = ttk.Frame(section2)
        date_frame1.grid(row=0, column=1, sticky='ew', pady=8, padx=(10, 0))

        self.card_start_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        card_start_entry = ttk.Entry(
            date_frame1,
            textvariable=self.card_start_var,
            font=('Arial', 10),
            width=20
        )
        card_start_entry.pack(side='left', padx=(0, 10))

        ttk.Button(
            date_frame1,
            text="📅 Hôm nay",
            command=lambda: self.card_start_var.set(datetime.now().strftime("%Y-%m-%d")),
            width=12
        ).pack(side='left')

        # Ngày hết hạn
        self._create_field(section2, "Ngày hết hạn:", row=1)
        date_frame2 = ttk.Frame(section2)
        date_frame2.grid(row=1, column=1, sticky='ew', pady=8, padx=(10, 0))

        default_end = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
        self.card_end_var = tk.StringVar(value=default_end)
        card_end_entry = ttk.Entry(
            date_frame2,
            textvariable=self.card_end_var,
            font=('Arial', 10),
            width=20
        )
        card_end_entry.pack(side='left', padx=(0, 10))

        ttk.Button(
            date_frame2,
            text="➕ 1 năm",
            command=self._add_one_year_to_card_end,
            width=12
        ).pack(side='left')

        # Configure grid weights
        section2.columnconfigure(1, weight=1)

        # ========== SECTION 3: TRẠNG THÁI ==========
        section3 = self._create_section(scrollable_frame, "⚙️ Cài đặt tài khoản")
        section3.pack(fill='x', pady=(0, 20))

        # Trạng thái
        self._create_field(section3, "Trạng thái:", row=0)
        status_frame = ttk.Frame(section3)
        status_frame.grid(row=0, column=1, sticky='ew', pady=8, padx=(10, 0))

        self.status_var = tk.StringVar(value="ACTIVE")
        status_combo = ttk.Combobox(
            status_frame,
            textvariable=self.status_var,
            values=get_all_statuses(),
            state='readonly',
            font=('Arial', 10),
            width=20
        )
        status_combo.pack(side='left')

        # Status indicator
        self.status_label = tk.Label(
            status_frame,
            text="🟢 Hoạt động",
            font=('Arial', 9),
            fg='#4CAF50'
        )
        self.status_label.pack(side='left', padx=(10, 0))

        # Bind status change
        self.status_var.trace('w', self._update_status_indicator)

        # Điểm uy tín
        self._create_field(section3, "Điểm uy tín:", row=1)
        reputation_frame = ttk.Frame(section3)
        reputation_frame.grid(row=1, column=1, sticky='ew', pady=8, padx=(10, 0))

        self.reputation_var = tk.IntVar(value=100)

        # Spinbox
        reputation_spin = ttk.Spinbox(
            reputation_frame,
            from_=0,
            to=100,
            textvariable=self.reputation_var,
            width=10,
            font=('Arial', 10)
        )
        reputation_spin.pack(side='left', padx=(0, 5))

        # Label
        tk.Label(
            reputation_frame,
            text="/ 100",
            font=('Arial', 10)
        ).pack(side='left', padx=(0, 15))

        # Progress bar
        self.reputation_progress = ttk.Progressbar(
            reputation_frame,
            length=200,
            mode='determinate',
            maximum=100
        )
        self.reputation_progress.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.reputation_progress['value'] = 100

        # Reputation label
        self.reputation_label = tk.Label(
            reputation_frame,
            text="⭐ Xuất sắc",
            font=('Arial', 9, 'bold'),
            fg='#4CAF50'
        )
        self.reputation_label.pack(side='left')

        # Bind reputation change
        self.reputation_var.trace('w', self._update_reputation_progress)

        # Configure grid weights
        section3.columnconfigure(1, weight=1)

        # Pack canvas and scrollbar
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # ========== FOOTER BUTTONS ==========
        footer_frame = tk.Frame(self, bg='#f5f5f5', height=80)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)

        button_container = ttk.Frame(footer_frame)
        button_container.place(relx=0.5, rely=0.5, anchor='center')

        # Save button
        save_btn = tk.Button(
            button_container,
            text="💾  Lưu",
            command=self._save,
            font=('Arial', 11, 'bold'),
            bg='#4CAF50',
            fg='white',
            activebackground='#45a049',
            activeforeground='white',
            width=15,
            height=2,
            cursor='hand2',
            relief='flat'
        )
        save_btn.pack(side='left', padx=10)

        # Cancel button
        cancel_btn = tk.Button(
            button_container,
            text="❌  Hủy",
            command=self._cancel,
            font=('Arial', 11, 'bold'),
            bg='#f44336',
            fg='white',
            activebackground='#da190b',
            activeforeground='white',
            width=15,
            height=2,
            cursor='hand2',
            relief='flat'
        )
        cancel_btn.pack(side='left', padx=10)

        # Hover effects
        self._add_button_hover(save_btn, '#4CAF50', '#45a049')
        self._add_button_hover(cancel_btn, '#f44336', '#da190b')

        # Bind keyboard shortcuts
        self.bind('<Return>', lambda e: self._save())
        self.bind('<Escape>', lambda e: self._cancel())

    def _create_section(self, parent, title):
        """Tạo section với tiêu đề"""
        section_frame = tk.LabelFrame(
            parent,
            text=title,
            font=('Arial', 11, 'bold'),
            fg='#1976D2',
            bg='white',
            relief='groove',
            borderwidth=2,
            padx=20,
            pady=15
        )
        return section_frame

    def _create_field(self, parent, text, required=False, row=0):
        """Tạo label cho field"""
        label_text = f"{text}"
        if required:
            label_text += " *"

        label = tk.Label(
            parent,
            text=label_text,
            font=('Arial', 10, 'bold' if required else 'normal'),
            fg='#d32f2f' if required else '#333',
            bg='white',
            anchor='w'
        )
        label.grid(row=row, column=0, sticky='w', pady=8)

    def _add_button_hover(self, button, normal_color, hover_color):
        """Thêm hover effect cho button"""

        def on_enter(e):
            button['bg'] = hover_color

        def on_leave(e):
            button['bg'] = normal_color

        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)

    def _update_status_indicator(self, *args):
        """Update status indicator"""
        status = self.status_var.get()

        status_config = {
            'ACTIVE': ('🟢 Hoạt động', '#4CAF50'),
            'SUSPENDED': ('🟡 Tạm khóa', '#FF9800'),
            'EXPIRED': ('🔴 Hết hạn', '#F44336'),
            'BANNED': ('⛔ Cấm', '#9E9E9E')
        }

        text, color = status_config.get(status, ('❓ Không xác định', '#9E9E9E'))
        self.status_label.config(text=text, fg=color)

    def _update_reputation_progress(self, *args):
        """Update progress bar và label khi điểm uy tín thay đổi"""
        try:
            value = self.reputation_var.get()
            self.reputation_progress['value'] = value

            # Update label và color
            if value >= 80:
                text = "⭐ Xuất sắc"
                color = '#4CAF50'
            elif value >= 60:
                text = "👍 Tốt"
                color = '#8BC34A'
            elif value >= 40:
                text = "😐 Trung bình"
                color = '#FF9800'
            elif value >= 20:
                text = "⚠️ Kém"
                color = '#FF5722'
            else:
                text = "❌ Rất kém"
                color = '#F44336'

            self.reputation_label.config(text=text, fg=color)
        except:
            pass

    def _add_one_year_to_card_end(self):
        """Cộng thêm 1 năm vào ngày hết hạn hiện tại"""
        try:
            end_str = self.card_end_var.get().strip()

            if end_str:
                base_date = datetime.strptime(end_str, "%Y-%m-%d")
            else:
                base_date = datetime.now()

            new_end = base_date + timedelta(days=365)
            self.card_end_var.set(new_end.strftime("%Y-%m-%d"))

        except ValueError:
            self.card_end_var.set(
                (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
            )

    def _fill_data(self):
        """Điền dữ liệu khi sửa"""
        if not self.reader:
            return

        self.full_name_var.set(self.reader.full_name or '')
        self.phone_var.set(self.reader.phone or '')
        self.email_var.set(self.reader.email or '')

        if self.reader.address:
            self.address_text.delete('1.0', 'end')
            self.address_text.insert('1.0', self.reader.address)

        self.card_start_var.set(self.reader.card_start or '')
        self.card_end_var.set(self.reader.card_end or '')
        self.status_var.set(self.reader.status or 'ACTIVE')
        self.reputation_var.set(self.reader.reputation_score or 100)

    def _cancel(self):
        """Xử lý khi nhấn Hủy"""
        from tkinter import messagebox

        # Kiểm tra xem có thay đổi gì không
        has_changes = False

        if self.is_edit_mode and self.reader:
            # So sánh với dữ liệu cũ
            if (self.full_name_var.get().strip() != (self.reader.full_name or '') or
                    self.phone_var.get().strip() != (self.reader.phone or '') or
                    self.email_var.get().strip() != (self.reader.email or '')):
                has_changes = True
        else:
            # Mode thêm mới - kiểm tra xem có nhập gì không
            if (self.full_name_var.get().strip() or
                    self.phone_var.get().strip() or
                    self.email_var.get().strip() or
                    self.address_text.get('1.0', 'end').strip()):
                has_changes = True

        if has_changes:
            if messagebox.askyesno(
                    "Xác nhận hủy",
                    "Bạn có thay đổi chưa lưu.\nBạn có chắc chắn muốn hủy?",
                    parent=self
            ):
                self.result = None
                self.destroy()
        else:
            self.result = None
            self.destroy()

    def _save(self):
        """Lưu dữ liệu"""
        # Lấy dữ liệu từ form
        full_name = self.full_name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()
        address = self.address_text.get('1.0', 'end').strip()
        card_start = self.card_start_var.get().strip()
        card_end = self.card_end_var.get().strip()
        status = self.status_var.get()
        reputation = self.reputation_var.get()

        # Validate cơ bản
        if not full_name:
            from tkinter import messagebox
            messagebox.showerror(
                "Lỗi",
                "Vui lòng nhập họ tên!\n\nHọ tên là thông tin bắt buộc.",
                parent=self
            )
            self.full_name_entry.focus()
            return

        # Validate email format (nếu có)
        if email:
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                from tkinter import messagebox
                messagebox.showerror(
                    "Lỗi",
                    "Email không đúng định dạng!\n\nVí dụ: example@email.com",
                    parent=self
                )
                return

        # Validate phone (nếu có)
        if phone:
            if not phone.replace('+', '').replace(' ', '').replace('-', '').isdigit():
                from tkinter import messagebox
                messagebox.showerror(
                    "Lỗi",
                    "Số điện thoại không hợp lệ!\n\nChỉ được nhập số và ký tự +, -, space",
                    parent=self
                )
                return

        # Tạo Reader object
        reader = Reader(
            full_name=full_name,
            phone=phone if phone else None,
            email=email if email else None,
            address=address if address else None,
            card_start=card_start if card_start else None,
            card_end=card_end if card_end else None,
            status=status,
            reputation_score=reputation
        )

        # Nếu là edit mode, giữ lại ID
        if self.is_edit_mode and self.reader:
            reader.reader_id = self.reader.reader_id

        self.result = reader
        self.destroy()