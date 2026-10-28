import pandas as pd
import streamlit as st
from utils import load_data, filter_csv_by_column
import io

import pandas as pd
import streamlit as st
from utils import load_data, filter_csv_by_column

def main():
    st.title("Məlumat Mərkəzi")

    # Secrets yoxlaması (Xətanın qarşısını almaq üçün try-except)
    try:
        file_ids = st.secrets["general"]["file_ids"]
        PASSWORD = st.secrets["general"]["password"]
        DOWNLOAD_PASS = st.secrets["general"]["download_pass"]
    except Exception as e:
        st.error("Streamlit Secrets konfiqurasiyası tapılmadı və ya səhvdir! Zəhmət olmasa Cloud panelindən əlavə edin.")
        return

    # Sessiya dəyişənlərini təyin et
    if "download_code_verified" not in st.session_state:
        st.session_state["download_code_verified"] = False
    if "filtered_data" not in st.session_state:
        st.session_state["filtered_data"] = None
    if "full_data" not in st.session_state:
        st.session_state["full_data"] = None

    # Şifrə ilə doğrulama
    user_input = st.text_input("İstifadəçi şifrəsini daxil edin:", type="password")
    if user_input != PASSWORD:
        st.warning("Zəhmət olmasa davam etmək üçün şifrəni daxil edin.")
        return

    # Fayl URL-lərini yarat
    file_urls = [f"https://drive.google.com/uc?id={file_id}" for file_id in file_ids]

    # Məlumatı yükləyən keşlənmiş funksiya
    def load_data_cached(urls):
        all_data = []
        for idx, url in enumerate(urls, start=1):
            st.info(f"{idx}-ci fayl yüklənir...")
            df = load_data(url)
            all_data.append(df)
        return pd.concat(all_data, axis=0)

    # Yüklənmiş məlumatı sessiyada saxla
    if st.session_state["full_data"] is None:
        try:
            st.session_state["full_data"] = load_data_cached(file_urls)
            st.success("Məlumat uğurla yükləndi!")
        except Exception as e:
            st.error(f"Məlumat yüklənərkən xəta baş verdi: {str(e)}")
            return

    df = st.session_state["full_data"]
    st.write(f"Məlumat sətir sayı: {df.shape[0]}")

    # Kateqoriya seçimi və axtarış
    column_name = st.selectbox("Axtarış etmək istədiyiniz kateqoriyanı seçin:", df.columns)
    filter_value = st.text_input("Axtarış mətnini daxil edin:")

    if st.button("Axtarış"):
        try:
            filtered_data = filter_csv_by_column(df, column_name, filter_value)
            st.session_state["filtered_data"] = filtered_data
            st.session_state["download_code_verified"] = False # Yeni axtarışda şifrə təsdiqini sıfırla
        except ValueError as e:
            st.error(f"Xəta: {e}")

    # Nəticələri göstər
    if st.session_state["filtered_data"] is not None:
        filtered_df = st.session_state["filtered_data"]
        if not filtered_df.empty:
            st.write("Axtarışın nəticəsi:")
            st.dataframe(filtered_df)

            # Endirmə üçün şifrə təsdiqi
            if not st.session_state["download_code_verified"]:
                download_code = st.text_input("Nəticəni endirmək üçün şifrəni daxil edin:", type="password", key="dl_pass")
                if st.button("Şifrəni Təsdiq Et"):
                    if download_code == DOWNLOAD_PASS:
                        st.session_state["download_code_verified"] = True
                        st.rerun()
                    else:
                        st.error("Şifrə səhvdir!")

            # Şifrə doğrudursa endir düyməsini göstər
            if st.session_state["download_code_verified"]:
                csv_data = filtered_df.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="Nəticəni CSV olaraq endir",
                    data=csv_data,
                    file_name="axtarish_neticesi.csv",
                    mime="text/csv"
                )
        else:
            st.warning("Heç bir nəticə tapılmadı.")

if __name__ == "__main__":
    main()

# def main():
#     # Şifrələr və fayl ID-lərini əldə et
#     file_ids = st.secrets["general"]["file_ids"]
#     PASSWORD = st.secrets["general"]["password"]
#     DOWNLOAD_PASS = st.secrets["general"]["download_pass"]

#     # Sessiya dəyişənlərini yoxla və təyin et
#     if "download_code_verified" not in st.session_state:
#         st.session_state["download_code_verified"] = False
#     if "filtered_data" not in st.session_state:
#         st.session_state["filtered_data"] = None
#     if "full_data" not in st.session_state:
#         st.session_state["full_data"] = None

#     # Şifrə ilə doğrulama
#     st.title("Məlumat Mərkəzi")
#     user_input = st.text_input("İstifadəçi şifrəsini daxil edin:", type="password")
#     if user_input != PASSWORD:
#         st.error("Kod səhvdir! Yenidən cəhd edin.")
#         return

#     # Fayl URL-lərini yarat
#     file_urls = [f"https://drive.google.com/uc?id={file_id}" for file_id in file_ids]

#     # Məlumatı yükləmək üçün cache-lənmiş funksiya yaradılır
#     # @st.cache_data
#     def load_data_cached(file_urls):
#         all_data = []
#         for idx, url in enumerate(file_urls, start=1):
#             st.write(f"{idx}-ci fayl yüklənir...")  # Faylın nömrəsini və URL-i çap et
#             df = load_data(url)
#             st.write(f"{idx}-ci fayl yükləndi!")  # Yüklənmə tamamlandıqda məlumat ver
#             all_data.append(df)
#         return pd.concat(all_data, axis=0)

#     # Yüklənmiş məlumatı yoxla və sessiyada saxla
#     if st.session_state["full_data"] is None:
#         try:
#             st.session_state["full_data"] = load_data_cached(file_urls)
#             st.success("Məlumat yükləndi və istifadə üçün hazırdır!")
#         except Exception as e:
#             st.error(f"Error: İstifadə etmək mümkün olmadı. {str(e)}")
#             return

#     df = st.session_state["full_data"]
#     st.write(f"Məlumat ən son 2024-cü ildə yenilənib! {df.shape[0]}")

#     # Kateqoriya seçimi
#     column_name = st.selectbox("Axtarış etmək istədiyiniz kateqoriyanı seçin:", df.columns)

#     # Axtarış mətni daxil edin
#     filter_value = st.text_input("Axtarış mətnini daxil edin:")

#     # Axtarış düyməsi
#     if st.button("Axtarış"):
#         try:
#             filtered_data = filter_csv_by_column(df, column_name, filter_value)
#             st.session_state["filtered_data"] = filtered_data
#             if not filtered_data.empty:
#                 st.write("Axtarışın nəticəsi:")
#                 st.dataframe(filtered_data)
#             else:
#                 st.warning("Heç bir nəticə tapılmadı.")
#         except ValueError as e:
#             st.error(f"Error: {e}")

#         # Filtr edilmiş məlumat varsa yükləmə əməliyyatları
#     if st.session_state["filtered_data"] is not None and not st.session_state["filtered_data"].empty:
#         if not st.session_state["download_code_verified"]:
#             download_code = st.text_input("Nəticəni endirmək üçün şifrəni daxil edin:", type="password", key="download_code_input")
#             if st.button("Endirmək üçün təsdiq edin", key="download_button"):
#                 if download_code == DOWNLOAD_PASS:
#                     st.session_state["download_code_verified"] = True
#                     st.success("Şifrə doğrudur! İndi faylı yükləyə bilərsiniz.")
#                 else:
#                     st.error("Şifrə doğru deyil! Yenidən cəhd edin.")
    
#         # Şifrə doğru daxil edilibsə, yükləmə düyməsini göstər
#         if st.session_state["download_code_verified"]: 
#             csv = st.session_state["filtered_data"].to_csv(index=False).encode('utf-8-sig')
#             st.download_button(
#                         label="Nəticəni endir",
#                         data=csv,
#                         file_name="axtarish_neticesi.csv",
#                         mime="text/csv")
         
#     else:
#         st.warning("Filtr edilmiş məlumat yoxdur.")

# if __name__ == "__main__":
#     main()
