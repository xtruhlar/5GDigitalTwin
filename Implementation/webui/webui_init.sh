#!/bin/bash

export DB_URI="mongodb://${MONGO_IP}/open5gs"

cd webui && npm run dev

# BSD 2-Clause License | Copyright © 2020 Supreeth Herle | All rights reserved.