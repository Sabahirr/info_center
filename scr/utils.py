import pandas as pd
import streamlit as st
import requests
import io

# Cache edilmiş yükləmə funksiyası (Google Drive-dakı Parquet üçün)
@st.cache_data
def load_data(file_url: str):
    """
    Google Drive linkindən Parquet faylını yaddaşa endirib oxuyur.
    """
    try:
        # Google Drive birbaşa endirmə linki formatı
        if "drive.google.com" in file_url and "id=" in file_url:
            file_id = file_url.split("id=")[1].split("&")[0]
            download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        else:
            download_url = file_url

        # Faylı requests ilə bayt şəklində çək
        response = requests.get(download_url)
        response.raise_for_status()
        
        # BytesIO vasitəsilə Parquet faylını oxu
        df = pd.read_parquet(io.BytesIO(response.content), engine='pyarrow')
        return df
    except Exception as e:
        raise RuntimeError(f"Parquet faylı yüklənərkən xəta baş verdi: {str(e)}")


def filter_csv_by_column(df, column_name, filter_value):
    """
    Filters a DataFrame based on a specific column's value and returns the filtered data.
    """
    # Ensure the column and filter value are strings and strip extra spaces
    df[column_name] = df[column_name].astype(str).str.strip()
    filter_value = str(filter_value).strip()

    # Apply the filter
    filtered_data = df[df[column_name] == filter_value]

    return filtered_data


# import pandas as pd
# import streamlit as st


# # Cache edilmiş yükləmə funksiyası
# @st.cache_data
# def load_data(file_path: str):
#     return pd.read_parquet(file_path, engine='pyarrow')


# def filter_csv_by_column(df, column_name, filter_value):
#     """
#     Filters a DataFrame based on a specific column's value and returns the filtered data.

#     Args:
#         df (pd.DataFrame): DataFrame to filter.
#         column_name (str): Column name to filter by.
#         filter_value (str): Value to filter the column by.

#     Returns:
#         pd.DataFrame: Filtered DataFrame.
#     """
#     # Ensure the column and filter value are strings and strip extra spaces
#     df[column_name] = df[column_name].astype(str).str.strip()
#     filter_value = str(filter_value).strip()

#     # Apply the filter
#     filtered_data = df[df[column_name] == filter_value]

#     return filtered_data
