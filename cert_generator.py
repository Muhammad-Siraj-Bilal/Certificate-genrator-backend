import cv2
from PIL import ImageFont, ImageDraw, Image  
import numpy as np 

#inputs
name = 'Anushka Narsima Amarnath'     #Gotta take name from database, using given email
track = 'Deep Learning'               #Input from webpage

# Three other files must be in the directory:
# 1 - the image of the certificate template, 'cert_template.png'
# 2 - Font 1 file NotoSans-CondensedSemiBold.ttf
# 3 - Font 2 file NotoSans-Italic.ttf

def generate_cert(name, track):

    #Dealing with 3 names, lengths
    if len(name) > 16:
        name = name.split(' ')
        if len(name) > 2:
            if len(name[0]+name[1]) < len(name[1]+name[2]):
                name = [name[0]+' '+name[1]] + name[2:]
            else:
                name = name[0:1] + [name[1]+' '+name[2]]

    #lines for the cert
    line_1 = 'for successfully completing the ''\'' + track + '\''
    line_2 = 'track, in the MDX Computing Society Study Group. Your dedication,'
    line_3 = 'hard work, and commitment have led you to achieve this significant'
    line_4 = 'milestone.  Congratulations on your accomplishment!'

    #now the image
    template = cv2.imread('cert_template.png')           #Loading the img
    template = cv2.cvtColor(template,cv2.COLOR_BGR2RGB)  #OpenCV uses BGR so converting to RGB
    template = Image.fromarray(template)                 #Sending to PIL
    draw = ImageDraw.Draw(template)

    #Loading fonts
    font1 = ImageFont.truetype('NotoSans-CondensedSemiBold.ttf', 100)  
    font2 = ImageFont.truetype('NotoSans-Italic.ttf', 40)  

    #Putting text into img
    h = 150
    w = 420
    draw.text((h, w), name[0].upper(), font=font1, fill='#646464')  
    draw.text((h, w+120), name[1].upper(), font=font1, fill='#646464')  
    draw.text((h, w+120+160), line_1, font=font2, fill='#646464')  
    draw.text((h, w+120+160+70), line_2, font=font2, fill='#646464') 
    draw.text((h, w+120+160+70+70), line_3, font=font2, fill='#646464')  
    draw.text((h, w+120+160+70+70+70), line_4, font=font2, fill='#646464')  

    return cv2.cvtColor(np.array(template), cv2.COLOR_RGB2BGR)   #Converting back to RGB

#Calling & saving
template = generate_cert(name, track)
cv2.imwrite('new/cert_m.png', template)