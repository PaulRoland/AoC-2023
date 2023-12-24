# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 05:59:01 2023

@author: Paul
"""
import itertools as it
import time
start_time = time.time_ns()

class hailstone:
    def __init__(self,x,y,z,vx,vy,vz,n):
        self.x=x
        self.y=y
        self.z=z
        self.vx=vx
        self.vy=vy
        self.vz=vz
        self.n=n

def intersect_xy_pos(hailA,hailB):
    #x= px + vx*time
    # time = (x-px) /vx
    #y= py + vy*time
    #y(x) = py + vy (x-px)/vx
    #y(x) = py-vy/vx*px + x*vy/vx
    #y(x) = c1 +c2x
    c1y = hailA.y-hailA.vy/hailA.vx*hailA.x
    c1v = hailA.vy/hailA.vx
    c2y = hailB.y-hailB.vy/hailB.vx*hailB.x
    c2v = hailB.vy/hailB.vx    
    
    if c1v != c2v:
        x_int = (c2y-c1y)/(c1v-c2v)
        y_int = c1y+x_int*c1v

        #x= px + vx*time   x_int-px / vx
        time_a = (x_int-hailA.x)/hailA.vx
        time_b = (x_int-hailB.x)/hailB.vx
        return True,time_a,time_b,x_int,y_int
    return False,0,0,0,0

f = open("input_dag24.txt", "r")
hailstones=list()
xmin=ymin=200000000000000
xmax=ymax=400000000000000
for i,line in enumerate(f):
    x,y,z,vx,vy,vz= line.replace('\n','').replace('@',',').split(',')
    hailstones.append(hailstone(int(x),int(y),int(z),int(vx),int(vy),int(vz),i+1))
f.close()

n_intersects=0
for stones in it.combinations(hailstones,2):
    intersect,time_a,time_b,x,y = intersect_xy_pos(stones[0],stones[1])
    if intersect == True and time_a>0 and time_b>0:
        if x>=xmin and x<=xmax and y>=ymin and y<=ymax:
            n_intersects +=1
            #print(stones[0].n,stones[1].n,x,y,time_a,time_b)
print("Part 1",n_intersects)

#Gooi een steen die elke hagelsteen raakt
#6 onbekenden x,y,z,u,v,w
#Tijden ook onbekend
#Elke hagelsteen geeft dus 3 vergelijkingen en een onbekende tijd
#3 hagelstenen heeft dus 9 vergelijkingen en 9 onbekenden, dit is op te lossen
import sympy as sp
x,y,z,u,v,w,t1,t2,t3 = sp.symbols('x,y,z,u,v,w,t1,t2,t3')
times_list = [t1,t2,t3]
eqs=list()
for i,stone in enumerate(hailstones[:3]):
    times = times_list[i]
    eqs.append(sp.Eq(x+u*times-(stone.x+stone.vx*times),0))
    eqs.append(sp.Eq(y+v*times-(stone.y+stone.vy*times),0))
    eqs.append(sp.Eq(z+w*times-(stone.z+stone.vz*times),0))

sol = sp.solve(eqs,[x,y,z,u,v,w,t1,t2,t3])
soln = [tuple(v.evalf() for v in s) for s in sol]        
print("Part 2",int(soln[0][0]+soln[0][1]+soln[0][2]))
print("--- %s ms ---" % ((time.time_ns() - start_time)/1000000))




