#I3B18 李信均
#Python 期末project

#實作台北市停車場查詢系統 ( 相關資料在政府開放式資料平台內 https://data.gov.tw/dataset/128435 )
#提供兩種查詢方式 : 使用者輸入或使用者選擇
#使用者手動輸入停車場名稱，程式將會尋找停車場名稱內有使用者輸入的關鍵字 ( ex: 輸入 101 將會出現愛馬屋101場、詮營信義101停車場等等 )
#使用者選擇停車場介面，會列出全部停車場或行政區供使用者選擇

#線上 GDB 使用 [選擇停車場 - 依名稱尋找] 會因為資料太多造成當機，建議使用vscode等等編譯器執行此功能
#一些停車場的資訊不完整，是因為政府開放式資料本身就無此資料原因造成的
import requests, json

#選擇查詢內容
def getJob () :
    try:
        print ( "----------------------------首頁--------------------------------")
        job = input ( "=> 0. 結束查詢\n"
                      "=> 1. 選擇停車場\n"
                      "=> 2. 手動輸入停車場\n"
                      "請輸入數字: ")
        print ( "---------------------------------------------------------------")

        if ( job == '0' or job == '1' or job == '2'):
            return job
        else :
            print ( "\n輸入錯誤 ! 請重新一次 !\n")
            return getJob()
    except ValueError:
        print ( "\n輸入錯誤 ! 請重新一次 !\n")
        return getJob ()

#系統給予停車場選擇選項
def getWay () :    
    try:
        way = input ( "=> 0. 回上一步\n"
                      "=> 1. 依行政區查詢\n"
                      "=> 2. 依名稱查詢\n"
                      "請輸入數字: ")
        print ( "---------------------------------------------------------------")
        if ( way == '0' or way == '1' or way == '2'):
            print ( "\n")
            return way
        else :
            print ( "\n[error] 輸入錯誤 ! 請重新一次 !\n")
            print ( "---------------------------------------------------------------")
            return getWay()
    except ValueError:
        print ( "\n[error] 輸入錯誤 ! 請重新一次 !\n")
        print ( "---------------------------------------------------------------")
        return getWay ()
    

#輸出停車場資料，某些停車場資料可能不完整，因此用try...except，避免衝突
def printParkInfo ( park, s, info) :
    try:
        print ( "[info] " + s + park[info])
    except KeyError:
        pass

#輸出停車場剩餘位置資料，某些停車場資料可能不完整，因此用try...except，避免衝突
def printParkAvailInfo ( park_avail, s, info) :
    try:
        if ( park_avail[info] == 0):
            print ( "[info] " + s + "車位已滿")
        elif ( park_avail[info] < 0):
            print ( "[info] " + s + "無車位")
        else:
            print ( "[info] " + s + str(park_avail[info]))
    except KeyError:
        pass

#取得指定停車場詳細資料
def getParkInfo ( park, park_avail) :
    print ( "---------------------------------------------------------------")
    print ( "\n")
    print ( park["area"] + " " + park["name"])
    printParkInfo ( park, "地址: ", "address")
    printParkInfo ( park, "電話: ", "tel")
    printParkInfo ( park, "汽車總車位: ", str(park["totalcar"]))
    printParkInfo ( park, "機車總車位: ", str(park["totalmotor"]))
    printParkInfo ( park, "殘障車位: ", "Handicap_First")
    printParkInfo ( park, "愛心車位: ", "Pregnancy_First")
    printParkInfo ( park, "營業時間: ", "serviceTime")
    printParkInfo ( park, "充電樁數量: ", "ChargingStation")

    if ( park_avail != None):
        print ( "\n目前剩餘車位:")
        printParkAvailInfo ( park_avail, "汽車: ", "availablecar")
        printParkAvailInfo ( park_avail, "機車: ", "availablemotor")

    print ( )
    printParkInfo ( park, "計價方式: \n", "payex")

    print ( )
    printParkInfo ( park, "簡介: \n", "summary")
    print ("\n")
    print ( "---------------------------------------------------------------")


#取得指定停車場
def getPark ( park_list, park_avail_list, park_name) :
    is_find = False
    for park in park_list:
        if ( park_name in park["name"]):
            no_avail = True
            for park_avail in park_avail_list:
                if ( park_avail["id"] == park["id"]):
                    getParkInfo ( park, park_avail)
                    is_find = True
                    no_avail = False
                
            if ( no_avail == True):
                getParkInfo ( park, None)
                is_find = True

    return is_find

    
#取得停車場名稱
def getParkName ( park_list, park_avail_list, area) :
    i = 0
    park_names = []
    park_names.clear()
    print ( "---------------------------------------------------------------")
    print ( "請選擇停車場:\n"+
            "=> 0. 回上一步")
    if ( area is None):
        for park in park_list:
            print ( "=> " + str(i + 1) + ". " + park["name"])
            park_names.append ( park["name"])
            i += 1
    else:
        for park in park_list:
            if ( park["area"] == area):
                print ( "=> " + str(i + 1) + ". " + park["name"])
                park_names.append ( park["name"])
                i += 1

    while ( True):
        try:
            name = int (input ( "請輸入數字: "))
            print ( "---------------------------------------------------------------")
            if ( name == 0):
                return False
            elif ( name > 0 and name <= len ( park_names)):
                getPark ( park_list, park_avail_list, park_names[(int(name) - 1)])
                return True
            else:
                print ( "[error] 輸入錯誤 ! 請重新一次 !")
                continue
        except ValueError:
            print ( "\n[error] 輸入錯誤 ! 請重新一次 !\n")
            continue
        
    


#取得行政區
def getArea ( park_list, park_avail_list) :
    areas = []
    areas.clear()

    print ( "---------------------------------------------------------------")
    print ( "請選擇行政區:\n"+
            "=> 0. 回上一步")
    for i in range ( len(park_list)):
        if ( park_list[i]["area"] not in areas):
            areas.append ( park_list[i]["area"])
    
    areas.pop()
    i = 0
    for area in areas:
        print ( "=> " + str(i + 1) + ". " + area)
        i += 1
    
    while ( True):
        area = int (input ( "請輸入數字: "))
        print ( "---------------------------------------------------------------")
        print ( "\n")
        if ( area == 0):
            return
        elif ( area > 0 and area <= len ( areas)):
            parkName = getParkName ( park_list, park_avail_list, areas[(area - 1)])
            if ( parkName == True):
                return
            else:
                getArea ( park_list, park_avail_list)
                return
        else:
            print ( "\n[error] 輸入錯誤 ! 請重新一次 !\n")
            print ( "---------------------------------------------------------------")
            continue

    

#Main
print ( "-------------------歡迎來到台北市停車場查詢系統-------------------\n")
url_desc = 'https://tcgbusfs.blob.core.windows.net/blobtcmsv/TCMSV_alldesc.json'
url_avail = 'https://tcgbusfs.blob.core.windows.net/blobtcmsv/TCMSV_allavailable.json'

#對停車場資料發出req
r = requests.get ( url_desc)
park_list = []
park_list = json.loads ( r.text)["data"]

#對停車場空位發出req
r = requests.get ( url_avail)
park_avail_list = []
park_avail_list = json.loads ( r.text)["data"]

#update time
print ( "停車場資料更新時間: " + park_list["UPDATETIME"])
print ( "剩餘空位資料更新時間: " + park_avail_list["UPDATETIME"] + "\n")

#停車場list
park_list = park_list["park"]

#剩餘空位list
park_avail_list = park_avail_list["park"]

#輸入0離開系統，其餘繼續
while ( True):

    #輸入查詢方式
    job = getJob()

    #輸入 0 結束查詢
    if ( job == '0'): break

    #輸入 1 系統給予清單熱使用者選擇
    elif ( job == '1'):
        print ( "\n\n---------------------------------------------------------------")
        print ( "請選擇查詢方式:")
        
        way = getWay ()
        
        if ( way == '0'):
            continue
        elif ( way == '1'):
            getArea ( park_list, park_avail_list)
        elif ( way == '2'):
            getParkName ( park_list, park_avail_list, None)

    #輸入 2 使用者自行輸入名稱，將會以輸入字串做關鍵字比對
    elif ( job == '2'):
        print ( "---------------------------------------------------------------")
        park_name = input ( "\n\n輸入 0 回上一步\n"
                            "=> 請輸入名稱: ")
        print ( "---------------------------------------------------------------")  
        if ( park_name != '0'):
            if not getPark ( park_list, park_avail_list, park_name):
                print ( "\n[info] 查無相關停車場\n")
                continue
        else:
            continue