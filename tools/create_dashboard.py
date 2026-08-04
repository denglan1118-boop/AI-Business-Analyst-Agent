from PIL import Image, ImageDraw
import os


# =========================
# 图片目录
# =========================

image_dir = "../visualization"


# 输出

output = "../visualization/dashboard.png"


# =========================
# 读取图片
# =========================

images = {

    "sales":
        "monthly_sales_trend.png",

    "rfm":
        "rfm_3d_scatter.png",

    "top_customer":
        "top10_customer_sales.png",

    "category":
        "category_sales.png",

    "region":
        "region_sales.png",

    "clv":
        "top10_customer_clv.png"

}



img_list = []


for name,file in images.items():

    path=os.path.join(
        image_dir,
        file
    )

    img=Image.open(path)

    img.thumbnail(
        (600,350)
    )

    img_list.append(
        img
    )



# =========================
# 创建Dashboard画布
# =========================

canvas = Image.new(

    "RGB",

    (1400,1600),

    "white"

)



draw = ImageDraw.Draw(canvas)



# 标题

draw.text(

    (450,30),

    "AI Business Analyst Dashboard",

    fill="black"

)



# =========================
# 排版
# =========================


positions=[

    (50,120),

    (750,120),

    (50,520),

    (750,520),

    (50,920),

    (750,920)

]



for img,pos in zip(

        img_list,

        positions

):

    canvas.paste(

        img,

        pos

    )



# 保存

canvas.save(

    output,

    dpi=(300,300)

)



print(
    "Dashboard saved:",
    output
)