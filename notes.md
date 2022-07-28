## Entity: Inventory
* Should it be called "Record"?

* If Inventory_Entity ID is autoincrement, then it becomes a record keeper;
* By using unique strings for ID we can have multiple inventories interpretation;
# By using ID strings + non_nullabel, multiple primary_key;

## MySql specific:
* UNSIGNED INT;
* % and _ wildcards;

## All code in pep8 form;

## Auth is simple, but I had plans for session handling;

### libraries
* SqlAlchemy;
    * +SchemaDisplay addon;
* Pandas;
* FastAPI;
* Pydantic;