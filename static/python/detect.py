import math


def d(x1, x2, y1, y2):
    return math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))

def lined(x,y,x1, y1, x2, y2):
    return y-((((x-x1)*(y2-y1))/(x2-x1))+y1)


# расчет Верхняя губа с галочкой и Прямая верхняя губа
def lips_gal(pose_landmarks, prop):
    d1 = d(pose_landmarks.part(50).x, pose_landmarks.part(51).x, pose_landmarks.part(50).y, pose_landmarks.part(51).y)
    d2 = d(pose_landmarks.part(51).x, pose_landmarks.part(52).x, pose_landmarks.part(51).y, pose_landmarks.part(52).y)
    d1 = (d1 + d2) / 2
    d3 = d(pose_landmarks.part(50).x, pose_landmarks.part(52).x, pose_landmarks.part(50).y, pose_landmarks.part(52).y)
    d3 = math.acos(d3 ** 2 / (2 * d3 * d1))
    d3 = d3 * 180 / 3.1415926
    d3 = (d3 - 5) / 0.2
    return (d3)


# расчет Толстая и тонкая верхняя губа
def lips_height(pose_landmarks, height):
    d1 = d(pose_landmarks.part(50).x, pose_landmarks.part(61).x, pose_landmarks.part(50).y, pose_landmarks.part(61).y)
    d2 = d(pose_landmarks.part(52).x, pose_landmarks.part(63).x, pose_landmarks.part(52).y, pose_landmarks.part(63).y)
    d1 = (d1 + d2) / 2
    d1 = d1 * 100 / height
    d1 = (d1 - 2) / 0.07
    if d1 > 100:
        d1 = 100
    if d1 < 0:
        d1 = 0
    return (d1)


# расчет Уголки губ - слева
def left_lips_ugolki(pose_landmarks, prop):
    d1=lined(pose_landmarks.part(48).x,pose_landmarks.part(48).y,pose_landmarks.part(60).x,pose_landmarks.part(60).y,pose_landmarks.part(64).x,pose_landmarks.part(64).y)
    d1=d1*100/prop
    d1 = (d1) / 0.0474
    if d1 > 100:
        d1 = 100
    if d1 < 0:
        d1 = 0
    return (d1)

# расчет Уголки губ - справа
def right_lips_ugolki(pose_landmarks, prop):
    d1=lined(pose_landmarks.part(54).x,pose_landmarks.part(54).y,pose_landmarks.part(60).x,pose_landmarks.part(60).y,pose_landmarks.part(64).x,pose_landmarks.part(64).y)
    d1=d1*100/prop
    d1 = abs(d1) / 0.03
    if d1 > 100:
        d1 = 100
    if d1 < 0:
        d1 = 0
    return (d1)


# расчет Узкий и широкий рот
def lips_rot(pose_landmarks):
    prop_hor=d(pose_landmarks.part(4).x, pose_landmarks.part(12).x, pose_landmarks.part(4).y,pose_landmarks.part(12).y)
    rot=d(pose_landmarks.part(60).x, pose_landmarks.part(64).x, pose_landmarks.part(60).y,pose_landmarks.part(64).y)
    d1=rot*100/prop_hor
    d1 = abs(d1-24) / 0.39
    if d1 > 100:
        d1 = 100
    if d1 < 0:
        d1 = 0
    return (d1)



# расчет Близко и широкопосаженные глаза
def eye_posadka(pose_landmarks):
    #prop_eye=d(pose_landmarks.part(42).x, pose_landmarks.part(45).x, pose_landmarks.part(42).y,pose_landmarks.part(45).y)
    #prop_eye2 = d(pose_landmarks.part(36).x, pose_landmarks.part(39).x, pose_landmarks.part(36).y, pose_landmarks.part(39).y)
    #prop_eye=(prop_eye+prop_eye2)/2
    prop_eye = d(pose_landmarks.part(1).x, pose_landmarks.part(15).x, pose_landmarks.part(1).y, pose_landmarks.part(15).y)
    posadka=d(pose_landmarks.part(39).x, pose_landmarks.part(42).x, pose_landmarks.part(39).y,pose_landmarks.part(42).y)
    d1=posadka*100/prop_eye
    d1 = abs(d1-20) / 0.13
    if d1 > 100:
        d1 = 100
    if d1 < 0:
        d1 = 0
    return (d1)


#расчет цвет глаз
def eye_color(pose_landmarks, im):
    count=((pose_landmarks.part(44).x- pose_landmarks.part(43).x)*(pose_landmarks.part(47).y-pose_landmarks.part(43).y))+((pose_landmarks.part(37).x - pose_landmarks.part(38).x) * (pose_landmarks.part(37).y - pose_landmarks.part(41).y))
    rs=0
    bs=0
    gs=0
    for i in range(pose_landmarks.part(43).x, pose_landmarks.part(44).x):
        for j in range(pose_landmarks.part(43).y, pose_landmarks.part(47).y):
            r, g, b = im.getpixel((i,j))
            rs+=r
            bs+=b
            gs+=g
    for i in range(pose_landmarks.part(37).x, pose_landmarks.part(38).x):
        for j in range(pose_landmarks.part(37).y, pose_landmarks.part(41).y):
            r, g, b = im.getpixel((i,j))
            rs+=r
            bs+=b
            gs+=g
    rs=rs / count
    gs=gs / count
    bs=bs / count
  
    gol=(bs-gs)+(bs-rs)
    
    zel=(gs-bs)+(gs-rs)
    
    kar=(rs-bs)+(rs-gs)
    
    ser=100-(abs(gs-rs)+abs(bs-bs))
    return (gol,zel,kar,ser)

# расчет Большой и маленький подбородок
def chin_size(pose_landmarks, prop):
    chin = d(pose_landmarks.part(57).x, pose_landmarks.part(8).x, pose_landmarks.part(57).y, pose_landmarks.part(8).y)
    d1=chin*100/prop
    d1 = abs(d1-18) / 0.53
    if d1 > 100:
        d1 = 100
    if d1 < 0:
        d1 = 0
    return (d1)

# расчет Квадратный и круглый подбородок
def chin_form(pose_landmarks, prop):
    form = pose_landmarks.part(8).y-(pose_landmarks.part(7).y+pose_landmarks.part(9).y)/2
    form=form*100/prop
    form = abs(form) / 0.05
    if form > 100:
        form = 100
    if form < 0:
        form = 0
    return (form)

# расчет Сросшиеся брови
def eyebrows_accreted(pose_landmarks, im):
    rs = 0
    bs = 0
    gs = 0
    all = 0
    nose_color = 0
    max_y = max(pose_landmarks.part(21).y,pose_landmarks.part(22).y)
    min_y = round((pose_landmarks.part(27).y - max_y)/2)+max_y
    count=((pose_landmarks.part(22).x - pose_landmarks.part(21).x))*(min_y - max_y)+1
    for i in range(pose_landmarks.part(21).x, pose_landmarks.part(22).x):
        for j in range(max_y, min_y):
            r, g, b = im.getpixel((i, j))
            all+=r+b+g
    all /= count
    for i in range(pose_landmarks.part(28).y, pose_landmarks.part(29).y):
        r, g, b = im.getpixel((pose_landmarks.part(30).x, pose_landmarks.part(30).y))
        nose_color += r + g + b
    nose_color/=pose_landmarks.part(29).y - pose_landmarks.part(28).y+1
    r=nose_color-all
    if r > 220:
        r = 100
    elif r < 40:
        r = 0
    else: r = (r - 40) / 1.8
    return (r)