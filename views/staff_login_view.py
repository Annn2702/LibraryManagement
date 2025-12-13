import tkinter as tk
from tkinter import ttk, messagebox

from controllers.staff_auth_controller import StaffAuthController


class StaffLoginView(tk.Toplevel):
    """
    Dialog đăng nhập nhân viên
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.title("🔐 Đăng nhập nhân viên")
        self.geometry("400x350")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.parent = parent
        self.auth = StaffAuthController()
        self.login_success = False

        # Cấu hình style
        self._configure_styles()
        self._build_ui()
        self._center(parent)

    def _configure_styles(self):
        """Cấu hình style cho các widget"""
        style = ttk.Style()

        # Thử các theme khác nhau để nút hiển thị rõ hơn
        try:
            style.theme_use('clam')  # Theme này thường hiển thị nút rõ hơn
        except:
            pass

        # Style cho button đăng nhập - màu xanh nổi bật
        style.configure(
            "Login.TButton",
            font=("Arial", 10, "bold"),
            padding=10,
            relief="raised",
            borderwidth=2
        )

        style.map("Login.TButton",
                  foreground=[('pressed', 'white'), ('active', 'white')],
                  background=[('pressed', '#1e7e34'), ('active', '#28a745')])

        # Style cho button hủy - màu xám
        style.configure(
            "Cancel.TButton",
            font=("Arial", 10),
            padding=10,
            relief="raised",
            borderwidth=2
        )

        style.map("Cancel.TButton",
                  foreground=[('pressed', 'white'), ('active', 'black')],
                  background=[('pressed', '#c82333'), ('active', '#e0e0e0')])

    def _build_ui(self):
        # Main container với padding lớn hơn
        container = ttk.Frame(self, padding=30)
        container.pack(fill="both", expand=True)

        # Header với icon và tiêu đề
        header_frame = ttk.Frame(container)
        header_frame.pack(fill="x", pady=(0, 25))

        ttk.Label(
            header_frame,
            text="🔐",
            font=("Arial", 24)
        ).pack()

        ttk.Label(
            header_frame,
            text="ĐĂNG NHẬP NHÂN VIÊN",
            font=("Arial", 14, "bold"),
            foreground="#2c3e50"
        ).pack(pady=(5, 0))

        # Form container
        form_frame = ttk.Frame(container)
        form_frame.pack(fill="both", expand=True)

        # Username field với icon
        username_frame = ttk.Frame(form_frame)
        username_frame.pack(fill="x", pady=(0, 15))

        ttk.Label(
            username_frame,
            text="👤 Tên đăng nhập",
            font=("Arial", 10)
        ).pack(anchor="w", pady=(0, 5))

        self.username_entry = ttk.Entry(
            username_frame,
            font=("Arial", 11)
        )
        self.username_entry.pack(fill="x", ipady=5)

        # Password field với icon
        password_frame = ttk.Frame(form_frame)
        password_frame.pack(fill="x", pady=(0, 25))

        ttk.Label(
            password_frame,
            text="🔑 Mật khẩu",
            font=("Arial", 10)
        ).pack(anchor="w", pady=(0, 5))

        self.password_entry = ttk.Entry(
            password_frame,
            show="●",
            font=("Arial", 11)
        )
        self.password_entry.pack(fill="x", ipady=5)

        # Buttons frame - Sử dụng tk.Button thay vì ttk.Button để có màu sắc rõ ràng
        btn_frame = ttk.Frame(form_frame)
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
            relief="raised",
            borderwidth=2,
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
            relief="raised",
            borderwidth=2,
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