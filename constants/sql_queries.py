REPORTS = {
    "last_values.csv": """
                       SELECT p.id, p.name, m.ts_utc, m.value
                       FROM panel p
                                JOIN measurement m ON m.panel_id = p.id
                       WHERE m.ts_utc = (SELECT MAX(ts_utc) FROM measurement WHERE panel_id = p.id)
                       ORDER BY p.id;
                       """,
    "daily_avg.csv": """
                     SELECT p.name, DATE (m.ts_utc) AS day, AVG (m.value) AS avg
                     FROM measurement m
                         JOIN panel p
                     ON p.id=m.panel_id
                     WHERE m.quality_code='OK'
                     GROUP BY p.name, DATE (m.ts_utc)
                     ORDER BY day, p.name;
                     """,
    "batch_avg.csv": """
                     SELECT b.id AS batch_id, p.name, AVG(m.value) AS avg
                     FROM v_measurement_in_batch m
                         JOIN panel p
                     ON p.id=m.panel_id
                         JOIN batch b ON b.id=m.batch_id
                     WHERE m.quality_code='OK'
                     GROUP BY b.id, p.name
                     ORDER BY b.id, p.name;
                     """,
    "outliers.csv": """
                    WITH stats AS (SELECT panel_id,
                                          COUNT(*)                                                               AS n,
                                          AVG(value)                                                             AS av,
                                          (SUM(value * value) - (SUM(value) * SUM(value)) / COUNT(*)) /
                                          COUNT(*)                                                               AS var
                                   FROM measurement
                                   WHERE quality_code = 'OK'
                                   GROUP BY panel_id)
                    SELECT m.panel_id, m.ts_utc, m.value
                    FROM measurement m
                             JOIN stats s USING (panel_id)
                    WHERE m.quality_code = 'OK'
                      AND s.var IS NOT NULL
                      AND ABS(m.value - s.av) > 3 * sqrt(s.var) LIMIT 100;
                    """,
    "daily_minmax.csv": """
                        SELECT p.name,
                               substr(m.ts_utc, 1, 10) AS day,
                MIN(m.value) AS min_value,
                MAX(m.value) AS max_value
                        FROM measurement m
                            JOIN panel p
                        ON p.id = m.panel_id
                        WHERE m.quality_code='OK'
                        GROUP BY p.name, day
                        ORDER BY day, p.name;
                        """
}