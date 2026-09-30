import os
import pandas as pd
import streamlit as st

# पेज की सेटिंग (वेब-पेज लुक के लिए)
st.set_page_config(
    page_title="Rahul Account - डिजिटल डायरी", page_icon="📖", layout="wide"
)

# प्रोफेशनल लुक और बोल्ड-ब्यूटीफुल बटन्स के लिए कस्टम CSS
st.markdown(
    """
    <style>
    .main {
        background-color: #f4f6f9;
    }
    h1 {
        color: #1b4f72;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: center;
        font-weight: 700;
    }
    /* बोल्ड और प्रोफेशनल बटन स्टाइल */
    .stButton>button {
        background: linear-gradient(135deg, #1f618d, #2980b9);
        color: white;
        font-size: 16px;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #154360, #1f618d);
        box-shadow: 0 6px 12px rgba(0,0,0,0.25);
        transform: translateY(-2px);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# डेटा सेव करने के लिए CSV फाइल का नाम
DATA_FILE = "rahul_account_data.csv"


# डेटा लोड या इनिशियलाइज करने का फंक्शन
def load_data():
  if os.path.exists(DATA_FILE):
    return pd.read_csv(DATA_FILE)
  else:
    return pd.DataFrame(columns=[
        "Customer ID",
        "Customer Name",
        "Address",
        "Payment Date",
        "Due Amount",
        "Paid Amount",
    ])


def save_data(df):
  df.to_csv(DATA_FILE, index=False)


df = load_data()

# ऐप का मुख्य शीर्षक
st.title("📖 राहुल अकाउंट - डिजिटल डायरी")
st.markdown(
    "<p style='text-align: center; color: #555; font-size: 18px;'>ग्राहकों का"
    " खाता, पता, बकाया और भुगतान प्रबंधन प्रणाली</p>",
    unsafe_allow_html=True,
)
st.write("---")

# साइडबार नेविगेशन मेनू
menu = st.sidebar.selectbox(
    "नेविगेशन मेनू",
    [
        "📋 सभी रिकॉर्ड देखें",
        "➕ नया ग्राहक जोड़ें",
        "✏️ रिकॉर्ड एडिट / अपडेट करें",
    ],
)

if menu == "📋 सभी रिकॉर्ड देखें":
  st.subheader("📋 ग्राहकों की सूची और खाता विवरण")

  if df.empty:
    st.info(
        "अभी तक कोई डेटा उपलब्ध नहीं है। कृपया 'नया ग्राहक जोड़ें' विकल्प का उपयोग"
        " करें।"
    )
  else:
    st.dataframe(df, use_container_width=True)

    # कुल बकाया और भुगतान का योग (Summary)
    total_due = df["Due Amount"].sum()
    total_paid = df["Paid Amount"].sum()

    col1, col2 = st.columns(2)
    with col1:
      st.metric(label="कुल बकाया राशि (Total Due)", value=f"₹ {total_due:,.2f}")
    with col2:
      st.metric(
          label="कुल भुगतान राशि (Total Paid)", value=f"₹ {total_paid:,.2f}"
      )

elif menu == "➕ नया ग्राहक जोड़ें":
  st.subheader("➕ नया ग्राहक रिकॉर्ड दर्ज करें")

  with st.form("add_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
      name = st.text_input("ग्राहक का नाम (Customer Name) *")
      date = st.date_input("भुगतान की तारीख (Payment Date)")
      due_amt = st.number_input(
          "बकाया राशि (Due Amount - ₹)", min_value=0.0, step=100.0
      )
    with col2:
      address = st.text_area("पता (Address)")
      paid_amt = st.number_input(
          "भुगतान की गई राशि (Paid Amount - ₹)", min_value=0.0, step=100.0
      )

    submitted = st.form_submit_button("💾 रिकॉर्ड सेव करें")

    if submitted:
      if name.strip() == "":
        st.error("कृपया ग्राहक का नाम अनिवार्य रूप से भरें!")
      else:
        new_id = len(df) + 1
        new_row = {
            "Customer ID": new_id,
            "Customer Name": name,
            "Address": address,
            "Payment Date": str(date),
            "Due Amount": due_amt,
            "Paid Amount": paid_amt,
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df)
        st.success(f"सफलतापूर्वक '{name}' का रिकॉर्ड जोड़ दिया गया है!")

elif menu == "✏️ रिकॉर्ड एडिट / अपडेट करें":
  st.subheader("✏️ मौजूदा ग्राहक का विवरण बदलें या अपडेट करें")

  if df.empty:
    st.warning("एडिट करने के लिए कोई रिकॉर्ड उपलब्ध नहीं है।")
  else:
    customer_list = df["Customer Name"].tolist()
    selected_customer = st.selectbox(
        "संशोधित करने के लिए ग्राहक चुनें", customer_list
    )

    # चुने गए ग्राहक का डेटा फेच करें
    cust_row = df[df["Customer Name"] == selected_customer].iloc[0]
    row_index = df[df["Customer Name"] == selected_customer].index[0]

    with st.form("edit_form"):
      new_name = st.text_input("ग्राहक का नाम", value=cust_row["Customer Name"])
      new_address = st.text_area("पता", value=str(cust_row["Address"]))
      new_date = st.text_input(
          "भुगतान की तारीख", value=str(cust_row["Payment Date"])
      )
      new_due = st.number_input(
          "बकाया राशि (Due Amount)",
          value=float(cust_row["Due Amount"]),
          step=100.0,
      )
      new_paid = st.number_input(
          "भुगतान की गई राशि (Paid Amount)",
          value=float(cust_row["Paid Amount"]),
          step=100.0,
      )

      update_btn = st.form_submit_button("🔄 रिकॉर्ड अपडेट करें")

      if update_btn:
        df.at[row_index, "Customer Name"] = new_name
        df.at[row_index, "Address"] = new_address
        df.at[row_index, "Payment Date"] = new_date
        df.at[row_index, "Due Amount"] = new_due
        df.at[row_index, "Paid Amount"] = new_paid
        save_data(df)
        st.success(f"'{new_name}' का रिकॉर्ड सफलतापूर्वक अपडेट कर दिया गया है!")
        st.rerun()
