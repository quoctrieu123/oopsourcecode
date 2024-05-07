
import numpy as np 
import pandas as pd 
import networkx as nx 
import json
import math
import time
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime 


def search_model(inputt):
    with open("dataofficial.json",encoding="UTF8") as fin:
        data = json.load(fin)
  
        

    keywords = inputt.split()
    docCount = len(data)
    sumLength =0

    sumLength=0
    sumLengthtitle=0
    for i in range(0,len(data),1):
        data[i]["fieldLength"] = len(data[i]["content"].split())
        sumLength+= data[i]["fieldLength"]
        data[i]["fieldLengthtitle"] = len(data[i]["title"].split())
        sumLengthtitle+= data[i]["fieldLengthtitle"]
        data[i]["fieldLengthtitle"] = 1
        

    avgFieldLength = sumLength/len(data)
    avgFieldLengthtitle=sumLengthtitle/len(data)
        
        
    for keyword in keywords:
        docFreq=0
        for j in range(0,len(data),1):
            if keyword.lower() in data[j]["content"].lower():
                docFreq+= 1

        for i in range(0,len(data),1):
            data[i]["idf"]= math.log(1+(docCount-docFreq+0.5)/(docFreq+0.5))
            count = ((data[i]["content"].lower())).split().count(keyword.lower())
            data[i]["freq"] = count
        
        
        
        
        docFreqtitle=0
        for j in range(0,len(data),1):
            if keyword.lower() in data[j]["title"].lower():
                docFreqtitle+= 1

        for i in range(0,len(data),1):
            data[i]["idftitle"]= math.log(1+(docCount-docFreqtitle+0.5)/(docFreqtitle+0.5))
            counttitle = ((data[i]["title"].lower())).split().count(keyword.lower())
            data[i]["freqtitle"] = counttitle

    

    
    for i in range(0,len(data),1):
        data[i]["scorecontent"] =(data[i]["idf"]*(data[i]["freq"]*(1.2+1)))/(data[i]["freq"]+1.2*(1-0.75+0.75*(data[i]["fieldLength"]/avgFieldLength)))
        data[i]["scoretitle"] =(data[i]["idftitle"]*(data[i]["freqtitle"]*(1.2+1)))/(data[i]["freqtitle"]+1.2*(1-0.75+0.75*(data[i]["fieldLengthtitle"]/avgFieldLengthtitle)))
        if data[i].get("score") is None:
            data[i]["score"]= data[i]["scorecontent"] +  0.5*data[i]["scoretitle"]
            
        else:
            data[i]["score"]+= data[i]["scorecontent"] +  0.5*data[i]["scoretitle"]
    data.sort(key=lambda x: x["score"],reverse=True)
    

    return data 



start_time = time.time() # đo thời gian chạy 
def search_algo(inputt):
    dp = search_model(inputt)
    df = [dp[0]]
    # xóa các bài báo trùng 

    for i in range(len(dp)):
        title_exists = False
        for j in range(len(df)):
            if dp[i]['title'] == df[j]['title']:
                title_exists = True
                break
        if not title_exists:
            df.append(dp[i])



    x = dict([(df[i]['link'],df[i]['referenceLinks']) for i in range(len(df))])


    # tạo set các key 
    all_keys = set(x.keys())

    # tạo dict chứa page và các link liên quan đồng thời loại bỏ các liên kết thừa 
    for key, value in x.items():
        new_value = []
        for item in value:
            if item in all_keys:
                new_value.append(item)
        if not new_value:
            new_value = []
        x[key] = new_value


    # fix các bài báo ko có creationDate, lược bỏ các lỗi và chuyển về dạng ngày tháng 
    for i in range(len(df)):
        try:
            df[i]["creationDate"] = datetime.strptime(df[i]["creationDate"], "%b %d, %Y %H:%M")
        except ValueError as V:
            df[i]["creationDate"] = datetime.strptime(df[i]["creationDate"], "%B %d, %Y")

        
    df = sorted(df, key = lambda x: x['creationDate'], reverse = True )
    recent_articles = df[:5]
    # ở đây recent articles chứa thông tin 5 bài báo mới nhất, ta có thể chỉnh hệ số tùy ý 


    # tạo danh sách các cạnh cho Page rank 
    lisss = [] 
    for key, value in x.items():
        if not value:
            continue
        else:
            for i in range (0,len(value)):
                myy = (key,value[i])
                lisss.append((key,value[i]))



    # tạo mạng và thêm các cạnh 
    G = nx.DiGraph()
    G.add_nodes_from(all_keys)
    G.add_edges_from(lisss)


    # Tính toán PageRank
    result = nx.pagerank(G)



    # khởi tạo column pagerank 
    for i in range(len(df)):
        df[i]['Page_rank'] = 0.0 

    for i in range(len(df)):
        for node, value in result.items():
            if node == df[i]['link']:
                df[i]['Page_rank'] = value




    scaler = MinMaxScaler() # scaler theo kiểu min max 
    # Chọn các feature để scale
    features = ['score','Page_rank']

    # Trích xuất các giá trị của các feature vào một array numpy
    matrix = pd.DataFrame(df)
    matrix[features] = scaler.fit_transform(matrix[features])

    matrix['total_score'] = 0.7 * matrix['score'] + 0.3 * matrix['Page_rank']




    for i in range(len(df)):
        if df[i]['title'] == matrix.loc[i,'title']:
            df[i]['total_score'] = matrix.loc[i,'total_score']
            df[i]['score'] = matrix.loc[i,'score']
            df[i]['Page_rank'] = matrix.loc[i,'Page_rank']



    df = sorted(df, key=lambda x: x["total_score"], reverse=True)


    # ở đây df là dict chứa thông tin các bài báo có điểm cao xuống thấp còn matrix là df dạng dataframe 
    # còn datareceived là dict các bài báo ta muốn hiển thị, có thể điều chỉnh số lượng tùy ý 

    lst=[]
    for i in range(len(df)):
        datareceived = {}
        if df[i]['score'] != 0:
            datareceived["title"]= df[i]["title"]
            datareceived["creationDate"]=df[i]["creationDate"]
            datareceived["content"]= df[i]["content"]
            lst.append(datareceived)
        if len(datareceived) == 10:
            break 
    if lst == []:
        return('Không tìm thấy kết quả phù hợp')    
    else:
        return lst


"""
    Tổng kết: recent_articles: là list chứa 5 bài báo gần đây, có thể chỉnh hệ số tùy ý 
            df             : là dict chứa thông tin tất cả bài báo và mọi loại điểm 
            matrix         : df dưới dạng dataframe
            datareceived   : tương tự như df nhưng ở đây chỉ lưu 10 bài báo có điểm tổng cao nhất, đồng thời lược bỏ các
                            bài báo có bm25 = 0 do không liên quan đến từ khóa, chỉnh hệ số tùy ý 
            time_diff      : thời gian chạy của search_engine, ở đây đã test trung bình là tầm dưới 2.5s 
"""
