from thefuzz import process
import pandas as pd
from fuzzywuzzy import process
import csv
class Class:
    name = ''
    num_student = 0
    student_list = []
    def __init__(self,name):
        self.name = name
    
    def add(self,student):
        self.student_list.append(student)
        Class.num_student += 1
    def delete(self, msv):
        found = False
        for stu in self.student_list:
            if int(stu.msv) == int(msv):
                self.student_list.remove(stu)
                Class.num_student -= 1 
                found = True
                break 
        if found:
            for i, stu in enumerate(self.student_list, start=1):
                stu.stt = i
            print(f"--> Đã xóa thành công sinh viên có MSV: {msv}")
        else:
            print(f"--> Không tìm thấy sinh viên có MSV: {msv} để xóa.")

    # def insert(self, msv,info):
        
    def show(self):
        if self.student_list == []:
            return None
        data = []
        for stu in self.student_list:
            row = {
                'STT': stu.stt,
                'MSV': stu.msv,
                'Họ Tên': stu.ho_ten,
                'Ngày Sinh': stu.birth,
                'Giới Tính': stu.sex,
                'Chuyên cần':stu.diem['chuyen_can'],
                'Giữa kỳ': stu.diem['gk'],
                'Cuối kỳ': stu.diem['ck']
            }
            data.append(row)
        data = pd.DataFrame(data).to_string(index=False)
        return data 
    def statistic(self):
        stu_stat = {}   # {"Student" , "GPA"}
        for hoc_sinh in self.student_list:  
           chuyen_can = hoc_sinh.diem.get('chuyen_can', 0.0)    # No mark = 0
           gk = hoc_sinh.diem.get('gk', 0.0)
           ck = hoc_sinh.diem.get('ck', 0.0)
           gpa = round((0.1 * chuyen_can) + (0.3 * gk) + (0.6 * ck),1)
           stu_stat[hoc_sinh] = gpa
        return stu_stat
    def show_gpa(self,stu_stat):
        data = []
        for stu in stu_stat:
            row = {
                'STT': stu.stt,
                'MSV': stu.msv,
                'Họ Tên': stu.ho_ten,
                'Ngày Sinh': stu.birth,
                'Giới Tính': stu.sex,
                'Chuyên cần':stu.diem['chuyen_can'],
                'Giữa kỳ': stu.diem['gk'],
                'Cuối kỳ': stu.diem['ck'],
                'GPA' : stu_stat[stu],
            }
            data.append(row)
        data = pd.DataFrame(data).to_string(index=False)
        return data

    def rank(self,stu_stat,bool):   
        if bool == 0:
            rank_stat = dict(sorted(stu_stat.items(), key=lambda item: item[1], reverse=False))   # Thấp -> Cao
        else:
            rank_stat = dict(sorted(stu_stat.items(), key=lambda item: item[1], reverse=True))    # Cao -> Thấp
        data = []
        for stu in rank_stat:
            row = {
                'MSV': stu.msv,
                'Họ Tên': stu.ho_ten,
                'Chuyên cần':stu.diem['chuyen_can'],
                'Giữa kỳ': stu.diem['gk'],
                'Cuối kỳ': stu.diem['ck'],
                'GPA' : stu_stat[stu],
            }
            data.append(row)
        data = pd.DataFrame(data) 
        return data
    def low_mark(self,stu_stat):
        stu_assessment={}
        gpa_list = self.statistic()

        rank_stat = sorted(stu_stat.items(), key=lambda item: item[1], reverse=False)
        low_stat = dict(rank_stat[:5])
        data = []
        for stu in low_stat:
            assess = ''
            if  gpa_list[stu] >= 9.5:
                assess='Xuất sắc'
            elif 9.5> gpa_list[stu] >= 8.5:
                assess = 'Giỏi'
            elif 8.5> gpa_list[stu] >= 7.0:
                assess = 'Khá'
            elif 7.0> gpa_list[stu] >= 6.0:
                assess = 'Trung bình'
            elif 6.0> gpa_list[stu] >= 5.0:
                assess = 'Trung bình yếu'
            elif 5.0> gpa_list[stu] >= 4.0:
                assess='Yếu'
            else:
                assess='Kém'
            row = {
                'MSV': stu.msv,
                'Họ Tên': stu.ho_ten,
                'Chuyên cần':stu.diem['chuyen_can'],
                'Giữa kỳ': stu.diem['gk'],
                'Cuối kỳ': stu.diem['ck'],
                'GPA' : stu_stat[stu],
                'Đánh giá' : assess
            }
            data.append(row)
        data = pd.DataFrame(data) 
        return data   
    def get_assessment(self):
        stu_assessment={}
        gpa_list = self.statistic()
        for stu in self.student_list:
            if  gpa_list[stu] >= 9.5:
                stu_assessment[stu]='Xuất sắc'
            elif 9.5> gpa_list[stu] >= 8.5:
                stu_assessment[stu] = 'Giỏi'
            elif 8.5> gpa_list[stu] >= 7.0:
                stu_assessment[stu] = 'Khá'
            elif 7.0> gpa_list[stu] >= 6.0:
                stu_assessment[stu] = 'Trung bình'
            elif 6.0> gpa_list[stu] >= 5.0:
                stu_assessment[stu] = 'Trung bình yếu'
            elif 5.0> gpa_list[stu] >= 4.0:
                stu_assessment[stu]='Yếu'
            else:
                stu_assessment[stu]='Kém'
        data = []
        for stu in stu_assessment:
            row = {
                'MSV': stu.msv,
                'Họ Tên': stu.ho_ten,
                'Chuyên cần':stu.diem['chuyen_can'],
                'Giữa kỳ': stu.diem['gk'],
                'Cuối kỳ': stu.diem['ck'],
                'GPA' : self.statistic()[stu],
                'Đánh giá' : stu_assessment[stu]
            }
            data.append(row)
        data = pd.DataFrame(data)
        return data             
    def get_letter_mark(self):
        stu_letter_mark={}
        gpa_list = self.statistic()
        for stu in self.student_list:
            if gpa_list[stu] >= 9.5:
                stu_letter_mark[stu] ='A+'
            elif 9.5> gpa_list[stu] >= 8.5:
                stu_letter_mark[stu] = 'A'
            elif 8.5> gpa_list[stu] >= 7.0:
                stu_letter_mark[stu] = 'B'
            elif 7.0> gpa_list[stu] >= 6.0:
                stu_letter_mark[stu] = 'C'
            elif 6.0> gpa_list[stu] >= 5.0:
                stu_letter_mark[stu] = 'D'
            elif 5.0> gpa_list[stu] >= 4.0:
                stu_letter_mark[stu] ='E'
            else:
                stu_letter_mark[stu]='F'
        data = []       
        for stu in stu_letter_mark:
            row = {
                'MSV': stu.msv,
                'Họ Tên': stu.ho_ten,
                'Chuyên cần':stu.diem['chuyen_can'],
                'Giữa kỳ': stu.diem['gk'],
                'Cuối kỳ': stu.diem['ck'],
                'Điểm hệ chữ' : stu_letter_mark[stu]
            }
            data.append(row)
        data = pd.DataFrame(data)
        return data                    
    def get_4_mark(self):
        stu_4_mark={} 
        gpa_list = self.statistic()
        for stu in self.student_list:
            if gpa_list[stu] >= 9.5:
                stu_4_mark[stu] = 4.0
            elif 9.5> gpa_list[stu] >= 8.5:
                stu_4_mark[stu] = 3.5
            elif 8.5> gpa_list[stu] >= 7.0:
                stu_4_mark[stu] = 3.0
            elif 7.0> gpa_list[stu] >= 6.0:
                stu_4_mark[stu] = 2.5
            elif 6.0> gpa_list[stu] >= 5.0:
                stu_4_mark[stu] = 2.0
            elif 5.0> gpa_list[stu] >= 4.0:
                stu_4_mark[stu] = 1.0
            else:
                stu_4_mark[stu] = 0.0
        data = []       
        for stu in stu_4_mark:
            row = {
                'MSV': stu.msv,
                'Họ Tên': stu.ho_ten,
                'Chuyên cần':stu.diem['chuyen_can'],
                'Giữa kỳ': stu.diem['gk'],
                'Cuối kỳ': stu.diem['ck'],
                'Điểm hệ 4' : stu_4_mark[stu]
            }
            data.append(row)
        data = pd.DataFrame(data)
        return data 
    def mark_stat(self):    
        data = {
            "A+ / 4.0 / Xuất sắc" : 0,
            "A / 3.5 / Giỏi": 0 ,
            "B / 3.0 / Khá": 0 ,
            "C / 2.5 / Trung bình" : 0,
            "D / 2.0 / Trung bình yếu" : 0,
            "E / 1.0 / Yếu" : 0,
            "F / 0.0 / Kém" : 0
        }
        gpa_list = self.statistic()
        for stu in self.student_list:
            if gpa_list[stu] >= 9.5:
                data["A+ / 4.0 / Xuất sắc"] += 1
            elif 9.5> gpa_list[stu] >= 8.5:
                data["A / 3.5 / Giỏi"] += 1
            elif 8.5> gpa_list[stu] >= 7.0:
                data["B / 3.0 / Khá"] += 1
            elif 7.0> gpa_list[stu] >= 6.0:
                data["C / 2.5 / Trung bình"] += 1
            elif 6.0> gpa_list[stu] >= 5.0:
                data["D / 2.0 / Trung bình yếu"] += 1
            elif 5.0> gpa_list[stu] >= 4.0:
                data["E / 1.0 / Yếu"] += 1
            else:
                data["F / 0.0 / Kém"] += 1                
        for criteria,count in data.items():
            print(f'{criteria} : {count}')

    def Search_by_msv(self, target):
        l = 0
        r = self.num_student - 1
        ans = -1
        while r >= l:
            mid = (r + l)//2
            if self.student_list[mid].msv >= target:
                ans = mid
                r = mid - 1
            else : l = mid + 1
        if ans == -1: print("Not Found!")
        else:
            tmp = self.student_list[ans]
            dic = {"STT":tmp.stt, "Mã sinh vien": tmp.msv, "Họ và tên": tmp.ho_ten, "Ngày sinh" : tmp.birth, "Giới tính": tmp.sex, "Điểm chuyên cần": tmp.diem['chuyen_can'], "Điểm giữa kì": tmp.diem['gk'], "Điểm cuối kì": tmp.diem['ck']}
            df = pd.DataFrame([dic])
            print(df)
    def Search_by_point_range(self, minpt, maxpt, type):
        # 0 - he 10
        # 1 - he 4
        # 2 - he chu
        if type == 1:
            minpt = float(minpt)
            maxpt = float(maxpt)
        if type == 2:
            minpt = float(minpt)*10/4
            maxpt = float(maxpt)*10/4
        if type == 3:
            if minpt == 'A': minpt = float(8.5)
            if minpt == 'B+': minpt = float(8.0)
            if minpt == 'B': minpt = float(7.0)
            if minpt == 'C+': minpt = float(6.5)
            if minpt == 'C': minpt = float(5.5)
            if minpt == 'D+': minpt = float(5.0)
            if minpt == 'D': minpt = float(4.0)
            if minpt == 'F': minpt = float(0)
            if maxpt == 'A': maxpt = float(10.0)
            if maxpt == 'B+': maxpt = float(8.4)
            if maxpt == 'B': maxpt = float(7.9)
            if maxpt == 'C+': maxpt = float(6.9)
            if maxpt == 'C': maxpt = float(5.4)
            if maxpt == 'D+': maxpt = float(5.4)
            if maxpt == 'D': maxpt = float(4.9)
            if maxpt == 'F': maxpt = float(0)
        ok = 0
        dic = {"STT": [], "Mã sinh viên": [], "Họ và tên": [], "Ngày sinh": [], "Giới tính": [], "Điểm chuyên cần": [], "Điểm giữa kì": [], "Điểm cuối kì": []}
        for i in range(self.num_student):
            cc = self.student_list[i].diem['chuyen_can']
            gk = self.student_list[i].diem['gk']
            ck = self.student_list[i].diem['ck']
            stt = self.student_list[i].stt
            msv = self.student_list[i].msv
            ho_ten = self.student_list[i].ho_ten
            birth = self.student_list[i].birth
            sex = self.student_list[i].sex
            tmp = cc*0.1 + gk*0.3 + ck*0.6
            if tmp >= minpt and tmp <= maxpt:
                ok = 1
                dic['STT'].append(stt)
                dic['Giới tính'].append(sex)
                dic['Họ và tên'].append(ho_ten)
                dic['Mã sinh viên'].append(msv)
                dic['Ngày sinh'].append(birth)
                dic['Điểm chuyên cần'].append(cc)
                dic['Điểm cuối kì'].append(ck)
                dic['Điểm giữa kì'].append(gk)
        if ok == 0:print("Not Found!")
        else:
            df = pd.DataFrame(dic)
            print(df)
    def Search_by_name(self, name):
        name_list = []
        ok = 0
        for it in self.student_list:   name_list.append(it.ho_ten)
        choices_dict = {idx: el for idx, el in enumerate(name_list)}
        matches = process.extract(name, choices_dict, limit = self.num_student)
        good_indices = [x[2] for x in matches if x[1] >= 80]
        dic = {
            "STT": [], "Mã sinh viên": [], "Họ và tên": [], 
            "Ngày sinh": [], "Giới tính": [], 
            "Điểm chuyên cần": [], "Điểm giữa kì": [], "Điểm cuối kì": []
        }
        for it in good_indices:
            student = self.student_list[it] 
            dic["STT"].append(student.stt)
            dic["Mã sinh viên"].append(student.msv)
            dic["Họ và tên"].append(student.ho_ten)
            dic["Ngày sinh"].append(student.birth)
            dic["Giới tính"].append(student.sex)
            dic["Điểm chuyên cần"].append(student.diem['chuyen_can'])
            dic["Điểm giữa kì"].append(student.diem['gk'])
            dic["Điểm cuối kì"].append(student.diem['ck'])
        if len(good_indices) == 0:
            print("Not Found!")
        else:
            df = pd.DataFrame(dic)
            print(df)

class Student:
    stt = 0
    msv = 0
    ho_ten = ''
    birth = ''
    sex = ''
    diem = {'chuyen_can': 0.0,'gk': 0.0,'ck' : 0.0}
        
    def __init__(self, stt,msv,ho_ten,birth,sex,diem):
        self.stt = stt
        self.msv = msv
        self.ho_ten = ho_ten
        self.birth = birth
        self.sex = sex
        self.diem = diem
        
    def show(self): # print 1 hoc sinh
        data = []
        row = {
            'STT': self.stt,
            'MSV': self.msv,
            'Họ Tên': self.ho_ten,
            'Ngày Sinh': self.birth,
            'Giới Tính': self.sex,
            'Chuyên cần':self.diem['chuyen_can'],
            'Giữa kỳ': self.diem['gk'],
            'Cuối kỳ': self.diem['ck']
        }
        data.append(row)
        data = pd.DataFrame(data).to_string(index=False)
        return data

    def __eq__(self, other):    # Equal (=) trùng msv
        if not isinstance(other, Student):
            return False
        return self.msv == other.msv  
    def __hash__(self): # Mã hóa svien theo msv
        return hash(self.msv)  

def read(file_name): #Tạo hàm đọc dữ liệu đầu vào
    danh_sach_hoc_sinh = Class('CS4')
    try:
        with open(file_name, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f) 
            
            for row in reader:
                hoc_sinh = Student(row['STT'],row['MSSV'],row['Họ và tên'],row['Ngày sinh'],row['Giới tính'],{'chuyen_can': float(row['Chuyên cần']),'gk': float(row['Giữa kỳ']),'ck' : float(row['Cuối kỳ'])})
                danh_sach_hoc_sinh.add(hoc_sinh)
                
        print(f"--> Đã nhập thành công {danh_sach_hoc_sinh.num_student} học sinh!")
        return danh_sach_hoc_sinh

    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file tên là '{file_name}'")
        return []
    except ValueError:
        print("Lỗi: Có dữ liệu điểm không phải là số trong file.")
        return []


# --- CHƯƠNG TRÌNH CHÍNH ---


text = "Student Management System (Made by Goonmaster3000)"
print(text.center(50,'*'))
ten_file = 'hocsinh.csv'
data_hoc_sinh = read(ten_file)
# print(data_hoc_sinh.show())

def menu_tinh_toan():
    while True:
        print("\n--- NHÓM 1: TÍNH TOÁN & CHUYỂN ĐỔI ---")
        print("1. Tính điểm GPA")
        print("2. Chuyển đổi điểm số sang điểm chữ (A, B, C...)")
        print('3. Chuyển đổi điểm số sang hệ số 4')
        print("4. Tính xếp loại học lực")
        print("0. Quay lại Menu chính") # Chức năng quay lại
        
        chon = input(">> Nhập lựa chọn của bạn: ")
        
        if chon == '1':
            print("[Info] Đang thực hiện tính điểm GPA...")
            print(data_hoc_sinh.show_gpa(data_hoc_sinh.statistic()))
        elif chon == '2':
            print("[Info] Đang đổi điểm số sang điểm chữ (A, B, C...)")
            print(data_hoc_sinh.get_letter_mark())
        elif chon == '3':
            print("[Info] Đang đổi điểm số sang hệ số 4...")
            print(data_hoc_sinh.get_4_mark())
        elif chon == '4':
            print("[Info] Đang tính xếp loại học lực...")
            print(data_hoc_sinh.get_assessment())
        elif chon == '0':
            print(">> Đang quay lại...")
            break # Thoát vòng lặp này để về Menu chính
        else:
            print("! Lựa chọn không hợp lệ, vui lòng chọn lại.")

def menu_tim_kiem():
    while True:
        print("\n--- NHÓM 2: TÌM KIẾM ---")
        print("1. Tìm theo Tên")
        print("2. Tìm theo Mã số sinh viên")
        print("3. Tìm theo khoảng điểm")
        print("0. Quay lại Menu chính")
        
        chon = input(">> Nhập lựa chọn của bạn: ")
        
        if chon == '1':
            name = input("Nhập tên sinh viên : ")
            print("[Info] Đang tìm theo tên...")
            data_hoc_sinh.Search_by_name(name)
            
        elif chon == '2':
            msv = input("Nhập mã sinh viên:")
            print("[Info] Đang tìm theo ID...")
            data_hoc_sinh.Search_by_msv(msv)
        elif chon == '3':            
            type = int(input('''Chọn hệ số điểm
1. Hệ số 10
2. Hệ số 4
3. Điểm chữ

>> Nhập vào lựa chọn của bạn: '''))
            start = input("Nhập điểm bắt đầu: ")
            end = input("Nhập điểm kết thúc: ")
            print("[Info] Đang tìm theo khoảng điểm...")
            data_hoc_sinh.Search_by_point_range(start, end, type)
        elif chon == '0':
            break 
        else:
            print("! Lựa chọn không hợp lệ.")

def menu_thong_ke():
    while True:
        print("\n--- NHÓM 3: THỐNG KÊ ---")
        print("1. Thống kê số lượng Giỏi/Khá/TB")
        print("2. Thống kê GPA")
        print("3. Cảnh báo học tập")
        print("0. Quay lại Menu chính")
        
        chon = input(">> Nhập lựa chọn của bạn: ")
        
        if chon == '1':
            print("[Info] Đang thống kê số lượng Giỏi/Khá/TB...")
            data_hoc_sinh.mark_stat()
        elif chon == '2':
            reverse = int(input('''
0. Từ thấp đến cao
1. Từ cao xuống thấp

>> Nhập vào lựa chọn của bạn: '''))
            print("[Info] Đang thống kê GPA ")
            print(data_hoc_sinh.rank(data_hoc_sinh.statistic(),reverse))
        elif chon == '3':
            print("[Info] Đang thống kê")
            print('Những sinh viên nằm trong danh sách cảnh báo học tập:')
            bang=data_hoc_sinh.low_mark(data_hoc_sinh.statistic())
            print(bang)
            print(f'YÊU CẦU CÁC SINH VIÊN TRÊN, ĐẶC BIỆT LÀ 2 ANH {str(bang['Họ Tên'].iloc[0]).upper()}, {str(bang['Họ Tên'].iloc[1]).upper()} CHỈNH ĐỐN HỌC TẬP KHÔNG THÌ ĐUỔI HỌC!!!')
        elif chon == '0':
            break 
        else:
            print("! Lựa chọn không hợp lệ.")

def menu_cap_nhat():
    while True:
        print("\n--- NHÓM 4: CẬP NHẬT ---")
        print("1. Thêm học sinh mới")
        print("2. Sửa thông tin sinh viên")
        print("3. Xóa học sinh")
        print("0. Quay lại Menu chính")
        
        chon = input(">> Nhập lựa chọn của bạn: ")
        
        if chon == '1':
            print("[Info] Thêm mới...")
            new = Student(data_hoc_sinh.num_student + 1, int(input("MSV: ")), input("Họ tên: "), input("Ngày sinh: "), input("Giới tính: "), {'chuyen_can':input("Điểm chuyên cần: "), 'gk': input("Điểm giữa kỳ: "), 'ck' : input("Điểm cuối kỳ: ")})
            data_hoc_sinh.add(new)
            print(new.show())
        elif chon == '2':
            msv = int(input("Nhập MSV của sinh viên cần sửa: "))
            choice = input('''
1. Tên
2. Ngày sinh
3. Giới tính
4. Điểm chuyên cần
5. Điểm giữa kỳ
6. Điểm cuối kỳ     
>> Nhập lựa chọn của bạn: ''')
            info = input("Nhập thông tin: ")
            print("[Info] Sửa thông tin...")
            check = False
            for stu in data_hoc_sinh.student_list:
                if int(stu.msv) == int(msv):
                    check = True
                    if choice == '1':
                        stu.ho_ten = info
                    elif choice == '2':
                        stu.birth = info
                    elif choice == '3':
                        stu.sex = info
                    elif choice == '4':
                        stu.diem['chuyen_can'] = info
                    elif choice == '5':
                        stu.diem['gk'] = info
                    elif choice == '6':
                        stu.diem['ck'] = info
                    else:
                        print("Thông tin không hợp lệ")
                    break
            if check:
                print("Đã sửa thông tin thành công")
            else:
                print("Mã sinh viên không hợp lệ.")
                    
        elif chon == '3':
            msv = int(input("Nhập MSV của sinh viên cần xóa: "))
            print("[Info] Xóa học sinh...")
            data_hoc_sinh.delete(msv)
        elif chon == '0':
            break 
        else:
            print("! Lựa chọn không hợp lệ.")

# --- MENU CHÍNH (LEVEL 1) ---

def main():
    while True:
        # Có thể dùng os.system('cls') hoặc 'clear' để làm sạch màn hình nếu muốn
        print("\n========================================")
        print("   CHƯƠNG TRÌNH QUẢN LÝ HỌC SINH")
        print("========================================")
        print("1. Tính toán & Chuyển đổi điểm")
        print("2. Tìm kiếm thông tin")
        print("3. Báo cáo & Thống kê")
        print("4. Cập nhật dữ liệu")
        print("0. Thoát chương trình")
        print("========================================")
        
        chon = input(">> Chọn nhóm chức năng (0-4): ")
        
        if chon == '1':
            menu_tinh_toan() # Nhảy vào vòng lặp con
        elif chon == '2':
            menu_tim_kiem()
        elif chon == '3':
            menu_thong_ke()
        elif chon == '4':
            menu_cap_nhat()
        elif chon == '0':
            print("Tạm biệt! Hẹn gặp lại.")
            break
        else:
            print("! Lựa chọn không hợp lệ, vui lòng thử lại.")

if __name__ == "__main__":
    main()



