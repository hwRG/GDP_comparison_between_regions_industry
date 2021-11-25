import csv
import time
import pop_GDP_bring, once_pop_GDP

def user_select():
    print("\n==================================================")
    print("지역, 산업 간 GDP 비교 및 확인 프로그램")
    time.sleep(0.5)
    print("종료를 원하시는 경우 바로 엔터를 눌러주세요.")
    time.sleep(0.5)
    print("==================================================")
    user_input = input("전국의 데이터를 불러오시겠습니까? (Yes or No) : ")

    return user_input   

            
def main():
    while(True):
        user_input = user_select()
        # 지역별로 검색 후 지정한 산업의 가장 높은 수치의 도시 찾아내기
        if user_input == 'Yes' or user_input == 'yes' or user_input == '응' :
            pop_GDP_bring.all_pop_GDP_bring()

        elif user_input == 'No' or user_input == 'no' or user_input == '아니' :
            once_pop_GDP.once_GDP_pop_bring()
            
        else : break

if __name__ == "__main__":
    main()
