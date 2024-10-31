import os
import glob
import vobject
import argparse
import re

def normalize_phone_number(number, country_code=None):
    """Normalize phone number, optionally replacing leading 0 with country code"""
    # Remove spaces, dashes, and plus signs
    clean_number = number.replace(' ', '').replace('-', '').replace('+', '')
    
    # If country code is provided and number starts with 0, replace it
    if country_code and clean_number.startswith('0'):
        return country_code + clean_number[1:]
    return clean_number

def parse_vcf(vcf_file, country_code=None):
    contacts = {}
    with open(vcf_file, 'r') as f:
        vcard_data = f.read()
        vcards = vobject.readComponents(vcard_data)
        for vcard in vcards:
            if hasattr(vcard, 'fn'):
                name = vcard.fn.value
                if hasattr(vcard, 'tel_list'):
                    for tel in vcard.tel_list:
                        number = normalize_phone_number(tel.value, country_code)
                        contacts[number] = name
                if hasattr(vcard, 'email_list'):
                    for email in vcard.email_list:
                        email_value = email.value.lower()
                        contacts[email_value] = name
    return contacts

def rename_html_files(directory, contacts, country_code=None):
    html_files = glob.glob(os.path.join(directory, "*.html"))
    phone_pattern = re.compile(r'\+\d+')
    
    for file in html_files:
        base_name = os.path.basename(file)
        name_part, ext = os.path.splitext(base_name)
        identifiers = name_part.split(', ')
        new_name_parts = []
        
        for identifier in identifiers:
            # Remove spaces and check if it's a phone number with + prefix
            clean_identifier = identifier.replace(' ', '')
            match = phone_pattern.search(clean_identifier)
            if match:
                # If it matches +\d+ pattern, remove the + for lookup
                normalized_identifier = match.group()[1:]
            else:
                # Check if it might be a phone number with leading 0
                normalized_identifier = normalize_phone_number(clean_identifier, country_code)
            
            if normalized_identifier in contacts:
                new_name_parts.append(contacts[normalized_identifier])
            else:
                # Try alternate format if it starts with 0 and country code is provided
                if country_code and clean_identifier.startswith('0'):
                    alt_number = normalize_phone_number(clean_identifier, country_code)
                    if alt_number in contacts:
                        new_name_parts.append(contacts[alt_number])
                        continue
                
                # Handle missing domain assumption for emails
                if '@' in normalized_identifier and '.' not in normalized_identifier.split('@')[1]:
                    normalized_identifier_with_com = normalized_identifier + '.com'
                    if normalized_identifier_with_com in contacts:
                        new_name_parts.append(contacts[normalized_identifier_with_com])
                    else:
                        new_name_parts.append(identifier)
                else:
                    new_name_parts.append(identifier)
        
        new_name = ', '.join(new_name_parts) + ext
        new_path = os.path.join(directory, new_name)
        
        if new_path != file and os.path.exists(new_path):
            counter = 1
            base_new_name = ', '.join(new_name_parts)
            while os.path.exists(new_path):
                new_name = f"{base_new_name}_{counter}{ext}"
                new_path = os.path.join(directory, new_name)
                counter += 1
                
        os.rename(file, new_path)
        print(f'Renamed {file} to {new_path}')

def main():
    parser = argparse.ArgumentParser(description="Parse VCF file and rename HTML files based on contacts.")
    
    parser.add_argument('-c', '--contacts', type=str, default='contacts.vcf',
                        help='Path to the VCF file (default: contacts.vcf)')
    parser.add_argument('--country-code', type=str,
                        help='Country code to replace leading 0 in phone numbers (e.g., "49" for Germany)')
    parser.add_argument('-o', '--export-path', type=str, default='source',
                        help='Directory containing HTML files (default: source)')
    
    args = parser.parse_args()
    contacts = parse_vcf(args.contacts, args.country_code)
    rename_html_files(args.export_path, contacts, args.country_code)

if __name__ == "__main__":
    main()
