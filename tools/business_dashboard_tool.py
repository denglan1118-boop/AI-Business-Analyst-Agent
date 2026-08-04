import pandas as pd
import matplotlib.pyplot as plt
import os


VIS_DIR = "visualization"

os.makedirs(
    VIS_DIR,
    exist_ok=True
)



def category_sales_analysis(df):


    category = (

        df.groupby(
            "Category"
        )
        ["Sales"]
        .sum()
        .sort_values(
            ascending=False
        )

    )


    path = os.path.join(
        VIS_DIR,
        "category_sales.png"
    )


    plt.figure(
        figsize=(6,6)
    )


    plt.pie(
        category.values,
        labels=category.index,
        autopct="%1.1f%%"
    )


    plt.title(
        "Category Sales Distribution"
    )


    plt.savefig(
        path,
        bbox_inches="tight"
    )


    plt.close()



    return {


        "category_sales":
            category.to_dict(),


        "category_chart":
            path

    }






def region_sales_analysis(df):


    region=(

        df.groupby(
            "Region"
        )
        ["Sales"]
        .sum()
        .sort_values()

    )


    path=os.path.join(
        VIS_DIR,
        "region_sales.png"
    )



    plt.figure(
        figsize=(8,5)
    )


    region.plot(
        kind="barh"
    )


    plt.title(
        "Region Sales"
    )


    plt.xlabel(
        "Sales"
    )


    plt.tight_layout()


    plt.savefig(
        path
    )


    plt.close()



    return {


        "region_sales":
            region.to_dict(),


        "region_chart":
            path

    }