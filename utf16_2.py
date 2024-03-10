import streamlit as st
import csv
import os
from tempfile import NamedTemporaryFile

def load_utf16_char_count(csv_file):
    utf16_char_count = {}
    with open(csv_file.name, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            utf16_code = row[0]  # 1列目にはUTF-16の文字コードが格納されていると仮定
            char_count_str = row[1].split()[0]  # 2列目の文字列を空白で分割し、最初の要素を取得
            char_count = int(char_count_str)  # 画数を整数に変換
            utf16_char_count[utf16_code] = char_count
    return utf16_char_count

def get_char_count(utf16_char_count, char):
    utf16_code = hex(ord(char)).upper()
    utf16_code = utf16_code[2:].zfill(4)  # 先頭に0を含む4桁の16進数文字列に変換
    check_code = "U+" + utf16_code
    if check_code in utf16_char_count:
        return utf16_char_count[check_code]
    else:
        return None

def calculate_total_stroke(utf16_char_count, input_str):
    total_stroke = 0
    not_found_chars = []  # 取得できなかった文字のリスト
    for char in input_str:
        char_count = get_char_count(utf16_char_count, char)
        if char_count is not None:
            st.sidebar.write(f"文字 「{char}」 の画数は {char_count} です。")
            total_stroke += char_count
        else:
            not_found_chars.append(char)
    return total_stroke, not_found_chars

def main():
    st.title("文字画数計算")

    # 中央のコンテンツ
    col1, col2 = st.columns([2, 1])
    with col1:
        csv_file = st.file_uploader("CSVファイルをアップロードしてください", type=["csv"])
        if csv_file is not None:
            with NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(csv_file.read())
                tmp_file_path = tmp_file.name
                utf16_char_count = load_utf16_char_count(tmp_file)

            input_str = st.text_input("文字列を入力してください")
            if st.button("計算"):
                if input_str:
                    total_stroke, not_found_chars = calculate_total_stroke(utf16_char_count, input_str)
                    st.write(f"入力した文字列の総画数は<strong>《{total_stroke}》</strong>です。", unsafe_allow_html=True)
                    if not_found_chars:
                        st.write("以下の文字の画数はデータにありません:")
                        st.write("『" + ", ".join(not_found_chars) + "』")

            os.remove(tmp_file_path)

if __name__ == "__main__":
    main()
