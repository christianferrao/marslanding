// MongoDB initialization script
db = db.getSiblingDB('marslanding');

// Create application user
db.createUser({
  user: 'app_user',
  pwd: 'app_password',
  roles: [
    {
      role: 'readWrite',
      db: 'marslanding'
    }
  ]
});

// Create collections with validation
db.createCollection('users', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['email', 'full_name', 'hashed_password'],
      properties: {
        email: {
          bsonType: 'string',
          pattern: '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
          description: 'Email must be a valid email address'
        },
        full_name: {
          bsonType: 'string',
          minLength: 1,
          maxLength: 100,
          description: 'Full name is required and must be between 1 and 100 characters'
        },
        hashed_password: {
          bsonType: 'string',
          description: 'Hashed password is required'
        },
        is_active: {
          bsonType: 'bool',
          description: 'is_active must be a boolean'
        },
        is_superuser: {
          bsonType: 'bool',
          description: 'is_superuser must be a boolean'
        },
        created_at: {
          bsonType: 'date',
          description: 'created_at must be a date'
        },
        updated_at: {
          bsonType: 'date',
          description: 'updated_at must be a date'
        }
      }
    }
  }
});

// Create indexes
db.users.createIndex({ 'email': 1 }, { unique: true });
db.users.createIndex({ 'created_at': 1 });
db.users.createIndex({ 'is_active': 1 });

// Create other collections
db.createCollection('sessions');
db.createCollection('logs');
db.createCollection('metrics');

// Create indexes for other collections
db.sessions.createIndex({ 'user_id': 1 });
db.sessions.createIndex({ 'expires_at': 1 }, { expireAfterSeconds: 0 });
db.logs.createIndex({ 'timestamp': 1 });
db.logs.createIndex({ 'level': 1 });
db.metrics.createIndex({ 'timestamp': 1 });
db.metrics.createIndex({ 'metric_name': 1 });

print('Database initialization completed successfully!');
