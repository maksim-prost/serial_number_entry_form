from model import db, TypeDevice, Device


serial_number_mask_by_device_type = {
    "D-Link DIR-300": "NXXAAXZXaa",
    "TP-Link TL-WR74": "XXAAAAAXAA",
    "D-Link DIR-300 S": "NXXAAXZXXX",
}


db.create_all()

for type_device in serial_number_mask_by_device_type:
    db.session.add( TypeDevice(title=type_device, serial_number_mask=serial_number_mask_by_device_type[type_device]))

db.session.commit()
