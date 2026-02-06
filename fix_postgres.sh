#!/bin/bash
# Fix PostgreSQL Credentials - Recreate with new credentials

set -e

echo "🔧 Fixing PostgreSQL Credentials"
echo "=================================="
echo ""
echo "⚠️  WARNING: This will delete all existing PostgreSQL data!"
echo "Press Ctrl+C to cancel, or Enter to continue..."
read

echo ""
echo "1. Stopping containers..."
docker-compose down

echo ""
echo "2. Removing old PostgreSQL volume..."
docker volume rm market_mood_ring_postgres_data 2>/dev/null || echo "Volume not found (already removed)"

echo ""
echo "3. Starting PostgreSQL with new credentials..."
docker-compose up -d postgres

echo ""
echo "4. Waiting for PostgreSQL to initialize..."
sleep 10

echo ""
echo "5. Verifying connection..."
if docker exec market_postgres psql -U market_user -d market_mood -c "SELECT version();" > /dev/null 2>&1; then
    echo "✅ PostgreSQL is ready with new credentials!"
    echo ""
    echo "Database: market_mood"
    echo "User: market_user"
    echo "Password: market_password"
    echo ""
    echo "6. Starting all services..."
    docker-compose up -d
    echo ""
    echo "✅ All done! You can now run producers."
else
    echo "❌ Connection failed. Check logs:"
    docker-compose logs postgres | tail -20
fi
