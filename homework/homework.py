"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel

import os
import zipfile
import pandas as pd

def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months
    """

    input_path = 'files/input/'
    output_path = 'files/output/'

    # Asegurarse de que el directorio de salida exista
    os.makedirs(output_path, exist_ok=True)

    # Eliminar los archivos existentes si ya existen
    for filename in ['client.csv', 'campaign.csv', 'economics.csv']:
        if os.path.exists(output_path + filename):
            os.remove(output_path + filename)

    # Inicialización para agregar cabeceras solo una vez
    header_client = True
    header_campaign = True
    header_economics = True

    # Iterar sobre los archivos zip en el directorio de entrada
    for file in os.listdir(input_path):
        if file.endswith('.zip'):
            
            # Abrir el archivo zip
            with zipfile.ZipFile(os.path.join(input_path, file), 'r') as z:
                # Iterar sobre los archivos dentro del zip
                for csv_file in z.namelist():
                    
                    # Leer el archivo CSV
                    with z.open(csv_file) as f:
                        df = pd.read_csv(f)
                        
                        # Procesar el archivo de clientes
                        client_df = df[['client_id', 'age', 'job', 'marital', 'education', 'credit_default', 'mortgage']].copy()
                        client_df['job'] = client_df['job'].str.replace('.', '').str.replace('-', '_')
                        client_df['education'] = client_df['education'].str.replace('.', '_').replace('unknown', pd.NA)
                        client_df['credit_default'] = client_df['credit_default'].map({'yes': 1}).fillna(0)
                        client_df['mortgage'] = client_df['mortgage'].map({'yes': 1}).fillna(0)
                        client_df.to_csv(output_path + 'client.csv', index=False, mode='a', header=header_client)
                        
                        header_client = False

                        # Procesar el archivo de campaña
                        campaign_df = df[['client_id', 'number_contacts', 'contact_duration', 'previous_campaign_contacts', 'previous_outcome', 'campaign_outcome', 'day', 'month']].copy()
                        campaign_df['previous_outcome'] = campaign_df['previous_outcome'].map({'success': 1}).fillna(0)
                        campaign_df['campaign_outcome'] = campaign_df['campaign_outcome'].map({'yes': 1}).fillna(0)
                        campaign_df['last_contact_date'] = pd.to_datetime('2022-' + campaign_df['month'].str.lower()
                         + '-' + campaign_df['day'].astype(str).str.zfill(2), format='%Y-%b-%d')

                        campaign_df.drop(columns=['month', 'day'], inplace=True)
                        campaign_df.to_csv(output_path + 'campaign.csv', index=False, mode='a', header=header_campaign)
                        
                        header_campaign = False

                        # Procesar el archivo económico
                        economics_df = df[['client_id', 'cons_price_idx', 'euribor_three_months']].copy()
                        economics_df.to_csv(output_path + 'economics.csv', index=False, mode='a', header=header_economics)
                        
                        header_economics = False
    return


if __name__ == "__main__":
    clean_campaign_data()
    