# Project Name

This project aims to automate the process of extracting data from an ODBC database, whether using Windows or SQL authentication, and then push that data into the IMIP database using the MuleSoft API.


## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [License](#license)

## Introduction

In today's dynamic business landscape, access to real-time data and efficient decision-making are paramount for success. The integration of APIs (Application Programming Interfaces) with Roche's IMIP database presents a transformative solution, offering a multitude of benefits across inventory planning, data-driven decision-making, and customer-centric operations.

Enhanced Inventory Planning:
Real-time insights into customers' inventory levels empower Roche to optimize stock levels effectively at both market and distributor levels. This ensures a streamlined supply chain, minimizes stock shortages, and reduces costly overstock situations, ultimately enhancing operational efficiency.

Data-Driven Decision Making:
Integration with customers' ERPs (Enterprise Resource Planning) expands Roche's decision-making capabilities beyond SAP data, enabling swift responses to market trends. Accurate and timely in-market data allows Roche to adjust strategies dynamically, improving overall operational efficiency and responsiveness to market changes.

Customer-Centric Approach:
Direct access to customers' sales and inventory data underscores Roche's commitment to understanding and meeting end-users' specific needs. By analyzing product data, Roche fine-tunes its supply to align precisely with customer preferences, fostering loyalty and long-term partnerships.

Moreover, the integration with MuleSoft API not only ensures data integrity and security but also drives innovation by setting new industry standards. By implementing multi-layered defenses against attacks and complying with industry security standards like ISO 27001 and SOC 2, MuleSoft's Anypoint Platform™ provides a secure environment for data transmission and storage.

In summary, the integration of APIs with Roche's IMIP database signifies a significant step towards leveraging data-driven insights, fostering customer relationships, and enhancing operational efficiency in today's competitive pharmaceutical landscape.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.x installed on your system
- Access to the required databases and APIs
- Installation of Certifications: The computer running the project must have the necessary certifications installed to establish secure connections and authenticate with the API endpoints. Ensure that the required certificates are installed and configured correctly on the system.

## Installation

To install the required dependencies, follow these steps:

1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. Install the dependencies using pip:
 pip install -r requirements.txt

## Usage

To use this project, follow these steps:

1. Configure the `config.ini` file according to your environment and requirements.
2. Run the `main.py` script:


## Configuration

The `config.ini` file contains configuration settings for connecting to the database and APIs. Here's a breakdown of its sections and keys:

- `[DEFAULT]`: General settings such as server, database, authentication type(SQL or Windows), API key, API secret, certificate path, and certificate password.
- `[SALES]`: Settings specific to the sales data, including API URL and table name.
- `[INVENTORY]`: Settings specific to the inventory data, including API URL and table name.

Please ensure all required keys are correctly configured before running the script.

## License

This project is proprietary and confidential to Roche and its authorized stakeholders. Redistribution or use outside of Roche or its related companies is strictly prohibited without prior written consent. Unauthorized use, reproduction, or distribution of this software, in whole or in part, may result in severe legal consequences. By accessing or using this software, you agree to abide by the terms of the Roche confidentiality agreement and any applicable laws and regulations. For inquiries regarding licensing or usage permissions, please contact the appropriate Roche department.


