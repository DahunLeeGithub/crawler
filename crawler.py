import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from datetime import datetime

def is_text_in_list_name(list:list, element:any) -> dict:
    text = element.get_text().strip()
    ngList = [
        'ア', 'イ', 'ウ', 'エ', 'オ',
        'カ', 'キ', 'ク', 'ケ', 'コ',
        'サ', 'シ', 'ス', 'セ', 'ソ',
        'タ', 'チ', 'ツ', 'テ', 'ト',
        'ナ', 'ニ', 'ヌ', 'ネ', 'ノ',
        'ハ', 'ヒ', 'フ', 'ヘ', 'ホ',
        'マ', 'ミ', 'ム', 'メ', 'モ',
        'ヤ', 'ユ', 'ヨ',
        'ラ', 'リ', 'ル', 'レ', 'ロ',
        'ワ', 'ヲ', 'ン',
        'ガ', 'ギ', 'グ', 'ゲ', 'ゴ',
        'ザ', 'ジ', 'ズ', 'ゼ', 'ゾ',
        'ダ', 'ヂ', 'ヅ', 'デ', 'ド',
        'バ', 'ビ', 'ブ', 'ベ', 'ボ',
        'パ', 'ピ', 'プ', 'ペ', 'ポ',
        'ャ', 'ュ', 'ョ',
        'ヴ', 'ッ', 'ー',
        'あ', 'い', 'う', 'え', 'お',
        'か', 'き', 'く', 'け', 'こ',
        'さ', 'し', 'す', 'せ', 'そ',
        'た', 'ち', 'つ', 'て', 'と',
        'な', 'に', 'ぬ', 'ね', 'の',
        'は', 'ひ', 'ふ', 'へ', 'ほ',
        'ま', 'み', 'む', 'め', 'も',
        'や', 'ゆ', 'よ',
        'ら', 'り', 'る', 'れ', 'ろ',
        'わ', 'を', 'ん',
        'が', 'ぎ', 'ぐ', 'げ', 'ご',
        'ざ', 'じ', 'ず', 'ぜ', 'ぞ',
        'だ', 'ぢ', 'づ', 'で', 'ど',
        'ば', 'び', 'ぶ', 'べ', 'ぼ',
        'ぱ', 'ぴ', 'ぷ', 'ぺ', 'ぽ',
        'ゃ', 'ゅ', 'ょ',
        'ゔ', 'っ', '店', '銀行', '信用金庫', '信用組合', '不動産', '事業', '保有資格', '中央金庫', '敷地調査', '出張所', 
        '代目', '東京都', '県', '商工中金', '​日本物流倉庫', '本店', '協会', '工事', '日本語', 'Web開発', '事業所', '機開発', '機構', 
        '開発', '営業', '｜', 'システム',  '工務部', '支店', '交代', 'として', '売上高', '挨拶', '。', '？', '！', '!', '?', '.', '株式会社', '研究', '「', 'っ', '～', '~', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '法人', 'ター', '大学', '海外', '保険', '本社', '営業所']
    result = {'is':False, 'output':''}
    if len(text) <= 3: return result
    for i in ngList:
        if i in text: return result
    for i in list:
        if i in text:
            result['is'] = True
            result['output'] = element
            break
    return result

def is_text_in_list_pos(list:list, element:any) -> dict:
    text = element.get_text().strip()
    ngList = ['交代', 'として', '売上高', '挨拶', '。', '？', '！', '!', '?', '.', '株式会社', '「', 'っ', '～', '~', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '法人', 'ター', '大学', '海外', '保険', '営業所']
    result = {'is':False, 'output':''}
    if len(text) <= 3: return result
    if len(text) >= 50: return result
    for i in ngList:
        if i in text: return result
    for i in list:
        if i in text:
            result['is'] = True
            result['output'] = element
            break
    return result

def get_html(url:str) ->BeautifulSoup:
    response = requests.get(url, timeout=1)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    return soup

def get_newHrefList(list:list, url:str) -> list:
    result = []
    new_url = ''
    if url[len(url)-1] =='/':
        new_url = url.rsplit('/', 1)[0]
    else:
        new_url = url

    for i in list:
        if not(i):continue
        if new_url in i:
            result.append(i)
        if i[0] =='/':
            result.append(new_url+i)
            
    
    return result

def search_nameAndPos(all_elements:any, nameList:list, posList:list, corp:str, url:str)->dict:
    nameResult = {'is':False, 'output':''}
    posResult = {'is':False, 'output':''}
    pos = ''
    name = ''
    found = False
    
    for i, element in enumerate(all_elements):
        # print(f'{i}/{len(all_elements)}')
        eNameResult = is_text_in_list_name(nameList, element)
        if eNameResult['is']:
            nameResult['is'] = eNameResult['is']
            nameResult['output'] = eNameResult['output']

        ePosResult = is_text_in_list_pos(posList, element)
        if ePosResult['is']:
            posResult['is'] = ePosResult['is']
            posResult['output'] = ePosResult['output']

        if nameResult['is'] and posResult['is']:

            found = True
            break

    if found:

        global outDf1
        global outputIndex
        global foundCnt

        # figure out what its type is
        found_nameList = []
        found_posList = []
        
        for element in all_elements:
            eNameResult = is_text_in_list_name(nameList, element)
            if eNameResult['is']:
                found_nameList.append(eNameResult['output'])

            ePosResult = is_text_in_list_pos(posList, element)
            if ePosResult['is']:
                found_posList.append(ePosResult['output'])

        print(f'found_nameList: {len(found_nameList)}')
        print(f'found_posList: {len(found_posList)}')

        # type 1: 1 on 1 matching
                
        if len(found_nameList) == len(found_posList):

            for i in range(len(found_nameList)):
                pos = found_posList[i].get_text().strip()
                name = found_nameList[i].get_text().strip()
                outDf1.loc[outputIndex] = {"企業名":corp, "URL":url, '役職名':pos, '氏名':name}
                foundCnt += 1
                outputIndex += 1
                
        # type 2: 1 on n matching(pos on name)
        
        if len(found_posList) < len(found_nameList):
            for ele in found_nameList:
                parents = ele.find_parents()
                switch = False

                eleResult = is_text_in_list_pos(posList, ele)
                if eleResult['is']:
                    pos = eleResult['output'].get_text().strip()
                    name = ele.get_text().strip()
                    outDf1.loc[outputIndex] = {"企業名":corp, "URL":url, '役職名':pos, '氏名':name}
                    outputIndex += 1
                    switch = True
                    continue

                parentResult = {'is':False, 'output':''}
                for parent in parents:
                    parentResult = is_text_in_list_pos(posList, parent)

                    if parentResult['is']:
                        pos = parentResult['output'].get_text(separator=' ', strip=True)
                        name = ele.get_text().strip()
                        outDf1.loc[outputIndex] = {"企業名":corp, "URL":url, '役職名':pos, '氏名':name}
                        outputIndex += 1
                        switch = True
                        break
                if not(switch):
                    pos = 'not found'
                    name = ele.get_text().strip()
                    outDf1.loc[outputIndex] = {"企業名":corp, "URL":url, '役職名':pos, '氏名':name}
                    outputIndex += 1
                    found = False

    return {'pos':pos, 'name':name, 'found':found}

start_time = datetime.now()
nameList = []
namePath = 'sei.csv'
with open(namePath, newline='') as csvfile:
    csv_reader = csv.reader(csvfile)
    switch = False
    for row in csv_reader:
        if not(switch):
            switch = True
            continue
        if len(row[1]) >= 2:
            nameList.append(row[1])

unsorted_posList = []
posPath = 'position.csv'
with open(posPath, newline='') as csvfile:
    csv_reader = csv.reader(csvfile)
    switch = False
    for row in csv_reader:
        if not(switch):
            switch = True
            continue
        if row[3] == '役職一覧': continue
        if row[0]:
            unsorted_posList.append(row[0])
        if row[1]:
            unsorted_posList.append(row[1])
        if row[3]:
            unsorted_posList.append(row[3])
unsorted_posList = list(set(unsorted_posList))
posList = sorted(unsorted_posList, key=len, reverse=True)

hrefList = []
hrefPath = 'hrefs.csv'
with open(hrefPath, newline='') as csvfile:
    csv_reader = csv.reader(csvfile)
    switch = False
    for row in csv_reader:
        if not(switch):
            switch = True
            continue
        hrefList.append(row[0])


outD1Dict = {"企業名":[], "URL":[], '役職名':[], '氏名':[]}
outDf1 = pd.DataFrame(outD1Dict)

total_rows = 0
inputD1Path = 'inputD.csv'
with open(inputD1Path, newline='') as csvfile:
    csv_reader = csv.reader(csvfile)
    
    for row in csv_reader:
        total_rows += 1

foundCnt = 0
notWorkingCnt = 0
missedCnt = 0
outputIndex = 0
with open(inputD1Path, newline='') as csvfile:
    csv_reader = csv.reader(csvfile)

    for index, row in enumerate(csv_reader):
        if index == 0: continue
        print(f'[{index/(total_rows-1)*100:.2f}] {index} in {total_rows-1}')
        print(f'found : {foundCnt}, notWorking : {notWorkingCnt}, missed : {missedCnt}')
        
        corp = ''
        url = ''
        pos = ''
        name = ''
        found = False

        corp = row[0]
        url = row[1]

        #start from index
        try:
            soup = get_html(url)
        except: # 404 error
            pos = 'not working'
            name = 'not working'
            notWorkingCnt += 1

            outDf1.loc[outputIndex] = {"企業名":corp, "URL":url, '役職名':pos, '氏名':name}
            outputIndex += 1
            continue

        all_elements = soup.find_all()
        ## 여기 수정하자
        text_only_elements = [element for element in all_elements if  element.string and not(element.name == 'script')]

        search_result = search_nameAndPos(all_elements=text_only_elements, nameList=nameList, posList=posList, corp=corp, url=url)
        found = search_result['found']
        name = search_result['name']
        pos = search_result['pos']

        if found:
            continue

        #find all href for going to the next page

        origin_href_list = [a_tag.get('href') for a_tag in soup.find_all('a')]
        Uhref_list = list(set(get_newHrefList(origin_href_list, url)))
        href_list = []
        hrefNgList = ['news', 'arti', 'sustainability', 'item', 'product', 'list', 'recruit', 'sup', '%', 'message', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ]
        for href1 in Uhref_list:
            switch = False
            for ngWord in hrefNgList:
                if ngWord in href1:
                    switch = True
                    break
            if switch:
                continue
            href_list.append(href1)
        new_href_list = []
        for keyword in hrefList:
            for href in href_list:
                if href in new_href_list: continue
                if keyword in href:
                    new_href_list.append(href)
        print(new_href_list)


                

        for href in new_href_list:
            print(f'now finding {href} ({len(new_href_list)})')
            try:
                soup = get_html(href)
            except:
                continue

            all_elements = soup.find_all()
            text_only_elements = [element for element in all_elements if  element.string and not(element.name == 'script')]

            search_result = search_nameAndPos(all_elements=text_only_elements, nameList=nameList, posList=posList, corp=corp, url=url)
            found = search_result['found']
            name = search_result['name']
            pos = search_result['pos']

            if found:
                break
        
        # found or missing
        if found:
            pass
        else:
            missedCnt += 1

        # set progress log
        if index%100 == 0:
            logPath = 'log/'
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            log_time = datetime.now()
            estimated_seconds = ((log_time - start_time) / (index / (total_rows - 1))).total_seconds()
            estimated_minutes = estimated_seconds / 60

            with open(f'{logPath}{current_time}_log{index//100}.txt', 'w') as file:
                file.write(f'{current_time}\n')
                file.write(f'[{index/(total_rows-1)*100:.2f}] {index} in {total_rows-1}\n')
                file.write(f'found : {foundCnt}, missed : {notWorkingCnt}, notWorking : {missedCnt}\n')
                file.write(f'started at {start_time}')
                file.write(f'now is {log_time}')
                file.write(f'estimated finish time is {estimated_minutes} minutes')
                outputPath = f'{logPath}{current_time}_log{index//100}.csv'
                outDf1.to_csv(outputPath)

# save the file to csv
outputPath = 'output_pos_and_name.csv'
outDf1 = outDf1.drop_duplicates()

outDf1 = outDf1.drop(outDf1[outDf1['役職名'] == 'not found'].index)

for i, row in outDf1.iterrows():
    curruntpos = str(row['役職名'])
    curruntname = str(row['氏名'])
    if curruntname == 'not working': continue
    for posrow in posList:
        if posrow in curruntname:
            curruntname = curruntname.replace(posrow, '').strip()
            outDf1.at[i, '氏名'] = curruntname
            break
    if curruntname in curruntpos:
        curruntpos = curruntpos.replace(curruntname, '').strip()
        outDf1.at[i, '役職名'] = curruntpos

outDf1.to_csv(outputPath, index=None)





        

