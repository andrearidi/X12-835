import os
import csv
import re

def parse_835_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Split the content into segments
    segments = content.split('~')

    # Extract relevant information
    data = []
    current_clp = {}

    for segment in segments:
        elements = segment.split('*')
        
        if elements[0] == 'CLP':
            if current_clp:
                data.append(current_clp)
            current_clp = {
                'Patient Control Number': elements[1],
                'Claim Status Code': elements[2],
                'Total Claim Charge Amount': elements[3],
                'Claim Payment Amount': elements[4],
                'Patient Responsibility Amount': elements[5],
                'Claim Filing Indicator Code': elements[6],
                'Payer Claim Control Number': elements[7],
                'Facility Type Code': elements[8],
                'Claim Frequency Type Code': elements[9]
            }
        elif elements[0] == 'NM1' and elements[1] == 'QC':
            current_clp['Patient Last Name'] = elements[3]
            current_clp['Patient First Name'] = elements[4]
            current_clp['Patient Middle Initial'] = elements[5]
            current_clp['Patient ID'] = str(elements[9])
        elif elements[0] == 'DTM' and elements[1] == '232':
            current_clp['Claim Date'] = elements[2]
        elif elements[0] == 'SVC':
            service_code = elements[1].split(':')[1]
            current_clp['Service Code'] = service_code
            current_clp['Service Amount'] = elements[2]

    if current_clp:
        data.append(current_clp)

    return data

def save_to_csv(data, output_file):
    if not data:
        print(f"No data to write to {output_file}")
        return

    fieldnames = data[0].keys()

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    print(f"Conversion complete. CSV file saved as {output_file}")

def main():
    input_directory = '.'
    output_file = 'output.csv'

    # Find all .835 files in the current directory
    input_files = [f for f in os.listdir(input_directory) if f.endswith('.835')]

    if not input_files:
        print("No .835 files found in the current directory.")
        return

    all_data = []
    for input_file in input_files:
        input_path = os.path.join(input_directory, input_file)
        try:
            file_data = parse_835_file(input_path)
            all_data.extend(file_data)
            print(f"Successfully processed {input_file}")
        except Exception as e:
            print(f"Error processing {input_file}: {str(e)}")

    if not all_data:
        print("No data found in any of the .835 files.")
        return

    save_to_csv(all_data, output_file)

if __name__ == "__main__":
    main()