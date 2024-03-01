import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# sns.set(style='dark')

def create_bycity_df(df):
    bycity_df = df.groupby(by="customer_city").customer_id.nunique().reset_index()
    bycity_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    
    return bycity_df

def create_bystate_df(df):
    bystate_df = df.groupby(by="customer_state").customer_id.nunique().reset_index()
    bystate_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    
    return bystate_df

data = pd.read_csv('dashboard/merged_data.csv')
review_df = data.groupby("product_category_name_english").review_score.mean().sort_values(ascending=False).reset_index()
sales_count = data.groupby('product_category_name_english')['order_id'].count().reset_index()
delivery_counts = data['delivery_on_time'].value_counts()
bystate_df = create_bystate_df(data)
bycity_df = create_bycity_df(data)

st.title('Olist Brazil Dashboard')

st.subheader("Best and Worst Performing Product Category")
tab1, tab2 = st.tabs(["Based on Reviews", "Based on Sales"])
with tab1:
    fig1, ax = plt.subplots(nrows=1, ncols=2, figsize=(50, 25))
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(x="review_score", y="product_category_name_english", data=review_df.head(5), palette=colors, ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("Best Performing Product Category", loc="center", fontsize=50)
    ax[0].tick_params(axis='y', labelsize=35)
    ax[0].tick_params(axis='x', labelsize=30)

    sns.barplot(x="review_score", y="product_category_name_english", data=review_df.sort_values(by='review_score', ascending=True).head(5), palette=colors, ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("Worst Performing Product Category", loc="center", fontsize=50)
    ax[1].tick_params(axis='y', labelsize=35)
    ax[1].tick_params(axis='x', labelsize=30)

    st.pyplot(fig1)

with tab2:
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    fig2, ax = plt.subplots(nrows=1, ncols=2, figsize=(50, 25))
    sns.barplot(x="order_id", y="product_category_name_english", data=sales_count.sort_values(by='order_id', ascending=False).head(5), palette=colors, ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("Best Performing Product Category", loc="center", fontsize=50)
    ax[0].tick_params(axis='y', labelsize=35)
    ax[0].tick_params(axis='x', labelsize=30)

    sns.barplot(x="order_id", y="product_category_name_english", data=sales_count.sort_values(by='order_id', ascending=True).head(5), palette=colors, ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("Worst Performing Product Category", loc="center", fontsize=50)
    ax[1].tick_params(axis='y', labelsize=35)
    ax[1].tick_params(axis='x', labelsize=30)

    st.pyplot(fig2)

st.subheader("Delivery Performance")
labels = delivery_counts.index.map({True: 'On Time', False: 'Not On Time'})
plt.figure(figsize=(5, 5))
plt.pie(delivery_counts.values, labels=labels, autopct='%1.1f%%')
plt.title('Delivery Status')
st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot()

st.subheader("Customer Demographics")
col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots(figsize=(20, 15))
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(
        x="customer_count", 
        y="customer_state",
        data=bystate_df.sort_values(by="customer_count", ascending=False).head(10),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Customer by State", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20, 20))
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(
        x="customer_count", 
        y="customer_city",
        data=bycity_df.sort_values(by="customer_count", ascending=False).head(10),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Customer by City", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)