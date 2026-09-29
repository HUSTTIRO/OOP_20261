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
    def getfullName(self):
        return self.fullName
    def calculateMonthlyCost(self):
        return self.baseSalary
    def displayInfo(self):
        print(f"ID: {self.id}")
        print(f"Full name: {self.fullName}")
        print(f"Base salary: {self.baseSalary}")       

class SoftwareEngineer(Employee): # Kế thừa từ employee
    def __init__(self, id="UNKNOWN", fullName="Unnamed employee", baseSalary=0, primaryLanguage = "UNKNOWN" , technicalAllowance = 0):
        super().__init__(id, fullName, baseSalary) #Kế thừa thuộc tính đã có từ employee
        self.primaryLanguage = primaryLanguage
        self.technicalAllowance = technicalAllowance

    def calculateMonthlyCost(self):
        return self.baseSalary + self.technicalAllowance
    def displayInfo(self):
        pass