import os,math,subprocess,wave
import numpy as np
from PIL import Image,ImageDraw,ImageFont
W,H=540,960
FPS=24
DUR=16
DIR='/mnt/data'
B='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
R='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BG=(9,16,25);WHITE=(241,246,250);LIME=(205,255,105);MUTED=(139,165,172)
def font(s,b=True):return ImageFont.truetype(B if b else R,s)
def center(d,s,y,size,col=WHITE,b=True):
 f=font(size,b)
 bb=d.multiline_textbbox((0,0),s,font=f,spacing=11,align='center')
 d.multiline_text(((W-bb[2]+bb[0])/2,y),s,font=f,fill=col,spacing=11,align='center')
def rect(d,r,rad,c,outline=None): d.rounded_rectangle(r,radius=rad,fill=c,outline=outline,width=2)
def ball(img,x,y,col):
 d=ImageDraw.Draw(img)
 d.ellipse((x-23,y-15,x+29,y+37),fill=(4,9,15))
 for z in range(24,0,-1):
  k=(24-z)/24
  shade=tuple(min(255,int(c*(.55+.58*k))) for c in col)
  d.ellipse((x-z+int(-3*k),y-z+int(-3*k),x+z-int(3*k),y+z-int(3*k)),fill=shade)
def smooth(t):
 t=max(0,min(1,t))
 return t*t*(3-2*t)
def frame(t):
 im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
 for j in range(20):
  yy=100+j*40
  d.line([(20,yy),(520,yy)],fill=(13,25,35),width=1)
 if t<2.78:
  center(d,'ODDLY SATISFYING',110,22,LIME)
  center(d,'just one more...',155,38)
  rect(d,(33,241,507,750),28,(15,29,42),(46,70,73))
  colors=[LIME,(121,205,255),(255,145,177),LIME,(121,205,255)]
  for i,x in enumerate([94,182,270,358,446]):
   rect(d,(x-35,278,x+35,709),30,(9,18,29),(37,57,62))
   for yy in [368,470,572,670]:
    d.ellipse((x-25,yy-25,x+25,yy+25),fill=(7,13,22),outline=(40,59,66),width=3)
   z=(t-i*.4)/.43
   if z>=0:ball(im,x,int(287+383*smooth(z)),colors[i])
  d=ImageDraw.Draw(im)
  center(d,'WAIT FOR THE LAST ONE',803,18,MUTED)
 elif t<3.32:
  d.rectangle((0,0,W,H),fill=LIME if t<2.88 else BG)
  if t>=2.88:
   center(d,'STOP.',357,100,LIME)
   center(d,'YOU WERE WATCHING THAT?',525,20,WHITE)
 elif t<5.79:
  center(d,'GOT YOUR',285,62)
  center(d,'ATTENTION.',368,65,LIME)
  rect(d,(76,493,464,502),4,(37,59,64))
  rect(d,(76,493,76+int(388*smooth((t-3.32)/2.5)),502),4,LIME)
  center(d,'That took less than 3 seconds.',552,21,MUTED,False)
  center(d,'Think about what gets ignored\\nin those same 3 seconds.',696,22,WHITE,False)
 elif t<8.35:
  center(d,'A CUSTOMER',240,49)
  center(d,"WON'T WAIT",320,60,LIME)
  center(d,'FOREVER.',403,57)
  center(d,'Especially when they have\\nthree more businesses to call.',554,22,MUTED,False)
  rect(d,(239,739,301,819),13,(33,72,65),LIME)
  d.rounded_rectangle((260,758,280,799),radius=4,outline=LIME,width=3)
 elif t<11.25:
  center(d,'INCOMING CALL',180,23,LIME)
  rect(d,(61,256,479,712),30,(17,34,47),(62,89,93))
  d.ellipse((219,299,321,401),fill=(36,60,74))
  center(d,'CUSTOMER',418,34)
  center(d,'Needs a quote • Calling now',475,18,MUTED,False)
  d.ellipse((152,560,237,645),fill=(107,40,55))
  d.ellipse((304,560,389,645),fill=(45,122,80))
  center(d,'Answer or lose the chance?',753,23)
  center(d,'Illustrative call scenario',893,14,MUTED,False)
 elif t<13.93:
  center(d,'WHAT IF',263,49)
  center(d,'EVERY CALL',345,60,LIME)
  center(d,'GOT ANSWERED?',429,45)
  rect(d,(73,585,467,742),24,(20,49,50),(87,147,123))
  d.ellipse((92,624,150,682),fill=(42,109,82))
  center(d,'VOX is answering',609,25)
  center(d,'24/7 • Qualify • Book',669,20,MUTED,False)
 else:
  center(d,'VOX',259,110,LIME)
  center(d,'BY VOKERO',416,28)
  center(d,'Your 24/7 AI receptionist.',525,22)
  rect(d,(64,645,476,720),17,LIME)
  center(d,'COMMENT "CALL"',663,26,BG)
  center(d,'for a live demo',767,22,MUTED,False)
 center(d,'VOKERO',893,20,LIME)
 return im
# Original synthetic beat, no copyrighted audio.
SR=44100
n=SR*DUR
a=np.zeros(n,np.float32)
def tone(start,dur,f,amp):
 st=int(start*SR);count=min(int(dur*SR),n-st)
 if count<=0:return
 tm=np.arange(count)/SR
 a[st:st+count]+=amp*np.sin(2*np.pi*f*tm)*np.exp(-5*tm/dur)
for t in np.arange(0,DUR,.5):tone(float(t),.18,72,.05)
for t in np.arange(0,2.5,.4):tone(float(t+.36),.11,680,.13)
for t in [2.8,3.35,5.8,8.35,11.25,13.93]:tone(t,.35,180,.14)
with wave.open('/mnt/data/.vox.wav','wb') as wf:
 wf.setnchannels(1);wf.setsampwidth(2);wf.setframerate(SR)
 wf.writeframes((np.clip(a,-.9,.9)*32767).astype('<i2').tobytes())
out='/mnt/data/vokero_stitch_hook_reel.mp4'
cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','pipe:0','-i','/mnt/data/.vox.wav','-vf','scale=1080:1920:flags=lanczos','-c:v','libx264','-preset','fast','-crf','24','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k','-movflags','+faststart','-shortest',out]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for i in range(DUR*FPS):
 im=frame(i/FPS)
 if i==DUR*FPS-25:im.save('/mnt/data/vokero_stitch_cover.jpg',quality=93)
 p.stdin.write(im.tobytes())
p.stdin.close()
assert p.wait()==0
print('rendered',os.stat(out).st_size)
