import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class ISPAutomationSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("V.T. ISP System | Created By - Vikash Tiwari")
        self.root.geometry("1100x750")
        self.root.configure(bg='#f5f5f5')
        
        # Database setup
        self.conn = sqlite3.connect('isp_database.db')
        self.create_tables()
        
        # Style configuration - Modern theme with custom colors
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors
        self.primary_color = '#3a7ca5'
        self.secondary_color = '#2f6690'
        self.accent_color = '#d9dcd6'
        self.background_color = '#f5f5f5'
        self.text_color = '#333333'
        self.success_color = '#4caf50'
        self.warning_color = '#ff9800'
        self.error_color = '#f44336'
        
        # Configure styles
        self.style.configure('.', background=self.background_color, foreground=self.text_color)
        self.style.configure('TFrame', background=self.background_color)
        self.style.configure('TLabel', background=self.background_color, font=('Segoe UI', 10))
        self.style.configure('TButton', font=('Segoe UI', 10), padding=6, 
                           background=self.primary_color, foreground='white')
        self.style.map('TButton', 
                      background=[('active', self.secondary_color), ('disabled', '#cccccc')],
                      foreground=[('disabled', '#888888')])
        self.style.configure('Header.TLabel', font=('Segoe UI', 16, 'bold'), 
                           foreground=self.primary_color)
        self.style.configure('Treeview', rowheight=28, font=('Segoe UI', 9))
        self.style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'), 
                           background=self.primary_color, foreground='white')
        self.style.map('Treeview.Heading', 
                      background=[('active', self.secondary_color)])
        self.style.configure('TNotebook', background=self.background_color)
        self.style.configure('TNotebook.Tab', padding=[10, 5], font=('Segoe UI', 10),
                           background=self.accent_color, foreground=self.text_color)
        self.style.map('TNotebook.Tab', 
                      background=[('selected', self.primary_color), ('active', self.secondary_color)],
                      foreground=[('selected', 'white')])
        self.style.configure('TCombobox', fieldbackground='white', background='white')
        self.style.configure('TEntry', fieldbackground='white')
        self.style.configure('TLabelframe', font=('Segoe UI', 10, 'bold'), 
                            foreground=self.primary_color)
        self.style.configure('TLabelframe.Label', foreground=self.primary_color)
        
        # Main container with subtle shadow effect
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Add a subtle status bar at the bottom
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self.main_frame, textvariable=self.status_var, 
                                   relief=tk.SUNKEN, anchor=tk.W, 
                                   font=('Segoe UI', 9), foreground='#666666')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=(0, 5))
        self.status_var.set("Ready")
        
        # Notebook for tabs with modern styling
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_customer_tab()
        self.create_plans_tab()
        self.create_complaints_tab()
        self.create_billing_tab()
        self.create_troubleshooting_tab()
        
        # Load initial data
        self.load_customers()
        self.load_plans()
        self.load_complaints()
         # Add a subtle status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self.main_frame, textvariable=self.status_var, 
                                   relief=tk.SUNKEN, anchor=tk.W, 
                                   font=('Segoe UI', 9), foreground='#666666')
        self.status_bar.pack(fill=tk.X, padx=5, pady=(0, 5))
        self.status_var.set("Ready")
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Customers table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            plan_id INTEGER,
            registration_date TEXT,
            FOREIGN KEY (plan_id) REFERENCES plans(plan_id)
        )
        ''')
        
        # Plans table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS plans (
            plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            speed TEXT NOT NULL,
            price REAL NOT NULL,
            data_limit TEXT,
            description TEXT
        )
        ''')
        
        # Complaints table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            complaint_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL,
            resolution TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
        ''')
        
        # Billing table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS billing (
            bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            due_date TEXT NOT NULL,
            paid INTEGER DEFAULT 0,
            payment_date TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
        ''')
        
        self.conn.commit()
    
    def create_dashboard_tab(self):
        self.dashboard_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_tab, text="Dashboard")
        
        # Header with accent color
        header_frame = ttk.Frame(self.dashboard_tab)
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        header = ttk.Label(header_frame, text="V.T. Internet Services Dashboard - Welcome Mr. Vikash Tiwari (Admin)", style='Header.TLabel')
        header.pack(side=tk.LEFT)
        
        # Refresh button
        refresh_btn = ttk.Button(header_frame, text="Refresh", command=self.update_dashboard_stats,
                               style='Accent.TButton')
        refresh_btn.pack(side=tk.RIGHT, padx=5)
        
        # Stats frame with card-like appearance
        stats_frame = ttk.LabelFrame(self.dashboard_tab, text="System Overview", padding=10)
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Customer stats card
        customer_frame = ttk.Frame(stats_frame, style='Card.TFrame')
        customer_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(customer_frame, text="Customers", font=('Segoe UI', 11, 'bold'), 
                 foreground=self.primary_color).pack(pady=(5, 10))
        
        self.total_customers_label = ttk.Label(customer_frame, text="Total: 0", font=('Segoe UI', 10))
        self.total_customers_label.pack(pady=5)
        
        self.active_customers_label = ttk.Label(customer_frame, text="Active: 0", font=('Segoe UI', 10))
        self.active_customers_label.pack(pady=5)
        
        # Plans stats card
        plans_frame = ttk.Frame(stats_frame, style='Card.TFrame')
        plans_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(plans_frame, text="Plans", font=('Segoe UI', 11, 'bold'), 
                 foreground=self.primary_color).pack(pady=(5, 10))
        
        self.total_plans_label = ttk.Label(plans_frame, text="Available: 0", font=('Segoe UI', 10))
        self.total_plans_label.pack(pady=5)
        
        self.popular_plan_label = ttk.Label(plans_frame, text="Popular: None", font=('Segoe UI', 10))
        self.popular_plan_label.pack(pady=5)
        
        # Complaints stats card
        complaints_frame = ttk.Frame(stats_frame, style='Card.TFrame')
        complaints_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(complaints_frame, text="Complaints", font=('Segoe UI', 11, 'bold'), 
                 foreground=self.primary_color).pack(pady=(5, 10))
        
        self.open_complaints_label = ttk.Label(complaints_frame, text="Open: 0", font=('Segoe UI', 10))
        self.open_complaints_label.pack(pady=5)
        
        self.resolved_complaints_label = ttk.Label(complaints_frame, text="Resolved: 0", font=('Segoe UI', 10))
        self.resolved_complaints_label.pack(pady=5)
        
        # Recent activity frame with subtle border
        activity_frame = ttk.LabelFrame(self.dashboard_tab, text="Recent Activity", padding=10)
        activity_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add a scrollbar to the activity tree
        tree_scroll = ttk.Scrollbar(activity_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.activity_tree = ttk.Treeview(activity_frame, columns=('type', 'details', 'date'), 
                                        show='headings', yscrollcommand=tree_scroll.set)
        self.activity_tree.heading('type', text='Activity Type')
        self.activity_tree.heading('details', text='Details')
        self.activity_tree.heading('date', text='Date')
        self.activity_tree.column('type', width=150, anchor=tk.W)
        self.activity_tree.column('details', width=400, anchor=tk.W)
        self.activity_tree.column('date', width=150, anchor=tk.W)
        self.activity_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        tree_scroll.config(command=self.activity_tree.yview)
        
        # Configure tag colors for different activity types
        self.activity_tree.tag_configure('customer', background='#e3f2fd')
        self.activity_tree.tag_configure('plan', background='#e8f5e9')
        self.activity_tree.tag_configure('complaint', background='#fff3e0')
        self.activity_tree.tag_configure('billing', background='#f3e5f5')
        
        # Update dashboard stats
        self.update_dashboard_stats()
    
    def create_customer_tab(self):
        self.customer_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.customer_tab, text="Customers")
        
        # Create a paned window for better layout management
        paned = ttk.PanedWindow(self.customer_tab, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left pane - Customer management form
        left_pane = ttk.Frame(paned)
        paned.add(left_pane, weight=1)
        
        # Customer management frame with modern styling
        management_frame = ttk.LabelFrame(left_pane, text="Customer Management", padding=10)
        management_frame.pack(fill=tk.BOTH, padx=5, pady=5)
        
        # Form frame with grid layout
        form_frame = ttk.Frame(management_frame)
        form_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Form fields with better spacing
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=8, sticky=tk.W)
        self.customer_name = ttk.Entry(form_frame, width=30, font=('Segoe UI', 10))
        self.customer_name.grid(row=0, column=1, padx=5, pady=8, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Address:").grid(row=1, column=0, padx=5, pady=8, sticky=tk.W)
        self.customer_address = ttk.Entry(form_frame, width=30, font=('Segoe UI', 10))
        self.customer_address.grid(row=1, column=1, padx=5, pady=8, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Phone:").grid(row=2, column=0, padx=5, pady=8, sticky=tk.W)
        self.customer_phone = ttk.Entry(form_frame, width=30, font=('Segoe UI', 10))
        self.customer_phone.grid(row=2, column=1, padx=5, pady=8, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Email:").grid(row=3, column=0, padx=5, pady=8, sticky=tk.W)
        self.customer_email = ttk.Entry(form_frame, width=30, font=('Segoe UI', 10))
        self.customer_email.grid(row=3, column=1, padx=5, pady=8, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Plan:").grid(row=4, column=0, padx=5, pady=8, sticky=tk.W)
        self.customer_plan = ttk.Combobox(form_frame, width=28, font=('Segoe UI', 10))
        self.customer_plan.grid(row=4, column=1, padx=5, pady=8, sticky=tk.EW)
        
        # Buttons frame with consistent spacing
        buttons_frame = ttk.Frame(management_frame)
        buttons_frame.pack(fill=tk.X, padx=5, pady=(10, 5))
        
        ttk.Button(buttons_frame, text="Add Customer", command=self.add_customer).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(buttons_frame, text="Update Customer", command=self.update_customer).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(buttons_frame, text="Delete Customer", command=self.delete_customer).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(buttons_frame, text="Clear Form", command=self.clear_customer_form).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Right pane - Customer list
        right_pane = ttk.Frame(paned)
        paned.add(right_pane, weight=2)
        
        # Customers list frame with scrollbar
        list_frame = ttk.LabelFrame(right_pane, text="Customer List", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add scrollbars
        tree_scroll_y = ttk.Scrollbar(list_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree_scroll_x = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.customers_tree = ttk.Treeview(list_frame, columns=('id', 'name', 'address', 'phone', 'email', 'plan'), 
                                         show='headings', yscrollcommand=tree_scroll_y.set,
                                         xscrollcommand=tree_scroll_x.set)
        
        # Configure columns
        self.customers_tree.heading('id', text='ID')
        self.customers_tree.heading('name', text='Name')
        self.customers_tree.heading('address', text='Address')
        self.customers_tree.heading('phone', text='Phone')
        self.customers_tree.heading('email', text='Email')
        self.customers_tree.heading('plan', text='Plan')
        
        self.customers_tree.column('id', width=50, anchor=tk.CENTER)
        self.customers_tree.column('name', width=150, anchor=tk.W)
        self.customers_tree.column('address', width=200, anchor=tk.W)
        self.customers_tree.column('phone', width=100, anchor=tk.W)
        self.customers_tree.column('email', width=150, anchor=tk.W)
        self.customers_tree.column('plan', width=150, anchor=tk.W)
        
        self.customers_tree.pack(fill=tk.BOTH, expand=True)
        
        tree_scroll_y.config(command=self.customers_tree.yview)
        tree_scroll_x.config(command=self.customers_tree.xview)
        
        # Bind selection event
        self.customers_tree.bind('<<TreeviewSelect>>', self.on_customer_select)
        
        # Add alternating row colors
        self.customers_tree.tag_configure('oddrow', background='#f5f5f5')
        self.customers_tree.tag_configure('evenrow', background='white')
    
    def create_plans_tab(self):
        self.plans_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.plans_tab, text="Plans")
        
        # Create a paned window for better layout management
        paned = ttk.PanedWindow(self.plans_tab, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left pane - Plan management form
        left_pane = ttk.Frame(paned)
        paned.add(left_pane, weight=1)
        
        # Plan management frame
        management_frame = ttk.LabelFrame(left_pane, text="Plan Management", padding=10)
        management_frame.pack(fill=tk.BOTH, padx=5, pady=5)
        
        # Form frame
        form_frame = ttk.Frame(management_frame)
        form_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Form fields with better spacing
        ttk.Label(form_frame, text="Plan Name:").grid(row=0, column=0, padx=5, pady=8, sticky=tk.W)
        self.plan_name = ttk.Entry(form_frame, width=30, font=('Segoe UI', 10))
        self.plan_name.grid(row=0, column=1, padx=5, pady=8, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Speed:").grid(row=1, column=0, padx=5, pady=8, sticky=tk.W)
        self.plan_speed = ttk.Entry(form_frame, width=30, font=('Segoe UI', 10))
        self.plan_speed.grid(row=1, column=1, padx=5, pady=8, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Price:").grid(row=2, column=0, padx=5, pady=8, sticky=tk.W)
        self.plan_price = ttk.Entry(form_frame, width=30, font=('Segoe UI', 10))
        self.plan_price.grid(row=2, column=1, padx=5, pady=8, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Data Limit:").grid(row=3, column=0, padx=5, pady=8, sticky=tk.W)
        self.plan_data_limit = ttk.Entry(form_frame, width=30, font=('Segoe UI', 10))
        self.plan_data_limit.grid(row=3, column=1, padx=5, pady=8, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Description:").grid(row=4, column=0, padx=5, pady=8, sticky=tk.W)
        self.plan_description = ttk.Entry(form_frame, width=30, font=('Segoe UI', 10))
        self.plan_description.grid(row=4, column=1, padx=5, pady=8, sticky=tk.EW)
        
        # Buttons frame
        buttons_frame = ttk.Frame(management_frame)
        buttons_frame.pack(fill=tk.X, padx=5, pady=(10, 5))
        
        ttk.Button(buttons_frame, text="Add Plan", command=self.add_plan).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(buttons_frame, text="Update Plan", command=self.update_plan).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(buttons_frame, text="Delete Plan", command=self.delete_plan).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(buttons_frame, text="Clear Form", command=self.clear_plan_form).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Right pane - Plans list
        right_pane = ttk.Frame(paned)
        paned.add(right_pane, weight=2)
        
        # Plans list frame
        list_frame = ttk.LabelFrame(right_pane, text="Available Plans", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add scrollbars
        tree_scroll_y = ttk.Scrollbar(list_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree_scroll_x = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.plans_tree = ttk.Treeview(list_frame, columns=('id', 'name', 'speed', 'price', 'data_limit', 'description'), 
                                     show='headings', yscrollcommand=tree_scroll_y.set,
                                     xscrollcommand=tree_scroll_x.set)
        
        # Configure columns
        self.plans_tree.heading('id', text='ID')
        self.plans_tree.heading('name', text='Name')
        self.plans_tree.heading('speed', text='Speed')
        self.plans_tree.heading('price', text='Price')
        self.plans_tree.heading('data_limit', text='Data Limit')
        self.plans_tree.heading('description', text='Description')
        
        self.plans_tree.column('id', width=50, anchor=tk.CENTER)
        self.plans_tree.column('name', width=150, anchor=tk.W)
        self.plans_tree.column('speed', width=100, anchor=tk.W)
        self.plans_tree.column('price', width=80, anchor=tk.E)
        self.plans_tree.column('data_limit', width=100, anchor=tk.W)
        self.plans_tree.column('description', width=250, anchor=tk.W)
        
        self.plans_tree.pack(fill=tk.BOTH, expand=True)
        
        tree_scroll_y.config(command=self.plans_tree.yview)
        tree_scroll_x.config(command=self.plans_tree.xview)
        
        # Bind selection event
        self.plans_tree.bind('<<TreeviewSelect>>', self.on_plan_select)
        
        # Add alternating row colors
        self.plans_tree.tag_configure('oddrow', background='#f5f5f5')
        self.plans_tree.tag_configure('evenrow', background='white')
    
    def create_complaints_tab(self):
        self.complaints_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.complaints_tab, text="Complaints")
        
        # Create a paned window for better layout management
        paned = ttk.PanedWindow(self.complaints_tab, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left pane - Complaint management form
        left_pane = ttk.Frame(paned)
        paned.add(left_pane, weight=1)
        
        # Complaint management frame
        management_frame = ttk.LabelFrame(left_pane, text="Complaint Management", padding=10)
        management_frame.pack(fill=tk.BOTH, padx=5, pady=5)
        
        # Form frame
        form_frame = ttk.Frame(management_frame)
        form_frame.pack(fill=tk.BOTH, padx=5, pady=5)
        
        # Form fields with better spacing
        ttk.Label(form_frame, text="Customer:").grid(row=0, column=0, padx=5, pady=8, sticky=tk.W)
        self.complaint_customer = ttk.Combobox(form_frame, width=25, font=('Segoe UI', 10))
        self.complaint_customer.grid(row=0, column=1, padx=5, pady=8, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Description:").grid(row=1, column=0, padx=5, pady=8, sticky=tk.NW)
        self.complaint_description = tk.Text(form_frame, width=40, height=5, wrap=tk.WORD, 
                                           font=('Segoe UI', 10), padx=5, pady=5)
        self.complaint_description.grid(row=1, column=1, padx=5, pady=8, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Status:").grid(row=2, column=0, padx=5, pady=8, sticky=tk.W)
        self.complaint_status = ttk.Combobox(form_frame, width=25, font=('Segoe UI', 10),
                                           values=['Open', 'In Progress', 'Resolved'])
        self.complaint_status.grid(row=2, column=1, padx=5, pady=8, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Resolution:").grid(row=3, column=0, padx=5, pady=8, sticky=tk.NW)
        self.complaint_resolution = tk.Text(form_frame, width=40, height=5, wrap=tk.WORD, 
                                          font=('Segoe UI', 10), padx=5, pady=5)
        self.complaint_resolution.grid(row=3, column=1, padx=5, pady=8, sticky=tk.EW)
        
        # Buttons frame
        buttons_frame = ttk.Frame(management_frame)
        buttons_frame.pack(fill=tk.X, padx=5, pady=(10, 5))
        
        ttk.Button(buttons_frame, text="Add Complaint", command=self.add_complaint).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(buttons_frame, text="Update Complaint", command=self.update_complaint).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(buttons_frame, text="Resolve Complaint", command=self.resolve_complaint).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(buttons_frame, text="Clear Form", command=self.clear_complaint_form).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Right pane - Complaints list
        right_pane = ttk.Frame(paned)
        paned.add(right_pane, weight=2)
        
        # Complaints list frame
        list_frame = ttk.LabelFrame(right_pane, text="Customer Complaints", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add scrollbars
        tree_scroll_y = ttk.Scrollbar(list_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree_scroll_x = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.complaints_tree = ttk.Treeview(list_frame, columns=('id', 'customer', 'date', 'status', 'description'), 
                                          show='headings', yscrollcommand=tree_scroll_y.set,
                                          xscrollcommand=tree_scroll_x.set)
        
        # Configure columns
        self.complaints_tree.heading('id', text='ID')
        self.complaints_tree.heading('customer', text='Customer')
        self.complaints_tree.heading('date', text='Date')
        self.complaints_tree.heading('status', text='Status')
        self.complaints_tree.heading('description', text='Description')
        
        self.complaints_tree.column('id', width=50, anchor=tk.CENTER)
        self.complaints_tree.column('customer', width=150, anchor=tk.W)
        self.complaints_tree.column('date', width=100, anchor=tk.W)
        self.complaints_tree.column('status', width=100, anchor=tk.W)
        self.complaints_tree.column('description', width=400, anchor=tk.W)
        
        self.complaints_tree.pack(fill=tk.BOTH, expand=True)
        
        tree_scroll_y.config(command=self.complaints_tree.yview)
        tree_scroll_x.config(command=self.complaints_tree.xview)
        
        # Bind selection event
        self.complaints_tree.bind('<<TreeviewSelect>>', self.on_complaint_select)
        
        # Add status-based row coloring
        self.complaints_tree.tag_configure('Open', foreground=self.error_color)
        self.complaints_tree.tag_configure('In Progress', foreground=self.warning_color)
        self.complaints_tree.tag_configure('Resolved', foreground=self.success_color)
    
    def create_billing_tab(self):
        self.billing_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.billing_tab, text="Billing")
        
        # Create a paned window for better layout management
        paned = ttk.PanedWindow(self.billing_tab, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left pane - Billing management form
        left_pane = ttk.Frame(paned)
        paned.add(left_pane, weight=1)
        
        # Billing management frame
        management_frame = ttk.LabelFrame(left_pane, text="Billing Management", padding=10)
        management_frame.pack(fill=tk.BOTH, padx=5, pady=5)
        
        # Form frame
        form_frame = ttk.Frame(management_frame)
        form_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Form fields with better spacing
        ttk.Label(form_frame, text="Customer:").grid(row=0, column=0, padx=5, pady=8, sticky=tk.W)
        self.billing_customer = ttk.Combobox(form_frame, width=25, font=('Segoe UI', 10))
        self.billing_customer.grid(row=0, column=1, padx=5, pady=8, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Amount:").grid(row=1, column=0, padx=5, pady=8, sticky=tk.W)
        self.billing_amount = ttk.Entry(form_frame, width=25, font=('Segoe UI', 10))
        self.billing_amount.grid(row=1, column=1, padx=5, pady=8, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Due Date:").grid(row=2, column=0, padx=5, pady=8, sticky=tk.W)
        self.billing_due_date = ttk.Entry(form_frame, width=25, font=('Segoe UI', 10))
        self.billing_due_date.grid(row=2, column=1, padx=5, pady=8, sticky=tk.EW)
        
        # Buttons frame
        buttons_frame = ttk.Frame(management_frame)
        buttons_frame.pack(fill=tk.X, padx=5, pady=(10, 5))
        
        ttk.Button(buttons_frame, text="Generate Bill", command=self.generate_bill).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(buttons_frame, text="Mark as Paid", command=self.mark_bill_paid).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(buttons_frame, text="Clear Form", command=self.clear_billing_form).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Right pane - Bills list
        right_pane = ttk.Frame(paned)
        paned.add(right_pane, weight=2)
        
        # Bills list frame
        list_frame = ttk.LabelFrame(right_pane, text="Customer Bills", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add scrollbars
        tree_scroll_y = ttk.Scrollbar(list_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree_scroll_x = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.bills_tree = ttk.Treeview(list_frame, columns=('id', 'customer', 'amount', 'due_date', 'status'), 
                                     show='headings', yscrollcommand=tree_scroll_y.set,
                                     xscrollcommand=tree_scroll_x.set)
        
        # Configure columns
        self.bills_tree.heading('id', text='ID')
        self.bills_tree.heading('customer', text='Customer')
        self.bills_tree.heading('amount', text='Amount')
        self.bills_tree.heading('due_date', text='Due Date')
        self.bills_tree.heading('status', text='Status')
        
        self.bills_tree.column('id', width=50, anchor=tk.CENTER)
        self.bills_tree.column('customer', width=150, anchor=tk.W)
        self.bills_tree.column('amount', width=100, anchor=tk.E)
        self.bills_tree.column('due_date', width=100, anchor=tk.W)
        self.bills_tree.column('status', width=100, anchor=tk.W)
        
        self.bills_tree.pack(fill=tk.BOTH, expand=True)
        
        tree_scroll_y.config(command=self.bills_tree.yview)
        tree_scroll_x.config(command=self.bills_tree.xview)
        
        # Bind selection event
        self.bills_tree.bind('<<TreeviewSelect>>', self.on_bill_select)
        
        # Add status-based row coloring
        self.bills_tree.tag_configure('Paid', foreground=self.success_color)
        self.bills_tree.tag_configure('Unpaid', foreground=self.error_color)
        
        # Load bills
        self.load_bills()
    
    def create_troubleshooting_tab(self):
        self.troubleshooting_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.troubleshooting_tab, text="Troubleshooting")
        
        # Header with accent color
        header_frame = ttk.Frame(self.troubleshooting_tab)
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        header = ttk.Label(header_frame, text="Internet Connection Troubleshooting", style='Header.TLabel')
        header.pack(side=tk.LEFT)
        
        # Issue selection frame with card-like appearance
        issue_frame = ttk.LabelFrame(self.troubleshooting_tab, text="Select Your Issue", padding=10)
        issue_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.issue_var = tk.StringVar()
        
        # Radio buttons with better spacing
        ttk.Radiobutton(issue_frame, text="No Internet Connection", variable=self.issue_var, 
                       value="no_connection").pack(anchor=tk.W, padx=5, pady=3, fill=tk.X)
        ttk.Radiobutton(issue_frame, text="Slow Internet Speed", variable=self.issue_var, 
                       value="slow_speed").pack(anchor=tk.W, padx=5, pady=3, fill=tk.X)
        ttk.Radiobutton(issue_frame, text="Intermittent Connection", variable=self.issue_var, 
                       value="intermittent").pack(anchor=tk.W, padx=5, pady=3, fill=tk.X)
        ttk.Radiobutton(issue_frame, text="Can't Connect to Specific Website", variable=self.issue_var, 
                       value="specific_website").pack(anchor=tk.W, padx=5, pady=3, fill=tk.X)
        ttk.Radiobutton(issue_frame, text="Router Issues", variable=self.issue_var, 
                       value="router").pack(anchor=tk.W, padx=5, pady=3, fill=tk.X)
        
        # Troubleshoot button with accent color
        ttk.Button(issue_frame, text="Troubleshoot", command=self.run_troubleshooting,
                  style='Accent.TButton').pack(pady=10, fill=tk.X)
        
        # Results frame with subtle border
        self.results_frame = ttk.LabelFrame(self.troubleshooting_tab, text="Troubleshooting Steps", padding=10)
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add scrollbar to results text
        text_scroll = ttk.Scrollbar(self.results_frame)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.results_text = tk.Text(self.results_frame, wrap=tk.WORD, height=10, 
                                  font=('Segoe UI', 10), yscrollcommand=text_scroll.set,
                                  padx=5, pady=5)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        text_scroll.config(command=self.results_text.yview)
        
        # Schedule technician button with accent color
        self.schedule_button = ttk.Button(self.troubleshooting_tab, text="Schedule Technician Visit", 
                                         command=self.schedule_technician, state=tk.DISABLED,
                                         style='Accent.TButton')
        self.schedule_button.pack(pady=10, padx=10, fill=tk.X)
    
    # Database operations (unchanged from original)
    def load_customers(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT c.customer_id, c.name, c.address, c.phone, c.email, p.name 
        FROM customers c LEFT JOIN plans p ON c.plan_id = p.plan_id
        ''')
        rows = cursor.fetchall()
        
        # Clear existing data
        for item in self.customers_tree.get_children():
            self.customers_tree.delete(item)
        
        # Insert new data with alternating row colors
        for i, row in enumerate(rows):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.customers_tree.insert('', tk.END, values=row, tags=(tag,))
        
        # Update customer comboboxes
        customer_names = [row[1] for row in rows]
        self.complaint_customer['values'] = customer_names
        self.billing_customer['values'] = customer_names
        
        # Update plan combobox
        cursor.execute('SELECT plan_id, name FROM plans')
        plans = cursor.fetchall()
        self.customer_plan['values'] = [f"{p[0]} - {p[1]}" for p in plans]
        
        self.status_var.set(f"Loaded {len(rows)} customers")
    
    def load_plans(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM plans')
        rows = cursor.fetchall()
        
        # Clear existing data
        for item in self.plans_tree.get_children():
            self.plans_tree.delete(item)
        
        # Insert new data with alternating row colors
        for i, row in enumerate(rows):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.plans_tree.insert('', tk.END, values=row, tags=(tag,))
        
        # Update plan combobox
        self.customer_plan['values'] = [f"{row[0]} - {row[1]}" for row in rows]
        
        self.status_var.set(f"Loaded {len(rows)} plans")
    
    def load_complaints(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT co.complaint_id, c.name, co.date, co.status, co.description 
        FROM complaints co JOIN customers c ON co.customer_id = c.customer_id
        ''')
        rows = cursor.fetchall()
        
        # Clear existing data
        for item in self.complaints_tree.get_children():
            self.complaints_tree.delete(item)
        
        # Insert new data with status-based coloring
        for row in rows:
            self.complaints_tree.insert('', tk.END, values=row, tags=(row[3],))
        
        self.status_var.set(f"Loaded {len(rows)} complaints")
    
    def load_bills(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT b.bill_id, c.name, b.amount, b.due_date, 
               CASE WHEN b.paid = 1 THEN 'Paid' ELSE 'Unpaid' END as status
        FROM billing b JOIN customers c ON b.customer_id = c.customer_id
        ''')
        rows = cursor.fetchall()
        
        # Clear existing data
        for item in self.bills_tree.get_children():
            self.bills_tree.delete(item)
        
        # Insert new data with status-based coloring
        for row in rows:
            self.bills_tree.insert('', tk.END, values=row, tags=(row[4],))
        
        self.status_var.set(f"Loaded {len(rows)} bills")
    
    def update_dashboard_stats(self):
        cursor = self.conn.cursor()
        
        # Customer stats
        cursor.execute('SELECT COUNT(*) FROM customers')
        total_customers = cursor.fetchone()[0]
        self.total_customers_label.config(text=f"Total: {total_customers}")
        
        cursor.execute('SELECT COUNT(*) FROM customers WHERE plan_id IS NOT NULL')
        active_customers = cursor.fetchone()[0]
        self.active_customers_label.config(text=f"Active: {active_customers}")
        
        # Plan stats
        cursor.execute('SELECT COUNT(*) FROM plans')
        total_plans = cursor.fetchone()[0]
        self.total_plans_label.config(text=f"Available: {total_plans}")
        
        cursor.execute('''
        SELECT p.name, COUNT(c.customer_id) as customer_count
        FROM plans p LEFT JOIN customers c ON p.plan_id = c.plan_id
        GROUP BY p.plan_id
        ORDER BY customer_count DESC
        LIMIT 1
        ''')
        popular_plan = cursor.fetchone()
        if popular_plan and popular_plan[1] > 0:
            self.popular_plan_label.config(text=f"Popular: {popular_plan[0]} ({popular_plan[1]})")
        else:
            self.popular_plan_label.config(text="Popular: None")
        
        # Complaint stats
        cursor.execute("SELECT COUNT(*) FROM complaints WHERE status != 'Resolved'")
        open_complaints = cursor.fetchone()[0]
        self.open_complaints_label.config(text=f"Open: {open_complaints}")
        
        cursor.execute("SELECT COUNT(*) FROM complaints WHERE status = 'Resolved'")
        resolved_complaints = cursor.fetchone()[0]
        self.resolved_complaints_label.config(text=f"Resolved: {resolved_complaints}")
        
        # Recent activity
        cursor.execute('''
        SELECT 'New Customer' as type, name as details, registration_date as date
        FROM customers
        ORDER BY registration_date DESC
        LIMIT 5
        ''')
        customer_activity = cursor.fetchall()
        
        cursor.execute('''
        SELECT 'New Complaint' as type, 
               (SELECT name FROM customers WHERE customer_id = c.customer_id) || ' - ' || 
               SUBSTR(c.description, 1, 30) || '...' as details, 
               c.date
        FROM complaints c
        ORDER BY c.date DESC
        LIMIT 5
        ''')
        complaint_activity = cursor.fetchall()
        
        # Clear activity tree
        for item in self.activity_tree.get_children():
            self.activity_tree.delete(item)
        
        # Add activities with appropriate tags
        for activity in customer_activity:
            self.activity_tree.insert('', tk.END, values=activity, tags=('customer',))
        
        for activity in complaint_activity:
            self.activity_tree.insert('', tk.END, values=activity, tags=('complaint',))
        
        self.status_var.set("Dashboard stats updated")
    
    # Customer operations (unchanged from original except for status bar updates)
    def add_customer(self):
        name = self.customer_name.get()
        address = self.customer_address.get()
        phone = self.customer_phone.get()
        email = self.customer_email.get()
        plan = self.customer_plan.get()
        
        if not name or not address or not phone or not email:
            messagebox.showerror("Error", "Please fill all required fields")
            return
        
        try:
            cursor = self.conn.cursor()
            
            # Extract plan_id if selected
            plan_id = None
            if plan:
                plan_id = int(plan.split(' - ')[0])
            
            # Insert customer
            registration_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('''
            INSERT INTO customers (name, address, phone, email, plan_id, registration_date)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, address, phone, email, plan_id, registration_date))
            
            self.conn.commit()
            self.load_customers()
            self.update_dashboard_stats()
            self.clear_customer_form()
            messagebox.showinfo("Success", "Customer added successfully")
            
            # Log activity
            self.log_activity(f"Added customer: {name}")
            self.status_var.set(f"Customer {name} added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add customer: {str(e)}")
            self.status_var.set("Error adding customer")
    
    def update_customer(self):
        selected = self.customers_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a customer to update")
            return
        
        customer_id = self.customers_tree.item(selected[0])['values'][0]
        name = self.customer_name.get()
        address = self.customer_address.get()
        phone = self.customer_phone.get()
        email = self.customer_email.get()
        plan = self.customer_plan.get()
        
        if not name or not address or not phone or not email:
            messagebox.showerror("Error", "Please fill all required fields")
            return
        
        try:
            cursor = self.conn.cursor()
            
            # Extract plan_id if selected
            plan_id = None
            if plan:
                plan_id = int(plan.split(' - ')[0])
            
            # Update customer
            cursor.execute('''
            UPDATE customers 
            SET name=?, address=?, phone=?, email=?, plan_id=?
            WHERE customer_id=?
            ''', (name, address, phone, email, plan_id, customer_id))
            
            self.conn.commit()
            self.load_customers()
            self.update_dashboard_stats()
            messagebox.showinfo("Success", "Customer updated successfully")
            
            # Log activity
            self.log_activity(f"Updated customer: {name}")
            self.status_var.set(f"Customer {name} updated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update customer: {str(e)}")
            self.status_var.set("Error updating customer")
    
    def delete_customer(self):
        selected = self.customers_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a customer to delete")
            return
        
        customer_id = self.customers_tree.item(selected[0])['values'][0]
        customer_name = self.customers_tree.item(selected[0])['values'][1]
        
        if not messagebox.askyesno("Confirm", f"Are you sure you want to delete customer {customer_name}?"):
            return
        
        try:
            cursor = self.conn.cursor()
            
            # First delete related records
            cursor.execute('DELETE FROM complaints WHERE customer_id=?', (customer_id,))
            cursor.execute('DELETE FROM billing WHERE customer_id=?', (customer_id,))
            
            # Then delete customer
            cursor.execute('DELETE FROM customers WHERE customer_id=?', (customer_id,))
            
            self.conn.commit()
            self.load_customers()
            self.load_complaints()
            self.load_bills()
            self.update_dashboard_stats()
            self.clear_customer_form()
            messagebox.showinfo("Success", "Customer deleted successfully")
            
            # Log activity
            self.log_activity(f"Deleted customer: {customer_name}")
            self.status_var.set(f"Customer {customer_name} deleted successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete customer: {str(e)}")
            self.status_var.set("Error deleting customer")
    
    def clear_customer_form(self):
        self.customer_name.delete(0, tk.END)
        self.customer_address.delete(0, tk.END)
        self.customer_phone.delete(0, tk.END)
        self.customer_email.delete(0, tk.END)
        self.customer_plan.set('')
        self.status_var.set("Customer form cleared")
    
    def on_customer_select(self, event):
        selected = self.customers_tree.selection()
        if not selected:
            return
        
        values = self.customers_tree.item(selected[0])['values']
        self.clear_customer_form()
        
        self.customer_name.insert(0, values[1])
        self.customer_address.insert(0, values[2])
        self.customer_phone.insert(0, values[3])
        self.customer_email.insert(0, values[4])
        
        if values[5]:
            # Find the matching plan in the combobox
            for plan in self.customer_plan['values']:
                if values[5] in plan:
                    self.customer_plan.set(plan)
                    break
        
        self.status_var.set(f"Selected customer: {values[1]}")
    
    # Plan operations (unchanged from original except for status bar updates)
    def add_plan(self):
        name = self.plan_name.get()
        speed = self.plan_speed.get()
        price = self.plan_price.get()
        data_limit = self.plan_data_limit.get()
        description = self.plan_description.get()
        
        if not name or not speed or not price:
            messagebox.showerror("Error", "Please fill all required fields")
            return
        
        try:
            price_float = float(price)
            
            cursor = self.conn.cursor()
            cursor.execute('''
            INSERT INTO plans (name, speed, price, data_limit, description)
            VALUES (?, ?, ?, ?, ?)
            ''', (name, speed, price_float, data_limit, description))
            
            self.conn.commit()
            self.load_plans()
            self.update_dashboard_stats()
            self.clear_plan_form()
            messagebox.showinfo("Success", "Plan added successfully")
            
            # Log activity
            self.log_activity(f"Added plan: {name}")
            self.status_var.set(f"Plan {name} added successfully")
        except ValueError:
            messagebox.showerror("Error", "Price must be a valid number")
            self.status_var.set("Error: Price must be a valid number")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add plan: {str(e)}")
            self.status_var.set("Error adding plan")
    
    def update_plan(self):
        selected = self.plans_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a plan to update")
            return
        
        plan_id = self.plans_tree.item(selected[0])['values'][0]
        name = self.plan_name.get()
        speed = self.plan_speed.get()
        price = self.plan_price.get()
        data_limit = self.plan_data_limit.get()
        description = self.plan_description.get()
        
        if not name or not speed or not price:
            messagebox.showerror("Error", "Please fill all required fields")
            return
        
        try:
            price_float = float(price)
            
            cursor = self.conn.cursor()
            cursor.execute('''
            UPDATE plans 
            SET name=?, speed=?, price=?, data_limit=?, description=?
            WHERE plan_id=?
            ''', (name, speed, price_float, data_limit, description, plan_id))
            
            self.conn.commit()
            self.load_plans()
            self.load_customers()  # To update plan references
            self.update_dashboard_stats()
            messagebox.showinfo("Success", "Plan updated successfully")
            
            # Log activity
            self.log_activity(f"Updated plan: {name}")
            self.status_var.set(f"Plan {name} updated successfully")
        except ValueError:
            messagebox.showerror("Error", "Price must be a valid number")
            self.status_var.set("Error: Price must be a valid number")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update plan: {str(e)}")
            self.status_var.set("Error updating plan")
    
    def delete_plan(self):
        selected = self.plans_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a plan to delete")
            return
        
        plan_id = self.plans_tree.item(selected[0])['values'][0]
        plan_name = self.plans_tree.item(selected[0])['values'][1]
        
        # Check if any customers are using this plan
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM customers WHERE plan_id=?', (plan_id,))
        customer_count = cursor.fetchone()[0]
        
        if customer_count > 0:
            messagebox.showerror("Error", f"Cannot delete plan. {customer_count} customers are using this plan.")
            self.status_var.set(f"Cannot delete plan - {customer_count} customers using it")
            return
        
        if not messagebox.askyesno("Confirm", f"Are you sure you want to delete plan {plan_name}?"):
            return
        
        try:
            cursor.execute('DELETE FROM plans WHERE plan_id=?', (plan_id,))
            self.conn.commit()
            self.load_plans()
            self.update_dashboard_stats()
            self.clear_plan_form()
            messagebox.showinfo("Success", "Plan deleted successfully")
            
            # Log activity
            self.log_activity(f"Deleted plan: {plan_name}")
            self.status_var.set(f"Plan {plan_name} deleted successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete plan: {str(e)}")
            self.status_var.set("Error deleting plan")
    
    def clear_plan_form(self):
        self.plan_name.delete(0, tk.END)
        self.plan_speed.delete(0, tk.END)
        self.plan_price.delete(0, tk.END)
        self.plan_data_limit.delete(0, tk.END)
        self.plan_description.delete(0, tk.END)
        self.status_var.set("Plan form cleared")
    
    def on_plan_select(self, event):
        selected = self.plans_tree.selection()
        if not selected:
            return
        
        values = self.plans_tree.item(selected[0])['values']
        self.clear_plan_form()
        
        self.plan_name.insert(0, values[1])
        self.plan_speed.insert(0, values[2])
        self.plan_price.insert(0, values[3])
        self.plan_data_limit.insert(0, values[4])
        self.plan_description.insert(0, values[5])
        
        self.status_var.set(f"Selected plan: {values[1]}")
    
    # Complaint operations (unchanged from original except for status bar updates)
    def add_complaint(self):
        customer = self.complaint_customer.get()
        description = self.complaint_description.get("1.0", tk.END).strip()
        status = self.complaint_status.get()
        
        if not customer or not description:
            messagebox.showerror("Error", "Please fill all required fields")
            return
        
        try:
            cursor = self.conn.cursor()
            
            # Get customer_id
            cursor.execute('SELECT customer_id FROM customers WHERE name=?', (customer,))
            customer_row = cursor.fetchone()
            
            if not customer_row:
                messagebox.showerror("Error", "Customer not found")
                return
            
            customer_id = customer_row[0]
            
            # Insert complaint
            complaint_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('''
            INSERT INTO complaints (customer_id, description, date, status)
            VALUES (?, ?, ?, ?)
            ''', (customer_id, description, complaint_date, status))
            
            self.conn.commit()
            self.load_complaints()
            self.update_dashboard_stats()
            self.clear_complaint_form()
            messagebox.showinfo("Success", "Complaint added successfully")
            
            # Log activity
            self.log_activity(f"Added complaint for: {customer}")
            self.status_var.set(f"Complaint added for {customer}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add complaint: {str(e)}")
            self.status_var.set("Error adding complaint")
    
    def update_complaint(self):
        selected = self.complaints_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a complaint to update")
            return
        
        complaint_id = self.complaints_tree.item(selected[0])['values'][0]
        customer = self.complaint_customer.get()
        description = self.complaint_description.get("1.0", tk.END).strip()
        status = self.complaint_status.get()
        resolution = self.complaint_resolution.get("1.0", tk.END).strip()
        
        if not customer or not description:
            messagebox.showerror("Error", "Please fill all required fields")
            return
        
        try:
            cursor = self.conn.cursor()
            
            # Get customer_id
            cursor.execute('SELECT customer_id FROM customers WHERE name=?', (customer,))
            customer_row = cursor.fetchone()
            
            if not customer_row:
                messagebox.showerror("Error", "Customer not found")
                return
            
            customer_id = customer_row[0]
            
            # Update complaint
            cursor.execute('''
            UPDATE complaints 
            SET customer_id=?, description=?, status=?, resolution=?
            WHERE complaint_id=?
            ''', (customer_id, description, status, resolution, complaint_id))
            
            self.conn.commit()
            self.load_complaints()
            self.update_dashboard_stats()
            messagebox.showinfo("Success", "Complaint updated successfully")
            
            # Log activity
            self.log_activity(f"Updated complaint #{complaint_id}")
            self.status_var.set(f"Complaint #{complaint_id} updated")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update complaint: {str(e)}")
            self.status_var.set("Error updating complaint")
    
    def resolve_complaint(self):
        selected = self.complaints_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a complaint to resolve")
            return
        
        complaint_id = self.complaints_tree.item(selected[0])['values'][0]
        resolution = self.complaint_resolution.get("1.0", tk.END).strip()
        
        if not resolution:
            messagebox.showerror("Error", "Please enter a resolution before marking as resolved")
            return
        
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
            UPDATE complaints 
            SET status='Resolved', resolution=?
            WHERE complaint_id=?
            ''', (resolution, complaint_id))
            
            self.conn.commit()
            self.load_complaints()
            self.update_dashboard_stats()
            messagebox.showinfo("Success", "Complaint resolved successfully")
            
            # Log activity
            self.log_activity(f"Resolved complaint #{complaint_id}")
            self.status_var.set(f"Complaint #{complaint_id} resolved")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to resolve complaint: {str(e)}")
            self.status_var.set("Error resolving complaint")
    
    def clear_complaint_form(self):
        self.complaint_customer.set('')
        self.complaint_description.delete("1.0", tk.END)
        self.complaint_status.set('Open')
        self.complaint_resolution.delete("1.0", tk.END)
        self.status_var.set("Complaint form cleared")
    
    def on_complaint_select(self, event):
        selected = self.complaints_tree.selection()
        if not selected:
            return
        
        values = self.complaints_tree.item(selected[0])['values']
        self.clear_complaint_form()
        
        self.complaint_customer.set(values[1])
        self.complaint_description.insert("1.0", values[4])
        self.complaint_status.set(values[3])
        
        # Get resolution from database
        cursor = self.conn.cursor()
        cursor.execute('SELECT resolution FROM complaints WHERE complaint_id=?', (values[0],))
        resolution = cursor.fetchone()
        
        if resolution and resolution[0]:
            self.complaint_resolution.insert("1.0", resolution[0])
        
        self.status_var.set(f"Selected complaint #{values[0]}")
    
    # Billing operations (unchanged from original except for status bar updates)
    def generate_bill(self):
        customer = self.billing_customer.get()
        amount = self.billing_amount.get()
        due_date = self.billing_due_date.get()
        
        if not customer or not amount or not due_date:
            messagebox.showerror("Error", "Please fill all required fields")
            return
        
        try:
            amount_float = float(amount)
            
            cursor = self.conn.cursor()
            
            # Get customer_id
            cursor.execute('SELECT customer_id FROM customers WHERE name=?', (customer,))
            customer_row = cursor.fetchone()
            
            if not customer_row:
                messagebox.showerror("Error", "Customer not found")
                return
            
            customer_id = customer_row[0]
            
            # Insert bill
            cursor.execute('''
            INSERT INTO billing (customer_id, amount, due_date)
            VALUES (?, ?, ?)
            ''', (customer_id, amount_float, due_date))
            
            self.conn.commit()
            self.load_bills()
            self.clear_billing_form()
            messagebox.showinfo("Success", "Bill generated successfully")
            
            # Log activity
            self.log_activity(f"Generated bill for: {customer}")
            self.status_var.set(f"Bill generated for {customer}")
        except ValueError:
            messagebox.showerror("Error", "Amount must be a valid number")
            self.status_var.set("Error: Amount must be a valid number")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate bill: {str(e)}")
            self.status_var.set("Error generating bill")
    
    def mark_bill_paid(self):
        selected = self.bills_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a bill to mark as paid")
            return
        
        bill_id = self.bills_tree.item(selected[0])['values'][0]
        customer = self.bills_tree.item(selected[0])['values'][1]
        
        if self.bills_tree.item(selected[0])['values'][4] == 'Paid':
            messagebox.showinfo("Info", "This bill is already marked as paid")
            return
        
        try:
            cursor = self.conn.cursor()
            payment_date = datetime.now().strftime('%Y-%m-%d')
            cursor.execute('''
            UPDATE billing 
            SET paid=1, payment_date=?
            WHERE bill_id=?
            ''', (payment_date, bill_id))
            
            self.conn.commit()
            self.load_bills()
            messagebox.showinfo("Success", "Bill marked as paid successfully")
            
            # Log activity
            self.log_activity(f"Marked bill #{bill_id} as paid for {customer}")
            self.status_var.set(f"Bill #{bill_id} marked as paid")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to mark bill as paid: {str(e)}")
            self.status_var.set("Error marking bill as paid")
    
    def clear_billing_form(self):
        self.billing_customer.set('')
        self.billing_amount.delete(0, tk.END)
        self.billing_due_date.delete(0, tk.END)
        self.status_var.set("Billing form cleared")
    
    def on_bill_select(self, event):
        selected = self.bills_tree.selection()
        if not selected:
            return
        
        values = self.bills_tree.item(selected[0])['values']
        self.clear_billing_form()
        
        self.billing_customer.set(values[1])
        self.billing_amount.insert(0, values[2])
        self.billing_due_date.insert(0, values[3])
        
        self.status_var.set(f"Selected bill #{values[0]}")
    
    # Troubleshooting operations (unchanged from original except for status bar updates)
    def run_troubleshooting(self):
        issue = self.issue_var.get()
        
        if not issue:
            messagebox.showerror("Error", "Please select an issue to troubleshoot")
            return
        
        self.results_text.delete(1.0, tk.END)
        self.schedule_button.config(state=tk.DISABLED)
        
        steps = []
        
        if issue == "no_connection":
            steps.extend([
                "1. Check if your router is powered on and all lights are normal",
                "2. Restart your router by unplugging it for 30 seconds and plugging it back in",
                "3. Check all cable connections between your devices and the router",
                "4. Try connecting a different device to see if the issue is device-specific",
                "5. Check if there are any known outages in your area"
            ])
        elif issue == "slow_speed":
            steps.extend([
                "1. Run a speed test at speedtest.net to confirm your current speeds",
                "2. Restart your router and modem",
                "3. Disconnect devices that may be using bandwidth unnecessarily",
                "4. Try connecting directly with an Ethernet cable to rule out Wi-Fi issues",
                "5. Check for background downloads or updates on your devices"
            ])
        elif issue == "intermittent":
            steps.extend([
                "1. Check for loose or damaged cables",
                "2. Move your router to a central location away from interference",
                "3. Change your Wi-Fi channel to avoid congestion",
                "4. Update your router's firmware",
                "5. Check if the issue occurs at specific times of day"
            ])
        elif issue == "specific_website":
            steps.extend([
                "1. Check if the website is down for everyone (use downdetector.com)",
                "2. Try accessing the website from a different browser",
                "3. Clear your browser cache and cookies",
                "4. Try accessing the website from a different device",
                "5. Check your firewall or security software settings"
            ])
        elif issue == "router":
            steps.extend([
                "1. Power cycle your router (unplug for 30 seconds)",
                "2. Check for firmware updates for your router",
                "3. Reset your router to factory settings if needed",
                "4. Check for overheating (ensure proper ventilation)",
                "5. Verify all indicator lights are functioning normally"
            ])
        
        steps.append("\nIf these steps don't resolve your issue, you may need technician assistance.")
        
        self.results_text.insert(tk.END, "\n".join(steps))
        self.schedule_button.config(state=tk.NORMAL)
        
        # Log activity
        self.log_activity(f"Ran troubleshooting for: {issue}")
        self.status_var.set(f"Ran troubleshooting for {issue.replace('_', ' ')}")
    
    def schedule_technician(self):
        # Get customer names for selection
        cursor = self.conn.cursor()
        cursor.execute('SELECT name FROM customers')
        customers = [row[0] for row in cursor.fetchall()]
        
        if not customers:
            messagebox.showerror("Error", "No customers found to schedule a visit")
            return
        
        # Create scheduling dialog
        schedule_dialog = tk.Toplevel(self.root)
        schedule_dialog.title("Schedule Technician Visit")
        schedule_dialog.geometry("400x300")
        schedule_dialog.resizable(False, False)
        
        # Center the dialog
        window_width = schedule_dialog.winfo_reqwidth()
        window_height = schedule_dialog.winfo_reqheight()
        position_right = int(schedule_dialog.winfo_screenwidth()/2 - window_width/2)
        position_down = int(schedule_dialog.winfo_screenheight()/2 - window_height/2)
        schedule_dialog.geometry(f"+{position_right}+{position_down}")
        
        ttk.Label(schedule_dialog, text="Customer:").pack(pady=5)
        customer_var = tk.StringVar()
        customer_dropdown = ttk.Combobox(schedule_dialog, textvariable=customer_var, values=customers)
        customer_dropdown.pack(pady=5, padx=10, fill=tk.X)
        
        ttk.Label(schedule_dialog, text="Date (YYYY-MM-DD):").pack(pady=5)
        date_entry = ttk.Entry(schedule_dialog)
        date_entry.pack(pady=5, padx=10, fill=tk.X)
        
        ttk.Label(schedule_dialog, text="Time (HH:MM):").pack(pady=5)
        time_entry = ttk.Entry(schedule_dialog)
        time_entry.pack(pady=5, padx=10, fill=tk.X)
        
        ttk.Label(schedule_dialog, text="Issue Description:").pack(pady=5)
        issue_text = tk.Text(schedule_dialog, height=5, width=40)
        issue_text.pack(pady=5, padx=10, fill=tk.X)
        
        def confirm_schedule():
            customer = customer_var.get()
            date = date_entry.get()
            time = time_entry.get()
            issue = issue_text.get("1.0", tk.END).strip()
            
            if not customer or not date or not time or not issue:
                messagebox.showerror("Error", "Please fill all fields")
                return
            
            # In a real application, you would save this to a database
            messagebox.showinfo("Scheduled", 
                              f"Technician visit scheduled for {customer} on {date} at {time}\n\nIssue: {issue}")
            schedule_dialog.destroy()
            
            # Log activity
            self.log_activity(f"Scheduled technician visit for: {customer}")
            self.status_var.set(f"Technician scheduled for {customer}")
        
        ttk.Button(schedule_dialog, text="Schedule", command=confirm_schedule).pack(pady=10, padx=10, fill=tk.X)
    
    # Utility methods
    def log_activity(self, activity):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Determine activity type for coloring
        if 'customer' in activity.lower():
            tag = 'customer'
        elif 'plan' in activity.lower():
            tag = 'plan'
        elif 'complaint' in activity.lower() or 'technician' in activity.lower():
            tag = 'complaint'
        elif 'bill' in activity.lower():
            tag = 'billing'
        else:
            tag = ''
        
        self.activity_tree.insert('', 0, values=(activity.split(':')[0], activity, timestamp), tags=(tag,))

    # [Rest of your methods remain exactly the same...]
    # Keep all other methods unchanged from your original code

if __name__ == "__main__":
    root = tk.Tk()
    app = ISPAutomationSystem(root)
    root.mainloop()