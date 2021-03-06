echo "Creating users ..."
docker-compose -f tests/compose/core/docker-compose.yml exec admin python3 manage.py admin admin mailu.io password || exit 1
docker-compose -f tests/compose/core/docker-compose.yml exec admin python3 manage.py user --hash_scheme='SHA512-CRYPT' user mailu.io 'password' || exit 1
echo "Admin and user successfully created!"
