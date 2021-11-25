import csv
import time
import numpy as np

def user_once_select():
    print("\n종료를 원하면 0을 입력해주세요.")          
    user_input = input("찾고싶은 지역을 입력해주세요 (ex.서울특별시 경기도 대구광역시) : ") 
    return user_input 
        
def once_pop_GDP(user_input):
    population = []
    # 도시(경기도)의 인구 데이터를 csv파일에서 가져옴
    with open('dataset/' + user_input + "_주민등록인구및세대현황_월간.csv","r") as nation_pop :
        print("Succeeded in calling", user_input + "_주민등록인구및세대현황_월간.csv!")
        for line in nation_pop :
            population.append(line.strip('\n').split(','))

    # 도시 문자열을 도시 이름으로 가공하는 과정 (ex.'경기도 수원시' -> '수원시')
    for i in range(len(population)) : 
        population[i][0] = population[i][0].replace(' ','')
        population[i][0] = population[i][0].replace(user_input,'')
        population[i][0] = population[i][0].replace('(','')
        population[i][0] = population[i][0].replace(')','')
        population[i][0] = population[i][0].replace('"','')

        # 도시 문자열의 불필요한 숫자들을 제거하는 과정
        for j in range(10) :
            j = str(j)
            population[i][0] = population[i][0].replace(j,'')


    # 사용자가 입력할 도시 선택
    for i in range(len(population)-1) :
        print(population[i][0],end=' / ')
    print(population[i+1][0])


    # 지역의 총생산량 파일 불러오는 과정
    allGDP = []
    with open('dataset/' + user_input + "_경제활동별_지역내총생산.csv","r") as nation_GDP :
        for line in nation_GDP :
            allGDP.append(line.strip('\n').split(','))

    # 도시 문자열을 도시 이름으로 가공하는 과정 (ex.'경기도 수원시' -> '수원시')
    for i in range(len(allGDP)) : 
        allGDP[i][1] = allGDP[i][1].replace(',',' ')
        allGDP[i][1] = allGDP[i][1].replace('"','')
        allGDP[i][0] = allGDP[i][0].replace('"','')
        allGDP[i][1] = allGDP[i][1].replace('지역내총생산(시장가격)','총GDP')
        allGDP[i][2] = allGDP[i][2].replace(',',' ')
        allGDP[i][2] = allGDP[i][2].replace('"','')
        allGDP[i][1] = allGDP[i][1].replace('"','')
        allGDP[i][2] = allGDP[i][2].replace('지역내총생산(시장가격)','총GDP')

    # 컴마 항목 오류 해결    
    for i in range(len(allGDP)) :
        if allGDP[i][2] == ' 가스' or allGDP[i][2] == '가스' or allGDP[i][2] == ' 영상' or allGDP[i][2] == '영상' or allGDP[i][2] == ' 국방 및  사회보장행정' or allGDP[i][2] == '국방및사회보장행정' or allGDP[i][2] == ' 국방 및 사회보장행정'or allGDP[i][2] == '국방 및 사회보장행정' : 
            for j in range(len(allGDP[i])-3) :
                allGDP[i][1] += ',' + allGDP[i][2]
                allGDP[i].remove(allGDP[i][2])
            allGDP[i][1] = allGDP[i][1].replace('"','')
            allGDP[i][1] = allGDP[i][1].replace(' ','')

    return population, allGDP

def user_twice_city_select(user_input, population):
    print("\n",user_input, sep ='')     
    first_city = input("확인하고 싶은 첫 번째 도시를 선택해 주세요 : ")
    second_city = input("확인하고 싶은 두 번째 도시를 선택해 주세요 : ")
    # 선택한 도시의 인구 수 출력 과정
    for i in range(len(population)) :      
        if first_city == population[i][0] :
            print(first_city,'인구 수 :',population[i][1],'명')
            user_first_pop = population[i][1]
        elif second_city == population[i][0] :
            print(second_city,'인구 수 :',population[i][1],'명')
            user_second_pop = population[i][1]
    print("")
    
    return first_city, second_city, user_first_pop, user_second_pop

def twice_city_GDP(user_input, allGDP, first_city, second_city):
    if user_input == '대구광역시' or user_input == '충청남도' :
        first_GDP_value = []
        first_GDP_name = []
        for i in range(len(allGDP)) :
            if first_city == allGDP[i][0] :
                first_GDP_name.append(allGDP[i][2])   # 컴마(,)로 이루어진 항목 탓에 이름이 잘려나오는 항목이 있음
                first_GDP_value.append(allGDP[i][3])  # 모든 이름을 출력하기 위해 방법 구상 중 // 해결 완료

        second_GDP_value = []
        second_GDP_name = []

        for i in range(len(allGDP)) :
            if second_city == allGDP[i][0] :
                second_GDP_name.append(allGDP[i][2]) 
                second_GDP_value.append(allGDP[i][3])

    else :     
        # 도시 별로 GDP 지정
        first_GDP_value = []
        first_GDP_name = []

        for i in range(len(allGDP)) :
            if first_city == allGDP[i][0] :
                first_GDP_name.append(allGDP[i][1])   # 컴마(,)로 이루어진 항목 탓에 이름이 잘려나오는 항목이 있음
                first_GDP_value.append(allGDP[i][2])  # 모든 이름을 출력하기 위해 방법 구상 중 // 해결 완료

        second_GDP_value = []
        second_GDP_name = []
        
        for i in range(len(allGDP)) :
            if second_city == allGDP[i][0] :
                second_GDP_name.append(allGDP[i][1]) 
                second_GDP_value.append(allGDP[i][2])

    # 산업 종류 출력
    print('산업 종류')
    for i in range(len(first_GDP_name)-1) :
        print(first_GDP_name[i],end=' / ')
    print(first_GDP_name[i+1])

    return first_GDP_name, first_GDP_value, second_GDP_name, second_GDP_value

def compare_GDP(user_industry_input, first_GDP_name, first_GDP_value, second_GDP_name, second_GDP_value, first_city, second_city, user_first_pop, user_second_pop):
    #두 도시에 지정한 산업의 GDP 값 비교
    for i in range(len(first_GDP_name) - 1) :
        comparardGDP = int(first_GDP_value[i]) - int(second_GDP_value[i])
        if user_industry_input == first_GDP_name[i] :
            if first_GDP_value[i] == '0' or second_GDP_value[i] == '0' :
                print("도시에 해당 산업이 확인되지 않습니다.")
                break                                        
            else :
                GDPOne = round(int(first_GDP_value[i])/int(user_first_pop),4)
                GDPTwo = round(int(second_GDP_value[i])/int(user_second_pop),4)
                compareFGDPvalue = 100*round(GDPOne/GDPTwo,4)
                compareSGDPvalue = 100*round(GDPTwo/GDPOne,4)
                
                print()
                print(first_city, user_industry_input, 'GDP :', first_GDP_value[i], '(단위 : 백만원)')
                print(second_city, user_industry_input, 'GDP :', second_GDP_value[i], '(단위 : 백만원)')
                print(first_city, user_industry_input, '1인당 GDP :', GDPOne)
                print(second_city, user_industry_input, '1인당 GDP :', GDPTwo)

                if comparardGDP > 0 :
                    print("1인당,",second_city, '대비', first_city, user_industry_input,'GDP :', compareFGDPvalue, '% ', '약', round(compareFGDPvalue/100,2),'배')
                else :
                    print("1인당,",first_city, '대비', second_city, user_industry_input,'GDP :', compareSGDPvalue, '% ', '약', round(compareSGDPvalue/100,2),'배')

def once_GDP_pop_bring():
    # 지정한 한 지역의 도시 두 개의 인구와 GDP 비교
    while True :
        user_input = user_once_select()

        if user_input == '0' : break

        population, allGDP = once_pop_GDP(user_input)

        while True :
            # 희망하는 지역의 두 도시를 입력 받음
            first_city, second_city, user_first_pop, user_second_pop = user_twice_city_select(user_input, population)

            first_GDP_name, first_GDP_value, second_GDP_name, second_GDP_value = twice_city_GDP(user_input, allGDP, first_city, second_city)
    
            # 사용자에게 산업을 선택받음
            while True :
                # print("\n",first_city, ' ',second_city, sep ='')
                user_industry_input = input('확인하고 싶은 산업을 선택해 주세요 : ')

                compare_GDP(user_industry_input, first_GDP_name, first_GDP_value, second_GDP_name, second_GDP_value, first_city, second_city, user_first_pop, user_second_pop)
         