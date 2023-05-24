import  math as m
import numpy as np
import yaml
from yaml.loader import SafeLoader

with open('/home/natanan/ros2_ws/src/mai/config/config_inv.yaml', 'r') as file:
    param = yaml.load(file, Loader=SafeLoader)

class head:
    # input is position references from base to end effector
    def __init__(self, px,py,pz):
        # position x in m
        self.px = px 
        # position y in m
        self.py = py
        # position z in m
        self.pz = pz
        # head link lenght in m 
        self.link_head_1 = param['head']['link1']
        self.link_head_2 = param['head']['link2']
        self.link_head_3 = param['head']['link3']
        self.link_head_4 = param['head']['link4']
        self.link_head_5 = param['head']['link5']
        self.link_head_6 = param['head']['link6']
        # head joint theta, default is 0 radian
        self.theta_head_1 = 0
        self.theta_head_2 = 0
        # all head joint array
        self.theta_head = []

    def inv_head(self):
        # c is short equation
        c = self.px**2+(self.py+self.link_head_6)**2+(self.pz-self.link_head_4-self.link_head_5)**2-self.link_head_1**2-self.link_head_2**2-self.link_head_3**2
        sin2 = (c*self.link_head_1-(2*self.link_head_2*self.link_head_3)*(self.pz-self.link_head_4-self.link_head_5))/((-2*(self.link_head_1**2)*self.link_head_3)-(2*(self.link_head_2**2)*self.link_head_3))
        cos2 = (-c*self.link_head_2-(2*self.link_head_1*self.link_head_3)*(self.pz-self.link_head_4-self.link_head_5))/((-2*(self.link_head_1**2)*self.link_head_3)-(2*(self.link_head_2**2)*self.link_head_3))
        if ((1-sin2**2) >= 0 ) and ((1-cos2**2) >= 0):
            self.theta_head_2 = m.atan2(sin2,cos2)
            sin1 = (-self.px)/(self.link_head_3+self.link_head_2*m.cos(self.theta_head_2)-self.link_head_1*m.sin(self.theta_head_2))
            cos1 = (self.py+self.link_head_6)/(self.link_head_3+self.link_head_2*m.cos(self.theta_head_2)-self.link_head_1*m.sin(self.theta_head_2))
            if ((1-sin1**2)>=0) and ((1-cos1**2)>=0):
                self.theta_head_1 = m.atan2(sin1,cos1)
                self.theta_head = [self.theta_head_1,self.theta_head_2]
            else:
                self.theta_head_1 = 0
                self.theta_head_2 = 0
                print("cannot calulate joint 1")
                self.theta_head = [self.theta_head_1,self.theta_head_2]
                return self.theta_head
        else:
            self.theta_head_1 = 0
            self.theta_head_2 = 0
            print("cannot calulate joint 2")
            self.theta_head = [self.theta_head_1,self.theta_head_2]
            return self.theta_head
        # output is array in radian
        return self.theta_head
    
    def convert_radian_to_degree(self):
        # output is array in degree
        return [self.theta_head_1*180/m.pi,self.theta_head_2*180/m.pi]

# test = head(-0.61237,1.2854,2.36602)
# print(test.inv_head())
# print(test.convert_radian_to_degree())

class right_arm:
    # input is position references from base to end effector
    def __init__(self, px,py,pz):
        # position x in m
        self.px = px 
        # position y in m
        self.py = py
        # position z in m
        self.pz = pz
        # right arm link lenght in m 
        self.link_right_arm_1 = param['arm']['right']['link1']
        self.link_right_arm_2 = param['arm']['right']['link2']
        self.link_right_arm_3 = param['arm']['right']['link3']
        self.link_right_arm_4 = param['arm']['right']['link4']
        self.link_right_arm_5 = param['arm']['right']['link5']
        self.link_right_arm_6 = param['arm']['right']['link6']
        self.link_right_arm_7 = param['arm']['right']['link7']
        self.link_right_arm_8 = param['arm']['right']['link8']
        # set right arm robot pose
        # can use only (gamma_right_arm_2, gamma_right_arm_3) = (-1,1) or (-1,-1) only
        self.gamma_right_arm_2 = param['arm']['right']['gamma2']
        self.gamma_right_arm_3 = param['arm']['right']['gamma3']
        # right arm joint theta, default is 0 radian
        self.theta_right_arm_1 = 0
        self.theta_right_arm_2 = 0
        self.theta_right_arm_3 = 0
        # decrease target in m
        self.target = param['arm']['right']['target']
        # all right arm joint
        self.theta_right_arm = []

    def inv_arm(self):
        # a b A B C are short equation
        A  =-(((self.px-self.link_right_arm_1-self.link_right_arm_8)**2+(self.py+self.link_right_arm_7)**2+(self.pz-self.link_right_arm_6)**2-(self.link_right_arm_2**2)-self.link_right_arm_3**2)-(self.link_right_arm_4**2)-(self.link_right_arm_5**2)/2+self.link_right_arm_3**2)
        B = -((self.px*self.link_right_arm_2)-(self.link_right_arm_1*self.link_right_arm_2)-(self.link_right_arm_2*self.link_right_arm_8))
        C = (self.px*self.link_right_arm_3)-(self.link_right_arm_1*self.link_right_arm_3)-(self.link_right_arm_3*self.link_right_arm_8)
        a = self.pz-self.link_right_arm_6
        b = self.py+self.link_right_arm_7
        sin_phi_2 = C/(m.sqrt(A**2+B**2))
        if ((1-sin_phi_2**2) >= 0):
            self.theta_right_arm_2 = m.atan2(sin_phi_2,self.gamma_right_arm_2*m.sqrt(1-sin_phi_2**2))-m.atan2(B,A)
            # sin(theta16) must be a divider , so it cannot equal 0
            while m.sin(self.theta_right_arm_2)==0:
                # decrease target (change end effector target)
                self.px = self.px - self.target 
                self.py = self.py - self.target
                self.pz = self.pz - self.target
                # a b A B C are short equation
                A  =-(((self.px-self.link_right_arm_1-self.link_right_arm_8)**2+(self.py+self.link_right_arm_7)**2+(self.pz-self.link_right_arm_6)**2-(self.link_right_arm_2**2)-self.link_right_arm_3**2)-(self.link_right_arm_4**2)-(self.link_right_arm_5**2)/2+self.link_right_arm_3**2)
                B = -((self.px*self.link_right_arm_2)-(self.link_right_arm_1*self.link_right_arm_2)-(self.link_right_arm_2*self.link_right_arm_8))
                C = (self.px*self.link_right_arm_3)-(self.link_right_arm_1*self.link_right_arm_3)-(self.link_right_arm_3*self.link_right_arm_8)
                a = self.pz-self.link_right_arm_6
                b = self.py+self.link_right_arm_7
                sin_phi_2 = C/(m.sqrt(A**2+B**2))
                if ((1-sin_phi_2**2) >= 0):
                    self.theta_right_arm_2 = m.atan2(sin_phi_2,self.gamma_right_arm_2*m.sqrt(1-sin_phi_2**2))-m.atan2(B,A)
                else : 
                    self.theta_right_arm_1 = 0
                    self.theta_right_arm_2 = 0
                    self.theta_right_arm_3 = 0
                    print("cannot calulate joint 2")
                    self.theta_right_arm = [self.theta_right_arm_1,self.theta_right_arm_2,self.theta_right_arm_3]
                    return self.theta_right_arm
            sin_beta_3 = (-(self.px-self.link_right_arm_1-self.link_right_arm_8)/(m.sin(self.theta_right_arm_2)*m.sqrt(self.link_right_arm_4**2+self.link_right_arm_5**2)))-(self.link_right_arm_3/(m.sqrt(self.link_right_arm_4**2+self.link_right_arm_5**2)))
            if ((1-sin_beta_3**2) >= 0):
                self.theta_right_arm_3 = m.atan2(sin_beta_3,self.gamma_right_arm_3*m.sqrt(1-sin_beta_3**2))-m.atan2(self.link_right_arm_5,self.link_right_arm_4)
                # c d are short equation
                c = self.link_right_arm_2+(self.link_right_arm_4*m.cos(self.theta_right_arm_2)*m.sin(self.theta_right_arm_3))+(self.link_right_arm_5*m.cos(self.theta_right_arm_2)*m.cos(self.theta_right_arm_3))+(self.link_right_arm_3*m.cos(self.theta_right_arm_2))
                d = (-self.link_right_arm_4*m.cos(self.theta_right_arm_3))+(self.link_right_arm_5*m.sin(self.theta_right_arm_3))
                sin1 = (((-c)*(b))+((-d)*(a)))/(-(c**2+d**2))
                cos1 = (((-d)*(b))+(c*a))/(-(c**2+d**2))
                if ((1-sin1**2)>=0) and ((1-cos1**2)>=0):
                    self.theta_right_arm_2 = m.atan2(sin1,cos1)
                    self.theta_right_arm = [self.theta_right_arm_1,self.theta_right_arm_2,self.theta_right_arm_3]
                else : 
                    self.theta_right_arm_1 = 0
                    self.theta_right_arm_2 = 0
                    self.theta_right_arm_3 = 0
                    print("cannot calulate joint 1")
                    self.theta_right_arm = [self.theta_right_arm_1,self.theta_right_arm_2,self.theta_right_arm_3]
                    return self.theta_right_arm
            else: 
                self.theta_right_arm_1 = 0
                self.theta_right_arm_2 = 0
                self.theta_right_arm_3 = 0
                print("cannot calulate joint 3")
                self.theta_right_arm = [self.theta_right_arm_1,self.theta_right_arm_2,self.theta_right_arm_3]
                return self.theta_right_arm
        else :
            self.theta_right_arm_1 = 0
            self.theta_right_arm_2 = 0
            self.theta_right_arm_3 = 0
            print("cannot calulate joint 2")
            self.theta_right_arm = [self.theta_right_arm_1,self.theta_right_arm_2,self.theta_right_arm_3]
            return self.theta_right_arm
        # output is array in radian
        return self.theta_right_arm
    
    def convert_radian_to_degree(self):
        # output is array in degree
        return [self.theta_right_arm_1*180/m.pi,self.theta_right_arm_2*180/m.pi,self.theta_right_arm_3*180/m.pi]

# test = right_arm(6.8081,21.6947,60.5833)
# print(test.inv_arm())
# print(test.convert_radian_to_degree())

class left_arm:
    # input is position references from base to end effector
    def __init__(self, px,py,pz):
        # position x in m
        self.px = px 
        # position y in m
        self.py = py
        # position z in m
        self.pz = pz
        # left arm link lenght in m 
        self.link_left_arm_1 = param['arm']['left']['link1']
        self.link_left_arm_2 = param['arm']['left']['link2']
        self.link_left_arm_3 = param['arm']['left']['link3']
        self.link_left_arm_4 = param['arm']['left']['link4']
        self.link_left_arm_5 = param['arm']['left']['link5']
        self.link_left_arm_6 = param['arm']['left']['link6']
        self.link_left_arm_7 = param['arm']['left']['link7']
        self.link_left_arm_8 = param['arm']['left']['link8']
        # set left arm robot pose
        # can use only (gamma_left_arm_2, gamma_left_arm_3) = (-1,1) or (-1,-1) only
        self.gamma_left_arm_2 = param['arm']['left']['gamma2']
        self.gamma_left_arm_3 = param['arm']['left']['gamma3']
        # right arm joint theta, default is 0 radian
        self.theta_left_arm_1 = 0
        self.theta_left_arm_2 = 0
        self.theta_left_arm_3 = 0
        # decrease target in m
        self.target = param['arm']['left']['target']
        # all right arm joint
        self.theta_left_arm = []
    
    def inv_arm(self):   
        # a b A B C are short equation
        A = -(((self.px+self.link_left_arm_1+self.link_left_arm_8)**2+(self.py+self.link_left_arm_7)**2+(self.pz-self.link_left_arm_6)**2-(self.link_left_arm_2**2)-(self.link_left_arm_3**2)-(self.link_left_arm_4**2)-(self.link_left_arm_5**2))/2+self.link_left_arm_3**2)
        B = (self.px*self.link_left_arm_2)+(self.link_left_arm_1*self.link_left_arm_2)+(self.link_left_arm_2*self.link_left_arm_8)
        C = (self.px*self.link_left_arm_3)+(self.link_left_arm_1*self.link_left_arm_3)+(self.link_left_arm_3*self.link_left_arm_8)
        a = self.pz-self.link_left_arm_6
        b = self.py+self.link_left_arm_7
        sin_phi_2 = C/m.sqrt(A**2+B**2)
        if 1-sin_phi_2**2 >= 0 :
            self.theta_left_arm_2 = m.atan2(sin_phi_2,self.gamma_left_arm_2*m.sqrt(1-sin_phi_2**2))+m.atan2(B,A)
            while m.sin(self.theta_left_arm_2) == 0 :
                self.px = self.px - self.target
                self.py = self.py - self.target
                self.pz = self.pz - self.target
                A = -(((self.px+self.link_left_arm_1+self.link_left_arm_8)**2+(self.py+self.link_left_arm_7)**2+(self.pz-self.link_left_arm_6)**2-(self.link_left_arm_2**2)-(self.link_left_arm_3**2)-(self.link_left_arm_4**2)-(self.link_left_arm_5**2))/2+self.link_left_arm_3**2)
                B = (self.px*self.link_left_arm_2)+(self.link_left_arm_1*self.link_left_arm_2)+(self.link_left_arm_2*self.link_left_arm_8)
                C = (self.px*self.link_left_arm_3)+(self.link_left_arm_1*self.link_left_arm_3)+(self.link_left_arm_3*self.link_left_arm_8)
                a = self.pz-self.link_left_arm_6
                b = self.py+self.link_left_arm_7
                sin_phi_2 = C/m.sqrt(A**2+B**2)
                if 1-sin_phi_2**2 >= 0:
                    self.theta_left_arm_2 = m.atan2(sin_phi_2,self.gamma_left_arm_2*m.sqrt(1-sin_phi_2**2))+m.atan2(B,A)
                else:
                    self.theta_left_arm_1 = 0
                    self.theta_left_arm_2 = 0
                    self.theta_left_arm_3 = 0
                    print("cannot calulate joint 2")
                    self.theta_left_arm = [self.theta_left_arm_1,self.theta_left_arm_2,self.theta_left_arm_3]
                    return self.theta_left_arm
            sin_beta_3 = (-(self.px+self.link_left_arm_1+self.link_left_arm_8)/(m.sin(self.theta_left_arm_2)*m.sqrt(self.link_left_arm_4**2+self.link_left_arm_5**2)))-(self.link_left_arm_3/(m.sqrt(self.link_left_arm_4**2+self.link_left_arm_5**2)))
            if 1-sin_beta_3**2 >= 0 :
                self.theta_left_arm_3 = m.atan2(sin_beta_3,self.gamma_left_arm_3*m.sqrt(1-sin_beta_3**2))-m.atan2(self.link_left_arm_5,self.link_left_arm_4)
                c = self.link_left_arm_2+(self.link_left_arm_4*m.cos(self.theta_left_arm_2)*m.sin(self.theta_left_arm_3))+(self.link_left_arm_5*m.cos(self.link_left_arm_5)*m.cos(self.theta_left_arm_3))+(self.link_left_arm_3*m.cos(self.theta_left_arm_2))
                d = (-self.link_left_arm_4*m.cos(self.theta_left_arm_3))+(self.link_left_arm_5*m.sin(self.theta_left_arm_3))
                sin1 = (((-c)*(b))+((-d)*(a)))/(-(c**2+d**2))
                cos1 = (((-d)*(b))+(c*a))/(-(c**2+d**2))
                if (1-sin1**2)>= 0 and (1-cos1**2)>= 0:
                    self.theta_left_arm_1 = m.atan2(sin1,cos1)
                    self.theta_left_arm = [self.theta_left_arm_1, self.theta_left_arm_2, self.theta_left_arm_3]
                else:
                    self.theta_left_arm_1 = 0
                    self.theta_left_arm_2 = 0
                    self.theta_left_arm_3 = 0
                    print("cannot calulate joint 1")
                    self.theta_left_arm = [self.theta_left_arm_1,self.theta_left_arm_2,self.theta_left_arm_3]
                    return  self.theta_left_arm
            else :
                self.theta_left_arm_1 = 0
                self.theta_left_arm_2 = 0
                self.theta_left_arm_3 = 0
                print("cannot calulate joitn 3")
                self.theta_left_arm = [self.theta_left_arm_1,self.theta_left_arm_2,self.theta_left_arm_3]
                return  self.theta_left_arm
        else:
            self.theta_left_arm_1 = 0
            self.theta_left_arm_2 = 0
            self.theta_left_arm_3 = 0
            print("cannot calulate joint 2")
            self.theta_left_arm = [self.theta_left_arm_1,self.theta_left_arm_2,self.theta_left_arm_3]
            return  self.theta_left_arm
        return self.theta_left_arm

    def convert_radian_to_degree(self):
        return [self.theta_left_arm_1*180/m.pi, self.theta_left_arm_2*180/m.pi, self.theta_left_arm_3*180/m.pi]

# test = left_arm(-6.8081,21.6947,60.5833)
# print(test.inv_arm())

class leg:
    # input is position references from base to end effector
    def __init__(self, px,py,pz,left_or_right):
        # position x in m
        self.px = px 
        # position y in m
        self.py = py
        # position z in m
        self.pz = pz
        # left or right leg
        # left = false, right = true
        self.left_or_right = left_or_right
        # leg link lenght in m 
        self.link_leg_1 = param['leg']['link1']
        self.link_leg_2 = param['leg']['link2']
        self.link_leg_3 = param['leg']['link3']
        self.link_leg_4 = param['leg']['link4']
        self.link_leg_5 = param['leg']['link5']
        # change leg direction
        self.gamma_leg_2 = param['leg']['gamma2']
        self.gamma_leg_4 = param['leg']['gamma4']
        self.gamma_leg_5 = param['leg']['gamma5']
        # leg joint theta, default is 0 radian
        self.theta_leg_1 = 0
        self.theta_leg_2 = 0
        self.theta_leg_3 = 0
        self.theta_leg_4 = 0
        self.theta_leg_5 = 0
        self.theta_leg_6 = 0
        # all leg joint
        self.theta_leg = []
    
    def inv_leg(self): 
        #        n  s  a  P 
        #  H = [ 0 -1  0  Px
        #        0  0  1 -Py      
        #       -1  0  0  Pz
        #        0  0  0   1]
        tform = np.array([[0,-1,0, self.px],[0,0,1,-self.py],[-1,0,0,self.pz],[0,0,0,1]])
        if int(self.left_or_right):
            self.link_leg_1 = -self.link_leg_1
        # 1) Perform some offsets
        tform[0][3] = -tform[0][3]
        tform = tform - np.array([[0, 0, 0, self.link_leg_1],[0,0,0,0],[0,0,0,-self.link_leg_2],[0,0,0,0]])
        # Extract position/orientation information
        R = np.array([[tform[0][0], tform[0][1], tform[0][2]],[tform[1][0], tform[1][1], tform[1][2]],[tform[2][0], tform[2][1], tform[2][2]]])
        p = np.array([[tform[0][3]],[tform[1][3]],[tform[2][3]]])
        
        # 2) Get inverse rotation matrix (in this case, a transpose)
        Rp = R.transpose()
        n = np.array(Rp[:,0])
        s = np.array(Rp[:,1])
        a = np.array(Rp[:,2])
        # P'x P'y P'z ref from end effector to base
        p = -Rp.dot(p)
        # 3) Compute nalytic solution from the paper
        cos4 = ((p[0][0]+self.link_leg_5)**2+(p[1][0])**2+(p[2][0])**2-(self.link_leg_3)**2-(self.link_leg_4)**2)/(2*self.link_leg_3*self.link_leg_4)
        temp = 1-cos4**2
        if temp < 0:
            temp = 0
            print("cannot calulate joint 4")
        self.theta_leg_4 = m.atan2(self.gamma_leg_4*m.sqrt(temp),cos4)
        temp = (p[0][0]+self.link_leg_5)**2+(p[1][0])**2
        if temp < 0:
            temp = 0
            print("cannot calulate joint 5")
        self.theta_leg_5 = m.atan2(-p[2][0],self.gamma_leg_5*m.sqrt(temp))-m.atan2(m.sin(self.theta_leg_4)*self.link_leg_3,m.cos(self.theta_leg_4)*self.link_leg_3+self.link_leg_4)
        self.theta_leg_6 = m.atan2(p[1][0],-p[0][0]-self.link_leg_5)
        temp = 1-(m.sin(self.theta_leg_6)*a[0]+m.cos(self.theta_leg_6)*a[1])**2
        if temp < 0:
            temp = 0
            print("cannot calulate joint 6")
        self.theta_leg_2 = m.atan2(self.gamma_leg_2*m.sqrt(temp),m.sin(self.theta_leg_6)*a[0]+m.cos(6)*a[1])
        self.theta_leg_2 = self.theta_leg_2 + (m.pi/2) # pi/2 offset
        self.theta_leg_1 = m.atan2(-m.sin(self.theta_leg_6)*s[0]-m.cos(self.theta_leg_6)*s[1],-m.sin(self.theta_leg_6)*n[0]-m.cos(self.theta_leg_6)*n[1])
        th345 = m.atan2(a[2],m.cos(self.theta_leg_6)*a[0]-m.sin(self.theta_leg_6)*a[1])
        th345 = th345 - m.pi
        self.theta_leg_3 = th345 - self.theta_leg_4 - self.theta_leg_5
        self.theta_leg = [self.theta_leg_1, self.theta_leg_2, self.theta_leg_3, self.theta_leg_4, self.theta_leg_5, self.theta_leg_6]
        return self.theta_leg
    
    def convert_radian_to_degree(self):
        return [self.theta_leg_1*180/m.pi, self.theta_leg_2*180/m.pi, self.theta_leg_3*180/m.pi, self.theta_leg_4*180/m.pi, self.theta_leg_5*180/m.pi, self.theta_leg_6*180/m.pi]

# test = leg(-0.1582,0.6607,-2.8084,True)
# print(test.inv_leg())
