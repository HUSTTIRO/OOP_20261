"""
/****************/
Mã sinh viên: 20241900
Họ tên: Nguyễn Tuấn Trường
/****************/
"""

class Employee:
    # Tham số mặc định giúp gọi constructor với 2, 3 hoặc 4 đối số.
    def __init__(self, employeeId, fullName, department="Unassigned", monthlyBonus=0):
        if employeeId.strip() == "":
            raise ValueError("Mã nhân sự không được rỗng")
        if fullName.strip() == "":
            raise ValueError("Họ tên không được rỗng")
        if department.strip() == "":
            raise ValueError("Phòng ban không được rỗng")
        if monthlyBonus < 0:
            raise ValueError("Thưởng tháng không được âm")
        # __ ở đầu tên để đóng gói thuộc tính; bên ngoài đọc bằng hàm get.
        self.__employeeId = employeeId.strip()
        self.__fullName = fullName.strip()
        self.__department = department.strip()
        self.__monthlyBonus = monthlyBonus

    def getEmployeeId(self):
        return self.__employeeId

    def getFullName(self):
        return self.__fullName

    def getDepartment(self):
        return self.__department

    def getMonthlyBonus(self):
        return self.__monthlyBonus

    # *args gom các đối số vào tuple, giống cách làm constructor ở BT3.
    # Python dùng số lượng đối số để mô phỏng 3 cách gọi addBonus.
    def addBonus(self, *args):
        if len(args) == 1:
            amount = args[0]
        elif len(args) == 2:
            amount, reason = args
            if reason.strip() == "":
                raise ValueError("Lý do thưởng không được rỗng")
        elif len(args) == 3:
            rate, referenceAmount, reason = args
            if rate <= 0 or rate > 0.5:
                raise ValueError("Tỷ lệ thưởng phải lớn hơn 0 và không quá 0.5")
            if referenceAmount <= 0:
                raise ValueError("Giá trị tham chiếu phải lớn hơn 0")
            if reason.strip() == "":
                raise ValueError("Lý do thưởng không được rỗng")
            amount = rate * referenceAmount
        else:
            raise TypeError("addBonus nhận 1, 2 hoặc 3 đối số")
        if amount <= 0:
            raise ValueError("Khoản thưởng phải lớn hơn 0")
        # Kiểm tra xong mới cộng, nên lời gọi lỗi không thay đổi thưởng cũ.
        self.__monthlyBonus += amount

    def resetMonthlyBonus(self):
        self.__monthlyBonus = 0

    def calculateGrossPay(self):
        # Employee chưa có khoản lương riêng, chỉ tính thưởng.
        # Các lớp con sẽ ghi đè hàm này bằng công thức của từng loại.
        return self.__monthlyBonus

    def getEmployeeType(self):
        return "Employee"

    def displayPayrollInfo(self):
        print(f"Mã: {self.__employeeId}")
        print(f"Họ tên: {self.__fullName}")
        print(f"Phòng ban: {self.__department}")
        print(f"Loại: {self.getEmployeeType()}")
        print(f"Thưởng tháng: {self.__monthlyBonus}")


class SalariedEmployee(Employee):
    def __init__(self, employeeId, fullName, department="Unassigned",
                 monthlySalary=0, responsibilityAllowance=0, monthlyBonus=0):
        # super() gọi constructor lớp cha để dùng lại kiểm tra dữ liệu chung.
        super().__init__(employeeId, fullName, department, monthlyBonus)
        if monthlySalary < 0:
            raise ValueError("Lương tháng không được âm")
        if responsibilityAllowance < 0:
            raise ValueError("Phụ cấp không được âm")
        self.__monthlySalary = monthlySalary
        self.__responsibilityAllowance = responsibilityAllowance

    # Ghi đè 3 phương thức của Employee.
    def calculateGrossPay(self):
        return self.__monthlySalary + self.__responsibilityAllowance + self.getMonthlyBonus()

    def getEmployeeType(self):
        return "SalariedEmployee"

    def displayPayrollInfo(self):
        # Dùng lại phần hiển thị chung rồi in thêm các khoản riêng.
        super().displayPayrollInfo()
        print(f"Lương tháng: {self.__monthlySalary}")
        print(f"Phụ cấp trách nhiệm: {self.__responsibilityAllowance}")
        print(f"Thu nhập: {self.calculateGrossPay()}")


class HourlyEmployee(Employee):
    def __init__(self, employeeId, fullName, department="Unassigned",
                 hourlyRate=0, workedHours=0, monthlyBonus=0):
        super().__init__(employeeId, fullName, department, monthlyBonus)
        if hourlyRate < 0:
            raise ValueError("Đơn giá giờ không được âm")
        if workedHours < 0 or workedHours > 250:
            raise ValueError("Số giờ làm phải từ 0 đến 250")
        self.__hourlyRate = hourlyRate
        self.__workedHours = workedHours

    def calculateGrossPay(self):
        if self.__workedHours <= 160:
            basePay = self.__workedHours * self.__hourlyRate
        else:
            # Chỉ phần giờ vượt 160 mới được nhân hệ số 1.5.
            basePay = 160 * self.__hourlyRate
            basePay += (self.__workedHours - 160) * self.__hourlyRate * 1.5
        return basePay + self.getMonthlyBonus()

    def getEmployeeType(self):
        return "HourlyEmployee"

    def displayPayrollInfo(self):
        super().displayPayrollInfo()
        if self.__workedHours <= 160:
            normalHours = self.__workedHours
            overtimeHours = 0
        else:
            normalHours = 160
            overtimeHours = self.__workedHours - 160
        print(f"Đơn giá giờ: {self.__hourlyRate}")
        print(f"Giờ thường: {normalHours}")
        print(f"Giờ vượt ngưỡng: {overtimeHours}")
        # Tiền làm thêm được tính khi cần, không lưu thành thuộc tính riêng.
        print(f"Lương giờ thường: {normalHours * self.__hourlyRate}")
        print(f"Lương làm thêm: {overtimeHours * self.__hourlyRate * 1.5}")
        print(f"Thu nhập: {self.calculateGrossPay()}")


class SalesEmployee(Employee):
    def __init__(self, employeeId, fullName, department="Unassigned",
                 baseSalary=0, salesRevenue=0, commissionRate=0, monthlyBonus=0):
        super().__init__(employeeId, fullName, department, monthlyBonus)
        if baseSalary < 0:
            raise ValueError("Lương cơ bản không được âm")
        if salesRevenue < 0:
            raise ValueError("Doanh số không được âm")
        if commissionRate < 0 or commissionRate > 0.3:
            raise ValueError("Tỷ lệ hoa hồng phải từ 0 đến 0.3")
        self.__baseSalary = baseSalary
        self.__salesRevenue = salesRevenue
        self.__commissionRate = commissionRate

    def getSalesRevenue(self):
        return self.__salesRevenue

    def updateSalesRevenue(self, value):
        if value < 0:
            raise ValueError("Doanh số không được âm")
        self.__salesRevenue = value

    def calculateGrossPay(self):
        return self.__baseSalary + self.__salesRevenue * self.__commissionRate + self.getMonthlyBonus()

    def getEmployeeType(self):
        return "SalesEmployee"

    def displayPayrollInfo(self):
        super().displayPayrollInfo()
        print(f"Lương cơ bản: {self.__baseSalary}")
        print(f"Doanh số: {self.__salesRevenue}")
        print(f"Tỷ lệ hoa hồng: {self.__commissionRate * 100}%")
        print(f"Hoa hồng: {self.__salesRevenue * self.__commissionRate}")
        print(f"Thu nhập: {self.calculateGrossPay()}")


class Payroll:
    def __init__(self, period):
        if period.strip() == "":
            raise ValueError("Kỳ lương không được rỗng")
        self.__period = period
        self.__employees = []

    def getEmployees(self):
        # copy() trả danh sách mới, tránh sửa trực tiếp danh sách bên trong.
        # Các phần tử vẫn là tham chiếu tới những nhân viên ban đầu.
        return self.__employees.copy()

    def addEmployee(self, employee):
        if not isinstance(employee, Employee):
            raise TypeError("Chỉ thêm đối tượng Employee hoặc lớp con")
        if self.findEmployee(employee.getEmployeeId()) is not None:
            print("Mã nhân sự đã có trong bảng lương")
            return False
        self.__employees.append(employee)
        return True

    def findEmployee(self, employeeId):
        for employee in self.__employees:
            if employee.getEmployeeId() == employeeId:
                return employee
        return None

    def calculateTotalPayroll(self):
        total = 0
        for employee in self.__employees:
            # Đa hình: cùng lời gọi nhưng mỗi lớp con tính theo công thức riêng.
            total += employee.calculateGrossPay()
        return total

    def calculatePayrollByDepartment(self, department):
        total = 0
        for employee in self.__employees:
            if employee.getDepartment() == department:
                total += employee.calculateGrossPay()
        return total

    def findHighestPaidEmployee(self):
        if len(self.__employees) == 0:
            return None
        highest = self.__employees[0]
        for employee in self.__employees:
            if employee.calculateGrossPay() > highest.calculateGrossPay():
                highest = employee
        # Nếu bằng nhau thì giữ người xuất hiện trước.
        return highest

    def displayPayroll(self):
        print(f"Bảng lương kỳ {self.__period}")
        if len(self.__employees) == 0:
            print("Chưa có nhân sự")
        for employee in self.__employees:
            employee.displayPayrollInfo()
            print()
        print(f"Tổng bảng lương: {self.calculateTotalPayroll()}")


def createSamplePayroll():
    e1 = SalariedEmployee("E001", "Nguyễn Minh An", "Đào tạo", 15000000, 2000000)
    e2 = HourlyEmployee("E002", "Trần Thu Bình", "Hỗ trợ", 100000, 150)
    e3 = HourlyEmployee("E003", "Lê Hoàng Chi", "Hỗ trợ", 100000, 170)
    e4 = SalesEmployee("E004", "Phạm Quốc Dũng", "Kinh doanh", 8000000, 200000000, 0.05)
    e1.addBonus(1000000)
    e2.addBonus(500000, "Hoàn thành công việc")
    e4.addBonus(0.02, 50000000, "Thưởng theo tỷ lệ")
    payroll = Payroll("2026-09")
    payroll.addEmployee(e1)
    payroll.addEmployee(e2)
    payroll.addEmployee(e3)
    payroll.addEmployee(e4)
    return payroll


def main():
    print("1. Tạo bảng lương với dữ liệu của đề")
    payroll = createSamplePayroll()
    payroll.displayPayroll()

    print("\n2. Tổng lương phòng Hỗ trợ")
    print(payroll.calculatePayrollByDepartment("Hỗ trợ"))

    print("\n3. Tìm người có thu nhập cao nhất")
    highest = payroll.findHighestPaidEmployee()
    if highest is not None:
        print(highest.getFullName(), highest.calculateGrossPay())

    print("\n4. Thêm lại nhân viên có mã E001")
    print(payroll.addEmployee(payroll.findEmployee("E001")))

    print("\n5. Tìm mã không tồn tại")
    print(payroll.findEmployee("E999"))

    print("\n6. Tạo nhân viên bằng constructor rút gọn")
    s = SalariedEmployee("S01", "Nhân viên cố định")
    h = HourlyEmployee("H01", "Nhân viên theo giờ")
    k = SalesEmployee("K01", "Nhân viên kinh doanh")
    s.displayPayrollInfo()
    h.displayPayrollInfo()
    k.displayPayrollInfo()

    print("\n7. Cập nhật doanh số nhân viên kinh doanh")
    sales = payroll.findEmployee("E004")
    sales.updateSalesRevenue(300000000)
    sales.displayPayrollInfo()

    print("\n8. Đặt lại thưởng")
    sales.resetMonthlyBonus()
    print(sales.getMonthlyBonus())

    print("\n9. Bảng lương rỗng")
    empty = Payroll("2026-10")
    empty.displayPayroll()
    print("Người có lương cao nhất:", empty.findHighestPaidEmployee())


# Khi chạy trực tiếp bt.py thì gọi main(); khi import để kiểm thử thì không gọi.
if __name__ == "__main__":
    main()
