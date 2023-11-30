import boto3
client = boto3.client('rds')
response = client.create_db_instance(
    AllocatedStorage=20,
    DBInstanceClass='db.t3.micro',
    DBInstanceIdentifier='inventorydb1',
    DBName= 'inventorydb1',
    Engine='PostgreSQL',
    MasterUserPassword='Anoop12345678',
    MasterUsername='postgres',
    PubliclyAccessible=True,
    Port=5432
)
print(response)