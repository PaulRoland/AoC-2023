# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 05:54:58 2023

@author: Paul
"""
import time
#import numpy as np
start_time = time.time_ns()   
        
data_part=1
workflows=dict()     


def exc_workflow(key,x,m,a,s):
    new_key = ''
    for wf in workflows[key][:-1]:

        #Get letter
        if wf[0]=='x':
            wf_var=x
        if wf[0]=='m':
            wf_var=m
        if wf[0]=='a':
            wf_var=a
        if wf[0]=='s':
            wf_var=s
        #Get comparison
        if '>' in wf:
            factor=1
        if '<' in wf:
            factor=-1
        #Get boundary
        bound = int(wf.split(':')[0][2:])
         
        if wf_var*factor > bound*factor:
            new_key = wf.split(':')[1]
            break
    #Niets gezet    
    if new_key=='':
        new_key=workflows[key][-1]
    
    if new_key=='A':
        return 'accepted'
    elif new_key=='R':
        return('rejected')
    else:
        return exc_workflow(new_key,x,m,a,s)
    
def exc_workflow2(key,xmin,xmax,mmin,mmax,amin,amax,smin,smax):
    print(key,xmin,xmax,mmin,mmax,amin,amax,smin,smax)
    new_key = ''
    if key=='R':
        return
    if key =='A':
        print('Accepted',xmin,xmax,mmin,mmax,amin,amax,smin,smax)
        accepted.append([xmin,xmax,mmin,mmax,amin,amax,smin,smax])
        return
    
    for wf in workflows[key][:-1]:  
        
        new_key=wf.split(':')[1]

        #Get boundary
        bound = int(wf.split(':')[0][2:])
        
        #Bewaar de oude grenzen
        xmin_n=xmin
        xmax_n=xmax
        mmin_n=mmin
        mmax_n=mmax
        amin_n=amin
        amax_n=amax
        smin_n=smin
        smax_n=smax 
        #Get letter
        if wf[0:2]=='x>' and xmax>bound: #als er een gebied is om af te splitten
            xmin=bound+1
            xmax_n=bound #Stuk waarmee we doorgaan heeft niet deze x
                
        if wf[0:2]=='x<' and xmin<bound:
            xmax=bound-1
            xmin_n=bound #Stuk waarmee we doorgaan heeft niet deze x
        if wf[0:2]=='m>' and mmax>bound:
            mmin=bound+1
            mmax_n=bound #Stuk waarmee we doorgaan heeft niet deze m
                
        if wf[0:2]=='m<' and mmin<bound:
            mmax=bound-1
            mmin_n=bound #Stuk waarmee we doorgaan heeft niet deze m
        if wf[0:2]=='a>' and amax>bound:
            amin=bound+1
            amax_n=bound #Stuk waarmee we doorgaan heeft niet deze a
                
        if wf[0:2]=='a<' and amin<bound:
            amax=bound-1
            amin_n=bound #Stuk waarmee we doorgaan heeft niet deze a
        if wf[0:2]=='s>' and smax>bound:
            smin=bound+1
            smax_n=bound #Stuk waarmee we doorgaan heeft niet deze s
                
        if wf[0:2]=='s<' and smin<bound:
            smax=bound-1
            smin_n=bound #Stuk waarmee we doorgaan heeft niet deze s
        
        if new_key!='R': #Alleen aftakken als het niet rejected is natuurlijk he
            exc_workflow2(new_key,xmin,xmax,mmin,mmax,amin,amax,smin,smax)
            
        #Pas de nieuwe grenzen aan
        xmin=xmin_n
        xmax=xmax_n
        mmin=mmin_n
        mmax=mmax_n
        amin=amin_n
        amax=amax_n
        smin=smin_n
        smax=smax_n
    
    #Ga door met het overgebleven stuk                   
    new_key=workflows[key][-1]
    exc_workflow2(new_key,xmin,xmax,mmin,mmax,amin,amax,smin,smax)

f = open("input_dag19.txt", "r")
group_list = list()
for i,line in enumerate(f):
    if line=='\n':
        data_part=2
        continue
    line=line.replace('(','').replace(')','').replace('\n','')
    
    if data_part==1:
        wf_name=line.split('{')[0]
        instr=(line.split('{')[1]).replace('}','').split(',')
        workflows.update({wf_name:instr})
    else:
        group_data = line.replace('{','').replace('}','').split(',')
        group_list.append([int(group_data[0][2:]),int(group_data[1][2:]),int(group_data[2][2:]),int(group_data[3][2:])])
f.close()

total_p1=0
for x,m,a,s in group_list:
    if exc_workflow('in',x,m,a,s) == 'accepted':
        total_p1 += (x+m+a+s)

#Eventually a part will have to be rejected or accepted blijf ranges opsplitten tot je bij een accepted komt
#Verzamel alle instructies die leiden tot A
accepted=list()
exc_workflow2('in',1,4000,1,4000,1,4000,1,4000)

total_p2=0
for groups in accepted:
    x_acc = groups[1]-groups[0]+1
    m_acc = groups[3]-groups[2]+1
    a_acc = groups[5]-groups[4]+1
    s_acc = groups[7]-groups[6]+1
    total_p2 += x_acc*m_acc*a_acc*s_acc
print("Part 1:", total_p1)
print("Part 2:", total_p2)
print("--- %s ms ---" % ((time.time_ns() - start_time)/1000000))
