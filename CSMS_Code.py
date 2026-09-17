# =====================================================================
# PROGRAM NAME: Cleaning Services Management System (CSMS)
# FILE NAME: CSMS.py
# DESCRIPTION: Unified data layer matching Cleaning.dbo schema
# =====================================================================

class Customer:
    def __init__(self, customer_id, first_name, last_name, email, phone):
        self.customer_id = int(customer_id)
        self.first_name = str(first_name)
        self.last_name = str(last_name)
        self.email = str(email)
        self.phone = str(phone)

class Cleaner:
    def __init__(self, cleaner_id, first_name, last_name, hourly_rate):
        self.cleaner_id = int(cleaner_id)
        self.first_name = str(first_name)
        self.last_name = str(last_name)
        self.hourly_rate = float(hourly_rate)

class Service:
    def __init__(self, service_id, service_name, base_price):
        self.service_id = int(service_id)
        self.service_name = str(service_name)
        self.base_price = float(base_price)

class Invoice:
    def __init__(self, invoice_id, total_amount, payment_status):
        self.invoice_id = int(invoice_id)
        self.total_amount = float(total_amount)
        self.payment_status = str(payment_status).strip().upper()

class Appointment:
    def __init__(self, appointment_id, customer, service, cleaner, invoice, job_date, status):
        self.appointment_id = int(appointment_id)
        self.customer = customer   # Expects a Customer Object Instance
        self.service = service     # Expects a Service Object Instance
        self.cleaner = cleaner     # Expects a Cleaner Object Instance
        self.invoice = invoice     # Expects an Invoice Object Instance
        self.job_date = str(job_date)
        self.status = str(status).strip().upper()

    def calculate_true_cost(self, simulated_hours=3.0):
        """
        Core Calculation Function: Multiplies cleaner labor by standard hours
        and adds the service base flat pricing. Returns 0 if cancelled.
        """
        if self.status == "CANCELLED":
            return 0.0
        return self.service.base_price + (self.cleaner.hourly_rate * simulated_hours)


class CSMS_Engine:
    def __init__(self):
        # Master lookup collections (Dictionaries)
        self.appointments_dict = {}
        
        # Internal temporary entity maps for object relational construction
        self._customers_map = {}
        self._cleaners_map = {}
        self._services_map = {}
        self._invoices_map = {}

        # Hydrate system state with the source relational data records
        self._load_database_records()
        self._assemble_relational_models()

    def _load_database_records(self):
        # 1. Customers Table Dataset
        raw_cust = [
            (101, "JOHN", "SMITH", "JOHN@SMITH.CA", "613-555-1001"),
            (102, "HELEN", "ELK", "HELEN@ELK.CA", "613-555-1002"),
            (103, "KEVIN", "DOE", "KEVIN@DOE.CA", "613-555-1003"),
            (104, "CHRIS", "KLINE", "CHRIS@KLINE.CA", "613-555-1004"),
            (105, "CONNOR", "MCDAVID", "CONNOR@MCDAVID.CA", "613-555-1005"),
            (106, "MARY", "MOE", "MARY@MOE.CA", "613-555-1006"),
            (107, "CODY", "MUIR", "CODY@MUIR.CA", "613-555-1007"),
            (108, "KAREN", "SLY", "KAREN@SLY.CA", "613-555-1008"),
            (109, "HENRY", "GRAY", "HENRY@GRAY.CA", "613-555-1009"),
            (110, "CHAD", "KELVIN", "CHAD@KELVIN.CA", "613-555-1010")
        ]
        for c in raw_cust:
            self._customers_map[c[0]] = Customer(*c)

        # 2. Cleaners Table Dataset
        raw_cleaners = [
            (20, "SAVANNAH", "LEE", 27.0),
            (21, "AVERY", "LEON", 27.0),
            (22, "ROBIN", "LOVE", 35.0),
            (23, "WILLOW", "HEART", 25.0),
            (24, "LILLY", "MARY", 26.0),
            (25, "JAMES", "BROWN", 30.0),
            (26, "EMMA", "WILSON", 28.0),
            (27, "NOAH", "MARTIN", 29.0),
            (28, "OLIVIA", "CLARK", 32.0),
            (29, "LIAM", "ANDERSON", 32.0)
        ]
        for cl in raw_cleaners:
            self._cleaners_map[cl[0]] = Cleaner(*cl)

        # 3. Services Table Dataset
        raw_services = [
            (111, "DEEP CLEAN", 100.0),
            (222, "LIGHT CLEAN", 50.0),
            (333, "DUMP RUN", 200.0),
            (444, "WINDOWS", 150.0),
            (555, "STANDARD", 75.0),
            (666, "CARPET CLEANING", 125.0),
            (777, "MOVE OUT CLEAN", 175.0),
            (888, "OFFICE CLEAN", 150.0),
            (999, "GARAGE CLEAN", 125.0),
            (1000, "POST RENOVATION", 250.0)
        ]
        for s in raw_services:
            self._services_map[s[0]] = Service(*s)

        # 4. Invoice Table Dataset
        raw_invoices = [
            (1010, 250.0, "COMPLETED"),
            (1111, 100.0, "INCOMPLETE"),
            (2222, 50.0, "COMPLETED"),
            (3333, 200.0, "COMPLETED"),
            (4444, 150.0, "COMPLETED"),
            (5555, 75.0, "INCOMPLETE"),
            (6666, 125.0, "COMPLETED"),
            (7777, 175.0, "INCOMPLETE"),
            (8888, 150.0, "COMPLETED"),
            (9999, 125.0, "COMPLETED")
        ]
        for inv in raw_invoices:
            inv_obj = Invoice(*inv)
            self._invoices_map[inv[0]] = inv_obj

    def _assemble_relational_models(self):
        # 5. Appointments Table Dataset Linked Interactively
        raw_appointments = [
            (1, 101, 111, 20, 1111, "AUG-10-2026", "COMPLETED"),
            (2, 102, 222, 21, 2222, "JULY-19-2026", "SCHEDULED"),
            (3, 103, 333, 22, 3333, "JUNE-06-2026", "CANCELLED"),
            (4, 104, 444, 23, 4444, "JAN-25-2026", "COMPLETED"),
            (5, 105, 555, 24, 5555, "APRIL-14-2026", "CANCELLED"),
            (6, 106, 666, 25, 6666, "FEB-3-2026", "COMPLETED"),
            (7, 107, 777, 26, 7777, "MAR-22-2026", "COMPLETED"),
            (8, 108, 888, 27, 8888, "APRIL-6-2026", "COMPLETED"),
            (9, 109, 999, 28, 9999, "AUG-1-2026", "SCHEDULED"),
            (10, 110, 1000, 29, 1010, "AUG-8-2026", "SCHEDULED")
        ]
        for app in raw_appointments:
            app_id, cust_id, serv_id, clean_id, inv_id, j_date, status = app
            
            # Form structural model associations via mapped dictionary pointers
            appt_obj = Appointment(
                appointment_id=app_id,
                customer=self._customers_map[cust_id],
                service=self._services_map[serv_id],
                cleaner=self._cleaners_map[clean_id],
                invoice=self._invoices_map[inv_id],
                job_date=j_date,
                status=status
            )
            self.appointments_dict[app_id] = appt_obj

    def display_unpaid_invoices(self):
        """
        HUMAN CORRECTION INTEGRATED:
        Dynamically calculates the outstanding balances using the verified business logic formula
        and ensures cancelled appointments correctly map to a balance due of $0.00.
        """
        print("\n" + "="*50)
        print("🔴 CRITICAL REPORT: OUTSTANDING INVOICES")
        print("="*50)
        print(f"{'Invoice ID':<12} | {'Balance Due':<12} | {'Status':<12}")
        print("-"*50)
        
        # Traverse appointments to apply dynamic logic directly to outstanding invoices
        for app_id, app in self.appointments_dict.items():
            if app.invoice.payment_status == "INCOMPLETE":
                true_balance = app.calculate_true_cost(simulated_hours=3.0)
                print(f"{app.invoice.invoice_id:<12} | ${true_balance:<11.2f} | {app.invoice.payment_status:<12}")
        print("="*50)

    def display_all_schedules(self):
        print("\n" + "="*85)
        print("📅 MASTER ADMINISTRATIVE WORKING SCHEDULE")
        print("="*85)
        header = f"{'Appt ID':<8} | {'Client':<16} | {'Service Name':<18} | {'Date':<14} | {'Status':<10}"
        print(header)
        print("-"*85)
        for app_id, app in self.appointments_dict.items():
            client_fullname = f"{app.customer.first_name} {app.customer.last_name}"
            print(f"{app.appointment_id:<8} | {client_fullname:<16} | {app.service.service_name:<18} | {app.job_date:<14} | {app.status:<10}")
        print("="*85)

    def audit_true_job_yields(self):
        print("\n" + "="*85)
        print("FINANCIAL COMBINED OPERATIONAL COST AUDIT (Assumes 3-Hour Standard Labor)")
        print("="*85)
        print(f"{'Appt ID':<8} | {'Service Flat Fee':<18} | {'Labor Rate/Hr':<15} | {'True Combined Cost':<18}")
        print("-"*85)
        for app_id, app in self.appointments_dict.items():
            true_cost = app.calculate_true_cost(simulated_hours=3.0)
            print(f"{app.appointment_id:<8} | ${app.service.base_price:<17.2f} | ${app.cleaner.hourly_rate:<14.2f} | ${true_cost:<17.2f}")
        print("="*85)


def main():
    engine = CSMS_Engine()

    while True:
        print("\n::: CLEANING SERVICES MANAGEMENT SYSTEM (CSMS) :::")
        print("1. View Master Administrative Work Schedule")
        print("2. View Outstanding (Unpaid) Balances Report")
        print("3. Run Financial Cost Audit Per Job")
        print("4. Exit Application")
        
        choice = input("\nEnter selection option (1-4): ").strip()
        
        if choice == "1":
            engine.display_all_schedules()
        elif choice == "2":
            engine.display_unpaid_invoices()
        elif choice == "3":
            engine.audit_true_job_yields()
        elif choice == "4":
            print("\nShutting down CSMS Engine... Goodbye.")
            break
        else:
            print("\n❌ Invalid choice selection. Please try again.")

if __name__ == "__main__":
    main()
