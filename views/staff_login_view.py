import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageFilter

from controllers.staff_auth_controller import StaffAuthController


class StaffLoginView(tk.Toplevel):
    """
    Dialog đăng nhập nhân viên
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.title("TFO_Library_Management")
        self.geometry("800x600")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.parent = parent
        self.auth = StaffAuthController()
        self.login_success = False

        # Load và set background
        self._setup_background()

        # Cấu hình style
        self._configure_styles()
        self._build_ui()
        self._center(parent)

    def _setup_background(self):
        """Thiết lập background image"""
        try:
            # Load image (thay đường dẫn này bằng đường dẫn thực tế của bạn)
            bg_image = Image.open("assets/Library.jpg")

            # Resize để fit với cửa sổ
            bg_image = bg_image.resize((800, 600), Image.Resampling.LANCZOS)

            # Làm mờ nhẹ để form nổi bật hơn
            bg_image = bg_image.filter(ImageFilter.GaussianBlur(radius=2))

            # Giảm độ sáng
            from PIL import ImageEnhance
            enhancer = ImageEnhance.Brightness(bg_image)
            bg_image = enhancer.enhance(0.7)

            self.bg_photo = ImageTk.PhotoImage(bg_image)

            # Tạo label để hiển thị background
            bg_label = tk.Label(self, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        except Exception as e:
            print(f"Không thể load background: {e}")
            # Fallback: dùng màu nền gradient
            self.configure(bg="#f0f0f0")

    def _configure_styles(self):
        """Cấu hình style cho các widget"""
        style = ttk.Style()

        try:
            style.theme_use('clam')
        except:
            pass

    def _build_ui(self):
        # Main container - Floating card với shadow effect
        main_frame = tk.Frame(
            self,
            bg="white",
            relief="raised",
            borderwidth=0
        )
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=420, height=380)

        # Shadow effect (frame phía sau)
        shadow_frame = tk.Frame(
            self,
            bg="#cccccc",
            relief="flat"
        )
        shadow_frame.place(relx=0.5, rely=0.505, anchor="center", width=425, height=385)
        shadow_frame.lower()

        # Container với padding
        container = tk.Frame(main_frame, bg="white", padx=40, pady=30)
        container.pack(fill="both", expand=True)

        # Header với icon và tiêu đề
        header_frame = tk.Frame(container, bg="white")
        header_frame.pack(fill="x", pady=(0, 25))

        tk.Label(
            header_frame,
            text="🔐",
            font=("Arial", 28),
            bg="white"
        ).pack()

        tk.Label(
            header_frame,
            text="ĐĂNG NHẬP NHÂN VIÊN",
            font=("Arial", 14, "bold"),
            foreground="#2c3e50",
            bg="white"
        ).pack(pady=(5, 0))

        # Form container
        form_frame = tk.Frame(container, bg="white")
        form_frame.pack(fill="both", expand=True)

        # Username field với icon
        username_frame = tk.Frame(form_frame, bg="white")
        username_frame.pack(fill="x", pady=(0, 15))

        tk.Label(
            username_frame,
            text="👤 Tên đăng nhập",
            font=("Arial", 10),
            bg="white",
            fg="#555555"
        ).pack(anchor="w", pady=(0, 5))

        self.username_entry = tk.Entry(
            username_frame,
            font=("Arial", 11),
            relief="solid",
            borderwidth=1,
            bg="#f8f9fa"
        )
        self.username_entry.pack(fill="x", ipady=8)

        # Password field với icon
        password_frame = tk.Frame(form_frame, bg="white")
        password_frame.pack(fill="x", pady=(0, 25))

        tk.Label(
            password_frame,
            text="🔑 Mật khẩu",
            font=("Arial", 10),
            bg="white",
            fg="#555555"
        ).pack(anchor="w", pady=(0, 5))

        self.password_entry = tk.Entry(
            password_frame,
            show="●",
            font=("Arial", 11),
            relief="solid",
            borderwidth=1,
            bg="#f8f9fa"
        )
        self.password_entry.pack(fill="x", ipady=8)

        # Buttons frame
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.pack(fill="x", pady=(15, 0))

        self.btn_login = tk.Button(
            btn_frame,
            text="Đăng nhập",
            command=self._login,
            font=("Arial", 10, "bold"),
            bg="#007bff",
            fg="white",
            activebackground="#0056b3",
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            height=2
        )
        self.btn_login.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.btn_cancel = tk.Button(
            btn_frame,
            text="Hủy",
            command=self._cancel,
            font=("Arial", 10),
            bg="#6c757d",
            fg="white",
            activebackground="#5a6268",
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            height=2
        )
        self.btn_cancel.pack(side="left", expand=True, fill="x", padx=(5, 0))

        # Bind Enter key cho đăng nhập
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self._login())

        # Bind Escape key cho hủy
        self.bind("<Escape>", lambda e: self._cancel())

        self.username_entry.focus()

    def _login(self):
        """Xử lý đăng nhập"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ")
            return

        # Đăng nhập
        if self.auth.login(username, password):
            staff = self.auth.get_current_staff()
            role_name = self._get_role_name(staff['role_id'])

            messagebox.showinfo(
                "Thành công",
                f"Chào mừng {staff['full_name']}!\nChức vụ: {role_name}"
            )

            self.login_success = True

            # ✅ Trigger event để MainWindow refresh permissions
            self.parent.event_generate("<<LoginSuccess>>")

            self.destroy()
        else:
            messagebox.showerror(
                "Thất bại",
                "Sai tài khoản, mật khẩu hoặc tài khoản bị khóa"
            )

    def _cancel(self):
        """Xử lý hủy - thoát dialog"""
        self.destroy()

    def _center(self, parent):
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    @staticmethod
    def _get_role_name(role_id):
        """Chuyển role_id thành tên role"""
        role_names = {
            1: "Admin",
            2: "Thủ thư",
            3: "Nhân viên",
            5: "Super Admin"
        }
        return role_names.get(role_id, f"Role {role_id}")