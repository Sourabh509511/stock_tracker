import pandas
import os


file_name=os.path.join(os.getcwd(),"screener_data.xlsx")
data=pandas.read_excel(file_name,names=['Ticker','Date','Time','Open', 'High', 'Low', 'Close','Volume'])

data["timestamp"]=data["Date"].apply(lambda x: str(x))+" "+data['Time'].apply(lambda x: x.strftime("%H:%M:%S"))

data["timestamp"]=pandas.to_datetime(data["timestamp"])

data.set_index('timestamp',inplace=True)

df2 = data.resample('4s').agg({"Open":'first','High':'max','Low':'min','Close':"last","Volume":'sum'})

df2=data.dropna(thresh=2)


previous_low=0
previous_high=0

full_data={}
for a in range(len(df2["Low"])):
    rows=[]
    row=df2.iloc[a]
    rows.append(str(row["Date"])[0:10])
    rows.append(row["Low"])
    rows.append(row["High"])
    full_data[a]=rows

for i in range(1,len(full_data)):
    # print(full_data[i][1])
    if full_data[i][1]<full_data[i-1][1]:
        current_high=full_data[i][2]
        value=0
        a=i
        while(full_data[a][2]<full_data[a-1][2] or full_data[a][0]!=full_data[a-1][0]):
            previous_high=full_data[a-1][2]
            print(f"current high value {full_data[a][2]}")
            print(f"last high value {full_data[a-1][2]}")
            print(f"date is {full_data[a][0]}")
            value=full_data[a][2]
            try:
                a+=1
            except Exception as e:
                print(e)
        if value-current_high>0:
            print(f"profit of {value-current_high}")
        elif current_high== value:
            print("NO profit no loss")
        else:
            print(f"Loss of {current_high-value}")
