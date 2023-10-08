from PIL import Image, ImageDraw
import json

group = []
name_file = "2023-10-08(masive_all_brights_pixels)"
#with open(name_file + ".json", "r") as f:
#    data = json.loads(f.read())
#    for i in data['masive_all_brights_pixels:']:
#        print(i)
f = open (name_file + '.json', "r")
data = json.loads(f.read())
massiv = data['masive_all_brights_pixels'].split("], [")
print(massiv)
groups = []
for i in massiv:
    #groups = i.replace("[", "")
    #groups = i.replace("]", "")
    #groups = i.replace("(", "")
    groups.append(i.replace(")", "").replace("(", "").replace("[", "").replace("]", ""))
#print(groups)
#for i in data['masive_all_brights_pixels']:
#    print(i)

f.close()


width = 4056
height = 3040
out_image = Image.new(mode = "RGB", size = (width, height))
draw = ImageDraw.Draw(out_image)
rsp = 0
draw.rectangle((0, 0, width, height), (0, 50, 0), outline = None)
for i in groups:
    ms = i.split(", ")
    for j in range(0, len(ms), 2):
        #print(ms[j])
        draw.rectangle((int(ms[j + 1]) - rsp, int(ms[j]) - rsp, int(ms[j + 1]) + rsp, int(ms[j]) + rsp), (255, 255, 255), outline = None)
out_image.save(name_file + "_track_1.png")

