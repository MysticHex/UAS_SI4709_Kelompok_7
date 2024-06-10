# Kelas: SI-47-09
# Kelompok: 07
# Anggota kelompok:
# 1. Naufal Athalino Bakti (102022300239)
# 2. Affan Maulana Raffi (102022300224)
# 3. Andikanajmi Levi Maheswara (102022300083)
# 4. Aurellia Verly (102022330371)

import streamlit as st
import sqlite3
import pandas as pd
from datetime import *

# Function Mengambil data pengguna dari basis data berdasarkan username dan password.
def get_data_0709(username_0709, password_0709):
    conn_0709 = sqlite3.connect('tubes.db')
    c_0709 = conn_0709.cursor()
    c_0709.execute('SELECT * FROM users WHERE username=? AND password=?', (username_0709, password_0709))
    user_0709 = c_0709.fetchone()
    conn_0709.close()
    return user_0709

def get_user_0709(username_0709):
    conn_0709 = sqlite3.connect('tubes.db')
    c_0709 = conn_0709.cursor()
    c_0709.execute('SELECT * FROM users WHERE username=?', (username_0709,))
    user_0709 = c_0709.fetchone()
    conn_0709.close()
    return user_0709
# function Mengambil semua data dari tabel restaurants, menus, daily_needs_products, dan cleaning dari basis data.
def get_all_0709():
    conn_0709 = sqlite3.connect('tubes.db')
    restaurants_0709 = pd.read_sql_query('SELECT * FROM restaurants', conn_0709)
    
    menus_0709 = pd.read_sql_query('SELECT * FROM menus', conn_0709)
    
    products_0709 = pd.read_sql_query('SELECT * FROM daily_needs_products', conn_0709)
    
    cleaning_0709 = pd.read_sql_query('SELECT * FROM cleaning', conn_0709)
    
    conn_0709.close()
    return restaurants_0709,menus_0709,products_0709,cleaning_0709

def getriwayat_0709(id_0709):
    conn_0709 = sqlite3.connect('tubes.db')
    c_0709 = conn_0709.cursor()
    c_0709.execute('''
    SELECT fd.id, fd.alamat, fd.price,
           GROUP_CONCAT(f.food_name) AS food_items,
           GROUP_CONCAT(f.quantity) AS quantities
    FROM food_delivery fd
    JOIN foods f ON fd.id = f.id_food_delivery
    WHERE fd.customer_id =?
    GROUP BY fd.id, fd.alamat, fd.price
    ''',(id_0709,))  
    orders_0709 = c_0709.fetchall()
    
    c_0709.execute('''
              SELECT dn.id, dn.customer_id, dn.alamat, dn.tanggal, dn.status, dno.product, dno.quantity, dno.total FROM daily_needs dn LEFT JOIN daily_needs_order dno ON dn.id = dno.order_id
              ''')
    orderdneed_0709=c_0709.fetchall()
    c_0709.execute("""
              SELECT * FROM cleaning WHERE customer_id=?
              """,(id_0709,))
    orderclean_0709=c_0709.fetchall()
    c_0709.execute("""
              SELECT * FROM laundry WHERE id_customer=?
              """,(id_0709,))
    orderlaundry_0709=c_0709.fetchall()
    
    conn_0709.commit()
    conn_0709.close()
    
    return orders_0709,orderdneed_0709,orderclean_0709,orderlaundry_0709

def display_results_0709(results_0709):
    st.title("Food Delivery Results")
    df_0709 = pd.DataFrame(results_0709, columns=['Delivery ID', 'Alamat', 'Price', 'Food Name', 'Quantity'])
    st.dataframe(df_0709)

# Function Menangani proses login pengguna.
def login_0709():
    st.title("Login Page")
    st.write("Please enter your username and password")

    username_0709 = st.text_input("Username")
    password_0709 = st.text_input("Password", type="password")

    if st.button("Login"):
        user_0709 = get_data_0709(username_0709, password_0709)
        if user_0709[2]=='user':
            st.write(f"Welcome, {user_0709[1]}!")
            st.session_state.logged_in_0709 = True
            st.session_state.username_0709 = username_0709
            st.session_state.target_page_0709 = 'home'
            st.rerun()
        elif user_0709[2]=='admin':
            st.write(f"Welcome, {user_0709[1]}!")
            st.session_state.logged_in_0709 = True
            st.session_state.username_0709 = username_0709
            st.session_state.target_page_0709 = 'admin'
            st.rerun()
        else:
            st.error("Invalid username or password")

#function Menampilkan halaman utama setelah pengguna berhasil login.
def home_0709():
    st.title("Home Page")
    st.write(f"Welcome {st.session_state.username_0709}!")
    
    st.markdown(
        """
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/5.0.0-alpha1/css/bootstrap.min.css" integrity="sha384-r4NyP46KrjDleawBgD5tp8Y7UzmLA05oM1iAEQ17CSuDqnUK2+k9luXQOfXJCJ4I" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/5.0.0-alpha1/js/bootstrap.min.js" integrity="sha384-oesi62hOLfzrys4LxRF63OJCXdXDipiYWBnvTl9Y9/TRlw5xlKIEHpNyvvDShgf/" crossorigin="anonymous"></script>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
            <div class="container text-center mb-2">
                <div class="row">
                    <div class="col card mr-3" style="width: 18rem;">
                        <img src="https://png.pngtree.com/png-clipart/20220818/ourmid/pngtree-blue-washing-machine-for-laundry-logo-png-image_6114594.png" class="img-thumbnail" width="200" alt="...">
                        <div class="card-body">
                        </div>
                    </div>
                    <div class="col card mr-3" style="width: 18rem;">
                        <img src="https://logowik.com/content/uploads/images/free-food-delivery6258.logowik.com.webp" class="img-thumbnail" width="200" alt="...">
                        <div class="card-body">
                        </div>
                    </div>
                    <div class="col card mr-3" style="width: 18rem;">
                        <img src="https://marketplace.canva.com/EAF4y3V4yF0/1/0/1600w/canva-blue-and-white-cleaning-services-logo-sEqBBz8aTSU.jpg" class="img-thumbnail" width="200" alt="...">
                        <div class="card-body">
                        </div>
                    </div>
                    <div class="col card mr-3" style="width: 18rem;">
                        <img src="https://img.icons8.com/?size=100&id=QHJ0cVJXSlCx&format=png&color=000000" class="img-thumbnail" width="200" alt="...">
                        <div class="card-body">
                        </div>
                    </div>
                    <div class="col card mr-3" style="width: 18rem;">
                        <img src="https://img.icons8.com/?size=100&id=zVNKJOGkHoQg&format=png&color=000000" class="img-thumbnail" width="200" alt="...">
                        <div class="card-body">
                        </div>
                    </div>
            </div>
        """"",
        unsafe_allow_html=True
    )

    # Create Streamlit buttons
    col1_0709, col2_0709, col3_0709, col4_0709,col5_0709 = st.columns(5)
    with col1_0709:
        if st.button("Laundry"):
            st.session_state.target_page_0709 = 'laundry'
            st.rerun()
    with col2_0709:
        if st.button("Food Delivery"):
            st.session_state.target_page_0709 = 'food_deliv'
            st.rerun()
    with col3_0709:
        if st.button("Cleaning Service"):
            st.session_state.target_page_0709 = 'cleaning'
            st.rerun()
    with col4_0709:
        if st.button("Daily Needs"):
            st.session_state.target_page_0709 = 'daily_needs'
            st.rerun()
    with col5_0709:
        if st.button("Pickup and Drop Off"):
            st.session_state.target_page_0709 = 'pickup'
            st.rerun()
            
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username_0709 = ""
        st.session_state.target_page_0709 = 'login'
        st.rerun()

def laundry_0709():
    st.title("Laundry")
    st.write("This is the laundry page.")
    name_0709 = st.text_input("Nama", st.session_state.username_0709)
    alamat_0709 = st.text_input("Alamat")
    jenis_0709 = st.selectbox("Jenis", ["Pakaian", "Selimut"])
    berat_0709 = st.number_input("Berat")
    service_0709 = st.selectbox("Paket Laundry", ["Reguler (2 Hari)", "Express (1 Hari)"])

    if st.button("Order"):
        user_0709 = get_user_0709(st.session_state.username_0709)
        conn_0709 = sqlite3.connect('tubes.db')
        c_0709 = conn_0709.cursor()
        c_0709.execute("INSERT INTO laundry (id_customer, nama, alamat, jenis, berat, service) VALUES (?,?,?,?,?,?)", 
                      (user_0709[0], name_0709, alamat_0709, jenis_0709, berat_0709, service_0709))
        conn_0709.commit()
        st.success("Order berhasil dibuat")

    if st.button("Home"):
        st.session_state.target_page_0709 = 'home'
        st.experimental_rerun()

def food_deliv_0709():
    st.title("Food Delivery")
    st.write(f"This is the food delivery page.")
    alamat_0709 = st.text_input("Alamat")
    restaurants_0709, menus_0709, _, _ = get_all_0709()
    restaurant_names_0709 = restaurants_0709['name'].tolist()
    selected_name_0709 = st.selectbox("Nama Restoran", restaurant_names_0709)
    selected_restaurant_0709 = restaurants_0709[restaurants_0709['name'] == selected_name_0709].iloc[0]
    st.subheader("Menu")
    foods_0709 = menus_0709[(menus_0709['restaurant_id'] == selected_restaurant_0709['id'])]
    
    menu_inputs_0709 = {}
    total_price_0709 = 0

    for idx_0709, row_0709 in foods_0709.iterrows():
        menu_inputs_0709[idx_0709] = st.number_input(f"{row_0709['name']} ({row_0709['harga']})", step=1)
        total_price_0709 += row_0709['harga'] * menu_inputs_0709[idx_0709]

    st.write(menu_inputs_0709)
    st.write(f"Total Price: {total_price_0709}")
            
    if st.button("Order"):
        conn_0709 = sqlite3.connect('tubes.db')
        c_0709 = conn_0709.cursor()
        user_0709 = get_user_0709(st.session_state.username_0709)
        c_0709.execute("INSERT INTO food_delivery (restaurant_id, customer_id, alamat, price) VALUES (?, ?, ?, ?)",
                      (selected_restaurant_0709['id'], user_0709[0], alamat_0709, total_price_0709))
        id_food_delivery_0709 = c_0709.lastrowid

        # Insert the order details into the database
        for idx_0709, count_0709 in menu_inputs_0709.items():
            if count_0709 > 0:
                food_name_0709 = foods_0709.iloc[idx_0709]['name']
                food_price_0709 = foods_0709.iloc[idx_0709]['harga']
                c_0709.execute("INSERT INTO foods (id_food_delivery, food_name, quantity) VALUES ( ?, ?, ?)",
                              (id_food_delivery_0709, food_name_0709, count_0709))
        conn_0709.commit()
        st.success("Pesanan berhasil dibuat!")

    if st.button("Home"):
        st.session_state.target_page_0709 = 'home'
        st.rerun()

def cleaning_0709():
    st.title("Cleaning services")
    st.write("This is the cleaning services page.")
    name_0709 = st.text_input("Nama", st.session_state.username_0709)
    alamat_0709 = st.text_input("Alamat")
    tanggal_0709 = st.date_input("Tanggal", min_value=date.today())
    
    if st.button("Order"):
        user_0709 = get_user_0709(st.session_state.username_0709)
        conn_0709 = sqlite3.connect('tubes.db')
        c_0709 = conn_0709.cursor()
        c_0709.execute("""
                  INSERT INTO cleaning (customer_id, nama, alamat, tanggal) VALUES (?,?,?,?)""", (user_0709[0], name_0709, alamat_0709, tanggal_0709))
        conn_0709.commit()
        conn_0709.close()
        st.success("Pesanan telah dibuat")
    
    if st.button("Home"):
        st.session_state.target_page_0709 = 'home'
        st.rerun()

def daily_needs_0709():
    st.title("Daily Needs")
    st.write("This is the Daily Needs page.")
    
    _, _, products_0709, _ = get_all_0709() 
    
    products_input_0709 = {}
    total_price_0709 = 0

    alamat_0709 = st.text_input("Alamat")
    for idx_0709, row_0709 in products_0709.iterrows():
        products_input_0709[idx_0709] = st.number_input(f"{row_0709['product_name']} ({row_0709['price']})", step=1)
        total_price_0709 += row_0709['price'] * products_input_0709[idx_0709]

    st.write(total_price_0709)

    if st.button("Order"):
        user_0709 = get_user_0709(st.session_state.username_0709)
        conn_0709 = sqlite3.connect('tubes.db')
        c_0709 = conn_0709.cursor()
        c_0709.execute('''
                INSERT INTO daily_needs (customer_id, alamat, tanggal) VALUES (?,?,?)
                ''',(user_0709[0], alamat_0709, datetime.now()))

        id_order_0709 = c_0709.lastrowid
        
        for idx_0709, quantity_0709 in products_input_0709.items():
            if quantity_0709 > 0:
                product_0709 = products_0709.loc[idx_0709, 'product_name']
                price_0709 = products_0709.loc[idx_0709, 'price']
                totalpr_0709 = int(price_0709 * quantity_0709)
                c_0709.execute('''
                        INSERT INTO daily_needs_order (order_id, product, quantity, total) VALUES (?,?,?,?)
                        ''',(id_order_0709, product_0709, quantity_0709, totalpr_0709))

        conn_0709.commit()
        conn_0709.close()   
        
        st.success("Order dibuat")    
    
    if st.button("Home"):
        st.session_state.target_page_0709 = "home"

def create_order_0709(user_id_0709, destination_0709, pickup_datetime_0709, num_passengers_0709):
    conn_0709 = sqlite3.connect("tubes.db")
    c_0709 = conn_0709.cursor()
    c_0709.execute("""
        INSERT INTO pickups (customer_id, destination, pickup_datetime, num_passengers)
        VALUES (?,?,?,?)
    """, (user_id_0709, destination_0709, pickup_datetime_0709, num_passengers_0709))
    conn_0709.commit()
    conn_0709.close()

# Fungsi untuk membaca daftar pesanan
def read_orders_0709(user_id_0709):
    conn_0709 = sqlite3.connect("tubes.db")
    c_0709 = conn_0709.cursor()
    c_0709.execute("SELECT * FROM pickups WHERE customer_id=?",(user_id_0709,))
    orders_0709 = c_0709.fetchall()
    conn_0709.commit()
    conn_0709.close()
    return orders_0709

def update_order_0709(order_id_0709, new_destination_0709, new_datetime_0709, new_num_passengers_0709):
    conn_0709 = sqlite3.connect("tubes.db")
    c_0709 = conn_0709.cursor()
    new_datetime_str_0709 = new_datetime_0709.strftime("%Y-%m-%d %H:%M:%S")
    c_0709.execute("""
        UPDATE pickups
        SET destination = ?, pickup_datetime = ?, num_passengers = ?
        WHERE id = ?
    """, (new_destination_0709, new_datetime_str_0709, new_num_passengers_0709, order_id_0709))
    conn_0709.commit()
    conn_0709.close()
    
def cancel_order_0709(order_id_0709):
    conn_0709 = sqlite3.connect("tubes.db")
    c_0709 = conn_0709.cursor()
    c_0709.execute("""
        DELETE FROM pickups
        WHERE id = ?
    """, (order_id_0709,))
    conn_0709.commit()
    conn_0709.close()


def pickup_0709():
    st.title("Pickup page")
    st.write("Selamat datang di halaman pickup!")
    st.write("Silakan pilih menu di bawah ini:")
    
    user_0709 = get_user_0709(st.session_state.username_0709)
    menu_option_0709 = st.selectbox("Pilih menu:", ["Buat Pesanan", "Lihat Pesanan", "Perbarui Pesanan", "Batalkan Pesanan"])
    
    if menu_option_0709 == "Buat Pesanan":
        destination_0709 = st.text_input("Tujuan:")
        pickup_datetime_0709 = st.time_input("Waktu Pickup:")
        pickup_datetime_str_0709 = pickup_datetime_0709.strftime("%Y-%m-%d %H:%M:%S")

        num_passengers_0709 = st.number_input("Jumlah Penumpang:", min_value=1, step=1)
        if st.button("Buat Pesanan"):
            create_order_0709(user_0709[0], destination_0709, pickup_datetime_str_0709, num_passengers_0709)
            st.success("Pesanan Berhasil Dibuat")
    
    elif menu_option_0709 == "Lihat Pesanan":
        orderan_0709 = read_orders_0709(user_0709[0])
        if not orderan_0709:
            st.warning("Anda Belum Memiliki order")
        else:
            st.write(orderan_0709)
    
    elif menu_option_0709 == "Perbarui Pesanan":
        user_orders_0709 = read_orders_0709(user_0709[0])
        if not user_orders_0709:
            st.warning("Anda belum memiliki order")
        else:
            order_ids_0709 = [order_0709[0] for order_0709 in user_orders_0709]
            order_id_0709 = st.selectbox("Pilih ID Pesanan:", order_ids_0709)
            new_destination_0709 = st.text_input("Tujuan Baru:")
            for order_0709 in user_orders_0709:
                if order_0709[0] == order_id_0709:
                    jumlah_p_0709 = order_0709[4]
                    break
            
            new_datetime_0709 = st.time_input("Tanggal & Waktu Baru:")
            new_num_passengers_0709 = st.number_input("Jumlah Penumpang Baru:", min_value=1, step=1, value=jumlah_p_0709)
            
            if st.button("Perbarui Pesanan"):
                update_order_0709(order_id_0709, new_destination_0709, new_datetime_0709, new_num_passengers_0709)
                
    elif menu_option_0709 == "Batalkan Pesanan":
        order_id_0709 = st.number_input("ID Pesanan yang akan dibatalkan:", min_value=1, step=1)
        if st.button("Batalkan Pesanan"):
            cancel_order_0709(order_id_0709)    
                    
    if st.button("Home"):
        st.session_state.target_page_0709 = "home"
        
     
def riwayat_0709():
    st.header("Riwayat Pesanan")
    username_0709 = st.session_state.username_0709
    st.write(f"Welcome {username_0709}!")
    user_0709 = get_user_0709(username_0709)   
    orders_0709, orderneed_0709, orderclean_0709, orderlaundry_0709 = getriwayat_0709(user_0709[0])
    pickups_0709 = read_orders_0709(user_0709[0])

    if orders_0709:
        st.subheader("Riwayat Order Food Delivery")
        df_0709 = pd.DataFrame(orders_0709, columns=['ID', 'Alamat', 'Price', 'Food Items', 'Quantities'])
        
        col1_0709, col2_0709 = st.columns((4, 1))
        with col1_0709:
            st.write(df_0709[['ID', 'Alamat', 'Price', 'Food Items', 'Quantities']])
    else:
        st.write("No Order Food Delivery")
        
    if orderneed_0709:
        st.subheader("Riwayat Order Daily Needs")
        df_orders_need_0709 = pd.DataFrame(orderneed_0709, columns=['Order Id', 'Customer Id', 'Alamat', 'Waktu Transaksi', 'Status', 'Produk', 'Kuantitas', 'Harga'])
        st.table(df_orders_need_0709)
    else:
        st.write("No Order Daily Needs")
        
    if orderclean_0709:
        st.subheader("Riwayat Order Cleaning")
        df_orders_clean_0709 = pd.DataFrame(orderclean_0709)
        st.table(df_orders_clean_0709)
    else:
        st.write("No Order Cleaning")

    if orderlaundry_0709:
        st.subheader("Riwayat Order Laundry")
        df_orderlaundry_0709 = pd.DataFrame(orderlaundry_0709)
        st.table(df_orderlaundry_0709)
    else:
        st.write("No Order Laundry")

    if pickups_0709:
        st.subheader("Riwayat Order Pickups")
        df_pickups_0709 = pd.DataFrame(pickups_0709)
        st.table(df_pickups_0709)
    else:
        st.write("No Order Pickups")

#function Mengambil jumlah pesanan dari berbagai tabel di basis data.
def get_order_counts_0709():
    conn_0709 = sqlite3.connect('tubes.db')
    c_0709 = conn_0709.cursor()
    tables_0709 = ["laundry", "cleaning", "food_delivery", "daily_needs", "pickups"]
    order_counts_0709 = {}
    for table_0709 in tables_0709:
        c_0709.execute(f"SELECT COUNT(*) FROM {table_0709}")
        count_0709 = c_0709.fetchone()[0]
        order_counts_0709[table_0709] = count_0709
    return order_counts_0709

#function Menampilkan visualisasi data menggunakan grafik.
def admin_0709():
    # Create a Streamlit app
    st.title("Order Counts")

    order_counts_0709 = get_order_counts_0709()
    st.bar_chart(order_counts_0709)
    
    st.write("Order Counts:")
    st.write(pd.DataFrame(list(order_counts_0709.items()), columns=["Table", "Count"]))
    
    if st.button("Home"):
        st.session_state.target_page_0709 = "home"


def main_0709():
    if 'logged_in_0709' not in st.session_state:
        st.session_state.logged_in_0709 = False
        st.session_state.target_page_0709 = 'login'
        
    if not st.session_state.logged_in_0709:
        login_0709()
    else:
        if st.session_state.target_page_0709 == 'home':
            home_0709()
        elif st.session_state.target_page_0709 == 'laundry':
            laundry_0709()
        elif st.session_state.target_page_0709 == 'food_deliv':
            food_deliv_0709()
        elif st.session_state.target_page_0709 == 'cleaning':
            cleaning_0709()
        elif st.session_state.target_page_0709 == 'daily_needs':
            daily_needs_0709()
        elif st.session_state.target_page_0709 == 'pickup':
            pickup_0709()
        elif st.session_state.target_page_0709 == 'riwayat':
            riwayat_0709()
        elif st.session_state.target_page_0709 == 'admin':
            admin_0709()
        else:
            login_0709()

if "target_page_0709" in st.session_state:
    if st.session_state.target_page_0709 == "home" or st.session_state.target_page_0709 == "riwayat":
        st.sidebar.title("Panel")
        choice_0709 = st.sidebar.selectbox("Menu", ["Menu Utama", "Riwayat Pesanan"])
        if choice_0709 == "Menu Utama":
            if st.session_state.target_page_0709 != "home":
                st.session_state.target_page_0709 = "home"
        elif choice_0709 == "Riwayat Pesanan":
            if st.session_state.target_page_0709 != "riwayat":
                st.session_state.target_page_0709 = "riwayat"
            # Run the main function

if __name__ == "__main__":
    main_0709()