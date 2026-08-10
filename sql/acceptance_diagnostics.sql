-- Authorization rate by market and PSP
SELECT country, psp, COUNT(*) AS attempts,
       AVG(authorized * 1.0) AS authorization_rate
FROM transactions
GROUP BY country, psp
ORDER BY country, authorization_rate DESC;

-- 3DS / device diagnostic
SELECT device, three_ds, payment_method, COUNT(*) AS attempts,
       AVG(authorized * 1.0) AS authorization_rate
FROM transactions
WHERE payment_method IN ('visa','mastercard')
GROUP BY device, three_ds, payment_method;

-- Soft decline concentration
SELECT decline_reason, COUNT(*) AS declines
FROM transactions
WHERE authorized = 0 AND decline_type = 'soft'
GROUP BY decline_reason
ORDER BY declines DESC;
