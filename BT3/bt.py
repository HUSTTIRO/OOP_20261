"""
# Mã sinh viên: 20241900
# Họ tên: Nguyễn Tuấn Trường
"""
class Employee:
    def __init__(self, id = "UNKNOWN", fullName = "Unnamed employee", baseSalary = 0):
        if id == "":
            raise ValueError("Giá trị id phải khác rỗng")
        self.id = id
        if fullName == "":
            raise ValueError("Full name phải khác rỗng")
        self.fullName = fullName
        if baseSalary < 0:
            raise ValueError("Giá trị lương không âm")
        self.baseSalary = baseSalary
    def increaseSalary(self, value, byPercentage=False):
        if value <= 0:
            raise ValueError("Tăng lương phải dương")
        if byPercentage :
            self.baseSalary = self.baseSalary*(1+value/100)    
        else: 
            self.baseSalary += value

    def getId(self):
        return self.id
    def getFullName(self):
        return self.fullName
    def getBaseSalary(self):
        return self.baseSalary
    
    def calculateMonthlyCost(self):
        return self.baseSalary
    def displayInfo(self):
        print(f"ID: {self.id}")
        print(f"Full name: {self.fullName}")
        print(f"Base salary: {self.baseSalary}")       

    def __del__(self):
        print(f"Employee {self.id} đã bị xóa")


class SoftwareEngineer(Employee):
    #Dùng *args để gom các tham số sau fullName vào 1 tuple, rồi đếm số lượng
    def __init__(self, id, fullName, *args):
        if len(args) == 1:
            baseSalary = 0
            primaryLanguage = args[0]
            technicalAllowance = 0
        else:
            baseSalary, primaryLanguage, technicalAllowance = args
        if primaryLanguage == "":
            raise ValueError("primaryLanguage không rỗng")
        if technicalAllowance < 0:
            raise ValueError("technicalAllowance không âm")
        super().__init__(id, fullName, baseSalary)
        self.primaryLanguage = primaryLanguage
        self.technicalAllowance = technicalAllowance
    #ghi đè 2 hàm:
    def calculateMonthlyCost(self):
        return self.baseSalary + self.technicalAllowance
    def displayInfo(self):
        print(f"ID: {self.id}")
        print(f"Full name: {self.fullName}")
        print(f"Base salary: {self.baseSalary}")      
        print(f"Primary language: {self.primaryLanguage}")
        print(f"Technical Allowance: {self.technicalAllowance}")
    def __del__(self):
        print(f"SoftwareEngineer {self.id} đã bị xóa")
        super().__del__()


class ProjectTeam:
    def __init__(self, projectCode, projectName, leader=None):
        self.projectCode = projectCode
        self.projectName = projectName
        self.leader = None
        self.members = []
        if leader is not None:
            self.addMember(leader, True)
 
    def contains(self, employeeId):
        for m in self.members:
            if m.getId() == employeeId:
                return True
        return False
 
    def addMember(self, employee, makeLeader=False):
        if self.contains(employee.getId()):
            print(f"{employee.getId()} đã có trong nhóm")
            return False
        self.members.append(employee)
        if makeLeader:
            self.leader = employee
        return True
    def removeMember(self, employeeId):
        if self.leader is not None and self.leader.getId() == employeeId:
            print("Không thể xóa trưởng nhóm")
            return False
        for m in self.members:
            if m.getId() == employeeId:
                self.members.remove(m)
                return True
        print("Không tìm thấy nhân sự")
        return False
 
    def changeLeader(self, employee):
        if not self.contains(employee.getId()):
            self.members.append(employee)
        self.leader = employee
 
    def calculateTotalMonthlyCost(self):
        total = 0
        for m in self.members:
            total += m.calculateMonthlyCost()
        return total
 
    def displayTeam(self):
        print(f"Nhóm {self.projectCode} - {self.projectName}")
        if self.leader is not None:
            print(f"Trưởng nhóm: {self.leader.getFullName()}")
        else:
            print("Trưởng nhóm: chưa có")
        for m in self.members:
            m.displayInfo()
 
    def __del__(self):
        print(f"ProjectTeam {self.projectCode} đã bị xóa")
        self.members.clear()
        self.leader = None

 
def main():
    print("1. Tạo hai Employee")
    e1 = Employee("E01", "Nguyễn Văn An")
    e2 = Employee("E02", "Trần Thị Bình", 15000000)
    e1.displayInfo()
    e2.displayInfo()
 
    print("\n2. Tạo hai SoftwareEngineer")
    se1 = SoftwareEngineer("SE01", "Lê Minh Cường", "Python")
    se2 = SoftwareEngineer("SE02", "Phạm Thu Dung", 25000000, "C#", 5000000)
    se1.displayInfo()
    se2.displayInfo()
 
    print("\n3. Tăng lương cố định")
    e2.increaseSalary(2000000)
    e2.displayInfo()
 
    print("\n4. Tăng lương theo phần trăm")
    se2.increaseSalary(10, True)
    se2.displayInfo()
 
    print("\n5. Tạo nhóm chưa có trưởng nhóm")
    team1 = ProjectTeam("P01", "Ứng dụng quản lý thư viện")
    team1.displayTeam()
 
    print("\n6. Thêm nhân sự")
    print(team1.addMember(e2))
 
    print("\n7. Thêm kỹ sư làm trưởng nhóm")
    print(team1.addMember(se2, True))
 
    print("\n8. Thêm lại thành viên đã có")
    print(team1.addMember(e2))
 
    print("\n9. Hiển thị danh sách")
    team1.displayTeam()
 
    print("\n10. Tổng chi phí hằng tháng")
    print(team1.calculateTotalMonthlyCost())
 
    print("\n11. Xóa trưởng nhóm")
    print(team1.removeMember("SE02"))
 
    print("\n12. Đổi trưởng nhóm rồi xóa trưởng nhóm cũ")
    team1.changeLeader(e2)
    print(team1.removeMember("SE02"))
    team1.displayTeam()
 
    print("\n13. Tạo nhóm thứ hai")
    team2 = ProjectTeam("P02", "Hệ thống chấm công", se1)
    team2.addMember(e2)             # e2 đã có ở nhóm 1 -> 1 người thuộc 2 nhóm
    team2.displayTeam()

    print("\n14. Hủy nhóm thứ hai")
    del team2                       # Xóa biến team2 -> nhóm bị hủy, __del__ chạy ngay
 
    print("\n15. Nhân sự vẫn tồn tại sau khi nhóm bị hủy")
    e2.displayInfo()
    se1.displayInfo()
 
    print("\nKết thúc chương trình")
main()