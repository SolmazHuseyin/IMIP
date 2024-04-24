import pyodbc
import json
from requests_pkcs12 import post
from requests.auth import HTTPBasicAuth
import configparser
from decimal import Decimal

# Load configuration from a file
def load_config(config_file):
    """Loads configuration from the specified file and dynamically retrieves table names."""
    config = configparser.ConfigParser()
    config.read('.\config.ini', encoding='utf-8')

    # Ensure the DEFAULT section is read
    if 'DEFAULT' not in config:
        raise ValueError("No DEFAULT section found in config.ini")

    # Validate required keys in 'DEFAULT' section
    if not all(key in config['DEFAULT'] for key in ('Server', 'Database', 'AuthType', 'APIKey', 'APISecret')):
        raise ValueError("Missing required keys in 'DEFAULT' section of config.ini")

    # Get table_name, column names, and API URL from the 'SALES' section
    sales_table_name = config['SALES'].get('sales_table_name')
    sales_column_names = config['SALES'].get('SalesColumnNames')
    sales_api_url = config['SALES'].get('SalesAPIUrl')

    # Get table_name, column names, and API URL from the 'INVENTORY' section
    inventory_table_name = config['INVENTORY'].get('inventory_table_name')
    inventory_column_names = config['INVENTORY'].get('InventoryColumnNames')
    inventory_api_url = config['INVENTORY'].get('InventoryAPIUrl')

    # Validate required keys in both sections
    if not all(val for val in (sales_table_name, sales_column_names, sales_api_url)):
        raise ValueError("Missing required keys in 'SALES' section of config.ini")
    if not all(val for val in (inventory_table_name, inventory_column_names, inventory_api_url)):
        raise ValueError("Missing required keys in 'INVENTORY' section of config.ini")

    return config, sales_table_name, sales_api_url, inventory_table_name, inventory_api_url





# Database Connection
def connect_to_database(server, database, auth_type, username=None, password=None):
    try:
        if auth_type == 'Windows':
            conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;')
        elif auth_type == 'SQL':
            conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
        else:
            raise ValueError("Invalid authentication type")
        cursor = conn.cursor()
        return conn, cursor
    except Exception as e:
        print("Database connection error:", e)
        return None, None

# Select data from database
def select_from_db(table_name, columns, condition, cursor):
    list_of_rows = []
    query = f"SELECT {columns} FROM {table_name} {condition}"
    cursor.execute(query)
    for row in cursor.fetchall():
        list_of_rows.append(row)
    return list_of_rows

# Main function to execute the script
def main():
    config, sales_table_name, sales_api_url, inventory_table_name, inventory_api_url = load_config('Test\config.ini')  # Load configuration from a file
    server = config['DEFAULT']['Server']
    database = config['DEFAULT']['Database']
    auth_type = config['DEFAULT']['AuthType']
    username = config['DEFAULT']['Username']
    password = config['DEFAULT']['Password']
    api_key = config['DEFAULT']['APIKey']
    api_secret = config['DEFAULT']['APISecret']
    certificate = config['DEFAULT']['Certificate']
    certificate_password = config['DEFAULT']['CertificatePassword']
    certificate_path = config['DEFAULT']['Certificate']
    print("Certificate path:", certificate_path)


    conn, cursor = connect_to_database(server, database, auth_type, username, password)

    if conn:
        print("Connected to the database.")
        tables = [sales_table_name, inventory_table_name]  # List of tables to import
        for table_name in tables:
            print(f"Importing data from {table_name}...")
            columns = '*'  # For simplicity, select all columns
            condition = ''  # Specify any conditions if needed
            data = select_from_db(table_name, columns, condition, cursor)
            print("Data from database:", data)


            # Define the column names for sales data
            sales_column_names = [
                "DATA_DATE", "COUNTRY_NAME", "ORGANIZATION_NAME", "PRODUCT_ID", "PRODUCT_NAME",
                "CUSTOMER_ID", "CUSTOMER_NAME", "SALES_QUANTITY", "DELIVERY_DATE", "INVOICE_DATE",
                "ORGANIZATION_REGION", "SAP_Material_No", "GTIN", "MISC1", "MISC2", "MISC3",
                "CUSTOMER_REGION", "RETURN_QUANTITY", "SALES_CATEGORY", "SALES_VALUE", "RETURN_VALUE",
                "ORGANIZATION_ID", "ADDRESS_LINE_1", "ADDRESS_LINE_2", "CITY", "ZIP_CODE",
                "PARENT_CUSTOMER_NAME"
            ]

            # Define the column names for inventory data
            inventory_column_names = [
                "DATA_DATE", "COUNTRY_NAME", "ORGANIZATION_NAME", "PRODUCT_ID", "PRODUCT_NAME",
                "AVAILABLE_QUANTITY", "DELIVERY_DATE", "SAP_Material_No", "GTIN", "MISC1",
                "MISC2", "MISC3", "ORGANIZATION_REGION", "EXPIRY_DATE", "BATCH_NO", "BLOCKED_QUANTITY",
                "STOCK_CATEGORY", "ORGANIZATION_ID"
            ]

            # Define the column names and URL based on the table
            if table_name == "API_TEST_SALES":
                column_names = sales_column_names
                url = sales_api_url
            elif table_name == "API_TEST_INV":
                column_names = inventory_column_names
                url = inventory_api_url
            else:
                print("Unknown table name")
                continue

            # Generating the Payload
            payload = []
            for row in data:
                data_dict = dict(zip(column_names, row))
                print("Raw data_dict:", data_dict)  # Debugging
                sales_quantity = data_dict.get("SALES_QUANTITY")
                return_quantity = data_dict.get("RETURN_QUANTITY")
                print("Raw quantities:", sales_quantity, return_quantity)  # Debugging
                data_dict["SALES_QUANTITY"] = float(sales_quantity) if sales_quantity is not None else None
                data_dict["RETURN_QUANTITY"] = float(return_quantity) if return_quantity is not None else None
                payload.append(data_dict)

            json_payload = json.dumps(payload)
            print(json_payload)




            # Headers with basic authorization
            headers = {
                'Content-Type': 'application/json'
            }
            print("Sections in config:", config.sections())
            for section in config.sections():
                print(f"Keys in section '{section}': {config[section]}")
            # Importing Data into IMIP Database
            ## You can use HTTPBasicAuth to handle basic authentication
            auth = HTTPBasicAuth(api_key, api_secret)

            response = post(url, data=json_payload, headers=headers, auth=auth, verify=False,
                            pkcs12_filename=certificate, pkcs12_password=certificate_password)
            print(response.text)
    else:
        print("Failed to connect to the database.")

if __name__ == "__main__":
    main()
