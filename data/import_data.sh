#!/bin/bash

# Import sample data into MongoDB
# Usage: ./import_data.sh

DB_NAME="vendor_analytics"
COLLECTION="shares"
DATA_FILE="sample_data.json"

echo "📦 Importing sample data into MongoDB..."
echo "Database: $DB_NAME"
echo "Collection: $COLLECTION"
echo ""

# Check if mongoimport is available
if ! command -v mongoimport &> /dev/null
then
    echo "❌ mongoimport not found. Please install MongoDB tools."
    echo "   Visit: https://www.mongodb.com/try/download/database-tools"
    exit 1
fi

# Import data
mongoimport \
  --db "$DB_NAME" \
  --collection "$COLLECTION" \
  --file "$DATA_FILE" \
  --jsonArray \
  --drop

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Data imported successfully!"
    echo ""
    echo "Verify with:"
    echo "  mongosh $DB_NAME --eval 'db.shares.countDocuments()'"
else
    echo ""
    echo "❌ Import failed. Check your MongoDB connection."
    exit 1
fi
