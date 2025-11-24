CREATE TABLE IF NOT EXISTS users
(
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    login      TEXT NOT NULL UNIQUE,
    password   TEXT NOT NULL,
    salt       TEXT UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS candidates
(
    tg_id      TEXT PRIMARY KEY UNIQUE NOT NULL,
    user_name  TEXT                    NOT NULL,
    name       TEXT,
    phone      TEXT UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS rules
(
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER,
    tags       TEXT NOT NULL,
    date_start DATETIME,
    date_end   DATETIME,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS analytic_records
(
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER,
    rule_id      INTEGER NOT NULL,
    cv_path      TEXT,
    ai_result    TEXT,
    opinion      TEXT,
    is_viewed    BOOLEAN DEFAULT FALSE,
    candidate_id TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (candidate_id) REFERENCES candidates (tg_id),
    FOREIGN KEY (rule_id) REFERENCES rules (id)
);



