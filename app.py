from flask import Flask, render_template, request, url_for
from flaskext.mysql import MySQL
import os
from dotenv import load_dotenv

# Inisialisasi aplikasi Flask
app = Flask(__name__)

load_dotenv()

#Configurasi mysql
mysql = MySQL(app)
app.config['MYSQL_DATABASE_HOST'] = os.getenv('HOST')
app.config['MYSQL_DATABASE_USER'] = os.getenv('USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.getenv('DB')

# Rute untuk halaman utama
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Ambil data yang dikirim melalui form
        jenis_kulit = request.form.get('JenisKulit')
        permasalahan_kulit = request.form.get('PermasalahanKulit')
        manfaat = request.form.get('Manfaat')
        pencerah = request.form.get('pencerah')

        cur = mysql.connect().cursor()
        query = '''
            SELECT nama_produk, jenis_produk, Harga
            FROM hasil_topsis
            WHERE jenis_kulit1 = %s OR jenis_kulit2 = %s OR jenis_kulit3 = %s AND permasalahan_kulit = %s AND manfaat_lainnya = %s AND kandungan_pencerah = %s
            ORDER BY Rank_topsis ASC
            LIMIT 5
            '''
        
        cur.execute(query, (jenis_kulit, jenis_kulit, jenis_kulit, permasalahan_kulit, manfaat, pencerah))
        results = cur.fetchall()  # Mengambil semua hasil query
        
        # Menutup cursor
        cur.close()

        # Cek apakah ada hasil query
        if not results:
            # Jika tidak ada hasil, kirim pesan bahwa rekomendasi tidak ditemukan
            pesan = "Rekomendasi produk belum ditemukan berdasarkan kriteria yang Anda pilih."
            return render_template('index.html', pesan=pesan)
        
        # Jika ada hasil, kirimkan hasil rekomendasi
        return render_template('index.html', rekomendasi=results)
    
    return render_template('index.html')

# Rute untuk halaman 'Tentang'
@app.route('/data_topsis')
def tentang():
    cur = mysql.connect().cursor()
    cur.execute('SELECT nama_produk, jenis_produk, Harga, Preferensi, Rank_topsis FROM hasil_topsis ORDER BY Rank_topsis ASC')
    data = cur.fetchall()
    cur.close

    return render_template('data_topsis.html', data=data)

# Menjalankan server Flask
if __name__ == "__main__":
    app.run(debug=True)