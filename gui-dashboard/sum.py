from transformers import pipeline
import sqlite3
summarizer = pipeline("summarization", model="kabita-choudhary/finetuned-bart-for-conversation-summary")
#'sshleifer/distilbart-cnn-12-6'
#kabita-choudhary/finetuned-bart-for-conversation-summary
conn = sqlite3.connect("../web-interface/instance/feedback.db")
cursor = conn.cursor()

# Query data from the table
cursor.execute('SELECT DISTINCT CATEGORY FROM fb')
rows = cursor.fetchall() #list of tuples
print(rows)
def summarization(category):
    d={}
    ds={}
    # p_msgs="POSITIVE RESPONSES:\n\n "
    # n_msgs="NEGATIVE RESPONSES:\n\n "
    p_msgs=" "
    n_msgs=" "
    key=category
    cursor.execute(f'SELECT message_en FROM fb where category=? and sentiment=1',(key,))
    text = cursor.fetchall()
    # print(text)
    for j in text:
        p_msgs=p_msgs+j[0]+"\n"
    print(p_msgs) #positive messages
    # ds[1]=p_msgs #storing positive messages
    cursor.execute(f'SELECT message_en FROM fb where category=? and sentiment=-1',(key,))
    text = cursor.fetchall()
    # print(text)
    for j in text:
        n_msgs=n_msgs+j[0]+"\n"
    print(n_msgs) #negative messages
    # ds[-1]=n_msgs #storing negative messages
    # d[key]=ds #{'category':1:"positive messages",-1:"negative messages"}-(d[key][1])
    # print(d[key])
    if(p_msgs!=" "):
        ml=int(len(p_msgs)//2)
        mxl=int(len(p_msgs))
        summary = summarizer(p_msgs, max_length=200, min_length=10, do_sample=False)
        p_msgs=summary[0]['summary_text']
        ds[1]=p_msgs.replace('.','\n')
        ds[1]="POSITIVE RESPONSES:\n\n"+ds[1]
    else:
        ds[1]="POSITIVE RESPONSES:\n\nNo Responses Yet!"
    if(n_msgs!=" "):
        ml=int(len(n_msgs)//2)
        mxl=int(len(n_msgs))
        summary = summarizer(n_msgs, max_length=200, min_length=10, do_sample=False)
        n_msgs=summary[0]['summary_text']
        ds[-1]=n_msgs.replace('.','\n')
        ds[-1]="NEGATIVE RESPONSES:\n\n"+ds[-1]
    else:
        ds[-1]="NEGATIVE RESPONSES:\n\nNo Responses Yet!"
    d[key]=ds
    # msg=p_msgs+"\n"+n_msgs  
    msg=d[key][1]+"\n\n"+d[key][-1]
    # +'\nSummary:\n"+d[key]
    print(msg)
    return(msg)

# for i in rows:
    # 'category':{0:abc
    #             1:xyz}


