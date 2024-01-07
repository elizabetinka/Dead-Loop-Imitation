# импортируем модули
import math
from typing import Final






def solve_quadratic_equation(a, b, c):
    """
    Решает квадратное уравнение ax^2 + bx + c = 0

    :param a: коэффициент при x^2
    :param b: коэффициент при x
    :param c: свободный член
    :return: корни уравнения
    """
    discriminant = b**2 - 4*a*c
    if discriminant > 0:
        x1 = (-b + math.sqrt(discriminant)) / (2*a)
        x2 = (-b - math.sqrt(discriminant)) / (2*a)
        return x1, x2
    elif discriminant == 0:
        x1 = -b / (2*a)
        return x1
    else:
        return None




class MyClass:
    g : Final = 9.8
    m : Final = 3
    R : Final = 5
    toch : Final = 1000
    alpha : Final  = 4*math.pi/6
    mu : Final  = 0.04


    v_0 = 8
    v_0_ans = 13.084710478782654
    a_0 = 0
    start_pos_x = 0
    start_pos_y = 0
    dist = 0

    cur_v = 0
    cur_t = 0
    pos_x = 0
    pos_y = 0
    cur_a = 0
    cur_ax = 0
    cur_ay = 0
    cur_vx = 0
    cur_vy = 0
    
    t_ = []
    x_ = []
    y_ = []
    v_ = []
    a_ = []

    def __init__(self,start_pos_x, start_pos_y, dist,v_0 = 8, a = 0):
        self.pos_x = start_pos_x
        self.pos_y = start_pos_y
        self.v_0 = v_0
        self.a_0 = a
        self.start_pos_x = start_pos_x
        self.start_pos_y = start_pos_y
        self.dist = dist

        self.v_0_ans = self.BinPoisk()
        self.v_0 = v_0
        self.a_0 = a
        self.pos_x = start_pos_x
        self.pos_y = start_pos_y

    def clean(self):
        self.x_= []
        self.y_= []
        self.t_ = []
        self.v_ = []
        self.a_ = []

        self.cur_t = 0
        self.cur_l = 0
        self.cur_v = self.v_0
        self.cur_a = self.a_0
        self.pos_x = self.start_pos_x
        self.pos_y = self.start_pos_y

# движение по прямой
    def FirstPath(self):
        fullt = 0
        result = 0
        if (self.a_0 == 0):
            result = self.dist/self.cur_v 
        else:
            result = solve_quadratic_equation(self.a_0/2, self.cur_v ,-self.dist )
        if result is None:
            print("Уравнение не имеет действительных корней")
        elif isinstance(result, tuple):
            fullt = result[0]
        else:
            fullt = result
        dt =1/self.toch
        self.cur_a = self.a_0
        while (self.pos_x <(self.dist+self.start_pos_x)):
            self.t_.append(self.cur_t)
            self.a_.append(self.cur_a)
            self.v_.append(self.cur_v)
            self.x_.append(self.pos_x)
            self.y_.append(self.pos_y)

            
            self.pos_x = self.start_pos_x + self.cur_v*self.cur_t +  self.cur_a*self.cur_t*self.cur_t/2
            self.pos_y = self.start_pos_y
            self.cur_v = self.v_0 + self.cur_a*self.cur_t
            self.cur_t += dt
        self.cur_vx = self.cur_v
        self.cur_vy = 0
        return
      
 #скат тело послепадения
    def FifthPath(self):
            dt =1/self.toch
            time = 0
            alpha_cur = math.acos((-self.pos_y + self.start_pos_y+self.R)/self.R)

            while (self.pos_x>(self.start_pos_x+self.dist)):

                a_c= self.cur_v**2/self.R
                a_t = -self.mu * (a_c + self.g*math.cos(alpha_cur)) + self.g*math.sin(alpha_cur)
                '''
                if (alpha_cur >= math.pi/2):
                    self.cur_ay = -math.cos(alpha_cur)*a_c +math.sin(alpha_cur)*(a_t)
                    self.cur_ax = -math.sin(alpha_cur)*a_c -math.cos(alpha_cur)*(a_t)
                else:
                    self.cur_ay = math.cos(alpha_cur)*a_c +math.sin(alpha_cur)*(a_t)
                    self.cur_ax = -math.sin(alpha_cur)*a_c +math.cos(alpha_cur)*(a_t)
                '''
                #self.cur_ay = math.cos(alpha_cur)*a_c +math.sin(alpha_cur)*(a_t)
                self.cur_ay = math.cos(alpha_cur)*a_c -math.sin(alpha_cur)*(a_t)
                self.cur_ax = -math.sin(alpha_cur)*a_c -math.cos(alpha_cur)*(a_t)
                self.cur_a = math.sqrt(self.cur_ax**2 + self.cur_ay**2)

                self.cur_vx += self.cur_ax*dt
                self.cur_vy += self.cur_ay*dt
                #self.cur_v += self.cur_a*dt
                #self.cur_vx = -math.sqrt(self.cur_v**2 - self.cur_vy**2)
                self.cur_v = math.sqrt(self.cur_vx**2 + self.cur_vy**2)


                self.pos_x = max(self.pos_x +self.cur_vx*dt + self.cur_ax*dt*dt/2, 0)
                self.pos_y = max(self.pos_y + self.cur_vy*dt + self.cur_ay*dt*dt/2, self.UnderModel())
                #self.pos_y = min(self.start_pos_y + 2*self.R, self.pos_y)

                alpha_cur = math.acos((-self.pos_y + self.start_pos_y+self.R)/self.R)

                needx = self.start_pos_x + self.dist + self.R*math.sin(alpha_cur)
                needy = self.start_pos_y +self.R - self.R*math.cos(alpha_cur)

                #self.pos_x = needx

                self.cur_t += dt
                time += dt

                self.t_.append(self.cur_t)
                self.a_.append(self.cur_a)
                self.v_.append(self.cur_v)

                self.x_.append(self.pos_x)
                self.y_.append(self.pos_y)

# движение по дуге до отрыва
    def SecondPath(self):
        dt =1/self.toch
        time = 0
        fail = False
        self.pos_x = self.dist+self.start_pos_x
        self.pos_y = self.start_pos_y
        l = 0
        a_c= self.cur_v**2/self.R
        a_t = -self.mu * (a_c + self.g)
        v_c = 0
        v_t = self.cur_v
        allWay= False
        alpha_cur = 0
        self.cur_vx = self.cur_v
        prevPosy = 0

        while (not fail):

            a_c= self.cur_v**2/self.R
            a_t = -self.mu * (a_c + self.g*math.cos(alpha_cur)) - self.g*math.sin(alpha_cur)
            '''
            if (alpha_cur >= math.pi/2):
                self.cur_ay = -math.cos(alpha_cur)*a_c +math.sin(alpha_cur)*(a_t)
                self.cur_ax = -math.sin(alpha_cur)*a_c -math.cos(alpha_cur)*(a_t)
            else:
                self.cur_ay = math.cos(alpha_cur)*a_c +math.sin(alpha_cur)*(a_t)
                self.cur_ax = -math.sin(alpha_cur)*a_c +math.cos(alpha_cur)*(a_t)
            '''
            #self.cur_ay = math.cos(alpha_cur)*a_c +math.sin(alpha_cur)*(a_t)
            self.cur_ay = math.cos(alpha_cur)*a_c +math.sin(alpha_cur)*(a_t)
            self.cur_ax = -math.sin(alpha_cur)*a_c +math.cos(alpha_cur)*(a_t)
            self.cur_a = math.sqrt(self.cur_ax**2 + self.cur_ay**2)

            self.cur_vx += self.cur_ax*dt
            self.cur_vy += self.cur_ay*dt
            #self.cur_v += self.cur_a*dt
            #self.cur_vx = -math.sqrt(self.cur_v**2 - self.cur_vy**2)
            self.cur_v = math.sqrt(self.cur_vx**2 + self.cur_vy**2)


            self.pos_x = max(self.pos_x +self.cur_vx*dt + self.cur_ax*dt*dt/2, 0)
            prevPosy = self.pos_y
            self.pos_y = max(self.pos_y + self.cur_vy*dt + self.cur_ay*dt*dt/2, self.start_pos_y)
            if (self.pos_x > (self.start_pos_x+self.dist)):
                alpha_cur = math.acos((-self.pos_y + self.start_pos_y+self.R)/self.R)
            else:
                alpha_cur = math.acos((self.pos_y - self.start_pos_y-self.R)/self.R)+math.pi

            if (alpha_cur >= self.alpha):
                fail = True
                allWay = True
                break


            if ((prevPosy > self.pos_y) and alpha_cur<math.pi):
                fail = True
                break
            #self.pos_y = min(self.start_pos_y + 2*self.R, self.pos_y)

            needx = self.start_pos_x + self.dist + self.R*math.sin(alpha_cur)
            needy = self.start_pos_y +self.R - self.R*math.cos(alpha_cur)

            #self.pos_x = needx

            self.cur_t += dt
            time += dt

            self.t_.append(self.cur_t)
            self.a_.append(self.cur_a)
            self.v_.append(self.cur_v)

            self.x_.append(self.pos_x)
            self.y_.append(self.pos_y)

            N = self.m *(a_c + self.g*math.cos(alpha_cur))
    
            
            if (N <= 0 or (alpha_cur == 0)):
                fail = True
                break

            
            '''
            if ((self.pos_x != self.R * math.cos(alpha_cur) ) or (self.pos_y != self.R * math.sin(alpha_cur))):
                fail = True
                break
            '''

    

        '''
            v_c  = self.cur_vx/math.cos(alpha) + self.cur_vy/math.sin(alpha)
            v_t  = self.cur_vx/math.cos(alpha) + 
            v_c += a_c*dt
            v_t += a_t*dt
            self.cur_vx = -math.sin(alpha)*v_c +math.cos(alpha)*v_t
            self.cur_vy = -math.cos(alpha)*v_c +math.sin(alpha)*v_t
        '''
        return allWay
            
#отрыв от дуги
    def ThirdPath(self):

        fullt = 0
        result = solve_quadratic_equation(self.g/2,-self.cur_vy ,-(self.pos_y - self.start_pos_y) )
        if result is None:
            print("Уравнение не имеет действительных корней")
        elif isinstance(result, tuple):
            fullt = result[0]
        else:
            fullt = result
        dt =fullt/self.toch
        self.cur_a = -self.g
        vy00 =  self.cur_vy
        pos0 = self.pos_y
        pos0x = self.pos_x
        time = 0
        while self.pos_y >= self.start_pos_y:    

            self.cur_vy += self.cur_a  * dt
   

            self.cur_v = math.sqrt(self.cur_vy**2 + self.cur_vx**2 )

            self.pos_x = max(self.pos_x +self.cur_vx*dt, 0)
            self.pos_y = self.pos_y + self.cur_vy*dt +  self.cur_a*dt**2/2
            #self.pos_y = max(self.pos_y + self.cur_vy*dt +  self.cur_a*dt**2/2, self.UnderModel())
            if (self.pos_y <= self.UnderModel()):
                self.pos_y = self.UnderModel()
                self.t_.append(self.cur_t)
                self.a_.append(abs(self.cur_a))
                self.v_.append(self.cur_v)

                self.x_.append(self.pos_x)
                self.y_.append(self.pos_y)
                self.FifthPath()
                break

            #self.pos_y = max(pos0 + vy00*time + self.g*time*time/2 , self.start_pos_y)
            #self.pos_x = max(pos0x +self.cur_vx*time, 0)

        
            self.cur_t += dt
            time +=dt

            self.t_.append(self.cur_t)
            self.a_.append(abs(self.cur_a))
            self.v_.append(self.cur_v)

            self.x_.append(self.pos_x)
            self.y_.append(self.pos_y)

        return
    

    def DO(self):
        self.clean()
        self.FirstPath()
        allWay = self.SecondPath()
        self.ThirdPath()
        return allWay
    

    def BinPoisk2(self, a):
        self.a_0 = a
        return self.BinPoisk()
    
    
    def BinPoisk(self):
        left = 2
        right = 1000
        while right - left > 0.00001:
            mid = (left+right)/2
            self.v_0 = mid 
            if self.DO():
                right = mid 
            else:
                left = mid 
        self.v_0_ans = right
        return right

    def UnderModel(self):
        
        if (self.pos_x <=( self.start_pos_x + self.dist)):
            return  self.start_pos_y
        if (self.pos_x <=( self.start_pos_x + self.dist + self.R)):
            alpha = math.asin((self.pos_x - self.start_pos_x - self.dist)/self.R)
            y = self.start_pos_y +self.R - self.R*math.cos(alpha)
            return y
        return 0

        
        
