import requests , re , os , time , random ,sys 
from c0nf import key
import json 





def valid_mail(mail , agent_):
    
    api_url = "http://apilayer.net/api/check?access_key={}&email={}&smtp=1&format=1".format(key , mail)


    header = {'User-Agent':str(agent_).replace("\n" , "" )}
    resp = requests.get(api_url , headers=header)

    json_data = json.loads(resp.text)

    #print (json_data)

    return json_data 



def load_agents():
    try:
        with open('AGENTS.txt' ,'r') as handle_ :
            data = handle_.readlines()
            return data 

    except FileNotFoundError as nofile:
        print ("AGENTS File not found ")

        return False 







def call_domain(URL , agent_ ):
    ''' this function load one agent and creates a GET request to the URL '''



    header = {'User-Agent':str(agent_).replace("\n" , "" )}
    #print (str(agent_).replace("\n" , "" ))

    r = requests.get(URL,headers=header)


    response = str(r.content)

    return r.status_code , response





def find_urls(content):
    reg_one = r"https:\/\/+[a-zA-Z0-9:\/_\-:;.,?={}\\]*"
    reg_two = r"http:\/\/+[a-zA-Z0-9:\/_\-:;.,?={}\\]*"


    secure_links  = re.findall(reg_two , content)     

    unsecure_links = re.findall(reg_two , content)


    return len(secure_links) , len(unsecure_links) , secure_links , unsecure_links




def find_emails(content):
    ''' using a simple regex this function searchs for all emails in the url scanned'''

    #email_reg = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"

    email_reg =  r"""[a-zA-Z0-9_.]+@+[a-zA-Z0-9]+\.+[a-zA-Z0-9]*"""
    

    


    mail_lst = re.findall(email_reg , content)
    
   
   # print (len(mail_lst))
  
    for mail in mail_lst:
        if mail in all_mails:
            pass
        else: 
        
            json_data = valid_mail(mail , agent_=random.choice(agents))
            if json_data['format_valid'] == True and json_data['mx_found'] == True or json_data['smtp_check']:

                all_mails.append(str(mail))
                print ("Score of this email =====>  {} ".format(json_data["score"]))

    return len(mail_lst)







def check_url(URL , agents):


   

    x , resp = call_domain(URL , agent_=random.choice(agents))
    print ("Site response is {} ".format(x) )


    mail_count = find_emails(content=resp)

    print ("Found {} emails at this URL {}".format(mail_count, URL))

    return 




if __name__ == "__main__":

    all_mails = [] 
    agents = load_agents()

   
    URL =  str(input("Please input a valid url : "))


    #valid_mail(mail="hello000@aol.com" , agent_=random.choice(agents))
    #sys.exit()



    
    

    print ("Agents Found : {}".format(len(agents)))

    x , resp = call_domain(URL , agent_=random.choice(agents))
    print ("Site response is {} ".format(x) )


    mail_count = find_emails(content=resp)

    print ("Found {} emails ".format(mail_count ))

    
    i,j, secure_links_lst  , Unsecure_links_lst  = find_urls(content=resp)


    print ( "Found {}  secure_links , Found {} Unsecure_links ".format(i,j ))
        


    print ("Searching secure links .....")
    for link in secure_links_lst:
        check_url(URL=str(link) , agents=agents )

    print ("Searching Unsecure links .....")
    for link in Unsecure_links_lst:
        check_url(URL=str(link) , agents=agents )   


    try:

        if sys.argv[1] == True:
            ## this option saves the emails to a log file 
            with open("Found_emails.txt", "a" ) as h_:
                for item in all_mails:
                    h_.write(str(item)+"\n")
    
    except IndexError as no_val:
        for item in all_mails:
            print (item)




    print ( len(all_mails))