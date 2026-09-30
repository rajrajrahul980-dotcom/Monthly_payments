import os
import pandas as pd
import streamlit as st

# पेज की सेटिंग और वेब-पेज लुक
st.set_page_config(
    page_title="Rahul Account - डिजिटल डायरी", page_icon="📖", layout="wide"
)

# प्रोफेशनल लुक और बोल्ड-ब्यूटीफुल बटन्स के लिए कस्टम CSS
st.markdown(
    """
    <style>
    .main {
        background-color: #f8f9fa;
    }
    h1, h2, h3 {
        color: #117a65;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
    }
    /* बोल्ड और प्रोफेशनल बटन स्टाइल */
    .stButton>button {
        background: linear-gradient(135deg, #117a65, #1abc9c);
        color: white;
        font-size: 16px;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem 1.4rem;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #0e6251, #117a65);
        box-shadow: 0 6px 12px rgba(0,0,0,0.25);
        transform: translateY(-2px);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# डेटा स्टोर करने के लिए CSV फाइल
DATA_FILE = "rahul_account_data.csv"


# डेटा लोड करने का फंक्शन
def load_data():
  if os.path.exists(DATA_FILE):
    return pd.read_csv(DATA_FILE)
  else:
    return pd.DataFrame(columns=[
        "ID",
        "Customer Name",
        "Address",
        "Payment Date",
        "Due Amount",
        "Paid Amount",
    ])


def save_data(df):
  df.to_csv(DATA_FILE, index=False)


df = load_data()

# ऐप का हेडर
st.title("📖 राहुल अकाउंट - प्रोफेशनल डिजिटल डायरी")
st.markdown(
    "<p style='color: #555; font-size: 18px; font-weight: 500;'>ग्राहकों का"
    " खाता, पता, बकाया और भुगतान प्रबंधन प्रणाली</p>",
    unsafe_allow_html=True,
)
st.write("---")

# साइडबार मेनू
menu = st.sidebar.selectbox(
    "🧭 नेविगेशन मेनू",
    [
        "📋 सभी ग्राहक रिकॉर्ड देखें",
        "➕ नया ग्राहक / पेमेंट जोड़ें",
        "✏️ रिकॉर्ड एडिट / अपडेट करें",
    ],
)

# 1. सभी रिकॉर्ड देखना और समरी
if menu == "📋 सभी ग्राहक रिकॉर्ड देखें":
  st.subheader("📋 ग्राहकों की सूची और खाता विवरण")

  if df.empty:
    st.info(
        "💡 अभी तक कोई रिकॉर्ड नहीं है। बाएं मेनू से 'नया ग्राहक / पेमेंट जोड़ें'"
        " पर क्लिक करें।"
    )
  else:
    # कुल बकाया और कुल भुगतान का कार्ड
    total_due = df["Due Amount"].sum()
    total_paid = df["Paid Amount"].sum()

    c1, c2 = st.columns(2)
    with c1:
      st.metric(
          label="🔴 कुल बकाया राशि (Total Due)", value=f"₹ {total_due:,.2f}"
      )
    with c2:
      st.metric(
          label="🟢 कुल भुगतान राशि (Total Paid)", value=f"₹ {total_paid:,.2f}"
      )

    st.write("")
    # टेबल डिस्प्ले
    st.dataframe(df, use_container_width=True)

# 2. नया ग्राहक जोड़ना
elif menu == "➕ नया ग्राहक / पेमेंट जोड़ें":
  st.subheader("➕ नया ग्राहक रिकॉर्ड दर्ज करें")

  with st.form("add_customer_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
      cust_name = st.text_input("👤 ग्राहक का नाम (Customer Name) *")
      pay_date = st.date_input("📅 पेमेंट की तारीख (Payment Date)")
      due_amt = st.number_input(
          "🔴 बकाया राशि (Due Amount - ₹)", min_value=0.0, step=100.0
      )

    with col2:
      address = st.text_area(
          "🏠 ग्राहक का पूरा पता (Address)",
          placeholder="गाँव/मोहल्ला, शहर, पिन कोड",
      )
      paid_amt = st.number_input(
          "🟢 भुगतान की गई राशि (Paid Amount - ₹)", min_value=0.0, step=100.0
      )

    submitted = st.form_submit_button("💾 रिकॉर्ड सेव करें")

    if submitted:
      if not cust_name.strip():
        st.error("❌ कृपया ग्राहक का नाम अनिवार्य रूप से दर्ज करें!")
      else:
        new_id = int(df["ID"].max() + 1) if not df.empty and "ID" in df else 1
        new_row = {
            "ID": new_id,
            "Customer Name": cust_name,
            "Address": address,
            "Payment Date": str(pay_date),
            "Due Amount": due_amt,
            "Paid Amount": paid_amt,
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df)
        st.success(f"✅ '{cust_name}' का रिकॉर्ड सफलतापूर्वक जोड़ दिया गया है!")

# 3. रिकॉर्ड एडिट / अपडेट करना
elif menu == "✏️ रिकॉर्ड एडिट / अपडेट करें":
  st.subheader("✏️ मौजूदा ग्राहक का विवरण बदलें या अपडेट करें")

  if df.empty:
    st.warning("⚠️ एडिट करने के लिए कोई रिकॉर्ड उपलब्ध नहीं है।")
  else:
    customer_names = df["Customer Name"].tolist()
    selected_name = st.selectbox(
        "🔍 संशोधित (Edit) करने के लिए ग्राहक चुनें", customer_names
    )

    # चुने गए ग्राहक का डेटा निकालना
    row_idx = df[df["Customer Name"] == selected_name].index[0]
    curr_data = df.loc[row_idx]

    with st.form("edit_customer_form"):
      col1, col2 = st.columns(2)

      with col1:
        new_name = st.text_input(
            "👤 ग्राहक का नाम", value=str(curr_data["Customer Name"])
        )
        new_date = st.text_input(
            "📅 पेमेंट की तारीख", value=str(curr_data["Payment Date"])
        )
        new_due = st.number_input(
            "🔴 बकाया राशि (Due Amount)",
            value=float(curr_data["Due Amount"]),
            step=100.0,
        )

      with col2:
        new_address = st.text_area(
            "🏠 पता (Address)", value=str(curr_data["Address"])
        )
        new_paid = st.number_input(
            "🟢 भुगतान की गई राशि (Paid Amount)",
            value=float(curr_data["Paid Amount"]),
            step=100.0,
        )

      update_btn = st.form_submit_button("🔄 रिकॉर्ड अपडेट करें")

      if update_btn:
        df.at[row_idx, "Customer Name"] = new_name
        df.at[row_idx, "Address"] = new_address
        df.at[row_idx, "Payment Date"] = new_date
        df.at[row_idx, "Due Amount"] = new_due
        df.at[row_idx, "Paid Amount"] = new_paid

        save_data(df)
        st.success(
            f"✅ '{new_name}' का रिकॉर्ड सफलतापर्वूक अपडेट कर दिया गया है!"
        )
        st.rerun()
