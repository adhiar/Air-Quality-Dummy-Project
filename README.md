# Air Quality Dashboard
Dashboard ini merupakan dashboard sederhana yang menampilkan proses eksplorasi data dan penjelasan
atas data yang dieksplorasi melalui beberapa pertanyaan.

Pertanyaan analisis akan meliputi:
- Daerah mana yang memiliki indeks kualitas udara paling baik? dan mengapa? (analisis lanjutan geo analisis)
- Unsur kimia mana yang paling berpengaruh terhadap nilai indeks kualitas udara berdasarkan PM2.5 dan PM10?
- Bagaimana tingkat polusi rata-rata tiap waktunya? dan dipengaruhi oleh apa?

### Setup Environment - Anaconda
```sh
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```
### Setup Environment - terminal
```sh
mkdir submission
cd submission
pipenv install
pipenv shell
pip install -r ../requirements.txt
```
### Run Dashboard
```sh
streamlit run dashboard.py
```

### Feature
- Terdapat Pilihan Tab yang terbagi menjadi 2 yaitu "Data Mining" dan "Explanation"
![Alt text](https://drive.google.com/file/d/1t-MmmFF2WSWs8kqFwl7XhMjOWL_mqxmR/view?usp=sharing)
- Terdapat Check box filter untuk menampilkan grafik yang tersedia
![Alt text](https://drive.google.com/file/d/1XidE27XaMll1MuYFprmDLXTyhEHfsHrA/view?usp=drive_link)