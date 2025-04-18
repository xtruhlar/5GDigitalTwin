from pymongo import MongoClient

# Podrobnosti o pripojení k MongoDB
MONGO_URI = "mongodb://mongo:27017"  # Použite názov kontajnera "mongo" ako hostiteľa
DB_NAME = "open5gs"
COLLECTION_NAME = "subscribers"

# Definujte základné hodnoty IMSI, KI, OP a AMF
IMSI_PREFIX = "001011234567"
KI_PREFIX = "8baf473f2f8fd09487cccbd7097c6"
OP_PREFIX = "11111111111111111111111111111"
AMF = "8000"

# Klient MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Odstrániť všetkých existujúcich subscribers
def remove_all_subscribers():
    result = collection.delete_many({})
    print(f"Odstránených {result.deleted_count} existujúcich subscribers z databázy.")

# Generovať a vložiť subscribers
def add_subscribers(count):
    subscribers = []
    for i in range(1, count + 1):
        # Generovať IMSI, KI a OP s riadnym doplnením
        imsi = f"{IMSI_PREFIX}{i:03d}"  # Doplnte nulami na zachovanie dĺžky
        ki = f"{KI_PREFIX}{i:03d}"      # Doplnte nulami na zachovanie dĺžky
        op = f"{OP_PREFIX}{i:03d}"      # Doplnte nulami na zachovanie dĺžky

        # Vytvoriť subscriber
        subscriber = {
            "_id": imsi,
            "imsi": imsi,
            "subscribed_rau_tau_timer": 12,
            "network_access_mode": 2,
            "subscriber_status": 0,
            "access_restriction_data": 32,
            "slice": [
                {
                    "sst": 1,
                    "default_indicator": True,
                    "session": [
                        {
                            "name": "internet",
                            "type": 3,
                            "pcc_rule": [],
                            "ambr": {
                                "uplink": { "value": 1, "unit": 3 },  
                                "downlink": { "value": 1, "unit": 3 }
                            },
                            "qos": {
                                "index": 9,
                                "arp": {
                                    "priority_level": 8,
                                    "pre_emption_capability": 1,
                                    "pre_emption_vulnerability": 1
                                }
                            }
                        }
                    ]
                }
            ],
            "ambr": {
                "uplink": { "value": 2, "unit": 3 },  
                "downlink": { "value": 2, "unit": 3 }  
            },
            "security": {
                "k": ki,
                "amf": AMF,
                "op": op,
                "opc": None
            }
        }
        subscribers.append(subscriber)

    # Vložiť subscribers do databázy
    collection.insert_many(subscribers)
    print(f"Úspešne pridaných {count} subscribers do databázy.")

# Hlavná funkcia
def main():
    remove_all_subscribers()
    add_subscribers(10)

if __name__ == "__main__":
    main()