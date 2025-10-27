import seaborn as sns
import matplotlib.pyplot as plt

def top_users_by_points(df):
    sns.barplot(x="name", y="puntos", data=df.sort_values("puntos", ascending=False).head(5))
    plt.title("Top 5 usuarios con más puntos")
    plt.xticks(rotation=45)
    plt.show()

def price_distribution(df):
    sns.histplot(df["price"], bins=10, kde=True)
    plt.title("Distribución de precios de productos")
    plt.show()
