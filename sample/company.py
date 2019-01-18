# class Company():
#     def __init__(self, employee_list):
#         self.employee = employee_list

#     def __getitem__(self, item):
#         return self.employee[item]

# company = Company(['zhh', 'hzl', 'zc'])
# for em in company:
#     print(em)
class Company():
    def __init__(self, employee_list):
        self.employee = employee_list

    def __len__(self):
        return len(self.employee)

company = Company(['zhh', 'hzl', 'zc'])
print(len(company))
