//create user for mongoDB
db.createUser(
    {
        user:"admin_mongo",
        pwd:"admin_mongo",
        roles: [
            {
                role:"readWrite",
                db:"DPML_db"
            }
        ]
    }
)