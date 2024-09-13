import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from unidecode import unidecode as und

def get_link(alias,country,player_name):
    url='https://fbref.com/en/country/players/'+alias+'/'+country+'-Football-Players'
    ping=requests.get(url)
    if ping.status_code==200:
        soup=bs(ping.text,'html.parser')
        player_link=pd.DataFrame(columns=['Name','Link'])

        player_div=soup.find('div',class_='section_content')

        rows=player_div.find_all('a')

        prot='https://fbref.com'
        for row in rows:
            data=[und(row.text),prot+row['href']]
            index=len(player_link)
            player_link.loc[index]=data
        player_link=player_link.set_index('Name')

        player_url=None
        try:
            player_url=player_link.loc[player_name]['Link']
        except Exception as e:
            print("Player Not Found")
            pass
        finally:
            return player_url
    else:
        return None

def get_df(url,season):
    string=url.split('/')
    newString=''
    for i in range(6):
        newString+=(string[i]+'/')
    newString=newString+'matchlogs/'+season+'/'+string[6]+'-Match-Logs'
    url=newString
    ping=requests.get(url)

    if ping.status_code==200:
        soup=bs(ping.text,"html.parser")
        headers=soup.find('tr',class_=False)
        cols=[]
        for header in headers.find_all('th'):
            cols.append(header.text)
        df=pd.DataFrame(columns=cols)
        data_rows=soup.find_all('tr',class_=False)[1:-1]
        for rows in data_rows:
            row_data=[]
            #Date
            row_data.append(rows.find('th').text)
            for data in rows.find_all('td')[:-1]:
                row_data.append(data.text)
            link='https://fbref.com'+rows.find('a')['href']
            row_data.append(link)
            index=len(df)
            df.loc[index]=row_data
        df['Date']=pd.to_datetime(df['Date'])
        df['Result']=df['Result'].astype(str)
        return df
    else:
        return None


if __name__=='__main__':
    alias=input('Enter national team alias: ')
    alias=alias.upper()
    country=input('Enter country name: ')
    country=country.capitalize()
    name=input("Enter Player Name(case sensitive): ")
    
    url=get_link(alias,country,name)
    if url:
        season=input('Enter season: ')
        player_stats_dataframe=get_df(url,season)
        if player_stats_dataframe is not None:
            filename=input("Enter file name: ")
            filename=filename+'.csv'
            player_stats_dataframe.to_csv(filename,index=False)
            print(filename,"hase been created successfully")
        else:
            print("The player might not have played that season or the season format is not correct")

    else:
        print("Player information not correct")