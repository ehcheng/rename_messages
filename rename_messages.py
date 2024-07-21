import os
import glob
import vobject

def parse_vcf(vcf_file):
    contacts = {}
    with open(vcf_file, 'r') as f:
        vcard_data = f.read()
        vcards = vobject.readComponents(vcard_data)
        for vcard in vcards:
            if hasattr(vcard, 'fn'):
                name = vcard.fn.value
                if hasattr(vcard, 'tel_list'):
                    for tel in vcard.tel_list:
                        number = tel.value.replace(' ', '').replace('-', '').replace('+', '')
                        contacts[number] = name
                if hasattr(vcard, 'email_list'):
                    for email in vcard.email_list:
                        email_value = email.value
                        contacts[email_value] = name
                        if not email_value.endswith(('.com', '.net', '.org', '.edu', '.gov')):
                            contacts[email_value + '.com'] = name  # Assuming missing domain is .com
    return contacts

def rename_html_files(directory, contacts):
    html_files = glob.glob(os.path.join(directory, "*.html"))
    for file in html_files:
        base_name = os.path.basename(file)
        name_part, ext = os.path.splitext(base_name)
        identifiers = name_part.split(', ')
        new_name_parts = []
        for identifier in identifiers:
            normalized_identifier = identifier.replace(' ', '').replace('-', '').replace('+', '')
            if normalized_identifier in contacts:
                new_name_parts.append(contacts[normalized_identifier])
            else:
                # Handle missing domain assumption
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


if __name__ == "__main__":
    vcf_file = 'contacts.vcf'  # Path to your vCard file
    html_directory = 'source'  # Path to the directory containing HTML files

    contacts = parse_vcf(vcf_file)
    rename_html_files(html_directory, contacts)
