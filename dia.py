import math
objects = []

FONT = 'Iosevka'
TFILL = 'white'
W = 800
H = 600

M = 5 * min(H, W) / 100

print('<svg viewBox="0 0 {} {}" xmlns="http://www.w3.org/2000/svg">'.format(W, H))

class Rect:
  def __init__(self, x=0, y=0, w=100, h=100, r=0, fill=''):
    self.fill = fill
    self.x = x * W / 100
    self.y = y * H / 100
    self.w = w * W / 100
    self.h = h * H / 100
    self.r = r * min(W, H) / 100
    objects.append(self)

  def inx(self, other):
    other.w = self.w - 2*M
    other.x = self.x + M

  def iny(self, other):
    other.h = self.h - 2*M
    other.y = self.y + M

  def inset(self, other):
    self.inx(other)
    self.iny(other)

  def horiz(self, *others):
    n = len(others)
    margins = (n+1)*M
    w = (self.w - margins) / n
    x = self.x + M
    for other in others:
      other.w = w
      other.x = x
      self.iny(other)
      x += w + M

  def vert(self, *others):
    n = len(others)
    margins = (n+1)*M
    h = (self.h - margins) / n
    y = self.y + M
    for other in others:
      other.h = h
      other.y = y
      self.inx(other)
      y += h + M

  def mtext(self, **kwargs):
    t = Text(**kwargs)
    t.x = self.x + self.w/2
    t.y = self.y + self.h/2 + t.h*.75/2
    return t

  def ttext(self, **kwargs):
    t = Text(**kwargs)
    t.x = self.x + self.w/2
    t.y = self.y + t.h * 1.4 + M/2
    tail = Rect()
    tail.x = self.x
    tail.y = self.y
    tail.w = self.w
    tail.h = self.h
    tail.h -= t.h + M*1
    tail.y += t.h + M*1
    return tail

  def render(self):
    if self.fill == '': return ''
    return '<rect x="{}" y="{}" width="{}" height="{}" rx="{}" ry="{}" fill="{}" />'.format(self.x, self.y, self.w, self.h, self.r, self.r, self.fill)


class Text:
  def __init__(self, text="text", x=0, y=0, h=5, fill=TFILL):
    self.x = x*W/100
    self.y = y*H/100
    self.h = h*H/100
    self.w = len(text) * self.h / 2
    self.fill = fill
    self.text = text
    objects.append(self)
  def render(self):
    if self.fill=='': return ''
    return '<text x="{}" y="{}" fill="{}" font-size="{}" font-family="{}" text-anchor="middle">{}</text>'.format(self.x,self.y,self.fill,self.h,FONT,self.text)

class Arrow:
  def __init__(self, a, b):
    if a.x + a.w > b.x and b.x + b.w > a.x:
      low = max(a.x, b.x)
      high = min(a.x+a.w, b.x+b.w)
      self.startX = (low + high)/2
      self.endX = self.startX
      if a.y < b.y:
        self.startY = a.y + a.h
        self.endY = b.y
      else:
        self.startY = a.y
        self.endY = b.y + b.h
    elif a.y + a.h > b.y and b.y + b.h > a.y:
      low = max(a.y, b.y)
      high = min(a.y+a.h, b.y+b.h)
      self.startY = (low + high)/2
      self.endY = self.startY
      if a.x < b.x:
        self.startX = a.x + a.w
        self.endX = b.x
      else:
        self.startX = a.x
        self.endX = b.x + b.w
    else:
      self.startX = a.x
      self.startY = a.y
      self.endX = b.x
      self.endY = b.y
    objects.append(self)

  def _svg_line(self, aX, aY, bX, bY):
    return '<path d="M{},{} L{},{}" stroke="black" stroke-width="5" />'.format(aX, aY, bX, bY)

  def render(self):
    a = math.atan2(self.endY - self.startY, self.endX - self.startX)
    l = 15

    s = self._svg_line(self.startX, self.startY, self.endX, self.endY)

    return s + '<path d="M{},{} L{},{} L{},{}" stroke="black" fill="transparent" stroke-width="5" />'.format(self.endX + math.cos(a + math.pi * 0.75) * l, self.endY + math.sin(a + math.pi * 0.75) * l, self.endX, self.endY, self.endX + math.cos(a - math.pi * 0.75) * l, self.endY + math.sin(a - math.pi * 0.75) * l)


bg = Rect()

android = Rect(fill="#6d4", r=5)

cloud = Rect(fill='#48d', r=5)

bg.horiz(android, cloud)

android = android.ttext(text="Android")
cloud = cloud.ttext(text="Cloud")

engine = Rect(fill='#86b', r=5)

android.inset(engine)

engine = engine.ttext(text="LibEngine", fill='white')

handler = Rect(fill='#d48', r=3)
loader = Rect(fill='#d84', r=3)
engine.vert(handler, loader)

handler.mtext(text="Handler")
loader.mtext(text="Loader")

frontend = Rect(fill='#d48', r=5)
service = Rect(fill = '#d84', r=5)

cloud.vert(frontend, service)

frontend.mtext(text='FRONTEND')
service.mtext(text='Service')

Arrow(loader, handler)
Arrow(handler, frontend)
Arrow(frontend, service)

for o in objects: print(o.render())

print('</svg>')
