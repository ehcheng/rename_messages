# rename_messages
Backup Messages using imessage-exporter, and then run this script to do file renaming based on Contact matching of phone numbers and email addresses

Install imessage-exporter: https://crates.io/crates/imessage-exporter

Export using "compatible" mode to an output folder of your choice
```
imessage-exporter -f html -c compatible -o /Volumes/external/export
```

Export your contacts to "contacts.vcf"

Edit "rename_messages.py" to make sure vcf_file and html_directory (to the export) are accurate

Run it!
```
python rename_messages.py
```
