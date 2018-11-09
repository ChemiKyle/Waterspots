# Database initialization

You can import `.tsv` files prefilled with information from a standard method

Formatted as so:

standard | test | param | lower\_bound | upper\_bound | units
generic\_standard\_name | metals\_reduction | temperature | 15 | 25 | C


In the `sqlite3` database created in the `initialize_db`, these `.tsv` files like so:

`sqlite> .mode tabs
sqlite3> .import <file_name>.tsv <table_name>`

