-- Set the PRAGMA to enforce lowercase table names
-- PRAGMA case_sensitive_like = true;

-- Create tables with lowercase names
CREATE TABLE clients (
    client_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    date_of_birth DATE,
    email TEXT,
    phone TEXT,
    photo TEXT,
    street TEXT,
    city TEXT,
    state TEXT,
    zip TEXT
);
CREATE TABLE insurance_policies (
    policy_id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER,
    policy_number TEXT NOT NULL,
    policy_type TEXT NOT NULL,
    start_date DATE,
    end_date DATE,
    premium_amount REAL,
    renewed INTEGER DEFAULT 0,
    old_end_date DATE,
    old_start_date DATE,
    status TEXT NOT NULL DEFAULT 'Requested',
    FOREIGN KEY (client_id) REFERENCES clients (client_id) ON DELETE CASCADE
);
CREATE TABLE claims (
    claim_id INTEGER PRIMARY KEY AUTOINCREMENT,
    policy_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    claim_amount REAL NOT NULL,
    claim_date TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (policy_id) REFERENCES insurance_policies (policy_id) ON DELETE CASCADE
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER,  
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('administrator', 'insured')),
    FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE
);