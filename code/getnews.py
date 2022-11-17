import pandas as pd
import requests
import json
import re
import numpy as np

class get_data():

    def __init__(self,dic,url):
        self.url = url
        self.dic = dic
    def get_url(self,lid,page,pageid=153):
        return self.url +"&lid="+str(lid)+"&pageid="+str(pageid)+"&page="+str(page)

    def get_json_url(self,url):
        out = []
        json_req = requests.get(url)
        user_dict = json.loads(json_req.text)
        print(url)
        for dic in user_dict["result"]["data"]:
            out.append([dic["url"],dic['intro'],dic['title']])

        return out

    def getfind_data(self,list1,label):
        out_date = []

        for line in list1:
            try:
                req = requests.get(line[0])
                req.encoding = "utf-8"
                req = req.text
                content = re.findall('<!-- 行情图end -->.*<!-- news_keyword_pub',req,re.S)
                if len(content)!=0:
                    pass
                else:
                    content = re.findall('<!-- 正文 start -->.*<!--', req, re.S)
                if len(content)!=0:
                    pass
                else:
                    content = re.findall('<!--新增众测推广文案-->.*?<!-- ', req, re.S)

                print(content)
                if len(line[0].split("/")[3])==10:
                    out_date.append([line[0].split("/")[3], line[2], line[1], content, label])

                elif len(line[0].split("/")[4])==10:
                    out_date.append([line[0].split("/")[4], line[2], line[1], content, label])


                elif len(line[0].split("/")[5])==10:
                    out_date.append([line[0].split("/")[5], line[2], line[1], content, label])

                elif len(line[0].split("/")[6]) == 10:
                    out_date.append([line[0].split("/")[6],line[2],line[1],content,label])


            except:
                pass

        return out_date

    def main(self):
        out_data_list = []
        for label,lid in self.dic.items():
            for page in range(1,101):
                he_url = self.get_url(lid,page)
                json_url_list = self.get_json_url(he_url)
                output_data = self.getfind_data(json_url_list,label)
                out_data_list+=output_data
        data = pd.DataFrame(np.array(out_data_list), columns=['时间', '标题', '摘要', '内容','类别'])
        data.to_csv("data.csv")


if __name__ == "__main__":
    data_dic = {"国内":2510,
                "国际":2511,
                "社会":2669,
                "体育":2512,
                "娱乐":2513,
                "军事":2514,
                "科技":2515,
                "财经":2516,
                "股市":2517,
                "美股":2518}
    url = "https://feed.mix.sina.com.cn/api/roll/get?&k=&num=50"
    get = get_data(data_dic,url)
    get.main()