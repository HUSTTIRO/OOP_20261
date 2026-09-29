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
    def getBaseSalary(Self):
        return Self.baseSalary
    
    def calculateMonthlyCost(self):
        return self.baseSalary
    def displayInfo(self):
        print(f"ID: {self.id}")
        print(f"Full name: {self.fullName}")
        print(f"Base salary: {self.baseSalary}")       

    def __del__(self):
        print(f"Employee {self.id} đã bị xóa")


class SoftwareEngineer(Employee): # Kế thừa từ employee
    def __init__(self, id="UNKNOWN", fullName="Unnamed employee", baseSalary=0, primaryLanguage = "UNKNOWN" , technicalAllowance = 0):
        super().__init__(id, fullName, baseSalary) #Kế thừa thuộc tính đã có từ employee
        if primaryLanguage == "":
            raise ValueError("primaryLanguage không rỗng")
        if technicalAllowance < 0:
            raise ValueError("technicalAllowance không âm")
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

    