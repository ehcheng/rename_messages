# rename_messages
Backup Messages using imessage-exporter, and then run this script to do file renaming based on Contact matching of phone numbers and email addresses

For example, if the export yields a filename like this:

+14155551212, foo@bar.html

And you have Contacts in the .vcf file that match, a rename might output:

Joe Time, Bill Holman.html

## Export Messages on a Mac

Install imessage-exporter: https://crates.io/crates/imessage-exporter

Export using "compatible" mode to an output folder of your choice
```
imessage-exporter -f html -c compatible -o /Volumes/external/export
```

## Export your contacts

Export your contacts to "contacts.vcf"

## Run the script

Edit "rename_messages.py" to make sure vcf_file and html_directory (to the export) are accurate

Run it!
```
python rename_messages.py
```
