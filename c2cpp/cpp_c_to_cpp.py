#!/usr/bin/python3

import argparse
import os
import time
def set_args():
    global input
    input = argparse.ArgumentParser()
    input.add_argument("-project_name",help="project_name",type=str,required=True)
    input.add_argument("-remove",help="flag true remove main.c",type=int)
    input = input.parse_args()
def logg():
    try:
        pathr = os.path.join("/home/imchin/STM32CubeIDE/workspace_1.10.1/"+input.project_name+"/Core/Src/main.cpp")
        fr=open(pathr, 'r')
        t=time.localtime()
        pathw = os.path.join(".log/"+input.project_name+"_"+str(t.tm_year)+"-"+str(t.tm_mon)+"-"+str(t.tm_mday)+"_"+str(t.tm_hour)+"-"+str(t.tm_min)+"-"+str(t.tm_sec)+".log")
        fw=open(pathw, 'w')
        for line in fr:
            fw.write(line)
        fw.close()
        print("log file Done")
        return 1
    except:
        return 0
def gen():
    pathr = os.path.join("/home/imchin/STM32CubeIDE/workspace_1.10.1/"+input.project_name+"/Core/Src/main.cpp")
    fr=open(pathr, 'r') 
    flag=False
    UserCode=[]
    begin=[]
    endd=[]
    for line in fr:
        if(line.find("/* USER CODE BEGIN")!=-1):
            begin.append(line)
            flag=True
        elif(line.find("/* USER CODE END")!=-1):
            endd.append(line)
            UserCode.append(line)
            flag=False
        if(flag):
            UserCode.append(line)
    fr.close()
    # print("Check file....")
    # print(begin,"\n\n",endd)
    if(len(begin)==len(endd)):
        print("Can convert")
    else:
        print("Can't convert")
        return 0
    max=len(begin)
    pathr = os.path.join("/home/imchin/STM32CubeIDE/workspace_1.10.1/"+input.project_name+"/Core/Src/main.c")
    fr=open(pathr, 'r') 
    raw = list(fr)
    fr.close()
    i=0
    Ncpp=[]
    Fwaitend=False
    for line in raw:
        if(i<=max-1 and line==begin[i] and line==UserCode[0]):
            i=i+1    
            while(1):
                Ncpp.append(UserCode[0])
                UserCode.pop(0)
                if(UserCode[0]==endd[i-1]):
                    Ncpp.append(UserCode[0])
                    UserCode.pop(0)
                    Fwaitend=True
                    break
        

        if(Fwaitend and line==endd[i-1]):
            Fwaitend=False
        elif(i>=max+1 and Fwaitend):
            Ncpp.append(line)
        elif(Fwaitend):
            pass
        else:
            Ncpp.append(line)
       
    pathw = os.path.join("/home/imchin/STM32CubeIDE/workspace_1.10.1/"+input.project_name+"/Core/Src/main.cpp")
    fw=open(pathw, 'w') 
    for line in Ncpp:
        fw.write(line)
    fw.close()
    print("convert Done.")
    if(input.remove == 1):
        print("Remove main.c")
        try:
            os.system("rm /home/imchin/STM32CubeIDE/workspace_1.10.1/"+input.project_name+"/Core/Src/main.c")
            print("remove main.c Done.")
        except:
            print("remove main.c Fail")

    return 1
def main():
    set_args()
    try:
        if(logg()==1):
            if(gen()==1):
                print("\n\n------ compair cpp_c tranfer to cpp Done. -------")
            else:
                print("\n\n------- compair cpp_c fail. -------")
        else:
            print("Can't log file")
    except:
        print("\n\n------- compair cpp_c fail. -------")

if __name__ == '__main__':
    main()
