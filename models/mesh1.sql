
MODEL (
  name PORTFOLIO_DB2.PUBLIC.STG_CLIENTDETAILS,
  kind INCREMENTAL_BY_UNIQUE_KEY (
    unique_key client_id
  ),
  cron '*/5 * * * *',
  start '2026-06-08',
  grain (client_id),
  signals (
    clientdetails_loaded(),
  )
);

SELECT
  CLIENTID    AS client_id,
  CLIENTNAME  AS client_name,
  USERNAME    AS username,
  ASSIGNED    AS assigned_advisor,
  INSERTED_AT AS inserted_at
FROM PORTFOLIO_DB2.PUBLIC.CLIENTDETAILS1
WHERE CLIENTID IS NOT NULL
QUALIFY ROW_NUMBER() OVER (
  PARTITION BY CLIENTID
  ORDER BY CLIENTID
) = 1
