from pymongo import MongoClient

# MongoDB connection details
MONGO_URI = "mongodb://mongo:27017"  # Use the container name "mongo" as the host
DB_NAME = "open5gs"
COLLECTION_NAME = "subscribers"

# Define the base IMSI, KI, OP, and AMF values
IMSI_PREFIX = "001011234567"
KI_PREFIX = "8baf473f2f8fd09487cccbd7097c6"
OP_PREFIX = "11111111111111111111111111111"
AMF = "8000"

# MongoDB client
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Remove all existing subscribers
def remove_all_subscribers():
    result = collection.delete_many({})
    print(f"Removed {result.deleted_count} existing subscribers from the database.")

# Generate and insert subscribers
def add_subscribers(count):
    subscribers = []
    for i in range(1, count + 1):
        # Generate IMSI, KI, and OP with proper padding
        imsi = f"{IMSI_PREFIX}{i:03d}"  # Pad with leading zeros to maintain length
        ki = f"{KI_PREFIX}{i:03d}"      # Pad with leading zeros to maintain length
        op = f"{OP_PREFIX}{i:03d}"      # Pad with leading zeros to maintain length

        # Create the subscriber document
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
                                "uplink": { "value": 1, "unit": 3 },  # 1 Gbps uplink
                                "downlink": { "value": 1, "unit": 3 }  # 1 Gbps downlink
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
                "uplink": { "value": 2, "unit": 3 },  # 2 Gbps uplink
                "downlink": { "value": 2, "unit": 3 }  # 2 Gbps downlink
            },
            "security": {
                "k": ki,
                "amf": AMF,
                "op": op,
                "opc": None  # Set to None if using OP instead of OPC
            }
        }
        subscribers.append(subscriber)

    # Insert subscribers into the database
    collection.insert_many(subscribers)
    print(f"Successfully added {count} subscribers to the database.")

# Main function
def main():
    remove_all_subscribers()
    add_subscribers(256)

if __name__ == "__main__":
    main()