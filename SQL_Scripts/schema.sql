PRAGMA foreign_keys = ON;

-- ======== PANEL (HŰTŐPANELEK) ========
CREATE TABLE IF NOT EXISTS panel (
                                     id          INTEGER PRIMARY KEY,          -- 1..15 azonosító
                                     name        TEXT NOT NULL,                -- "Panel hofok 1"
                                     unit        TEXT NOT NULL DEFAULT '°C',
                                     min_valid   REAL,                         -- opcionális érvényes tartomány
                                     max_valid   REAL
);

-- ======== MÉRÉSEK (IDŐSOROS ADATOK) ========
CREATE TABLE IF NOT EXISTS measurement (
                                           id            INTEGER PRIMARY KEY,
                                           panel_id      INTEGER NOT NULL,
                                           ts_utc        TEXT NOT NULL,              -- ISO formátumú idő (YYYY-MM-DDTHH:MM:SS)
                                           value         REAL NOT NULL,
                                           quality_code  TEXT NOT NULL DEFAULT 'OK', -- OK / WARN / BAD
                                           FOREIGN KEY (panel_id) REFERENCES panel(id)
    );

CREATE INDEX IF NOT EXISTS idx_measurement_panel_time ON measurement(panel_id, ts_utc);
CREATE INDEX IF NOT EXISTS idx_measurement_time       ON measurement(ts_utc);

-- ======== ADAGOK (BATCH ADATOK) ========
CREATE TABLE IF NOT EXISTS batch (
                                     id               INTEGER PRIMARY KEY,     -- adagszám (forrásból)
                                     start_ts         TEXT NOT NULL,
                                     end_ts           TEXT NOT NULL,
                                     duration_s       INTEGER,                 -- ADAGIDŐ
                                     intra_duration_s INTEGER                  -- ADAGKÖZI IDŐ
);

-- ======== NÉZET (mérés batchhez idő szerint) ========
CREATE VIEW IF NOT EXISTS v_measurement_in_batch AS
SELECT
    m.*,
    b.id AS batch_id
FROM measurement m
         LEFT JOIN batch b
                   ON m.ts_utc >= b.start_ts AND m.ts_utc < b.end_ts;

-- ======== TRIGGER (érvénytelen érték tiltása) ========
CREATE TRIGGER IF NOT EXISTS trg_measurement_range
BEFORE INSERT ON measurement
FOR EACH ROW
BEGIN
SELECT CASE
           WHEN (SELECT min_valid FROM panel WHERE id = NEW.panel_id) IS NOT NULL
               AND NEW.value < (SELECT min_valid FROM panel WHERE id = NEW.panel_id)
               THEN RAISE(ABORT, 'Value below min_valid')
           END;
SELECT CASE
           WHEN (SELECT max_valid FROM panel WHERE id = NEW.panel_id) IS NOT NULL
               AND NEW.value > (SELECT max_valid FROM panel WHERE id = NEW.panel_id)
               THEN RAISE(ABORT, 'Value above max_valid')
           END;
END;
