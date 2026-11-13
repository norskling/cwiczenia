"""Pomocnicze funkcje do prezentacji Norskling (python-pptx). Użycie: from norskling_pptx import *; ... ; p.save(plik)."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
NATT=RGBColor(0x0D,0x1F,0x2D);FJORD=RGBColor(0x1B,0x4F,0x72);IS=RGBColor(0x00,0xB4,0xD8);POL=RGBColor(0x90,0xE0,0xEF)
SKY=RGBColor(0x4A,0x60,0x70);BOR=RGBColor(0xE2,0xED,0xF2);TINT=RGBColor(0xEA,0xF7,0xFB);BG=RGBColor(0xF4,0xF9,0xFC);W=RGBColor(255,255,255)
OK=RGBColor(0x1E,0x7F,0x4F);BAD=RGBColor(0xB3,0x26,0x1E)
p=Presentation();p.slide_width=Inches(13.333);p.slide_height=Inches(7.5)
blank=p.slide_layouts[6]
def bg(s):
    f=s.background.fill;f.solid();f.fore_color.rgb=BG
def box(s,x,y,w,h,fill=W,line=BOR,rad=True):
    sh=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if rad else MSO_SHAPE.RECTANGLE,Inches(x),Inches(y),Inches(w),Inches(h))
    if rad: sh.adjustments[0]=0.06
    sh.fill.solid();sh.fill.fore_color.rgb=fill
    if line is None: sh.line.fill.background()
    else: sh.line.color.rgb=line;sh.line.width=Pt(1)
    sh.shadow.inherit=False
    return sh
def text(s,x,y,w,h,runs,size=20,font='Inter',color=SKY,bold=False,align=PP_ALIGN.LEFT,anchor=MSO_ANCHOR.TOP,spacing=1.15):
    tb=s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h));tf=tb.text_frame;tf.word_wrap=True
    tf.margin_left=tf.margin_right=Inches(0.05);tf.vertical_anchor=anchor
    lines=runs if isinstance(runs,list) else [runs]
    for i,l in enumerate(lines):
        para=tf.paragraphs[0] if i==0 else tf.add_paragraph();para.alignment=align;para.line_spacing=spacing
        segs=l if isinstance(l,list) else [(l,{})]
        for seg in segs:
            t,o=(seg,{}) if isinstance(seg,str) else seg
            r=para.add_run();r.text=t;f=r.font;f.name=o.get('font',font);f.size=Pt(o.get('size',size))
            f.bold=o.get('bold',bold);f.color.rgb=o.get('color',color)
    return tb
def pill(s,label,x=0.8,y=0.6):
    w=0.3+0.115*len(label)
    b=box(s,x,y,w,0.42);b.adjustments[0]=0.5
    dot=s.shapes.add_shape(MSO_SHAPE.OVAL,Inches(x+0.18),Inches(y+0.16),Inches(0.1),Inches(0.1));dot.fill.solid();dot.fill.fore_color.rgb=IS;dot.line.fill.background()
    text(s,x+0.33,y+0.04,w,0.34,label.upper(),size=10,bold=True,color=NATT)
def title(s,t,hl=None,y=1.2,size=36):
    if hl:
        # pasek podkreślenia pod wyróżnioną częścią: osobny box
        text(s,0.8,y,11.5,0.9,[[(t+' ',{'font':'Space Grotesk','bold':True,'color':NATT,'size':size}),(hl,{'font':'Space Grotesk','bold':True,'color':FJORD,'size':size})]])
    else:
        text(s,0.8,y,11.5,0.9,t,font='Space Grotesk',bold=True,color=NATT,size=size)
    bar=box(s,0.85,y+0.95,0.92,0.06,fill=IS,line=None,rad=False)
def slide(lbl,t,hl=None):
    s=p.slides.add_slide(blank);bg(s);pill(s,lbl);title(s,t,hl);return s
def table(s,x,y,colw,rows,head=True,size=18,rowh=0.55):
    tb=s.shapes.add_table(len(rows),len(colw),Inches(x),Inches(y),Inches(sum(colw)),Inches(rowh*len(rows))).table
    for j,cw in enumerate(colw): tb.columns[j].width=Inches(cw)
    for i,r in enumerate(rows):
        tb.rows[i].height=Inches(rowh)
        for j,v in enumerate(r):
            c=tb.cell(i,j);c.fill.solid();c.fill.fore_color.rgb=TINT if (head and i==0) else W
            c.margin_left=Inches(0.15);c.vertical_anchor=MSO_ANCHOR.MIDDLE
            tf=c.text_frame;tf.paragraphs[0].text='';r_=tf.paragraphs[0].add_run();r_.text=v
            f=r_.font;f.name='Inter';f.size=Pt(13 if (head and i==0) else size);f.bold=(head and i==0) or j==0
            f.color.rgb=NATT if j==0 or (head and i==0) else SKY
    return tb
