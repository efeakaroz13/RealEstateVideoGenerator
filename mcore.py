from multiprocessing import Process 
from anton import Anton
from colorama import Fore
import time 
import json 


try:
    config = open("entry.txt","r").read()
    city = config.split(",")[0].strip()
    state = config.split(",")[1].strip()
except:
    open("entry.txt","w").write("<city>,<state>")
    print(Fore.RED,"ERR",Fore.RESET," Could not find entry.txt, created it, please format it correctly as: city,state")
    print(Fore.BLUE,"Exitting...",Fore.RESET)
    exit()





def taskzillow():
    anton = Anton()
    try:
        oldreader = open("old.txt","r").readlines()    
    except:
        oldreader = []




    try:
        data = anton.getZillowData(city=city,state=state)
    
    except Exception as e:
        print(e)
        print(Fore.YELLOW,"Warning, could not get data from zillow,trying in 5 secs.",Fore.RESET)
        time.sleep(5)
        taskzillow()
    did = []
    for d in data:
        #print(json.dumps(d,indent=4))
        url = d["detailUrl"]
        gonnadoit = True 
        for old_read in oldreader:
            if url in old_read:
                gonnadoit = False 
            else:
                pass
                 
        if gonnadoit == True:
            print(Fore.GREEN,f"INFO | Generating video for:",Fore.RESET,d["hdpData"]["homeInfo"]["streetAddress"])
            generated = False 
            try:
                anton.videoGenZillow(d)
                generated = True
                print(Fore.GREEN,f"Success |Generated video for:",Fore.RESET,d["hdpData"]["homeInfo"]["streetAddress"])
            except Exception as e:
                print(Fore.RED,"An error occured, read err.log for more information",Fore.RESET)
                open("err.log","a").write(f"{time.ctime(time.time())} - {e}\n")
            
            
            
            if generated == True:

                open("old.txt","a").write(url+"\n")
                did.append(url)

    if len(did)==0:
        print(Fore.YELLOW,"There were not any new data, skipped.",Fore.RESET)

def taskrealtor():
    anton = Anton()
    try:
        oldreader = open("old.txt","r").readlines()    
    except:
        oldreader = []




    try:
        data = anton.getData(city=city,state=state)
    
    except Exception as e:
        print(e)
        print(Fore.YELLOW,"Warning, could not get data from zillow,trying in 5 secs.",Fore.RESET)
        time.sleep(5)
        taskrealtor()
    did = []
    for d in data:
        #print(json.dumps(d,indent=4))
        url = d["href"]
        gonnadoit = True 
        for old_read in oldreader:
            if url in old_read:
                gonnadoit = False 
            else:
                pass
                 
        if gonnadoit == True:
            print(Fore.GREEN,f"INFO | Generating video for:",Fore.RESET,d["location"]["address"]["line"],d["location"]["address"]["city"],d["location"]["address"]["state"])
            generated = False 
            try:
                anton.videoGenRealtor(d)
                generated = True
                print(Fore.GREEN,f"Success |Generated video for:",Fore.RESET,d["location"]["address"]["line"],d["location"]["address"]["city"],d["location"]["address"]["state"])
            except Exception as e:
                print(Fore.RED,"An error occured, read err.log for more information",Fore.RESET)
                open("err.log","a").write(f"{time.ctime(time.time())} - {e}\n")
            
            
            
            if generated == True:

                open("old.txt","a").write(url+"\n")
                did.append(url)

    if len(did)==0:
        print(Fore.YELLOW,"There were not any new data, skipped.",Fore.RESET)

if __name__ == "__main__":
    p1= Process(target=taskzillow)
    p2= Process(target=taskrealtor)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    
