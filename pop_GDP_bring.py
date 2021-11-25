import csv
import time

import matplotlib.pyplot as plt
import numpy as np
 
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)    

regionDic = {0 : '서울특별시', 1 : '경기도', 2 : '인천광역시', 3 : '부산광역시', 4 : '대전광역시', 
             5 : '대구광역시', 6 : '광주광역시', 7 : '울산광역시', 8 : '충청북도', 9 : '충청남도', 
             10 : '전라북도', 11 : '전라남도', 12 : '경상북도', 13 : '경상남도'} 

def user_select():
    print("\n==================================================")
    print("지역, 산업 간 GDP 비교 및 확인 프로그램")
    time.sleep(0.5)
    print("종료를 원하시는 경우 바로 엔터를 눌러주세요.")
    time.sleep(0.5)
    print("==================================================")
    user_input = input("전국의 데이터를 불러오시겠습니까? (Yes or No) : ")

    return user_input

def user_compare_select(allGDP):
    print('\n산업 종류')
    for i in range(13) :
        print(allGDP[1][i+3][1], end=' / ')
    print(allGDP[1][i+4][1], "\n※ 도매및소매업, 출판영상방송통신및정보서비스업, 부동산및임대업은 확인 불가 ※")

    print("\nIf you want to back, press 0")
    user_industry_input = input("Select the industry you want to compare. : ")

    return user_industry_input

def pop_GDP_bring():
    population = []
    allGDP = []
    tempPop = []
    tempGDP = []

    print("")

    # 모든 지역의 인구 수를 리스트에 저장 (3중 리스트)
    for i in range(len(regionDic)) :
        with open('dataset/' + str(regionDic[i]) + "_주민등록인구및세대현황_월간.csv","r") as nation_pop :
            for line in nation_pop :
                tempPop.append(line.strip('\n').split(','))
            print("Succeeded in calling", str(regionDic[i]) + "_주민등록인구및세대현황_월간.csv!")
            population.append(tempPop)
            tempPop = []
        
    # 도시 문자열을 도시 이름으로 가공하는 과정 (ex.'경기도 수원시' -> '수원시')
    for k in range(len(regionDic)) :
        for i in range(len(population[k])) : 
            population[k][i][0] = population[k][i][0].replace(' ','')
            population[k][i][0] = population[k][i][0].replace(regionDic[k],'')
            population[k][i][0] = population[k][i][0].replace('(','')
            population[k][i][0] = population[k][i][0].replace(')','')
            population[k][i][0] = population[k][i][0].replace('"','')

            # 도시 문자열의 불필요한 숫자들 제거
            for j in range(10) :
                population[k][i][0] = population[k][i][0].replace(str(j),'')


    # 모든 지역의 GDP를 리스트에 저장 (3중 리스트)
    for i in range(len(regionDic)) :
        with open('dataset/' + str(regionDic[i]) + "_경제활동별_지역내총생산.csv","r") as nation_GDP :
            for line in nation_GDP :
                tempGDP.append(line.strip('\n').split(','))
            print("Succeeded in calling", str(regionDic[i]) + "_경제활동별_지역내총생산.csv!")
            allGDP.append(tempGDP)
            tempGDP = []

    # 도시 문자열을 도시 이름으로 가공 (ex.'경기도 수원시' -> '수원시')
    for k in range(len(regionDic)) :
        for i in range(len(allGDP[k])) : 
            allGDP[k][i][0] = allGDP[k][i][0].replace('"','')
            allGDP[k][i][1] = allGDP[k][i][1].replace(',',' ')
            allGDP[k][i][1] = allGDP[k][i][1].replace('"','')
            allGDP[k][i][1] = allGDP[k][i][1].replace('지역내총생산(시장가격)','총GDP')
            allGDP[k][i][1] = allGDP[k][i][1].replace('"','')
            allGDP[k][i][2] = allGDP[k][i][2].replace(',',' ')
            allGDP[k][i][2] = allGDP[k][i][2].replace('"','')
            allGDP[k][i][2] = allGDP[k][i][2].replace('지역내총생산(시장가격)','총GDP')

    # GDP 항목의 컴마 오류 해결    
    for k in range(len(regionDic)) :
        for i in range(len(allGDP[k])) :
            if allGDP[k][i][2] == ' 가스' or allGDP[k][i][2] == '가스' or allGDP[k][i][2] == ' 영상' or allGDP[k][i][2] == '영상' or allGDP[k][i][2] == ' 국방 및  사회보장행정' or allGDP[k][i][2] == '국방및사회보장행정' or allGDP[k][i][2] == ' 국방 및 사회보장행정' or allGDP[k][i][2] == '국방 및 사회보장행정' or allGDP[k][i][2] == '국방 및  사회보장행정' or allGDP[k][i][2] == '국방및사회보장행정': 
                for j in range(len(allGDP[k][i])-3) :
                    allGDP[k][i][1] += ',' + allGDP[k][i][2]
                    allGDP[k][i].remove(allGDP[k][i][2])
                allGDP[k][i][1] = allGDP[k][i][1].replace('"','')
                allGDP[k][i][1] = allGDP[k][i][1].replace(' ','')
                allGDP[k][i][1] = allGDP[k][i][1].replace(',','')

    # 지역 산업의 GDP가 0일 때 '-' 라고 표기된 것을 '0'으로 수정            
    for i in range(len(regionDic)) :
        for j in range(len(allGDP[i])) :
            if i == 5 or i == 9 :
                if allGDP[i][j][3] == '-' :
                    allGDP[i][j][3] = '0'
            else :
                if allGDP[i][j][2] == '-' :
                    allGDP[i][j][2] = '0'


    # 지역마다 다른 이름 구성으로 인해 띄어쓰기를 없애고 최대한 이름 통일
    for k in range(len(regionDic)) :
        for i in range(len(allGDP[k])) :    
            for j in range(len(allGDP[k][i])) :
                allGDP[k][i][j] = allGDP[k][i][j].replace(' ','') 

    return population, allGDP
    
def region_best_industry(allGDP, user_industry_input):
    hope_GDP = []
    hope_GDP_name = []
    temp_hope_GDP = []
    temp2_hope_GDP = []   

    # 지역 별로 지정한 산업의 가장 높은 수치를 지니고 있는 산업 선택 후 리스트 저장
    for i in range(len(regionDic)) :
        # 대구와 충청남도는 csv파일에서 다르게 저장되어 다르게 저장
        if i == 5 or i == 9 :
            for j in range(len(allGDP[i])) :
                if allGDP[i][j][2] == user_industry_input :
                    temp_hope_GDP.append(allGDP[i][j][3])
                for m in range(len(temp_hope_GDP)) :
                    temp_hope_GDP[m] = int(temp_hope_GDP[m])
            temp_hope_GDP.sort()
            temp_hope_GDP.reverse()
            
            temp2_hope_GDP.append(temp_hope_GDP[0])
            hope_GDP.append(temp_hope_GDP[0])
            temp_hope_GDP = []
            
            for k in range(len(allGDP[i])) :
                for l in range(len(temp2_hope_GDP)) :
                    if allGDP[i][k][3] == str(temp2_hope_GDP[l]) :
                        hope_GDP_name.append(allGDP[i][k][0])
            temp2_hope_GDP = []
        

        else :
            for j in range(len(allGDP[i])) :
                if allGDP[i][j][1] == user_industry_input :
                    temp_hope_GDP.append(allGDP[i][j][2])
                for m in range(len(temp_hope_GDP)) :
                    temp_hope_GDP[m] = int(temp_hope_GDP[m])
            temp_hope_GDP.sort()
            temp_hope_GDP.reverse()


            temp2_hope_GDP.append(temp_hope_GDP[0])
            hope_GDP.append(temp_hope_GDP[0])
            temp_hope_GDP = []
            
            for k in range(len(allGDP[i])) :
                for l in range(len(temp2_hope_GDP)) :
                    if allGDP[i][k][2] == str(temp2_hope_GDP[l]) :
                        hope_GDP_name.append(allGDP[i][k][0])
            temp2_hope_GDP = []

    return hope_GDP, hope_GDP_name

def region_sort(population, hope_GDP_name, hope_GDP):
    region_name = []
    temp_region = []
    region_top_pop = []

    # 지정한 지역 산업의 인구 수 리스트에 저장
    for i in range(len(regionDic)) :
        for j in range(len(population[i])) :
            if population[i][j][0] == hope_GDP_name[i] :
                region_top_pop.append(population[i][j][1])
    for i in range(len(regionDic)) :
        region_top_pop[i] = int(region_top_pop[i])

    # 나뉘어진 데이터를 각 지역의 리스트로 묶음
    for i in range(len(regionDic)) :
        temp_region.append(regionDic[i])
        temp_region.append(hope_GDP_name[i])
        temp_region.append(hope_GDP[i])
        temp_region.append(region_top_pop[i])

        region_name.append(temp_region)
        temp_region = []
    
    
    sorted_region = []
    sorted_region_name = []
                
    # 내림차순으로 GDP값 재정렬
    for i in range(len(regionDic)) :
        sorted_region.append(region_name[i][2])
    sorted_region.sort()
    sorted_region.reverse()


    # 내림차순으로 도시 이름 재정렬
    for i in range(len(regionDic)) :
        for j in range(len(regionDic)) :
            if sorted_region[i] == region_name[j][2] :
                sorted_region_name.append(region_name[j])
    
    return region_name, sorted_region, sorted_region_name

def per_region_sort(user_industry_input, region_name, sorted_region_name):
    per_sorted_region = []
    # 지역의 도시 별 1인당 GDP 값 계산
    for i in range(len(regionDic)) :
        per_sorted_region.append(sorted_region_name[i][2] / sorted_region_name[i][3])
    
    # 순서대로 지정한 산업 출력
    print("\n" + user_industry_input)
    print(region_name[0], "(단위 : 백만원, 명)")
    for i in range(len(regionDic) - 1) :
        print(region_name[i+1])


    # 순서대로 지정한 산업의 1인당 GDP 출력   
    print("\n" + user_industry_input, "내림차순")
    print(sorted_region_name[0], "(단위 : 백만원, 명)")
    for i in range(len(regionDic) - 1) :
        print(sorted_region_name[i+1])
        
    
    # 산업의 GDP를 내림차순으로 정리하여 그래프 표현
    sort_use_region_name = []
    for i in range(len(regionDic)-1) :
        sort_use_region_name.append(sorted_region_name[i][1])
    sort_use_region_name.append(sorted_region_name[i+1][1])

    return sort_use_region_name, per_sorted_region

def display_GDP(sort_use_region_name, sorted_region, user_industry_input, per_sorted_region):
    plt.barh(sort_use_region_name, sorted_region)
    plt.ylabel('GDP')
    plt.title(user_industry_input)
    plt.show()
    
    # 산업의 1인당 GDP를 내림차순으로 정리하여 그래프 표현
    plt.barh(sort_use_region_name, per_sorted_region)
    plt.ylabel('1인당 GDP')
    plt.title("인구대비 " + user_industry_input)
    plt.show()

def all_pop_GDP_bring():
    population, allGDP = pop_GDP_bring()
            
    time.sleep(0.3)
    print("")
        
    # 비교하고 싶은 산업 선택
    while True :
        user_industry_input = user_compare_select(allGDP)

        if user_industry_input == '0' : break

        hope_GDP, hope_GDP_name = region_best_industry(allGDP, user_industry_input)
        region_name, sorted_region, sorted_region_name = region_sort(population, hope_GDP_name, hope_GDP)
        sort_use_region_name, per_sorted_region = per_region_sort(user_industry_input, region_name, sorted_region_name)

        display_GDP(sort_use_region_name, sorted_region, user_industry_input, per_sorted_region)
        