from app import db, TypeDevice, Device

serial_number_mask_by_device_type = {
    "D-Link DIR-300": '\d[A-Z\d]{2}[A-Z]{2}[A-Z\d]{1}[-_@]{1}[A-Z\d]{1}[a-z]{2}',
    "TP-Link TL-WR74": '[A-Z\d]{2}[A-Z]{5}[A-Z\d]{1}[A-Z]{2}',
    "D-Link DIR-300 S": '\d[A-Z\d]{2}[A-Z]{2}[A-Z\d]{1}[-_@]{1}[A-Z\d]{3}',
}

# db.migrate()
db.create_all()

for type_device in serial_number_mask_by_device_type:
    db.session.add( TypeDevice(title=type_device, serial_number_mask=serial_number_mask_by_device_type[type_device]) )

db.session.commit()
