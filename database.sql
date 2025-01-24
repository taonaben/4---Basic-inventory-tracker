CREATE TABLE inventory (
    id SERIAL PRIMARY KEY NOT NULL,
    item_name TEXT NOT NULL,
    stock INTEGER NOT NULL,
    price REAL NOT NULL
);

