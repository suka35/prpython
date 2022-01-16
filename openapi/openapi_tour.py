from calendar import month
import os
import sys
from traceback import print_tb
from urllib import response
import urllib.request
import datetime
import time
import json
import pandas as pd

ServiceKey = "EyuCqLNyF+rTsHLeGxRl3c9+oLdV4Xu8+FtWxIZfQEizYgqOn0RaFiMoK3HaIGAAtDqXtMbqI9zUOOtudDMeXw=="

def getRequestUrl(url):
    req = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(req)120
        if response.getcode() == 200:
            print ("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('uff-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % datetime.datetime.now())
        return None

def getTourismStatsItem(yyyymm, national_code, ed_cd):
    service_url = "http://openapi,tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatslist"
    parameters = "?_type=json&serviceKey=" + ServiceKey
    parameters += "&YM=" + yyyymm
    parameters += "&NAT_CD=" + national_code
    parameters += "&ED_CD=" + ed_cd
    url = service_url + parameters
    retData = getRequestUrl(url) 
    if (retData==None):
        return None
    else:
        return json.loads(retData)

def getTourismStatsService(nat_cd, ed_cd, nStartYear, nEndYear):
    jsonResult = []
    result = []
    for year in range(nStartYear, nEndYear+1):
        for mont in range(1, 13):
            yyyymm = "{0}{1:0>2}".format(str(year), str(month))
            jsonData = getTourismStatsItem(yyyymm, nat_cd, ed_cd)
            if (jsonData['response']['header']['resultMsg']=='OK'):
                if jsonData['response']['body']['items'] == '':
                    dataEND = "{0}{1:0>2}".format(str(year), str(month-1))
                    print("데이터 없음... \n 제공되는 통계 데이터는 $s년 $s월 까지 입니다." %(str(year), str(month-1)))
                    break
                print(json.dumps(jsonData, indent=4, sort_keys=True, ensure_ascii=False))
                natName = jsonData['response']['body']['items']['item']['natKorNm']
                natName = natName.replace(' ', '')
                num = jsonData['response']['body']['items']['item']['num']
                ed = jsonData['response']['body']['items']['item']['ed']
                print('-----------------------------------------------------')
                jsonResult.append({'nat_name' : natName, 'nat_cd' : nat_cd, 'yyyymm' : yyyymm, 'visit_cnt': num})
                result.append([natName, nat_cd, yyyymm, num])
    return (jsonResult, result, natName, ed, dataEND)

def main():
    jsonResult = []
    result = []

    print("<<국내 입국한 외국인의 통계 데이터를 수집합니다.>>")
    nat_cd = input('국가 코드를 입력하세요')
    nStartYear = int(input('언제부터'))
    nEndYear = int(input('언제까지'))
    ed_cd = "E" # E : 방한, D : 출국
    jsonResult, result, natName, ed, dataEND = getTourismStatsService(nat_cd, ed_cd, nStartYear, nEndYear)
    with open('./%s_%s_%d_%s.json'%(natName, ed, nStartYear, dataEND), 'w', encoding='utf8') as outfile:
        jsonFile = json.dumps(jsonResult,indent=4,sort_keys=True, ensure_ascii=False)
        outfile.write(jsonFile)
    columns = ['국가', '코드', '기간', '수']
    result_df = pd.DataFrame(result, columns=columns)
    result_df.to_csv('./%s_%s_%d_%s.csv'% (natName, ed, nStartYear, dataEND),index=False, encoding='cp949')

if __name__ == '__main__':
    main()