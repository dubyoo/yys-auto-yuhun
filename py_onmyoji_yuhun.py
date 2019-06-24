import win32com.client 
import sys 
import time
import random

def mysleep(sleep_time, variable_time = 0): 
    '''
    randomly sleep for a short time between `sleep_time` and `sleep_time + variable_time` \n
    because of the legacy reason, sleep_time and variable_time are in millisecond
    '''
    slp = random.randint(sleep_time, sleep_time + variable_time); print('Going to sleep %d ms' % slp)
    time.sleep(slp/1000)

def click_in_region(ts, x1, x2, y1, y2): 
    '''
    randomly click a point in a rectangle region (x1, y1), (x2, y2)
    '''
    xr = random.randint(x1, x2)
    yr = random.randint(y1, y2)
    ts.MoveTo(xr, yr); print('Move to (%d, %d)'% (xr, yr))
    mysleep(10, 10)
    ts.LeftClick(); print('Left click')
    mysleep(10, 10)

def reject_xuanshang(ts): 
    colxs = ts.GetColor(750, 458)
    #print(colxs)
    if colxs == "df715e":
        click_in_region(ts, 750-5, 750+5, 458-5, 458+5)
        print("successfully rejected XUAN-SHANG")
        mysleep(1000)
    mysleep(50)

def wtfc1(ts, colx, coly, coll, x1, x2, y1, y2, zzz, adv):
  '''
  Usage: 
  等待并且持续判断点 (colx, coly) 的颜色，直到该点颜色
  等于 coll (if zzz == 0) 或者 不等于 coll (if zzz == 1) 
  然后开始随机点击范围 (x1, x2) (y1, y2) 内的点，直到点 (colx, coly) 的颜色
    if adv == 1: 
     不等于 coll (if zzz == 0) 或者 等于 coll (if zzz == 1)  
    if adv == 0: 
     不判断，点击一次后退出循环
  Example: 
  在准备界面时，通过判断鼓锤上某点的颜色（因为UI不会随着游戏人物摆动），来持续点击鼓面，
  直到鼓锤上该点的颜色改变，说明进入了战斗
  '''
  j = 0
  flgj =0
  while j == 0:
    reject_xuanshang(ts)
    coltest = ts.GetColor(colx, coly)
    #print(colx, coly, coltest)
    if (coltest == coll and zzz == 0) or (coltest != coll and zzz == 1):
        flgj = 1
    if flgj == 1:
        reject_xuanshang(ts)
        click_in_region(ts, x1, x2, y1, y2)
        mysleep(1000, 333)
        if adv == 0:
            j = 1
        reject_xuanshang(ts)
        coltest2 = ts.GetColor(colx, coly)
        if (coltest2 == coll and zzz == 1) or (coltest2 != coll and zzz == 0):
            j = 1

def yuhun(ts): 
    # 检测天使插件 COM Object 是否建立成功
    need_ver = '4.019'
    if(ts.ver() != need_ver): 
        print('register failed')
        return 
    print('register successful')

    # 绑定窗口
    hwnd = ts.FindWindow("", "阴阳师-网易游戏")
    ts_ret = ts.BindWindow(hwnd, 'dx2', 'windows', 'windows', 0) 
    if(ts_ret != 1): 
        print('binding failed')
        return 
    print('binding successful')
    mysleep(2000)

    # 颜色 Debug 测试 
    while True:
        tscoldebug = ts.GetColor(1, 1)
        print(tscoldebug)
        if tscoldebug != "000000" and tscoldebug != "ffffff":
            break
        mysleep(200)
    print('passed color debug')

    # 御魂战斗主循环
    while True:
        # 在御魂主选单，点击“挑战”按钮, 需要使用“阵容锁定”！
        wtfc1(ts, 807, 442, "f3b25e", 807, 881, 442, 459, 0, 1)
        print('already clicked TIAO-ZHAN')

        # 检测是否进入战斗
        while True:
            reject_xuanshang(ts)
            colib = ts.GetColor(71, 577)
            if colib == "f7f2df":
                break
            mysleep(500)
        print("now we are in the battle")

        # 检测是否结束战斗
        while True:
          reject_xuanshang(ts)
          colib = ts.GetColor(71, 577)
          if colib != "f7f2df":
              break
        mysleep(500, 500)
        print("battle finished")

        # 在战斗结算页面
        while True: 
          reject_xuanshang(ts)
          click_in_region(ts, 980, 1030, 225, 275)

          coljs = ts.GetColor(807, 442)
          if coljs == "f3b25e":
              break
          mysleep(500, 500)
        print("back to YUHUN level selection")
    

if __name__ == "__main__":
    print('python version:', sys.version)

    # 需要提前在 windows 中注册 TSPlug.dll
    # 方法: regsvr32.exe TSPlug.dll

    # Reference: http://timgolden.me.uk/pywin32-docs/html/com/win32com/HTML/QuickStartClientCom.html
    # 建立 COM Object
    ts = win32com.client.Dispatch("ts.tssoft") 

    try:
        yuhun(ts)
    except: 
        print('terminated')
        print('UnBindWindow return:', ts.UnBindWindow())
