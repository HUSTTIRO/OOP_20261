"""
/****************/
Mã sinh viên: 20241900
Họ tên: Nguyễn Tuấn Trường
/****************/
Chạy kiểm thử: python BT4/test_bt.py
"""
from bt import Employee, SalariedEmployee, HourlyEmployee, SalesEmployee, Payroll, createSamplePayroll


# assert báo lỗi nếu kết quả thực tế khác kết quả mong đợi.
def checkEqual(name, actual, expected):
    assert actual == expected, f"{name}: nhận {actual}, mong đợi {expected}"
    print("Đạt:", name)


# *args là các đối số sẽ truyền vào hàm cần kiểm tra.
# try/except dùng để kiểm tra hàm có phát sinh đúng loại lỗi hay không.
def checkError(name, errorType, function, *args):
    try:
        function(*args)
    except errorType:
        print("Đạt:", name)
    else:
        raise AssertionError(name + ": chưa phát sinh lỗi mong đợi")


class ContractEmployee(Employee):
    # Minh họa thêm loại nhân viên mới mà không sửa lớp Payroll.
    def calculateGrossPay(self):
        return 2000000 + self.getMonthlyBonus()

    def getEmployeeType(self):
        return "ContractEmployee"

    def displayPayrollInfo(self):
        super().displayPayrollInfo()
        print(f"Thu nhập: {self.calculateGrossPay()}")


def main():
    payroll = createSamplePayroll()
    checkEqual("Lương E001", payroll.findEmployee("E001").calculateGrossPay(), 18000000)
    checkEqual("Lương E002", payroll.findEmployee("E002").calculateGrossPay(), 15500000)
    checkEqual("Lương E003", payroll.findEmployee("E003").calculateGrossPay(), 17500000)
    checkEqual("Lương E004", payroll.findEmployee("E004").calculateGrossPay(), 19000000)
    checkEqual("Tổng bảng lương", payroll.calculateTotalPayroll(), 70000000)
    checkEqual("Tổng phòng Hỗ trợ", payroll.calculatePayrollByDepartment("Hỗ trợ"), 33000000)
    checkEqual("Phòng không tồn tại", payroll.calculatePayrollByDepartment("Khác"), 0)
    checkEqual("Thu nhập cao nhất", payroll.findHighestPaidEmployee().getEmployeeId(), "E004")
    checkEqual("Mã không tồn tại", payroll.findEmployee("E999"), None)
    duplicate = HourlyEmployee("E001", "Người khác")
    checkEqual("Không thêm mã trùng", payroll.addEmployee(duplicate), False)
    checkEqual("Số người sau khi thêm trùng", len(payroll.getEmployees()), 4)

    # Sửa bản sao danh sách không làm thay đổi danh sách bên trong Payroll.
    copiedEmployees = payroll.getEmployees()
    copiedEmployees.clear()
    checkEqual("Đóng gói danh sách", len(payroll.getEmployees()), 4)

    empty = Payroll("2026-10")
    checkEqual("Tổng bảng lương rỗng", empty.calculateTotalPayroll(), 0)
    checkEqual("Cao nhất khi rỗng", empty.findHighestPaidEmployee(), None)
    empty.displayPayroll()

    base = Employee("X", "Tên")
    checkEqual("Constructor cơ sở rút gọn", base.getDepartment(), "Unassigned")
    checkEqual("Constructor cơ sở đầy đủ", Employee("Y", "Tên", "Hỗ trợ").getDepartment(), "Hỗ trợ")
    for employee in (SalariedEmployee("S", "Tên"), HourlyEmployee("H", "Tên"), SalesEmployee("K", "Tên")):
        checkEqual("Constructor rút gọn " + employee.getEmployeeType(), employee.calculateGrossPay(), 0)
    checkEqual("Thưởng ban đầu", SalariedEmployee("X", "Tên", "Phòng", 1000, 200, 100).calculateGrossPay(), 1300)

    for hours, expected in ((0, 0), (160, 16000000), (161, 16150000), (250, 29500000), (160.5, 16075000)):
        employee = HourlyEmployee("X", "Tên", "Hỗ trợ", 100000, hours)
        checkEqual("Biên số giờ " + str(hours), employee.calculateGrossPay(), expected)

    employee = SalariedEmployee("X", "Tên")
    employee.addBonus(100)
    employee.addBonus(200, "Thưởng cố định")
    employee.addBonus(0.5, 1000, "Thưởng tỷ lệ tối đa")
    checkEqual("Cộng dồn cả ba cách thưởng", employee.getMonthlyBonus(), 800)
    checkError("Thưởng 0", ValueError, employee.addBonus, 0)
    checkError("Thưởng âm", ValueError, employee.addBonus, -1)
    checkError("Lý do rỗng", ValueError, employee.addBonus, 100, " ")
    checkError("Tỷ lệ thưởng 0", ValueError, employee.addBonus, 0, 1000, "Lý do")
    checkError("Tỷ lệ thưởng vượt 0.5", ValueError, employee.addBonus, 0.5001, 1000, "Lý do")
    checkError("Tham chiếu 0", ValueError, employee.addBonus, 0.1, 0, "Lý do")
    checkError("Tham chiếu âm", ValueError, employee.addBonus, 0.1, -1, "Lý do")
    checkError("Lý do thưởng tỷ lệ rỗng", ValueError, employee.addBonus, 0.1, 1000, "")
    checkError("Thiếu đối số thưởng", TypeError, employee.addBonus)
    checkError("Thừa đối số thưởng", TypeError, employee.addBonus, 1, 2, 3, 4)
    checkEqual("Thưởng không đổi sau lời gọi lỗi", employee.getMonthlyBonus(), 800)
    employee.resetMonthlyBonus()
    checkEqual("Đặt lại thưởng", employee.getMonthlyBonus(), 0)

    checkError("Mã rỗng", ValueError, Employee, "", "Tên")
    checkError("Tên rỗng", ValueError, Employee, "X", " ")
    checkError("Phòng rỗng", ValueError, Employee, "X", "Tên", "")
    checkError("Thưởng ban đầu âm", ValueError, Employee, "X", "Tên", "Phòng", -1)
    checkError("Lương tháng âm", ValueError, SalariedEmployee, "X", "Tên", "Phòng", -1)
    checkError("Phụ cấp âm", ValueError, SalariedEmployee, "X", "Tên", "Phòng", 0, -1)
    checkError("Đơn giá âm", ValueError, HourlyEmployee, "X", "Tên", "Phòng", -1)
    checkError("Giờ âm", ValueError, HourlyEmployee, "X", "Tên", "Phòng", 100000, -1)
    checkError("Giờ vượt 250", ValueError, HourlyEmployee, "X", "Tên", "Phòng", 100000, 250.1)
    checkError("Lương cơ bản âm", ValueError, SalesEmployee, "X", "Tên", "Phòng", -1)
    checkError("Doanh số âm", ValueError, SalesEmployee, "X", "Tên", "Phòng", 0, -1)
    checkError("Hoa hồng âm", ValueError, SalesEmployee, "X", "Tên", "Phòng", 0, 0, -0.01)
    checkError("Hoa hồng vượt 0.3", ValueError, SalesEmployee, "X", "Tên", "Phòng", 0, 0, 0.3001)
    checkError("Kỳ lương rỗng", ValueError, Payroll, " ")
    checkError("Thêm sai loại đối tượng", TypeError, payroll.addEmployee, "E005")

    sales = SalesEmployee("X", "Tên", "Phòng", 0, 100000000, 0.3)
    checkEqual("Hoa hồng tối đa 0.3", sales.calculateGrossPay(), 30000000)
    checkEqual("Hoa hồng 0", SalesEmployee("Y", "Tên", "Phòng", 0, 100000000, 0).calculateGrossPay(), 0)
    sales.updateSalesRevenue(200000000)
    checkEqual("Cập nhật doanh số", sales.calculateGrossPay(), 60000000)
    checkError("Cập nhật doanh số âm", ValueError, sales.updateSalesRevenue, -1)
    checkEqual("Giữ doanh số cũ sau lỗi", sales.getSalesRevenue(), 200000000)
    sales.updateSalesRevenue(0)
    checkEqual("Cập nhật doanh số về 0", sales.calculateGrossPay(), 0)

    tied = Payroll("2026-09")
    tied.addEmployee(SalariedEmployee("A", "Người đầu", "Phòng", 100))
    tied.addEmployee(HourlyEmployee("B", "Người sau", "Phòng", 100, 1))
    checkEqual("Lương bằng nhau chọn người trước", tied.findHighestPaidEmployee().getEmployeeId(), "A")

    contract = ContractEmployee("C001", "Nhân viên hợp đồng", "Hỗ trợ")
    contract.addBonus(100000)
    payroll.addEmployee(contract)
    checkEqual("Đa hình với loại mới", payroll.calculateTotalPayroll(), 72100000)
    checkEqual("Tổng theo phòng với loại mới", payroll.calculatePayrollByDepartment("Hỗ trợ"), 35100000)
    contract.displayPayrollInfo()
    print("\nTất cả kiểm thử đều đạt.")


if __name__ == "__main__":
    main()
