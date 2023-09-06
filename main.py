import streamlit as st
import pandas as pd
from datetime import date
import csv
today = date.today()

# Initial csv setting
#df = pd.DataFrame(columns=['Payer','Who','Amount','Date','Desc']).to_csv("expenses.csv", index=False, sep='|')  ### EXPENSES LOG
#df = pd.DataFrame(columns=['Who','Amount','To']).to_csv("transactions.csv", index=False, sep='|')   ### TRANSACTIONS BALANCE


# Read datasets
df = pd.read_csv("expenses.csv", sep='|')
trans = pd.read_csv("transactions.csv", sep='|')

# Calculate balance
trans_res = trans.groupby(["Who", "To"])["Amount"].sum()  ## detailed balance between persons
trans_kpi = trans.groupby(["Who"])["Amount"].sum()  ## total balance per person

# Convert group by results to dataframe and remove same payer and recepient
trans_res_df = trans_res.reset_index()  ## convert balance between people group by to df
trans_res_df = trans_res_df[trans_res_df['Who'] != trans_res_df['To']]
trans_res_df['Amount'] = trans_res_df['Amount'].apply(lambda x: float("{:.2f}".format(x)))  ## assign decimal format to amount



kpi_df = pd.DataFrame({'Who':trans_kpi.index, 'Amount':trans_kpi.values})  ## convert final group by to df
kpi_df['Amount'] = kpi_df['Amount'].apply(lambda x: float("{:.2f}".format(x)))  ## assign decimal format to amount

head1, head2 = st.columns(2)
with head1:
    st.title("Sofia Expenses")
with head2:
    st.write('')
    st.write('')
    refresh = st.button("Refresh")

st.write('')

a,b,c,d,e,f = st.columns(6)
with a:
    st.metric("**Amiram**",value = '', delta=kpi_df.loc[kpi_df['Who'] == "Amiram", "Amount"].iloc[0])

with b:
    st.metric("**Ran**",value = '', delta=kpi_df.loc[kpi_df['Who'] == "Ran", "Amount"].iloc[0])

with c:
    st.metric("**Roi**",value = '', delta=kpi_df.loc[kpi_df['Who'] == "Roi", "Amount"].iloc[0])

with d:
    st.metric("**Tom**",value = '', delta=kpi_df.loc[kpi_df['Who'] == "Tom", "Amount"].iloc[0])

with e:
    st.metric("**Tzur**",value = '', delta=kpi_df.loc[kpi_df['Who'] == "Tzur", "Amount"].iloc[0])

with f:
    st.metric("**Yaron**",value = '', delta=kpi_df.loc[kpi_df['Who'] == "Yaron", "Amount"].iloc[0])

with st.expander("Info"):
    st.markdown("**Amiram**")
    amiram_df = trans_res_df[trans_res_df['Who'] == "Amiram"]
    amiram_df = amiram_df[['To', 'Amount']]
    amiram_df = amiram_df.set_index('To')
    st.table(amiram_df)

    st.markdown("**Ran**")
    ran_df = trans_res_df[trans_res_df['Who'] == "Ran"]
    ran_df = ran_df[['To', 'Amount']]
    ran_df = ran_df.set_index('To')
    st.table(ran_df)

    st.markdown("**Roi**")
    roi_df = trans_res_df[trans_res_df['Who'] == "Roi"]
    roi_df = roi_df[['To', 'Amount']]
    roi_df = roi_df.set_index('To')
    st.table(roi_df)

    st.markdown("**Tom**")
    tom_df = trans_res_df[trans_res_df['Who'] == "Tom"]
    tom_df = tom_df[['To', 'Amount']]
    tom_df = tom_df.set_index('To')
    st.table(tom_df)

    st.markdown("**Tzur**")
    tzur_df = trans_res_df[trans_res_df['Who'] == "Tzur"]
    tzur_df = tzur_df[['To', 'Amount']]
    tzur_df = tzur_df.set_index('To')
    st.table(tzur_df)

    st.markdown("**Yaron**")
    yaron_df = trans_res_df[trans_res_df['Who'] == "Yaron"]
    yaron_df = yaron_df[['To', 'Amount']]
    yaron_df = yaron_df.set_index('To')
    st.table(yaron_df)
    

# Lists for display
payers = ["","Amiram","Ran","Roi","Tom","Tzur","Yaron"]
free_eaters = ["Amiram","Ran","Roi","Tom","Tzur","Yaron"]

add_new = st.button("New Expense", type="primary")

if refresh:
    st.experimental_rerun()

def is_user_active():
    if 'user_active' in st.session_state.keys() and st.session_state['user_active']:
        return True
    else:
        return False

if is_user_active():
    # Create new expense
    with st.form("new", clear_on_submit=True):
        pay = st.selectbox(f":money_mouth_face: Payer",payers)
        free = st.multiselect(f":face_with_cowboy_hat: Free Eaters",free_eaters, default=free_eaters)
        money = st.number_input(f":yellow_heart: How much Lev?", step=1)
        exp_date = st.date_input(f":date: Date",today, format="DD/MM/YYYY")
        desc = st.text_input(f":pencil2: Description")
        btn = st.form_submit_button("Submit")

    if btn:
        if len(pay) == 0 or len(free) == 0  or len(desc) == 0:
            st.error(f":heavy_exclamation_mark: Missing info, please complete all required fields")
        else:
            new_r = pd.DataFrame([[pay, free, money,exp_date,desc]], columns=['Payer','Who','Amount','Date','Desc'])
            new_r.to_csv('expenses.csv', mode='a', index=False, header=False, sep='|')

            counter = len(free)
            df_trans = pd.DataFrame(columns=['Who', 'Amount', 'To'])

            for item in free:
                new_trans = pd.DataFrame([[item, -money/counter, pay]], columns=['Who','Amount','To'])
                df_trans = pd.concat([df_trans, new_trans], ignore_index=True)

                mirror_trans = pd.DataFrame([[pay, money/counter, item]], columns=['Who','Amount','To'])
                df_trans = pd.concat([df_trans, mirror_trans], ignore_index=True)

            df_trans.to_csv('transactions.csv', mode='a', index=False, header=False, sep='|')
            st.success(f":thumbsup: Expense was updated")

else:
    if add_new:
        st.session_state['user_active']=True
        st.experimental_rerun()



